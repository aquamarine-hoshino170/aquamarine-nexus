import math

class PlasmaLandauLengthCore:
    E_CHARGE = 1.602176634e-19
    EPSILON_0 = 8.8541878128e-12

    @staticmethod
    def landau_collision_length(temp_ev: float, z1: int = 1, z2: int = 1) -> dict:
        """r_L = (Z1 * Z2 * e^2) / (4 * pi * epsilon_0 * k_B * T)"""
        if temp_ev <= 0:
            raise ValueError("Temperature must be positive.")
            
        e = PlasmaLandauLengthCore.E_CHARGE
        eps0 = PlasmaLandauLengthCore.EPSILON_0
        thermal_energy_joules = temp_ev * e
        
        r_l = (abs(z1 * z2) * (e ** 2)) / (4.0 * math.pi * eps0 * thermal_energy_joules)
        return {
            "temperature_eV": temp_ev,
            "charge_product_Z1_Z2": z1 * z2,
            "landau_collision_distance_m": f"{r_l:.6e}"
        }
