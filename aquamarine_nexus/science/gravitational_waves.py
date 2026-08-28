import math

class GravitationalWaveCore:
    """Gravitational Wave Physics & Kerr Spacetime Geometry"""

    G_CONST = 6.67430e-11
    C_LIGHT = 299792458.0

    @staticmethod
    def binary_chirp_mass(m1_kg: float, m2_kg: float) -> dict:
        """
        Computes Chirp Mass M_chirp = (m1 * m2)^(3/5) / (m1 + m2)^(1/5)
        and Total Mass M_tot = m1 + m2
        """
        if m1_kg <= 0 or m2_kg <= 0:
            raise ValueError("Masses must be strictly positive.")

        m_chirp = ((m1_kg * m2_kg) ** (3.0 / 5.0)) / ((m1_kg + m2_kg) ** (1.0 / 5.0))
        solar_mass = 1.989e30

        return {
            "m1_kg": m1_kg,
            "m2_kg": m2_kg,
            "chirp_mass_kg": f"{m_chirp:.6e}",
            "chirp_mass_solar": round(m_chirp / solar_mass, 4),
            "symmetric_mass_ratio_eta": round((m1_kg * m2_kg) / ((m1_kg + m2_kg) ** 2), 5)
        }

    @staticmethod
    def gw_quadrupole_power(m1_kg: float, m2_kg: float, separation_r_m: float) -> dict:
        """
        Peters-Mathews Quadrupole Formula: Radiated Gravitational Wave Power
        P = (32 / 5) * (G^4 / c^5) * (m1^2 * m2^2 * (m1 + m2)) / (r^5)
        """
        if separation_r_m <= 0:
            raise ValueError("Orbital separation must be positive.")

        g = GravitationalWaveCore.G_CONST
        c = GravitationalWaveCore.C_LIGHT

        factor = (32.0 / 5.0) * (g ** 4) / (c ** 5)
        mass_term = (m1_kg ** 2) * (m2_kg ** 2) * (m1_kg + m2_kg)
        power_watts = factor * (mass_term / (separation_r_m ** 5))

        return {
            "separation_r_m": separation_r_m,
            "radiated_gw_power_Watts": f"{power_watts:.6e}"
        }

    @staticmethod
    def kerr_ergosphere_radius(mass_kg: float, spin_param_a: float, theta_rad: float) -> dict:
        """
        Calculates Kerr Ergosphere Outer Boundary in Boyer-Lindquist coordinates:
        r_E(theta) = r_g + sqrt(r_g^2 - a^2 * cos^2(theta)) where r_g = GM / c^2
        """
        g = GravitationalWaveCore.G_CONST
        c = GravitationalWaveCore.C_LIGHT

        r_g = (g * mass_kg) / (c ** 2)
        if spin_param_a > r_g:
            raise ValueError(f"Spin parameter a ({spin_param_a}) cannot exceed r_g ({r_g}) to avoid naked singularity.")

        discriminant = (r_g ** 2) - ((spin_param_a * math.cos(theta_rad)) ** 2)
        r_e = r_g + math.sqrt(discriminant)

        return {
            "gravitational_radius_r_g": f"{r_g:.6e}",
            "ergosphere_radius_m": f"{r_e:.6e}",
            "theta_rad": theta_rad
        }
