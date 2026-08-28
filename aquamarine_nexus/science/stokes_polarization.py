import math

class StokesPolarizationCore:
    @staticmethod
    def stokes_parameters_from_intensities(i_h: float, i_v: float, i_45: float, i_135: float, i_rcp: float, i_lcp: float) -> dict:
        """
        S0 = I_H + I_V
        S1 = I_H - I_V
        S2 = I_45 - I_135
        S3 = I_RCP - I_LCP
        """
        s0 = i_h + i_v
        if s0 <= 0:
            raise ValueError("Total intensity must be strictly positive.")
        
        s1 = i_h - i_v
        s2 = i_45 - i_135
        s3 = i_rcp - i_lcp
        
        dop = math.sqrt(s1**2 + s2**2 + s3**2) / s0
        return {
            "S0_total_intensity": round(s0, 4),
            "S1_linear_horizontal": round(s1, 4),
            "S2_linear_45deg": round(s2, 4),
            "S3_circular": round(s3, 4),
            "degree_of_polarization_DOP": round(min(dop, 1.0), 5)
        }

    @staticmethod
    def malus_intensity_law(i0_intensity: float, angle_degrees: float) -> dict:
        """I = I_0 * cos^2(theta)"""
        if i0_intensity < 0:
            raise ValueError("Intensity must be non-negative.")
        
        theta_rad = math.radians(angle_degrees)
        transmitted = i0_intensity * (math.cos(theta_rad) ** 2)
        return {"angle_deg": angle_degrees, "transmitted_intensity": round(transmitted, 6)}
