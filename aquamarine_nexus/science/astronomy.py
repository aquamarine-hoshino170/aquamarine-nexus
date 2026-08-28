import math

class NexusAstrophysics:
    """Cosmological Distance & Celestial Mechanics Core (Astropy Alternative)"""
    AU_METERS = 1.495978707e11
    LY_METERS = 9.460730472e15
    PARSEC_METERS = 3.085677581e16

    @staticmethod
    def distance_converter(val: float, unit_from: str, unit_to: str) -> dict:
        """Converts astronomical distances between 'm', 'au', 'ly', 'pc'"""
        table = {
            'm': 1.0,
            'au': NexusAstrophysics.AU_METERS,
            'ly': NexusAstrophysics.LY_METERS,
            'pc': NexusAstrophysics.PARSEC_METERS
        }
        u_from, u_to = unit_from.lower(), unit_to.lower()
        if u_from not in table or u_to not in table:
            raise ValueError(f"Supported units: {list(table.keys())}")
        meters = val * table[u_from]
        res = meters / table[u_to]
        return {"input_val": val, "from_unit": u_from, "converted_val": f"{res:.6e}", "to_unit": u_to}

    @staticmethod
    def stellar_luminosity(radius_solar: float, temp_k: float) -> dict:
        """Stefan-Boltzmann Stellar Luminosity: L/L_sun = (R/R_sun)^2 * (T/5778)^4"""
        t_ratio = temp_k / 5778.0
        l_ratio = (radius_solar ** 2) * (t_ratio ** 4)
        return {"radius_solar_units": radius_solar, "temperature_K": temp_k, "luminosity_solar_units": round(l_ratio, 4)}
