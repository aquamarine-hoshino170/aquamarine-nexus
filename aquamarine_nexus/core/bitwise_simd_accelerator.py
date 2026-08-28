import array
from typing import List, Tuple, Dict, Any

class BitwiseSIMDCore:
    """
    Zero-Dependency High-Throughput 64-Bit Packed Bit-Matrix Accelerator.
    Computes 1-bit quantized neural operations (Binary Neural Networks - BNN)
    via native CPU bitwise XOR and popcount (Hamming weight) instructions.
    """

    @staticmethod
    def pack_bipolar_to_uint64(bit_list: List[int]) -> List[int]:
        """
        Packs arrays of {-1, 1} or {0, 1} values into dense 64-bit integer words.
        """
        words = []
        n = len(bit_list)
        for i in range(0, n, 64):
            chunk = bit_list[i : min(i + 64, n)]
            word = 0
            for bit_pos, val in enumerate(chunk):
                if val > 0:
                    word |= (1 << bit_pos)
            words.append(word)
        return words

    @staticmethod
    def xnor_popcount_dot_product(words_a: List[int], words_b: List[int], original_len: int) -> int:
        """
        Computes exact binary dot-product in 64-element parallel chunks:
        Result = 2 * PopCount(XNOR(A, B)) - Length
        """
        if len(words_a) != len(words_b):
            raise ValueError("Word buffers must be of equal length.")

        total_matches = 0
        for wa, wb in zip(words_a, words_b):
            # XNOR = ~(A ^ B) masked to 64 bits
            xnor = (~(wa ^ wb)) & 0xFFFFFFFFFFFFFFFF
            # Fast bitwise popcount (Hamming weight)
            total_matches += bin(xnor).count("1")

        # Adjust for non-multiple of 64 padding
        remainder = original_len % 64
        if remainder != 0:
            excess_bits = 64 - remainder
            total_matches -= excess_bits

        # Bipolar inner product mapping: Matches - Mismatches
        mismatches = original_len - total_matches
        return total_matches - mismatches

    @staticmethod
    def bnn_packed_matrix_multiply(
        packed_mat_a: List[List[int]], 
        packed_mat_b_t: List[List[int]], 
        original_dim: int
    ) -> List[List[int]]:
        """
        Matrix multiplication for 1-bit weights and activations: C = A @ B^T.
        """
        rows_a = len(packed_mat_a)
        rows_b = len(packed_mat_b_t)
        result: List[List[int]] = []

        for i in range(rows_a):
            row_res = []
            for j in range(rows_b):
                dot = BitwiseSIMDCore.xnor_popcount_dot_product(
                    packed_mat_a[i], packed_mat_b_t[j], original_dim
                )
                row_res.append(dot)
            result.append(row_res)

        return result
