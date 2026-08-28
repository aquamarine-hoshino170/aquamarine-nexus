import array
import ctypes
from typing import Dict, Any, List

class RawMemoryTensorCore:
    """
    Zero-Dependency High-Performance Native Memory Buffer & Raw C-Types Pointer Interface.
    Safe and cross-platform architecture targeting ARM/Android (Termux) and x86_64 systems.
    """

    @staticmethod
    def create_contiguous_f64_buffer(elements: List[float]) -> array.array:
        """
        Allocates a dense C-contiguous 64-bit IEEE floating-point array.
        """
        return array.array('d', elements)

    @staticmethod
    def raw_pointer_vector_dot(buf_a: array.array, buf_b: array.array) -> float:
        """
        Computes high-speed dot product safely accessing raw double pointers.
        """
        if len(buf_a) != len(buf_b):
            raise ValueError("Buffer dimensions must match for inner product.")

        n = len(buf_a)
        c_double_p = ctypes.POINTER(ctypes.c_double)
        
        # Safe raw buffer pointer resolution for Android Termux / CPython
        addr_a, _ = buf_a.buffer_info()
        addr_b, _ = buf_b.buffer_info()

        ptr_a = ctypes.cast(addr_a, c_double_p)
        ptr_b = ctypes.cast(addr_b, c_double_p)

        total = 0.0
        limit = n - (n % 4)

        # Unrolled loop
        for i in range(0, limit, 4):
            total += (ptr_a[i] * ptr_b[i] +
                      ptr_a[i+1] * ptr_b[i+1] +
                      ptr_a[i+2] * ptr_b[i+2] +
                      ptr_a[i+3] * ptr_b[i+3])

        for i in range(limit, n):
            total += ptr_a[i] * ptr_b[i]

        return total

    @staticmethod
    def raw_matrix_multiply_2d(
        mat_a: List[List[float]], 
        mat_b: List[List[float]]
    ) -> Dict[str, Any]:
        """
        Performs cache-localized contiguous buffer matrix multiplication C = A x B.
        """
        rows_a = len(mat_a)
        cols_a = len(mat_a[0])
        rows_b = len(mat_b)
        cols_b = len(mat_b[0])

        if cols_a != rows_b:
            raise ValueError(f"Shape mismatch: {rows_a}x{cols_a} cannot multiply {rows_b}x{cols_b}")

        flat_a = array.array('d', [val for row in mat_a for val in row])
        flat_b_t = array.array('d', [mat_b[r][c] for c in range(cols_b) for r in range(rows_b)])
        result_flat = array.array('d', [0.0] * (rows_a * cols_b))

        c_double_p = ctypes.POINTER(ctypes.c_double)
        
        addr_a, _ = flat_a.buffer_info()
        addr_bt, _ = flat_b_t.buffer_info()
        addr_res, _ = result_flat.buffer_info()

        ptr_a = ctypes.cast(addr_a, c_double_p)
        ptr_bt = ctypes.cast(addr_bt, c_double_p)
        ptr_res = ctypes.cast(addr_res, c_double_p)

        for r in range(rows_a):
            offset_a = r * cols_a
            for c in range(cols_b):
                offset_b = c * rows_b
                acc = 0.0
                for k in range(cols_a):
                    acc += ptr_a[offset_a + k] * ptr_bt[offset_b + k]
                ptr_res[r * cols_b + c] = acc

        res_matrix = [
            list(result_flat[i * cols_b : (i + 1) * cols_b]) 
            for i in range(rows_a)
        ]

        return {
            "result_shape": (rows_a, cols_b),
            "memory_layout": "C_CONTIGUOUS_DENSE_F64",
            "sample_output": res_matrix[0][:4] if cols_b >= 4 else res_matrix[0],
            "full_matrix": res_matrix,
            "status": "RAW_MEMORY_EXECUTION_SUCCESS"
        }
