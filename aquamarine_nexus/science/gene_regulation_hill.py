class GeneRegulationHillCore:
    @staticmethod
    def hill_transcription_kinetics(tf_conc_nm: float, k_dissociation_nm: float, hill_coeff_n: float, v_max_transcription: float = 100.0, is_repressor: bool = False) -> dict:
        """Activation: V = V_max * [TF]^n / (K^n + [TF]^n), Repression: V = V_max * K^n / (K^n + [TF]^n)"""
        if tf_conc_nm < 0 or k_dissociation_nm <= 0 or hill_coeff_n <= 0 or v_max_transcription <= 0:
            raise ValueError("Parameters must be strictly positive and concentration non-negative.")
            
        tf_pow = tf_conc_nm ** hill_coeff_n
        k_pow = k_dissociation_nm ** hill_coeff_n
        
        if is_repressor:
            rate = v_max_transcription * k_pow / (k_pow + tf_pow)
        else:
            rate = v_max_transcription * tf_pow / (k_pow + tf_pow)
            
        return {
            "transcription_factor_nM": tf_conc_nm,
            "k_threshold_nM": k_dissociation_nm,
            "hill_coefficient_n": hill_coeff_n,
            "mode": "Repression" if is_repressor else "Activation",
            "transcription_rate_mRNA_hr": round(rate, 4),
            "fractional_expression": round(rate / v_max_transcription, 6)
        }
