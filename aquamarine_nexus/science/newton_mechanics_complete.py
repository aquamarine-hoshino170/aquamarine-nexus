import math

class NewtonCompleteMechanicsCore:
    @staticmethod
    def newton_sound_speed_isothermal(pressure_pa: float, density_kg_m3: float) -> dict:
        """Newton's original isothermal sound speed: v = sqrt(P / rho)"""
        if pressure_pa <= 0 or density_kg_m3 <= 0: raise ValueError("Invalid inputs.")
        v = math.sqrt(pressure_pa / density_kg_m3)
        return {"pressure_Pa": pressure_pa, "density_kg_m3": density_kg_m3, "isothermal_sound_speed_m_s": round(v, 2)}

    @staticmethod
    def newton_third_law_momentum_transfer(mass_1: float, vel_1: float, mass_2: float, vel_2: float) -> dict:
        """Isolated momentum conservation: m1*v1 + m2*v2 = Constant"""
        p_total = (mass_1 * vel_1) + (mass_2 * vel_2)
        return {"mass1": mass_1, "mass2": mass_2, "total_momentum_kg_m_s": round(p_total, 4)}
