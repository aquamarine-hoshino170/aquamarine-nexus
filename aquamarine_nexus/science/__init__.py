import math

class ClassicalMechanics:
    """Rigid Body & Lagrangian Dynamics"""
    @staticmethod
    def projectile_motion(v0: float, angle_deg: float, g: float = 9.80665) -> dict:
        """Trajectory metrics: Range, Max Height, Time of Flight"""
        rad = math.radians(angle_deg)
        t_flight = (2.0 * v0 * math.sin(rad)) / g
        h_max = ((v0 * math.sin(rad)) ** 2) / (2.0 * g)
        r_max = ((v0 ** 2) * math.sin(2.0 * rad)) / g
        return {"time_of_flight_s": round(t_flight, 3), "max_height_m": round(h_max, 3), "range_m": round(r_max, 3)}

    @staticmethod
    def relativistic_momentum(mass_kg: float, velocity_m_s: float, c: float = 299792458.0) -> dict:
        """Relativistic Momentum p = gamma * m * v"""
        beta = velocity_m_s / c
        if beta >= 1.0:
            raise ValueError("Velocity must be less than speed of light c.")
        gamma = 1.0 / math.sqrt(1.0 - beta**2)
        p = gamma * mass_kg * velocity_m_s
        return {"lorentz_gamma": round(gamma, 4), "momentum_kg_m_s": f"{p:.4e}"}

class QuantumThermodynamics:
    """Statistical Ensembles & Partition Functions"""
    @staticmethod
    def planck_blackbody_radiance(wavelength_nm: float, temp_k: float) -> dict:
        """Planck's Law Spectral Radiance B(lambda, T)"""
        h = 6.62607015e-34
        c = 299792458.0
        kb = 1.380649e-23
        lam = wavelength_nm * 1e-9
        c1 = 2.0 * h * (c ** 2)
        exp_arg = (h * c) / (lam * kb * temp_k)
        if exp_arg > 700: # Prevent math overflow
            radiance = 0.0
        else:
            radiance = c1 / ((lam ** 5) * (math.exp(exp_arg) - 1.0))
        return {"wavelength_nm": wavelength_nm, "spectral_radiance_W_sr_m3": f"{radiance:.4e}"}
