from array import array
import math
from typing import List, Dict, Any

class AquamarineDergeMergeEngine:
    @staticmethod
    def _dot_product(vec_a: array, vec_b: array) -> float:
        return math.fsum(a * b for a, b in zip(vec_a, vec_b))

    @staticmethod
    def _norm(vec: array) -> float:
        return math.sqrt(math.fsum(x * x for x in vec))

    @staticmethod
    def slerp_weight_merge(model_a: List[float], model_b: List[float], interpolation_t: float = 0.5) -> Dict[str, Any]:
        """
        Spherical Linear Interpolation (SLERP) across high-dimensional parameter manifold:
        W(t) = [sin((1-t)*theta) / sin(theta)] * W_A + [sin(t*theta) / sin(theta)] * W_B
        """
        if len(model_a) != len(model_b) or len(model_a) == 0:
            raise ValueError("Model weight vectors must be non-empty and of identical dimensions.")
        if not (0.0 <= interpolation_t <= 1.0):
            raise ValueError("Interpolation factor t must be in range [0.0, 1.0].")

        va = array('d', model_a)
        vb = array('d', model_b)

        norm_a = AquamarineDergeMergeEngine._norm(va)
        norm_b = AquamarineDergeMergeEngine._norm(vb)

        if norm_a < 1e-15 or norm_b < 1e-15:
            # Degenerate linear fallback
            merged = array('d', ((1.0 - interpolation_t) * a + interpolation_t * b for a, b in zip(va, vb)))
            return {"merged_weights": list(merged), "merge_mode": "Linear Fallback"}

        # Normalize to unit vectors
        ua = array('d', (x / norm_a for x in va))
        ub = array('d', (x / norm_b for x in vb))

        dot = AquamarineDergeMergeEngine._dot_product(ua, ub)
        dot = max(-1.0, min(1.0, dot))

        # Check colinearity
        if abs(dot) > 0.9995:
            merged = array('d', ((1.0 - interpolation_t) * a + interpolation_t * b for a, b in zip(va, vb)))
            return {"merged_weights": list(merged), "merge_mode": "Linear Near-Colinear"}

        theta = math.acos(dot)
        sin_theta = math.sin(theta)

        scale_a = math.sin((1.0 - interpolation_t) * theta) / sin_theta
        scale_b = math.sin(interpolation_t * theta) / sin_theta

        # Interpolate unit vector and scale back by interpolated magnitude
        target_norm = (1.0 - interpolation_t) * norm_a + interpolation_t * norm_b
        merged_raw = array('d', ((scale_a * a + scale_b * b) * target_norm for a, b in zip(ua, ub)))

        return {
            "merged_weights": [round(x, 6) for x in merged_raw],
            "manifold_angle_degrees": round(math.degrees(theta), 4),
            "original_norms": [round(norm_a, 6), round(norm_b, 6)],
            "result_norm": round(AquamarineDergeMergeEngine._norm(merged_raw), 6),
            "algorithm": "SLERP_Curved_Manifold_Merge"
        }

    @staticmethod
    def ties_weight_merge(base_model: List[float], task_models: List[List[float]], top_k_fraction: float = 0.5) -> Dict[str, Any]:
        """
        TIES Merging (Trimming, Electing Sign, and Disjoint Merging):
        1. Task Vector Delta: \tau_m = W_m - W_base
        2. Top-K Trim: keep top |p| percentile magnitudes
        3. Sign Elect: majority sign per parameter
        4. Disjoint Mean: average only matching sign deltas
        """
        if not task_models or len(base_model) != len(task_models[0]):
            raise ValueError("Base model and task models must have matching parameter counts.")

        n_params = len(base_model)
        n_tasks = len(task_models)

        # 1. Calculate Task Vectors
        deltas = []
        for tm in task_models:
            if len(tm) != n_params:
                raise ValueError("All task models must match parameter length.")
            deltas.append([tm[i] - base_model[i] for i in range(n_params)])

        # 2. Trim Top-K per task vector
        trimmed_deltas = []
        k_keep = max(1, int(round(n_params * top_k_fraction)))

        for d in deltas:
            # Find threshold magnitude
            magnitudes = sorted([abs(x) for x in d], reverse=True)
            thresh = magnitudes[k_keep - 1] if k_keep <= len(magnitudes) else 0.0
            trimmed = [x if abs(x) >= thresh else 0.0 for x in d]
            trimmed_deltas.append(trimmed)

        # 3. Elect Sign & 4. Disjoint Mean
        merged_delta = array('d', [0.0] * n_params)
        for i in range(n_params):
            param_vals = [trimmed_deltas[t][i] for t in range(n_tasks) if trimmed_deltas[t][i] != 0.0]
            if not param_vals:
                continue

            sign_sum = sum(1.0 if v > 0 else -1.0 for v in param_vals)
            elected_sign = 1.0 if sign_sum >= 0 else -1.0

            # Filter values matching elected sign
            filtered = [v for v in param_vals if (v > 0 and elected_sign > 0) or (v < 0 and elected_sign < 0)]
            merged_delta[i] = sum(filtered) / len(filtered) if filtered else 0.0

        # Construct final model: W_final = W_base + Delta_merged
        final_weights = [round(base_model[i] + merged_delta[i], 6) for i in range(n_params)]

        return {
            "final_merged_weights": final_weights,
            "total_parameters": n_params,
            "tasks_combined": n_tasks,
            "trimmed_density_fraction": top_k_fraction,
            "delta_norm": round(AquamarineDergeMergeEngine._norm(merged_delta), 6),
            "algorithm": "TIES_Sign_Disjoint_Merge"
        }

    @staticmethod
    def dare_task_vector_fuse(base_model: List[float], finetuned_model: List[float], drop_rate: float = 0.5) -> Dict[str, Any]:
        """
        DARE (Drop And REscale) Task Vector Sparsification:
        Zeros out deltas with probability p and rescales remaining weights by 1 / (1 - p).
        """
        if len(base_model) != len(finetuned_model):
            raise ValueError("Base and fine-tuned models must match in length.")
        if not (0.0 <= drop_rate < 1.0):
            raise ValueError("Drop rate must be in range [0.0, 1.0).")

        scale = 1.0 / (1.0 - drop_rate)
        n = len(base_model)
        fused = []
        dropped_count = 0

        # Deterministic pseudo-random Bernoulli mask
        for i in range(n):
            delta = finetuned_model[i] - base_model[i]
            # Deterministic hash-based mask
            pseudo_rand = (math.sin(float(i + 1) * 12.9898) * 43758.5453) % 1.0
            if pseudo_rand < drop_rate:
                # Dropped
                fused.append(round(base_model[i], 6))
                dropped_count += 1
            else:
                # Rescaled
                fused.append(round(base_model[i] + delta * scale, 6))

        return {
            "fused_weights": fused,
            "parameters_count": n,
            "drop_rate": drop_rate,
            "weights_sparsified_count": dropped_count,
            "active_weights_ratio": round((n - dropped_count) / n, 4),
            "algorithm": "DARE_Drop_And_Rescale_Fusion"
        }
