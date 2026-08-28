import math

class AndersonLocalizationCore:
    @staticmethod
    def one_dimensional_localization_length(disorder_width_w: float, fermi_velocity_vf: float = 1.0, lattice_constant_a: float = 1.0) -> dict:
        """xi / a approx 96 * (E_F / W)^2 in 1D Born approximation for tight-binding chain"""
        if disorder_width_w <= 0 or lattice_constant_a <= 0 or fermi_velocity_vf <= 0:
            raise ValueError("Disorder width and spatial scale must be strictly positive.")
            
        # In weak disorder regime (W << hopping t): xi ~ 96 * (t / W)^2 * a
        loc_length_ratio = 96.0 / (disorder_width_w ** 2)
        xi_meters = loc_length_ratio * lattice_constant_a
        
        return {
            "disorder_strength_W": disorder_width_w,
            "lattice_spacing_m": f"{lattice_constant_a:.6e}",
            "localization_length_over_a": round(loc_length_ratio, 4),
            "localization_length_xi_m": f"{xi_meters:.6e}",
            "electronic_phase": "Exponentially Localized (Insulator)" if loc_length_ratio < 1000.0 else "Weakly Localized / Ballistic"
        }
