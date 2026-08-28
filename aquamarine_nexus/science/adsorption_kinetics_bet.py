class AdsorptionKineticsBETCore:
    N_AVOGADRO = 6.02214076e23

    @staticmethod
    def bet_isotherm_coverage(relative_pressure_x: float, c_constant: float) -> dict:
        """v / v_m = (C * x) / [ (1 - x) * (1 - x + C*x) ] where x = P / P_0"""
        if not (0.0 < relative_pressure_x < 1.0) or c_constant <= 0:
            raise ValueError("Relative pressure P/P0 must be in (0, 1) and BET constant C > 0.")
        
        x = relative_pressure_x
        c = c_constant
        theta_bet = (c * x) / ((1.0 - x) * (1.0 - x + (c * x)))
        
        return {
            "relative_pressure_P_P0": relative_pressure_x,
            "bet_constant_C": c_constant,
            "relative_adsorption_v_over_vm": round(theta_bet, 4),
            "regime": "Sub-monolayer" if theta_bet < 1.0 else "Multilayer Adsorption"
        }

    @staticmethod
    def specific_surface_area_bet(v_monolayer_stp_cm3: float, sample_mass_g: float, adsorbate_cross_section_nm2: float = 0.162) -> dict:
        """S_BET = (v_m * N_A * sigma) / (V_molar_STP * m_sample)"""
        if v_monolayer_stp_cm3 <= 0 or sample_mass_g <= 0 or adsorbate_cross_section_nm2 <= 0:
            raise ValueError("All parameters must be strictly positive.")
            
        v_molar_stp_cm3 = 22414.0
        sigma_m2 = adsorbate_cross_section_nm2 * 1e-18
        
        total_molecules = (v_monolayer_stp_cm3 * AdsorptionKineticsBETCore.N_AVOGADRO) / v_molar_stp_cm3
        total_surface_m2 = total_molecules * sigma_m2
        specific_surface_m2_g = total_surface_m2 / sample_mass_g
        
        return {
            "monolayer_volume_cm3_STP": v_monolayer_stp_cm3,
            "specific_surface_area_m2_g": round(specific_surface_m2_g, 2)
        }
