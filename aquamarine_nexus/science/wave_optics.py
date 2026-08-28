import math

class WaveOpticsCore:
    @staticmethod
    def rayleigh_diffraction_limit(wavelength_m: float, aperture_diameter_m: float) -> dict:
        """theta = 1.22 * lambda / D"""
        if aperture_diameter_m <= 0 or wavelength_m <= 0: raise ValueError("Invalid parameters.")
        theta_rad = 1.22 * wavelength_m / aperture_diameter_m
        return {"angular_resolution_radians": f"{theta_rad:.6e}", "angular_resolution_arcsec": round(math.degrees(theta_rad) * 3600.0, 4)}

    @staticmethod
    def beat_frequency_superposition(freq1_hz: float, freq2_hz: float) -> dict:
        """f_beat = |f1 - f2|, f_avg = (f1 + f2) / 2"""
        f_beat = abs(freq1_hz - freq2_hz)
        f_avg = (freq1_hz + freq2_hz) / 2.0
        return {"beat_frequency_Hz": round(f_beat, 4), "carrier_average_Hz": round(f_avg, 4)}

    @staticmethod
    def fabry_perot_finesse(reflectivity_r: float) -> dict:
        """F = (pi * sqrt(R)) / (1 - R)"""
        if reflectivity_r <= 0 or reflectivity_r >= 1.0: raise ValueError("R must be in (0, 1).")
        finesse = (math.pi * math.sqrt(reflectivity_r)) / (1.0 - reflectivity_r)
        return {"reflectivity_R": reflectivity_r, "cavity_finesse": round(finesse, 4)}
