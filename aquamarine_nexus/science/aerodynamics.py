import math

class AerodynamicsCore:
    """Compressible Aerodynamics & Relativistic Acoustic Wave Mechanics"""

    C_LIGHT = 299792458.0

    @staticmethod
    def prandtl_glauert_correction(incompressible_cp: float, mach_number: float) -> dict:
        """
        Prandtl-Glauert compressibility correction for subsonic flow:
        C_p = C_p0 / sqrt(1 - M^2)
        """
        if mach_number >= 1.0 or mach_number < 0.0:
            raise ValueError("Mach number must satisfy 0 <= M < 1 for subsonic Prandtl-Glauert correction.")

        beta = math.sqrt(1.0 - (mach_number ** 2))
        cp_corrected = incompressible_cp / beta

        return {
            "mach_number": mach_number,
            "incompressible_Cp": incompressible_cp,
            "corrected_Cp": round(cp_corrected, 5),
            "amplification_factor": round(1.0 / beta, 5)
        }

    @staticmethod
    def relativistic_doppler(source_freq_hz: float, velocity_m_s: float, theta_rad: float = 0.0) -> dict:
        """
        Relativistic Doppler frequency shift:
        f_observed = f_source * sqrt(1 - beta^2) / (1 - beta * cos(theta))
        where beta = v / c
        """
        c = AerodynamicsCore.C_LIGHT
        if abs(velocity_m_s) >= c:
            raise ValueError("Velocity cannot equal or exceed the speed of light.")

        beta = velocity_m_s / c
        gamma_inv = math.sqrt(1.0 - (beta ** 2))
        denominator = 1.0 - beta * math.cos(theta_rad)

        f_obs = source_freq_hz * (gamma_inv / denominator)

        return {
            "source_frequency_Hz": source_freq_hz,
            "velocity_m_s": velocity_m_s,
            "beta_fraction": round(beta, 6),
            "observed_frequency_Hz": f"{f_obs:.6e}",
            "frequency_ratio": round(f_obs / source_freq_hz, 5)
        }
