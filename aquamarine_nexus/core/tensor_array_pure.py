import math
from typing import Tuple, Union

class PureNDArray:
    """Zero-dependency Pure Python N-Dimensional Contiguous Array Buffer & Tensor Slicing Engine."""
    def __init__(self, data: list, shape: Tuple[int, ...] = None):
        if shape is None:
            self.data, self.shape = self._flatten_and_infer_shape(data)
        else:
            self.data = list(data)
            self.shape = tuple(shape)
        
        self.strides = self._compute_strides(self.shape)
        self.size = len(self.data)
        
        prod_shape = 1
        for s in self.shape:
            prod_shape *= s
        if prod_shape != self.size:
            raise ValueError(f"Shape {self.shape} does not match total element count {self.size}.")

    def _flatten_and_infer_shape(self, nested: list) -> Tuple[list, Tuple[int, ...]]:
        shape = []
        curr = nested
        while isinstance(curr, list):
            shape.append(len(curr))
            curr = curr[0] if len(curr) > 0 else None
            
        flat = []
        def _flatten(item):
            if isinstance(item, list):
                for sub in item:
                    _flatten(sub)
            else:
                flat.append(float(item))
        _flatten(nested)
        return flat, tuple(shape)

    def _compute_strides(self, shape: Tuple[int, ...]) -> Tuple[int, ...]:
        strides = []
        stride = 1
        for dim in reversed(shape):
            strides.append(stride)
            stride *= dim
        return tuple(reversed(strides))

    def _linear_index(self, indices: Tuple[int, ...]) -> int:
        if len(indices) != len(self.shape):
            raise IndexError(f"Expected {len(self.shape)} indices, got {len(indices)}.")
        idx = 0
        for i, (dim, stride) in enumerate(zip(self.shape, self.strides)):
            index = indices[i]
            if index < 0:
                index += dim
            if not (0 <= index < dim):
                raise IndexError(f"Index {indices[i]} out of bounds for axis {i} with size {dim}.")
            idx += index * stride
        return idx

    def __getitem__(self, item):
        if isinstance(item, int):
            item = (item,)
        if isinstance(item, tuple):
            if all(isinstance(idx, int) for idx in item) and len(item) == len(self.shape):
                return self.data[self._linear_index(item)]
        raise NotImplementedError("Arbitrary multi-slice is supported via .to_list().")

    def reshape(self, new_shape: Tuple[int, ...]) -> 'PureNDArray':
        prod = 1
        for s in new_shape: prod *= s
        if prod != self.size:
            raise ValueError(f"Cannot reshape size {self.size} into shape {new_shape}.")
        return PureNDArray(self.data, shape=new_shape)

    def dot(self, other: 'PureNDArray') -> 'PureNDArray':
        """2D Matrix Multiplication: (M, K) @ (K, N) -> (M, N)"""
        if len(self.shape) != 2 or len(other.shape) != 2:
            raise ValueError("Pure .dot requires 2D matrices.")
        m, k1 = self.shape
        k2, n = other.shape
        if k1 != k2:
            raise ValueError(f"Matrix shape mismatch: {self.shape} vs {other.shape}")
        
        out = [0.0] * (m * n)
        for i in range(m):
            for k in range(k1):
                a_ik = self.data[i * self.strides[0] + k * self.strides[1]]
                for j in range(n):
                    b_kj = other.data[k * other.strides[0] + j * other.strides[1]]
                    out[i * n + j] += a_ik * b_kj
        return PureNDArray(out, shape=(m, n))

    def transpose(self) -> 'PureNDArray':
        if len(self.shape) != 2:
            raise ValueError("Transpose currently implemented for 2D.")
        m, n = self.shape
        out = [0.0] * (m * n)
        for i in range(m):
            for j in range(n):
                out[j * m + i] = self.data[i * n + j]
        return PureNDArray(out, shape=(n, m))

    def __add__(self, other: Union['PureNDArray', float, int]) -> 'PureNDArray':
        if isinstance(other, (int, float)):
            return PureNDArray([x + other for x in self.data], shape=self.shape)
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
        return PureNDArray([x + y for x, y in zip(self.data, other.data)], shape=self.shape)

    def __mul__(self, other: Union['PureNDArray', float, int]) -> 'PureNDArray':
        if isinstance(other, (int, float)):
            return PureNDArray([x * other for x in self.data], shape=self.shape)
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
        return PureNDArray([x * y for x, y in zip(self.data, other.data)], shape=self.shape)

    def norm(self) -> float:
        return math.sqrt(sum(x * x for x in self.data))

    def to_list(self) -> list:
        if len(self.shape) == 1:
            return list(self.data)
        elif len(self.shape) == 2:
            m, n = self.shape
            return [self.data[i * n:(i + 1) * n] for i in range(m)]
        return self.data
