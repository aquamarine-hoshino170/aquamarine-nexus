import math
import random
from typing import List
from aquamarine_nexus.core.sovereign_tensor_engine import Tensor

class LoRALinear:
    """
    Zero-Dependency Sovereign Low-Rank Adaptation (LoRA) Layer.
    Freezes base weight W0 and trains only low-rank matrices A and B.
    """
    def __init__(self, in_features: int, out_features: int, rank: int = 4, alpha: float = 8.0):
        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.scaling = alpha / float(rank)

        # Base frozen weights W0
        scale = math.sqrt(2.0 / in_features)
        w0_data = [[random.gauss(0.0, scale) for _ in range(out_features)] for _ in range(in_features)]
        self.W0 = Tensor(w0_data)
        self.bias = Tensor([[0.0] * out_features])

        # Trainable Low-Rank Adapters: A ~ Gaussian, B = 0
        lora_a_data = [[random.gauss(0.0, 1.0 / math.sqrt(in_features)) for _ in range(rank)] for _ in range(in_features)]
        lora_b_data = [[0.0 for _ in range(out_features)] for _ in range(rank)]

        self.lora_A = Tensor(lora_a_data) # (in_features, rank)
        self.lora_B = Tensor(lora_b_data) # (rank, out_features)

    def __call__(self, x: Tensor) -> Tensor:
        # 1. Base forward: x @ W0
        base_out = x.matmul(self.W0)

        # 2. Low-rank path: (x @ A) @ B * scaling
        lora_mid = x.matmul(self.lora_A)
        lora_out = lora_mid.matmul(self.lora_B) * self.scaling

        # 3. Add base + adapter + bias
        r, c = base_out.shape
        repeated_bias = Tensor(self.bias.data * r)
        repeated_bias.shape = (r, c)

        return base_out + lora_out + repeated_bias

    def trainable_parameters(self) -> List[Tensor]:
        return [self.lora_A, self.lora_B]

    def merge_lora_into_base(self):
        """
        Merges W_merged = W0 + (A @ B) * scaling for zero-latency inference.
        """
        ab_delta = self.lora_A.matmul(self.lora_B) * self.scaling
        self.W0 = self.W0 + ab_delta
        # Reset adapters to zero
        self.lora_A = Tensor([[0.0] * self.rank for _ in range(self.in_features)])
        self.lora_B = Tensor([[0.0] * self.out_features for _ in range(self.rank)])
