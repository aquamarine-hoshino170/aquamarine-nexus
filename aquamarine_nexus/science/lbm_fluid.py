class LatticeBoltzmannCore:
    """Lattice Boltzmann Method (LBM) D2Q9 Microscopic Fluid Engine"""

    WEIGHTS_D2Q9 = [4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36]
    DIRECTIONS_D2Q9 = [
        (0, 0), (1, 0), (0, 1), (-1, 0), (0, -1),
        (1, 1), (-1, 1), (-1, -1), (1, -1)
    ]

    @staticmethod
    def d2q9_equilibrium_density(rho: float, ux: float, uy: float) -> dict:
        """
        Computes 9 discrete equilibrium distribution functions f_i^(eq) for D2Q9 lattice:
        f_i^(eq) = w_i * rho * [1 + 3*(c_i . u) + 4.5*(c_i . u)^2 - 1.5*(u . u)]
        """
        w = LatticeBoltzmannCore.WEIGHTS_D2Q9
        c = LatticeBoltzmannCore.DIRECTIONS_D2Q9
        u_sq = ux**2 + uy**2

        feq = []
        for i in range(9):
            c_dot_u = c[i][0] * ux + c[i][1] * uy
            fi = w[i] * rho * (1.0 + 3.0 * c_dot_u + 4.5 * (c_dot_u ** 2) - 1.5 * u_sq)
            feq.append(round(fi, 6))

        return {
            "density_rho": rho,
            "velocity_vector": [ux, uy],
            "f_equilibrium_d2q9": feq
        }
