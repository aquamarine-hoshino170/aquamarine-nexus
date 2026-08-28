import re

class UnitConverter:
    """Scientific Unit Conversion & SI Dimensional Normalizer"""

    UNIT_TABLE = {
        # Length
        "m": 1.0, "km": 1e3, "cm": 1e-2, "mm": 1e-3, "um": 1e-6, "nm": 1e-9, "pm": 1e-12,
        "au": 1.495978707e11, "ly": 9.460730472e15, "pc": 3.085677581e16, "kpc": 3.085677581e19, "mpc": 3.085677581e22,
        # Mass
        "kg": 1.0, "g": 1e-3, "mg": 1e-6, "ug": 1e-9, "msun": 1.989e30, "mearth": 5.972e24,
        # Energy
        "j": 1.0, "ev": 1.602176634e-19, "kev": 1.602176634e-16, "mev": 1.602176634e-13, "gev": 1.602176634e-10, "erg": 1e-7,
        # Frequency / Time
        "s": 1.0, "ms": 1e-3, "us": 1e-6, "ns": 1e-9, "min": 60.0, "hr": 3600.0, "day": 86400.0, "yr": 31557600.0,
        "hz": 1.0, "khz": 1e3, "mhz": 1e6, "ghz": 1e9, "thz": 1e12,
        # Temperature
        "k": 1.0,
        # Velocity
        "m_s": 1.0, "km_s": 1e3, "c": 299792458.0,
        # Pressure / Magnetic Field
        "pa": 1.0, "kpa": 1e3, "bar": 1e5, "atm": 101325.0,
        "t": 1.0, "g_field": 1e-4
    }

    @classmethod
    def parse_quantity(cls, val_str: str):
        """Parses inputs like '10_kpc', '5.5_eV', '300_K' to base SI floats."""
        if not isinstance(val_str, str) or "_" not in val_str:
            return None

        parts = val_str.rsplit("_", 1)
        if len(parts) != 2:
            return None

        num_str, unit_str = parts[0], parts[1].lower()

        # Handle composite units like km_s
        if "_" in num_str:
            sub_parts = val_str.split("_", 1)
            if sub_parts[1].lower() in cls.UNIT_TABLE:
                num_str, unit_str = sub_parts[0], sub_parts[1].lower()

        try:
            val = float(num_str)
            if unit_str in cls.UNIT_TABLE:
                return val * cls.UNIT_TABLE[unit_str]
        except ValueError:
            pass

        return None
