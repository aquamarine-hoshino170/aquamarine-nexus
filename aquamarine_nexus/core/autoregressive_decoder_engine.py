import math
import array
from typing import List, Tuple, Dict, Any
from aquamarine_nexus.core.sovereign_tensor_engine import Tensor, Linear

class RotaryPositionalEmbedding:
    """
    Pure-Python Rotary Positional Embedding (RoPE).
    Applies sinusoidal rotation to Query and Key projections.
    """
    @staticmethod
    def apply_rope(x: Tensor, seq_len: int, dim: int) -> Tensor:
        out_data = list(x.data)
        for pos in range(seq_len):
            for i in range(0, dim, 2):
                freq = 1.0 / (10000.0 ** (i / dim))
                theta = pos * freq
                cos_t = math.cos(theta)
                sin_t = math.sin(theta)

                idx1 = pos * dim + i
                idx2 = pos * dim + i + 1

                v1 = x.data[idx1]
                v2 = x.data[idx2]

                out_data[idx1] = v1 * cos_t - v2 * sin_t
                out_data[idx2] = v1 * sin_t + v2 * cos_t

        res = Tensor(out_data)
        res.shape = (seq_len, dim)
        return res

class SovereignKVCacheDecoderBlock:
    """
    Autoregressive Decoder Block equipped with dynamic KV-Cache.
    Eliminates redundant token recomputation during sequence generation.
    """
    def __init__(self, d_model: int):
        self.d_model = d_model
        self.w_q = Linear(d_model, d_model)
        self.w_k = Linear(d_model, d_model)
        self.w_v = Linear(d_model, d_model)
        self.w_proj = Linear(d_model, d_model)
        self.cached_k: List[float] = []
        self.cached_v: List[float] = []

    def reset_cache(self):
        self.cached_k.clear()
        self.cached_v.clear()

    def step(self, token_vec: Tensor) -> Tensor:
        """
        Executes single-token autoregressive decoding step with cached past keys/values.
        Input shape: (1, d_model)
        """
        q = self.w_q(token_vec)
        k = self.w_k(token_vec)
        v = self.w_v(token_vec)

        # Update persistent past memory
        self.cached_k.extend(k.data)
        self.cached_v.extend(v.data)

        num_cached_tokens = len(self.cached_k) // self.d_model
        scale = 1.0 / math.sqrt(float(self.d_model))

        # Compute cross attention scores against full KV history: (1, num_cached)
        scores = [0.0] * num_cached_tokens
        for past_idx in range(num_cached_tokens):
            k_offset = past_idx * self.d_model
            dot = sum(q.data[d] * self.cached_k[k_offset + d] for d in range(self.d_model))
            scores[past_idx] = dot * scale

        # Softmax over sequence history
        max_s = max(scores)
        exp_s = [math.exp(s - max_s) for s in scores]
        sum_exp = sum(exp_s)
        attn_weights = [e / sum_exp for e in exp_s]

        # Context reduction
        ctx_data = [0.0] * self.d_model
        for past_idx in range(num_cached_tokens):
            weight = attn_weights[past_idx]
            v_offset = past_idx * self.d_model
            for d in range(self.d_model):
                ctx_data[d] += weight * self.cached_v[v_offset + d]

        ctx = Tensor(ctx_data)
        ctx.shape = (1, self.d_model)
        return self.w_proj(ctx)
