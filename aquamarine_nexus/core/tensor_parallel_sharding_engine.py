import math
import random
from typing import List, Tuple
from aquamarine_nexus.core.sovereign_tensor_engine import Tensor

class ColumnParallelLinear:
    """
    Megatron-LM Style Column-Parallel Linear Layer:
    Splits Weight matrix along output dimension across N logical workers:
    Y_i = X @ W_i + b_i
    """
    def __init__(self, in_features: int, out_features: int, rank: int, world_size: int):
        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.world_size = world_size
        
        if out_features % world_size != 0:
            raise ValueError("out_features must be divisible by world_size.")
        
        self.split_out_features = out_features // world_size
        scale = math.sqrt(2.0 / in_features)
        
        # Sharded Weight slice: (in_features, split_out_features)
        w_slice = [
            [random.gauss(0.0, scale) for _ in range(self.split_out_features)]
            for _ in range(in_features)
        ]
        self.W = Tensor(w_slice)
        self.b = Tensor([0.0] * self.split_out_features)

    def forward(self, x: Tensor) -> Tensor:
        # Input shape: (seq_len, in_features) -> Output: (seq_len, split_out_features)
        return x.matmul(self.W)

class RowParallelLinear:
    """
    Megatron-LM Style Row-Parallel Linear Layer:
    Splits Weight matrix along input dimension across N logical workers:
    Y = sum_i(X_i @ W_i) + b (Requires All-Reduce across ranks)
    """
    def __init__(self, in_features: int, out_features: int, rank: int, world_size: int):
        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.world_size = world_size

        if in_features % world_size != 0:
            raise ValueError("in_features must be divisible by world_size.")

        self.split_in_features = in_features // world_size
        scale = math.sqrt(2.0 / self.split_in_features)

        # Sharded Weight slice: (split_in_features, out_features)
        w_slice = [
            [random.gauss(0.0, scale) for _ in range(out_features)]
            for _ in range(self.split_in_features)
        ]
        self.W = Tensor(w_slice)
        self.b = Tensor([0.0] * out_features)

    def forward_partial(self, x_slice: Tensor) -> Tensor:
        # Partial dot product before cross-node reduction
        return x_slice.matmul(self.W)

    @staticmethod
    def all_reduce_sum(partial_tensors: List[Tensor]) -> Tensor:
        """Simulates All-Reduce collective communication."""
        seq_len, out_dim = partial_tensors[0].shape
        summed_data = [0.0] * (seq_len * out_dim)

        for t in partial_tensors:
            for i in range(len(summed_data)):
                summed_data[i] += t.data[i]

        res = Tensor(summed_data)
        res.shape = (seq_len, out_dim)
        return res
