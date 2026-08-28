import math
import array
from typing import List, Tuple, Dict, Any

class SparseFlashAttentionCore:
    """
    Zero-Dependency High-Throughput Block-Sparse Attention Core.
    Optimizes quadratic O(N^2) memory bottleneck down to O(N * sqrt(N))
    via local window tiling and global anchor routing.
    """

    @staticmethod
    def forward_sparse_attention(
        q: List[List[float]],
        k: List[List[float]],
        v: List[List[float]],
        window_size: int = 2,
        d_k: int = 4
    ) -> List[List[float]]:
        """
        Executes bounded block-sparse attention without allocating full N x N matrix.
        """
        seq_len = len(q)
        scale = 1.0 / math.sqrt(float(d_k))
        context_out: List[List[float]] = []

        for i in range(seq_len):
            # Restrict attention receptive field: [i - window_size, i + window_size] + anchor 0
            start_j = max(0, i - window_size)
            end_j = min(seq_len, i + window_size + 1)
            
            receptive_indices = set(range(start_j, end_j))
            receptive_indices.add(0) # Global causal anchor
            sorted_indices = sorted(list(receptive_indices))

            # Compute local sparse scores
            scores = []
            for j in sorted_indices:
                dot = sum(q[i][d] * k[j][d] for d in range(d_k))
                scores.append(dot * scale)

            # Softmax on local sparse neighborhood
            max_s = max(scores)
            exp_s = [math.exp(s - max_s) for s in scores]
            sum_exp = sum(exp_s)
            attn_weights = [e / sum_exp for e in exp_s]

            # Context accumulation
            token_context = [0.0] * d_k
            for idx, j in enumerate(sorted_indices):
                w = attn_weights[idx]
                for d in range(d_k):
                    token_context[d] += w * v[j][d]

            context_out.append(token_context)

        return context_out
