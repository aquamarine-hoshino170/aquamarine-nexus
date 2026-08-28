from array import array
import math
import multiprocessing as mp
import time
from typing import Tuple, List, Union

def _chunk_matrix_multiply(args):
    """Worker process for parallel row-block tiled matrix multiplication."""
    a_bytes, b_bytes, m, k, n, start_row, end_row, block_size = args
    
    # Direct memory mapping without object reconstruction
    a_view = memoryview(a_bytes).cast('d')
    b_view = memoryview(b_bytes).cast('d')
    
    out_chunk = array('d', [0.0] * ((end_row - start_row) * n))
    
    # Cache Tiling Matrix Core
    for ii in range(start_row, end_row, block_size):
        i_max = min(ii + block_size, end_row)
        for kk in range(0, k, block_size):
            k_max = min(kk + block_size, k)
            for jj in range(0, n, block_size):
                j_max = min(jj + block_size, n)
                
                for i in range(ii, i_max):
                    local_row_offset = (i - start_row) * n
                    a_row_offset = i * k
                    for p in range(kk, k_max):
                        a_ip = a_view[a_row_offset + p]
                        b_row_offset = p * n
                        for j in range(jj, j_max):
                            out_chunk[local_row_offset + j] += a_ip * b_view[b_row_offset + j]
                            
    return out_chunk.tobytes()

class BigDataTensorAccelerator:
    """Ultra-Dense Memory-Mapped Parallel Array Engine."""
    def __init__(self, data: Union[List[float], array], shape: Tuple[int, ...]):
        self.shape = tuple(shape)
        if isinstance(data, array) and data.typecode == 'd':
            self.buffer = data
        else:
            self.buffer = array('d', data)
            
        expected_size = 1
        for s in self.shape: expected_size *= s
        if len(self.buffer) != expected_size:
            raise ValueError(f"Buffer size {len(self.buffer)} doesn't match shape {self.shape}")

    @classmethod
    def zeros(cls, shape: Tuple[int, ...]) -> 'BigDataTensorAccelerator':
        size = 1
        for s in shape: size *= s
        return cls(array('d', [0.0] * size), shape)

    @classmethod
    def arange_flat(cls, total_elements: int, shape: Tuple[int, ...]) -> 'BigDataTensorAccelerator':
        arr = array('d', (float(i) for i in range(total_elements)))
        return cls(arr, shape)

    def parallel_matmul(self, other: 'BigDataTensorAccelerator', num_workers: int = None, block_size: int = 64) -> 'BigDataTensorAccelerator':
        """High-Throughput Parallel Tiled Matrix Dot Product."""
        if len(self.shape) != 2 or len(other.shape) != 2:
            raise ValueError("Parallel matmul strictly requires 2D matrices.")
        m, k1 = self.shape
        k2, n = other.shape
        if k1 != k2:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")

        if num_workers is None:
            num_workers = max(1, mp.cpu_count())

        # Serial fast path for smaller workloads
        if m < 64 or num_workers == 1:
            out_raw = array('d', [0.0] * (m * n))
            a_v, b_v = memoryview(self.buffer), memoryview(other.buffer)
            for i in range(m):
                row_offset = i * n
                a_off = i * k1
                for p in range(k1):
                    val_a = a_v[a_off + p]
                    b_off = p * n
                    for j in range(n):
                        out_raw[row_offset + j] += val_a * b_v[b_off + j]
            return BigDataTensorAccelerator(out_raw, (m, n))

        # Parallel chunking across available CPU cores
        rows_per_worker = math.ceil(m / num_workers)
        tasks = []
        a_bytes = self.buffer.tobytes()
        b_bytes = other.buffer.tobytes()

        for w in range(num_workers):
            start_row = w * rows_per_worker
            end_row = min(start_row + rows_per_worker, m)
            if start_row < end_row:
                tasks.append((a_bytes, b_bytes, m, k1, n, start_row, end_row, block_size))

        with mp.Pool(processes=len(tasks)) as pool:
            results_bytes = pool.map(_chunk_matrix_multiply, tasks)

        combined = array('d')
        for chunk in results_bytes:
            combined.frombytes(chunk)

        return BigDataTensorAccelerator(combined, (m, n))

    def fast_reduce_sum(self) -> float:
        """Zero-overhead memoryview reduction."""
        return math.fsum(memoryview(self.buffer))

    def fast_elementwise_scale(self, scalar: float) -> 'BigDataTensorAccelerator':
        """In-place raw buffer scaling."""
        scaled = array('d', (x * scalar for x in memoryview(self.buffer)))
        return BigDataTensorAccelerator(scaled, self.shape)
