class ColligativePropertiesPureCore:
    @staticmethod
    def freezing_point_depression(molality_m: float, k_f_c_kg_mol: float, vant_hoff_i: float = 1.0) -> dict:
        """Delta_T_f = i * K_f * m"""
        if molality_m < 0 or k_f_c_kg_mol <= 0 or vant_hoff_i < 1.0:
            raise ValueError("Molality must be >= 0, K_f > 0, and van 't Hoff factor i >= 1.")
            
        delta_tf = vant_hoff_i * k_f_c_kg_mol * molality_m
        return {
            "molality_mol_kg": molality_m,
            "cryoscopic_constant_Kf": k_f_c_kg_mol,
            "vant_hoff_factor_i": vant_hoff_i,
            "freezing_point_depression_deg_C": round(delta_tf, 4)
        }

    @staticmethod
    def boiling_point_elevation(molality_m: float, k_b_c_kg_mol: float, vant_hoff_i: float = 1.0) -> dict:
        """Delta_T_b = i * K_b * m"""
        if molality_m < 0 or k_b_c_kg_mol <= 0 or vant_hoff_i < 1.0:
            raise ValueError("Molality must be >= 0, K_b > 0, and van 't Hoff factor i >= 1.")
            
        delta_tb = vant_hoff_i * k_b_c_kg_mol * molality_m
        return {
            "molality_mol_kg": molality_m,
            "ebullioscopic_constant_Kb": k_b_c_kg_mol,
            "vant_hoff_factor_i": vant_hoff_i,
            "boiling_point_elevation_deg_C": round(delta_tb, 4)
        }
