import math
from typing import List, Tuple

class SovereignFormulasEngine:
    """
    Pure Mathematical Implementation of Core AI Formulation Operators.
    Zero external dependencies.
    """

    @staticmethod
    def gelu(x: float) -> float:
        """
        Google GeLU (Gaussian Error Linear Unit) Operator:
        GeLU(x) = 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))
        """
        c = 0.7978845608028654  # sqrt(2.0 / math.pi)
        inner = c * (x + 0.044715 * (x ** 3))
        # Numerical clamping for stability
        clamped_inner = max(min(inner, 15.0), -15.0)
        return 0.5 * x * (1.0 + math.tanh(clamped_inner))

    @staticmethod
    def softmax_vector(vector: List[float]) -> List[float]:
        """Numerically stable softmax for probability normalization."""
        max_val = max(vector)
        exps = [math.exp(max(min(v - max_val, 50.0), -50.0)) for v in vector]
        sum_exps = sum(exps)
        return [e / sum_exps for e in exps]

    @classmethod
    def scaled_dot_product_attention(
        cls,
        Q: List[List[float]],
        K: List[List[float]],
        V: List[List[float]],
        d_k: int
    ) -> List[List[float]]:
        """
        Scaled Dot-Product Attention Core:
        Attention(Q, K, V) = Softmax( (Q @ K^T) / sqrt(d_k) ) @ V
        """
        seq_len_q = len(Q)
        seq_len_k = len(K)
        d_v = len(V[0])
        scale = 1.0 / math.sqrt(d_k)

        # 1. Matmul: Scores = (Q @ K^T) * scale
        scores = []
        for i in range(seq_len_q):
            row_scores = []
            for j in range(seq_len_k):
                dot_prod = sum(Q[i][d] * K[j][d] for d in range(d_k))
                row_scores.append(dot_prod * scale)
            scores.append(row_scores)

        # 2. Softmax normalization per query row
        attention_weights = [cls.softmax_vector(row) for row in scores]

        # 3. Context aggregation: Attention @ V
        output = []
        for i in range(seq_len_q):
            row_out = [0.0] * d_v
            for j in range(seq_len_k):
                weight = attention_weights[i][j]
                for v_dim in range(d_v):
                    row_out[v_dim] += weight * V[j][v_dim]
            output.append(row_out)

        return output

    @staticmethod
    def compound_scaling_dimensions(
        base_depth: int,
        base_width: int,
        base_resolution: int,
        phi: float,
        alpha: float = 1.2,
        beta: float = 1.1,
        gamma: float = 1.15
    ) -> Tuple[int, int, int]:
        """
        Compound Scaling Formula:
        d = alpha^phi, w = beta^phi, r = gamma^phi
        Constraint: alpha * beta^2 * gamma^2 ~ 2
        """
        scaled_depth = int(round(base_depth * (alpha ** phi)))
        scaled_width = int(round(base_width * (beta ** phi)))
        scaled_res = int(round(base_resolution * (gamma ** phi)))
        return scaled_depth, scaled_width, scaled_res

    @staticmethod
    def linear_state_space_step(
        h_prev: List[float],
        x_curr: List[float],
        A_bar: List[List[float]],
        B_bar: List[List[float]],
        C: List[List[float]]
    ) -> Tuple[List[float], List[float]]:
        """
        Discrete Recurrence Step:
        h_t = A_bar @ h_{t-1} + B_bar @ x_t
        y_t = C @ h_t
        """
        d_state = len(h_prev)
        d_in = len(x_curr)
        d_out = len(C)

        # State transition
        h_t = [0.0] * d_state
        for i in range(d_state):
            state_term = sum(A_bar[i][j] * h_prev[j] for j in range(d_state))
            in_term = sum(B_bar[i][k] * x_curr[k] for k in range(d_in))
            h_t[i] = state_term + in_term

        # Output projection
        y_t = [0.0] * d_out
        for m in range(d_out):
            y_t[m] = sum(C[m][i] * h_t[i] for i in range(d_state))

        return h_t, y_t
