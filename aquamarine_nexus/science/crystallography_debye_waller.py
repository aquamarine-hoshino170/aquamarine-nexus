import math

class CrystallographyDebyeWallerCore:
    @staticmethod
    def b_factor_atomic_displacement(mean_square_displacement_u2_angstrom2: float) -> dict:
        """B = 8 * pi^2 * <u^2>"""
        if mean_square_displacement_u2_angstrom2 < 0:
            raise ValueError("Mean-square displacement <u^2> must be non-negative.")
            
        b_factor = 8.0 * (math.pi ** 2) * mean_square_displacement_u2_angstrom2
        return {
            "mean_square_displacement_Angstrom2": mean_square_displacement_u2_angstrom2,
            "isotropic_B_factor_Angstrom2": round(b_factor, 4)
        }

    @staticmethod
    def structure_factor_intensity_attenuation(b_factor: float, theta_deg: float, wavelength_angstrom: float) -> dict:
        """Attenuation = exp( - 2 * B * (sin(theta) / lambda)^2 )"""
        if wavelength_angstrom <= 0 or b_factor < 0:
            raise ValueError("Wavelength must be positive and B-factor non-negative.")
            
        theta_rad = math.radians(theta_deg)
        sin_theta_over_lambda = math.sin(theta_rad) / wavelength_angstrom
        exponent = - 2.0 * b_factor * (sin_theta_over_lambda ** 2)
        attenuation = math.exp(exponent) if exponent > -700 else 0.0
        
        return {
            "B_factor": b_factor,
            "scattering_angle_theta_deg": theta_deg,
            "wavelength_Angstrom": wavelength_angstrom,
            "thermal_intensity_damping_factor": round(attenuation, 6)
        }
