class RenalFiltrationMechanicsCore:
    @staticmethod
    def glomerular_net_filtration_pressure(p_gc_hydrostatic: float, p_bs_bowman_hydrostatic: float, pi_gc_oncotic: float, pi_bs_bowman_oncotic: float = 0.0) -> dict:
        """NFP = (P_GC - P_BS) - (pi_GC - pi_BS)"""
        if p_gc_hydrostatic <= 0 or p_bs_bowman_hydrostatic < 0 or pi_gc_oncotic < 0:
            raise ValueError("Pressures must be non-negative, with capillary hydrostatic pressure strictly positive.")
            
        hydrostatic_gradient = p_gc_hydrostatic - p_bs_bowman_hydrostatic
        oncotic_gradient = pi_gc_oncotic - pi_bs_bowman_oncotic
        nfp = hydrostatic_gradient - oncotic_gradient
        
        return {
            "glomerular_capillary_hydrostatic_P_GC_mmHg": p_gc_hydrostatic,
            "bowman_space_hydrostatic_P_BS_mmHg": p_bs_bowman_hydrostatic,
            "glomerular_capillary_oncotic_pi_GC_mmHg": pi_gc_oncotic,
            "net_filtration_pressure_NFP_mmHg": round(nfp, 2),
            "filtration_state": "Forward Ultrafiltration" if nfp > 0 else "Filtration Cessation / Equilibrium"
        }

    @staticmethod
    def glomerular_filtration_rate_gfr(k_f_filtration_coeff: float, nfp_mmhg: float) -> dict:
        """GFR = K_f * NFP (in mL/min)"""
        if k_f_filtration_coeff <= 0:
            raise ValueError("Filtration coefficient K_f must be strictly positive.")
            
        gfr_val = k_f_filtration_coeff * nfp_mmhg
        gfr_daily_liters = (gfr_val * 60.0 * 24.0) / 1000.0
        
        return {
            "filtration_coefficient_Kf_mL_min_mmHg": k_f_filtration_coeff,
            "net_filtration_pressure_mmHg": nfp_mmhg,
            "GFR_mL_per_min": round(max(0.0, gfr_val), 2),
            "daily_ultrafiltrate_Liters": round(max(0.0, gfr_daily_liters), 2)
        }
