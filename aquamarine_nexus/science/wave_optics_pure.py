import math

class WaveOpticsPureCore:
    @staticmethod
    def young_double_slit_fringe_width(wavelength_m: float, slit_distance_d_m: float, screen_distance_d_cap_m: float) -> dict:
        """beta = (lambda * D) / d"""
        if wavelength_m <= 0 or slit_distance_d_m <= 0 or screen_distance_d_cap_m <= 0:
            raise ValueError("Wavelength and distances must be strictly positive.")
            
        fringe_width = (wavelength_m * screen_distance_d_cap_m) / slit_distance_d_m
        return {
            "wavelength_nm": round(wavelength_m * 1e9, 2),
            "slit_separation_mm": round(slit_distance_d_m * 1e3, 4),
            "screen_distance_m": screen_distance_d_cap_m,
            "fringe_width_beta_m": f"{fringe_width:.6e}",
            "fringe_width_beta_mm": round(fringe_width * 1e3, 4)
        }

    @staticmethod
    def single_slit_diffraction_intensity(intensity_i0: float, slit_width_a_m: float, wavelength_m: float, angle_rad: float) -> dict:
        """I(theta) = I_0 * ( sin(beta) / beta )^2 where beta = (pi * a * sin(theta)) / lambda"""
        if slit_width_a_m <= 0 or wavelength_m <= 0 or intensity_i0 < 0:
            raise ValueError("Physical dimensions must be valid and positive.")
            
        if angle_rad == 0.0:
            return {"angle_rad": 0.0, "intensity_ratio": 1.0, "diffracted_intensity": intensity_i0}
            
        beta = (math.pi * slit_width_a_m * math.sin(angle_rad)) / wavelength_m
        ratio = (math.sin(beta) / beta) ** 2
        intensity = intensity_i0 * ratio
        
        return {
            "angle_rad": round(angle_rad, 6),
            "phase_parameter_beta": round(beta, 6),
            "intensity_ratio": round(ratio, 8),
            "diffracted_intensity": round(intensity, 6)
        }
