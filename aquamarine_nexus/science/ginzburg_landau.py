import math

class GinzburgLandauCore:
    M_E = 9.10938356e-31
    E_CHARGE = 1.602176634e-19
    MU_0 = 1.25663706212e-6
    H_BAR = 1.054571817e-34

    @staticmethod
    def gl_coherence_and_penetration(alpha_parameter: float, beta_parameter: float, super_electron_density_m3: float) -> dict:
        """xi(T) = hbar / sqrt(2 * m * |alpha|), lambda_L = sqrt(m / (mu_0 * n_s * e^2)), kappa = lambda / xi"""
        if alpha_parameter >= 0 or beta_parameter <= 0 or super_electron_density_m3 <= 0:
            raise ValueError("alpha must be < 0 for superconducting state; beta and density must be positive.")
        m = GinzburgLandauCore.M_E
        e = GinzburgLandauCore.E_CHARGE
        mu0 = GinzburgLandauCore.MU_0
        hbar = GinzburgLandauCore.H_BAR
        
        xi = hbar / math.sqrt(2.0 * m * abs(alpha_parameter))
        lambda_l = math.sqrt(m / (mu0 * super_electron_density_m3 * (e ** 2)))
        kappa = lambda_l / xi
        
        sc_type = "Type-I Superconductor (kappa < 1/sqrt(2))" if kappa < (1.0 / math.sqrt(2.0)) else "Type-II Superconductor (kappa > 1/sqrt(2))"
        return {
            "coherence_length_xi_m": f"{xi:.6e}",
            "london_penetration_lambda_m": f"{lambda_l:.6e}",
            "ginzburg_landau_parameter_kappa": round(kappa, 4),
            "superconductor_classification": sc_type
        }

    @staticmethod
    def thermodynamic_critical_field(alpha_parameter: float, beta_parameter: float) -> dict:
        """B_c = mu_0 * sqrt( alpha^2 / (mu_0 * beta) ) = sqrt( mu_0 * alpha^2 / beta )"""
        if alpha_parameter == 0 or beta_parameter <= 0:
            raise ValueError("Invalid alpha or beta.")
        mu0 = GinzburgLandauCore.MU_0
        b_c = math.sqrt((mu0 * (alpha_parameter ** 2)) / beta_parameter)
        return {
            "critical_field_Bc_Tesla": f"{b_c:.6e}",
            "condensation_energy_density_J_m3": f"{(alpha_parameter**2 / (2.0 * beta_parameter)):.6e}"
        }
