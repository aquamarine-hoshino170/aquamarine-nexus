import math

class BlackHoleThermoCore:
    """Bekenstein-Hawking Black Hole Thermodynamics & Eddington Limit Core"""

    C_LIGHT = 299792458.0
    G_CONST = 6.67430e-11
    H_BAR = 1.054571817e-34
    K_BOLTZ = 1.380649e-23
    M_PROTON = 1.67262192369e-27
    SIGMA_THOMSON = 6.6524587321e-29

    @staticmethod
    def hawking_thermodynamics(mass_kg: float) -> dict:
        """
        Computes Event Horizon Area (A), Hawking Temperature (T_H), and Bekenstein-Hawking Entropy (S_BH):
        A = 16 * pi * G^2 * M^2 / c^4
        T_H = (hbar * c^3) / (8 * pi * G * M * k_B)
        S_BH = (k_B * c^3 * A) / (4 * G * hbar)
        """
        if mass_kg <= 0:
            raise ValueError("Black hole mass must be positive.")

        c = BlackHoleThermoCore.C_LIGHT
        g = BlackHoleThermoCore.G_CONST
        hbar = BlackHoleThermoCore.H_BAR
        kb = BlackHoleThermoCore.K_BOLTZ

        # Schwarzschild radius r_s = 2GM / c^2
        r_s = (2.0 * g * mass_kg) / (c ** 2)
        # Horizon surface area A = 4 * pi * r_s^2
        area = 4.0 * math.pi * (r_s ** 2)

        t_hawking = (hbar * (c ** 3)) / (8.0 * math.pi * g * mass_kg * kb)
        s_entropy = (kb * (c ** 3) * area) / (4.0 * g * hbar)

        return {
            "mass_kg": mass_kg,
            "schwarzschild_radius_m": f"{r_s:.6e}",
            "horizon_area_m2": f"{area:.6e}",
            "hawking_temperature_K": f"{t_hawking:.6e}",
            "bekenstein_entropy_J_K": f"{s_entropy:.6e}"
        }

    @staticmethod
    def eddington_luminosity(mass_kg: float) -> dict:
        """
        Computes Eddington Critical Accretion Luminosity:
        L_edd = (4 * pi * G * M * m_p * c) / sigma_T
        """
        if mass_kg <= 0:
            raise ValueError("Mass must be positive.")

        c = BlackHoleThermoCore.C_LIGHT
        g = BlackHoleThermoCore.G_CONST
        m_p = BlackHoleThermoCore.M_PROTON
        sigma_t = BlackHoleThermoCore.SIGMA_THOMSON

        l_edd = (4.0 * math.pi * g * mass_kg * m_p * c) / sigma_t
        solar_l = 3.828e26
        return {
            "mass_kg": mass_kg,
            "eddington_luminosity_Watts": f"{l_edd:.6e}",
            "luminosity_solar_units": f"{l_edd / solar_l:.4e}"
        }
