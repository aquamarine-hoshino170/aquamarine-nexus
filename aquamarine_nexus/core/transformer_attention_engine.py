import math
import random
from typing import List, Tuple
from aquamarine_nexus.core.sovereign_tensor_engine import Tensor, Linear

class ScaledDotProductAttention:
    """
    Pure-Python Scaled Dot-Product Attention Core.
    Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V
    """
    @staticmethod
    def forward(q: Tensor, k: Tensor, v: Tensor, d_k: int) -> Tensor:
        # q: (seq_len, d_k), k: (seq_len, d_k), v: (seq_len, d_v)
        seq_len, d_model = q.shape
        scale = 1.0 / math.sqrt(float(d_k))

        # 1. K Transpose -> (d_k, seq_len)
        k_t_data = [0.0] * (d_model * seq_len)
        for r in range(seq_len):
            for c in range(d_model):
                k_t_data[c * seq_len + r] = k.data[r * d_model + c]
        k_t = Tensor(k_t_data)
        k_t.shape = (d_model, seq_len)

        # 2. Raw Scores = Q @ K^T -> (seq_len, seq_len)
        scores = q.matmul(k_t) * scale

        # 3. Row-wise Softmax
        attn_weights_data = []
        for r in range(seq_len):
            row_vals = scores.data[r * seq_len : (r + 1) * seq_len]
            max_val = max(row_vals)
            exp_vals = [math.exp(x - max_val) for x in row_vals]
            sum_exp = sum(exp_vals)
            attn_weights_data.extend([e / sum_exp for e in exp_vals])

        attn_weights = Tensor(attn_weights_data)
        attn_weights.shape = (seq_len, seq_len)

        # 4. Context Output = Softmax(Scores) @ V -> (seq_len, d_v)
        return attn_weights.matmul(v)

class MultiHeadAttention:
    """
    Pure-Python Multi-Head Attention Block.
    """
    def __init__(self, d_model: int, num_heads: int):
        if d_model % num_heads != 0:
            raise ValueError("d_model must be divisible by num_heads.")
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.w_q = Linear(d_model, d_model)
        self.w_k = Linear(d_model, d_model)
        self.w_v = Linear(d_model, d_model)
        self.w_out = Linear(d_model, d_model)

    def __call__(self, x: Tensor) -> Tensor:
        # x shape: (seq_len, d_model)
        q = self.w_q(x)
        k = self.w_k(x)
        v = self.w_v(x)

        # Scaled dot-product attention
        attn_out = ScaledDotProductAttention.forward(q, k, v, self.d_k)
        return self.w_out(attn_out)

    def parameters(self) -> List[Tensor]:
        return (self.w_q.parameters() + 
                self.w_k.parameters() + 
                self.w_v.parameters() + 
                self.w_out.parameters())

class AdamWOptimizer:
    """
    Decoupled Weight Decay AdamW Optimizer in Pure Python.
    """
    def __init__(self, params: List[Tensor], lr: float = 0.001, betas: Tuple[float, float] = (0.9, 0.999), eps: float = 1e-8, weight_decay: float = 0.01):
        self.params = params
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.weight_decay = weight_decay
        self.t = 0
        self.m = [[0.0] * len(p.data) for p in params]
        self.v = [[0.0] * len(p.data) for p in params]

    def step(self):
        self.t += 1
        for idx, p in enumerate(self.params):
            for i in range(len(p.data)):
                # Decoupled Weight Decay
                p.data[i] -= self.lr * self.weight_decay * p.data[i]

                # Moving averages of gradient and squared gradient
                g = p.grad[i]
                self.m[idx][i] = self.beta1 * self.m[idx][i] + (1.0 - self.beta1) * g
                self.v[idx][i] = self.beta2 * self.v[idx][i] + (1.0 - self.beta2) * (g * g)

                # Bias correction
                m_hat = self.m[idx][i] / (1.0 - self.beta1 ** self.t)
                v_hat = self.v[idx][i] / (1.0 - self.beta2 ** self.t)

                # Parameter update
                p.data[i] -= self.lr * m_hat / (math.sqrt(v_hat) + self.eps)

    def zero_grad(self):
        for p in self.params:
            p.zero_grad()
