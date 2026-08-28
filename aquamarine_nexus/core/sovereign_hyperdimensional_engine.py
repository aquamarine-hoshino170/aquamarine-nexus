import random
from typing import List, Tuple

class HyperdimensionalVectorEngine:
    """
    Zero-Dependency 10,000-Bit Hyperdimensional Computing (HDC) Core.
    Replaces floating-point matrix multiplication with bitwise algebraic operations:
    - Binding (Association): Bitwise XOR
    - Bundling (Superposition): Majority Bit Voting
    - Permutation (Sequence / Order): Circular Bit Shift
    - Distance (Similarity): Normalized Hamming Distance
    """
    def __init__(self, dimension: int = 10000):
        # Must be multiple of 64 for 64-bit integer word packing
        self.dimension = (dimension // 64) * 64
        self.num_words = self.dimension // 64

    def generate_random_hypervector(self) -> List[int]:
        """Generates a pseudo-random orthogonal hypervector packed in 64-bit integers."""
        return [random.getrandbits(64) for _ in range(self.num_words)]

    @staticmethod
    def bind_xor(vec_a: List[int], vec_b: List[int]) -> List[int]:
        """Binds two concepts together using bitwise XOR (O(D/64) complexity)."""
        return [a ^ b for a, b in zip(vec_a, vec_b)]

    def permute_shift(self, vec: List[int], shift_amount: int = 1) -> List[int]:
        """Circular bit permutation for encoding temporal sequence order."""
        # Unpack, rotate, and pack back efficiently
        bit_str = "".join(f"{word:064b}" for word in vec)
        shift = shift_amount % self.dimension
        rotated_str = bit_str[shift:] + bit_str[:shift]
        return [int(rotated_str[i:i+64], 2) for i in range(0, self.dimension, 64)]

    def bundle_majority(self, vector_list: List[List[int]]) -> List[int]:
        """Superposition/Bundling of multiple vectors via majority voting."""
        k = len(vector_list)
        half_k = k / 2.0
        result = [0] * self.num_words

        for w_idx in range(self.num_words):
            accum_word = 0
            for bit_pos in range(64):
                ones_count = sum((vec[w_idx] >> (63 - bit_pos)) & 1 for vec in vector_list)
                if ones_count >= half_k:
                    accum_word |= (1 << (63 - bit_pos))
            result[w_idx] = accum_word

        return result

    @staticmethod
    def hamming_similarity(vec_a: List[int], vec_b: List[int]) -> float:
        """Computes normalized cosine-like similarity from Hamming distance (1.0 = Identical, 0.5 = Orthogonal)."""
        total_mismatch = 0
        total_bits = len(vec_a) * 64

        for a, b in zip(vec_a, vec_b):
            xor_val = a ^ b
            # Native Popcount (Hamming weight)
            total_mismatch += bin(xor_val).count('1')

        return 1.0 - (total_mismatch / float(total_bits))
