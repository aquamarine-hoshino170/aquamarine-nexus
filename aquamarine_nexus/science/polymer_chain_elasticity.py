import math

class PolymerChainElasticityCore:
    K_BOLTZ = 1.380649e-23

    @staticmethod
    def fjc_entropic_restoring_force(end_to_end_distance_nm: float, kuhn_length_b_nm: float, num_kuhn_segments_n: int, temp_k: float = 300.0) -> dict:
        """Gaussian regime: F = (3 * k_B * T / (N * b^2)) * R, Contour length L_c = N * b"""
        if end_to_end_distance_nm < 0 or kuhn_length_b_nm <= 0 or num_kuhn_segments_n <= 0 or temp_k <= 0:
            raise ValueError("Dimensions, segment counts, and temperature must be valid.")
            
        l_contour_nm = num_kuhn_segments_n * kuhn_length_b_nm
        if end_to_end_distance_nm >= l_contour_nm:
            raise ValueError("End-to-end extension cannot equal or exceed the total contour length in linear regime.")
            
        kb_t_j = PolymerChainElasticityCore.K_BOLTZ * temp_k
        r_m = end_to_end_distance_nm * 1e-9
        b_m = kuhn_length_b_nm * 1e-9
        
        # Gaussian spring constant k_spring = 3 * k_B * T / (N * b^2)
        k_spring = (3.0 * kb_t_j) / (num_kuhn_segments_n * (b_m ** 2))
        force_n = k_spring * r_m
        force_pn = force_n * 1e12
        
        relative_extension = end_to_end_distance_nm / l_contour_nm
        
        return {
            "contour_length_Lc_nm": round(l_contour_nm, 2),
            "relative_extension_ratio": round(relative_extension, 4),
            "entropic_spring_constant_N_m": f"{k_spring:.6e}",
            "entropic_restoring_force_pN": round(force_pn, 4),
            "elasticity_regime": "Gaussian Linear Entropy" if relative_extension < 0.5 else "Non-linear Langevin Strain"
        }
