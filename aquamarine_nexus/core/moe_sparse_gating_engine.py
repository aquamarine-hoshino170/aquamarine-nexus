import math
import random
from typing import List, Tuple, Dict, Any
from aquamarine_nexus.core.sovereign_tensor_engine import Tensor, Linear

class SovereignExpert:
    """
    Feed-Forward Expert Sub-Network.
    """
    def __init__(self, d_model: int, d_ff: int):
        self.w1 = Linear(d_model, d_ff)
        self.w2 = Linear(d_ff, d_model)

    def forward(self, x: Tensor) -> Tensor:
        # FFN(x) = ReLU(x @ W1 + b1) @ W2 + b2
        h = self.w1(x).relu()
        return self.w2(h)

    def parameters(self) -> List[Tensor]:
        return self.w1.parameters() + self.w2.parameters()

class SparseMoELayer:
    """
    Zero-Dependency Top-K Sparse Mixture-of-Experts Layer.
    Dynamically routes each token to Top-K experts based on learned gate logits.
    """
    def __init__(self, num_experts: int, d_model: int, d_ff: int, k: int = 2):
        self.num_experts = num_experts
        self.d_model = d_model
        self.k = min(k, num_experts)
        self.gate = Linear(d_model, num_experts)
        self.experts = [SovereignExpert(d_model, d_ff) for _ in range(num_experts)]

    def __call__(self, x: Tensor) -> Tensor:
        # x shape: (seq_len, d_model)
        seq_len = x.shape[0]
        gate_logits = self.gate(x) # (seq_len, num_experts)
        
        out_tokens: List[List[float]] = []

        for i in range(seq_len):
            row_logits = gate_logits.data[i * self.num_experts : (i + 1) * self.num_experts]
            
            # Find Top-K expert indices
            indexed_logits = list(enumerate(row_logits))
            indexed_logits.sort(key=lambda item: item[1], reverse=True)
            top_k_items = indexed_logits[:self.k]
            
            top_indices = [idx for idx, val in top_k_items]
            top_vals = [val for idx, val in top_k_items]

            # Softmax over top-k gating weights
            max_v = max(top_vals)
            exp_v = [math.exp(v - max_v) for v in top_vals]
            sum_exp = sum(exp_v)
            top_weights = [e / sum_exp for e in exp_v]

            # Extract single token tensor: (1, d_model)
            token_vec_data = x.data[i * self.d_model : (i + 1) * self.d_model]
            token_tensor = Tensor([token_vec_data])
            token_tensor.shape = (1, self.d_model)

            # Accumulate weighted expert outputs
            token_accum = [0.0] * self.d_model
            for weight, exp_idx in zip(top_weights, top_indices):
                exp_out = self.experts[exp_idx].forward(token_tensor)
                for d in range(self.d_model):
                    token_accum[d] += weight * exp_out.data[d]

            out_tokens.append(token_accum)

        res = Tensor(out_tokens)
        res.shape = (seq_len, self.d_model)
        return res

    def parameters(self) -> List[Tensor]:
        params = self.gate.parameters()
        for exp in self.experts:
            params.extend(exp.parameters())
        return params
