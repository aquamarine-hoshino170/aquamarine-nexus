import math

class ElectrodynamicsCore:
    """Classical Electrodynamics & Radiation Mechanics"""

    @staticmethod
    def poynting_vector(e_field_v_m: list, b_field_tesla: list) -> dict:
        """
        Calculates Poynting Vector S = (E x B) / mu_0
        Energy flux density vector in W/m^2.
        """
        mu_0 = 4.0 * math.pi * 1e-7
        # Cross product E x B
        ex, ey, ez = e_field_v_m
        bx, by, bz = b_field_tesla
        sx = (ey * bz - ez * by) / mu_0
        sy = (ez * bx - ex * bz) / mu_0
        sz = (ex * by - ey * bx) / mu_0
        mag = math.sqrt(sx**2 + sy**2 + sz**2)
        return {"S_vector_W_m2": [round(sx, 4), round(sy, 4), round(sz, 4)], "flux_magnitude_W_m2": round(mag, 4)}

    @staticmethod
    def larmor_radiation_power(charge_coulomb: float, acceleration_m_s2: float) -> dict:
        """
        Larmor Formula: Total power radiated by an accelerating non-relativistic point charge:
        P = (q^2 * a^2) / (6 * pi * epsilon_0 * c^3)
        """
        eps_0 = 8.8541878128e-12
        c = 299792458.0
        p = (charge_coulomb**2 * acceleration_m_s2**2) / (6.0 * math.pi * eps_0 * (c**3))
        return {"charge_C": charge_coulomb, "acceleration_m_s2": acceleration_m_s2, "radiated_power_Watts": f"{p:.6e}"}
