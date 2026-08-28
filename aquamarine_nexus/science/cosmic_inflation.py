import math

class CosmicInflationCore:
    M_PLANCK_REDUCED = 2.435e18  # GeV

    @staticmethod
    def slow_roll_parameters(v_potential: float, v_prime: float, v_double_prime: float) -> dict:
        """epsilon = (M_p^2 / 2) * (V'/V)^2, eta = M_p^2 * (V''/V)"""
        if v_potential <= 0:
            raise ValueError("Potential V must be positive.")
        mp = CosmicInflationCore.M_PLANCK_REDUCED
        
        epsilon = 0.5 * (mp ** 2) * ((v_prime / v_potential) ** 2)
        eta = (mp ** 2) * (v_double_prime / v_potential)
        
        # Tensor-to-scalar ratio r and scalar spectral tilt n_s
        r_ratio = 16.0 * epsilon
        n_s = 1.0 - 6.0 * epsilon + 2.0 * eta
        
        return {
            "slow_roll_epsilon": round(epsilon, 6),
            "slow_roll_eta": round(eta, 6),
            "scalar_spectral_index_ns": round(n_s, 6),
            "tensor_to_scalar_ratio_r": round(r_ratio, 6),
            "is_inflation_active": epsilon < 1.0
        }

    @staticmethod
    def e_folds_inflation(v_potential: float, v_prime: float, delta_phi: float) -> dict:
        """N = (1 / M_p^2) * int (V / V') dphi approx (V / (M_p^2 * V')) * delta_phi"""
        if v_prime == 0:
            raise ValueError("V' cannot be zero.")
        mp = CosmicInflationCore.M_PLANCK_REDUCED
        n_efolds = (v_potential / ((mp ** 2) * v_prime)) * delta_phi
        return {"e_folds_N": round(abs(n_efolds), 2)}
