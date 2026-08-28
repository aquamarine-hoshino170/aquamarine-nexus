import math

class SupergravityStringCore:
    H_BAR = 1.054571817e-34
    C_LIGHT = 299792458.0

    @staticmethod
    def regge_trajectory_spin(string_tension_alpha_prime: float, angular_momentum_j: float) -> dict:
        """M^2 = (J - alpha_0) / alpha_prime"""
        if string_tension_alpha_prime <= 0 or angular_momentum_j < 0:
            raise ValueError("alpha_prime must be > 0 and spin J >= 0.")
        alpha_0 = 1.0  # Open bosonic / standard Regge intercept
        m_squared = max(0.0, (angular_momentum_j - alpha_0) / string_tension_alpha_prime)
        m_val = math.sqrt(m_squared)
        return {
            "spin_J": angular_momentum_j,
            "alpha_prime_slope": string_tension_alpha_prime,
            "mass_squared": round(m_squared, 6),
            "mass_spectrum": round(m_val, 6)
        }

    @staticmethod
    def d_brane_tension(p_spatial_dim: int, string_coupling_gs: float, string_length_ls: float) -> dict:
        """T_p = 1 / ( (2*pi)^p * g_s * l_s^(p+1) )"""
        if string_coupling_gs <= 0 or string_length_ls <= 0 or p_spatial_dim < 0:
            raise ValueError("Parameters must be strictly positive.")
        denom = ((2.0 * math.pi) ** p_spatial_dim) * string_coupling_gs * (string_length_ls ** (p_spatial_dim + 1))
        tension = 1.0 / denom
        return {
            "p_brane_dimension": p_spatial_dim,
            "string_coupling_gs": string_coupling_gs,
            "d_brane_tension_T_p": f"{tension:.6e}"
        }
