import ctypes
import os
from typing import List, Tuple, Optional

# Load Rust compiled native binary
_lib_path = os.path.expanduser('~/aquamarine-nexus/aquamarine_nexus/core/librust_core.so')
try:
    _rust_lib = ctypes.CDLL(_lib_path)
    _rust_lib.rust_fast_gemm.argtypes = [
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_size_t,
        ctypes.c_size_t,
        ctypes.c_size_t
    ]
    _rust_lib.rust_relu_activation.argtypes = [
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_size_t
    ]
    HAS_RUST_BACKEND = True
except Exception:
    HAS_RUST_BACKEND = False

class RustTensor:
    """
    High-Performance Tensor Node powered by Native Rust FFI Backend.
    """
    def __init__(self, data: List[float], shape: Tuple[int, ...], requires_grad: bool = False):
        self.shape = shape
        self.size = 1
        for dim in shape:
            self.size *= dim
        
        self.data = (ctypes.c_double * self.size)(*data)
        self.grad: Optional[List[float]] = [0.0] * self.size if requires_grad else None
        self.requires_grad = requires_grad

    @classmethod
    def from_2d_list(cls, matrix: List[List[float]], requires_grad: bool = False) -> 'RustTensor':
        rows = len(matrix)
        cols = len(matrix[0])
        flat = [val for row in matrix for val in row]
        return cls(flat, (rows, cols), requires_grad)

    def matmul(self, other: 'RustTensor') -> 'RustTensor':
        if len(self.shape) != 2 or len(other.shape) != 2 or self.shape[1] != other.shape[0]:
            raise ValueError(f"Shape mismatch for matmul: {self.shape} vs {other.shape}")

        n, k = self.shape
        _, m = other.shape
        out_tensor = RustTensor([0.0] * (n * m), (n, m))

        if HAS_RUST_BACKEND:
            _rust_lib.rust_fast_gemm(self.data, other.data, out_tensor.data, n, k, m)
        else:
            # Fallback pure-python execution
            for i in range(n):
                for p in range(k):
                    a_val = self.data[i * k + p]
                    for j in range(m):
                        out_tensor.data[i * m + j] += a_val * other.data[p * m + j]

        return out_tensor

    def relu(self) -> 'RustTensor':
        out_tensor = RustTensor(list(self.data), self.shape)
        if HAS_RUST_BACKEND:
            _rust_lib.rust_relu_activation(out_tensor.data, self.size)
        else:
            for idx in range(self.size):
                if out_tensor.data[idx] < 0.0:
                    out_tensor.data[idx] = 0.0
        return out_tensor

    def to_list(self) -> List[float]:
        return list(self.data)
