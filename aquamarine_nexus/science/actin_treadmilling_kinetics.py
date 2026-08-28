class ActinTreadmillingKineticsCore:
    @staticmethod
    def treadmilling_net_flux(g_actin_conc_um: float, k_on_plus: float = 11.6, k_off_plus: float = 1.4, k_on_minus: float = 1.3, k_off_minus: float = 0.8) -> dict:
        """J_+ = k_on^+ * [G] - k_off^+, J_- = k_on^- * [G] - k_off^-, J_net = J_+ + J_-"""
        if g_actin_conc_um < 0 or any(k <= 0 for k in [k_on_plus, k_off_plus, k_on_minus, k_off_minus]):
            raise ValueError("Concentration must be non-negative and rate constants strictly positive.")
            
        c_crit_plus = k_off_plus / k_on_plus
        c_crit_minus = k_off_minus / k_on_minus
        
        flux_barbed_plus = (k_on_plus * g_actin_conc_um) - k_off_plus
        flux_pointed_minus = (k_on_minus * g_actin_conc_um) - k_off_minus
        total_flux = flux_barbed_plus + flux_pointed_minus
        
        # Steady-state treadmilling condition: flux_barbed_plus = -flux_pointed_minus
        c_treadmill = (k_off_plus + k_off_minus) / (k_on_plus + k_on_minus)
        
        return {
            "monomer_concentration_uM": g_actin_conc_um,
            "barbed_critical_conc_Cc_plus_uM": round(c_crit_plus, 4),
            "pointed_critical_conc_Cc_minus_uM": round(c_crit_minus, 4),
            "treadmilling_steady_state_conc_uM": round(c_treadmill, 4),
            "barbed_end_flux_s_inv": round(flux_barbed_plus, 4),
            "pointed_end_flux_s_inv": round(flux_pointed_minus, 4),
            "net_filament_growth_rate_s_inv": round(total_flux, 4),
            "polymerization_regime": "Pure Treadmilling" if abs(g_actin_conc_um - c_treadmill) < 1e-3 else ("Net Growth" if total_flux > 0 else "Net Depolymerization")
        }
