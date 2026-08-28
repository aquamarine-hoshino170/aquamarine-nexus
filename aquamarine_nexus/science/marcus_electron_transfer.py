import math

class MarcusElectronTransferCore:
    H_BAR = 1.054571817e-34
    K_BOLTZ = 1.380649e-23
    E_CHARGE = 1.602176634e-19

    @staticmethod
    def marcus_et_rate(delta_g_0_ev: float, reorganization_lambda_ev: float, hab_coupling_ev: float, temp_k: float = 298.15) -> dict:
        """k_ET = (2*pi / hbar) * |H_AB|^2 * (1 / sqrt(4*pi*lambda*k_B*T)) * exp( - (Delta_G0 + lambda)^2 / (4*lambda*k_B*T) )"""
        if reorganization_lambda_ev <= 0 or hab_coupling_ev <= 0 or temp_k <= 0:
            raise ValueError("Reorganization energy, electronic coupling, and temperature must be strictly positive.")
            
        e = MarcusElectronTransferCore.E_CHARGE
        kb = MarcusElectronTransferCore.K_BOLTZ
        hbar = MarcusElectronTransferCore.H_BAR
        
        lambda_j = reorganization_lambda_ev * e
        hab_j = hab_coupling_ev * e
        dg0_j = delta_g_0_ev * e
        kb_t_j = kb * temp_k
        
        prefactor = (2.0 * math.pi / hbar) * (hab_j ** 2) / math.sqrt(4.0 * math.pi * lambda_j * kb_t_j)
        activation_barrier_j = ((dg0_j + lambda_j) ** 2) / (4.0 * lambda_j)
        exponent = - activation_barrier_j / kb_t_j
        
        k_et = prefactor * math.exp(exponent) if exponent > -700 else 0.0
        
        regime = "Normal Marcus Regime" if -delta_g_0_ev < reorganization_lambda_ev else ("Activationless Regime" if abs(-delta_g_0_ev - reorganization_lambda_ev) < 1e-3 else "Inverted Marcus Region")
        
        return {
            "delta_G0_eV": delta_g_0_ev,
            "reorganization_lambda_eV": reorganization_lambda_ev,
            "activation_barrier_eV": round(activation_barrier_j / e, 4),
            "rate_constant_k_ET_s_inv": f"{k_et:.6e}",
            "marcus_regime": regime
        }
