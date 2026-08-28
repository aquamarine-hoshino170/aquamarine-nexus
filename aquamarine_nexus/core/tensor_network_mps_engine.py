import math
from typing import List, Tuple

class MatrixProductStateCore:
    """
    Zero-Dependency Quantum Tensor Network & Matrix Product State (MPS) Core.
    Compresses exponential state spaces (2^N) into linear chains O(N * d * D^2)
    using iterative tensor contractions and Schmidt bond dimension truncations.
    """

    @staticmethod
    def create_random_mps(num_sites: int, phys_dim: int = 2, bond_dim: int = 4) -> List[List[List[List[float]]]]:
        """
        Initializes an MPS chain: tensors of shape (bond_left, phys, bond_right).
        Left boundary: (1, d, D), Middle: (D, d, D), Right boundary: (D, d, 1).
        """
        mps = []
        for i in range(num_sites):
            d_l = 1 if i == 0 else bond_dim
            d_r = 1 if i == num_sites - 1 else bond_dim
            scale = 1.0 / math.sqrt(float(d_l * phys_dim))

            # Tensor shape: [d_l][phys][d_r]
            site_tensor = [
                [
                    [(0.1 * ((a + p + b) % 7) * scale) for b in range(d_r)]
                    for p in range(phys_dim)
                ]
                for a in range(d_l)
            ]
            mps.append(site_tensor)
        return mps

    @staticmethod
    def contract_mps_inner_product(mps_a: List[List[List[List[float]]]], mps_b: List[List[List[List[float]]]]) -> float:
        """
        Computes exact overlap <A|B> via sequential left-to-right transfer matrix contraction:
        O(N * d * D^3) complexity instead of exponential O(d^N).
        """
        num_sites = len(mps_a)
        # Transfer matrix E initialized to [[1.0]] (shape: 1 x 1)
        E = [[1.0]]

        for i in range(num_sites):
            A = mps_a[i]  # shape: (d_la, d, d_ra)
            B = mps_b[i]  # shape: (d_lb, d, d_rb)

            d_la, phys_d, d_ra = len(A), len(A[0]), len(A[0][0])
            d_lb, _, d_rb = len(B), len(B[0]), len(B[0][0])

            # Next transfer matrix E_next shape: (d_ra, d_rb)
            E_next = [[0.0] * d_rb for _ in range(d_ra)]

            for alpha_a in range(d_la):
                for alpha_b in range(d_lb):
                    e_val = E[alpha_a][alpha_b]
                    if e_val == 0.0:
                        continue
                    for p in range(phys_d):
                        for beta_a in range(d_ra):
                            a_val = A[alpha_a][p][beta_a]
                            for beta_b in range(d_rb):
                                b_val = B[alpha_b][p][beta_b]
                                E_next[beta_a][beta_b] += e_val * a_val * b_val

            E = E_next

        return E[0][0]
