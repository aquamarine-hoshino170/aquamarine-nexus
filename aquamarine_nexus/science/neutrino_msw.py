import math

class NeutrinoMSWCore:
    G_FERMI = 1.1663787e-5 * (1e-9**2)  # In eV units proxy
    H_BAR_C = 1.9732705e-7  # eV * m

    @staticmethod
    def msw_resonance_electron_density(delta_m2_ev2: float, theta_vacuum_deg: float, neutrino_energy_mev: float) -> dict:
        """n_e,res = (Delta_m^2 * cos(2*theta)) / (2 * sqrt(2) * G_F * E_nu)"""
        if delta_m2_ev2 <= 0 or neutrino_energy_mev <= 0 or theta_vacuum_deg <= 0 or theta_vacuum_deg >= 90:
            raise ValueError("Invalid oscillation parameters.")
        theta_rad = math.radians(theta_vacuum_deg)
        cos_2theta = math.cos(2.0 * theta_rad)
        if cos_2theta <= 0:
            raise ValueError("Resonance requires cos(2*theta) > 0.")
        
        e_nu_ev = neutrino_energy_mev * 1e6
        # Effective potential V_W = sqrt(2) * G_F * n_e
        # In SI converted formula:
        g_f_si = 1.1663787e-5 * (1.602176634e-19 * 1e9)**(-2) * (1.054571817e-34 * 299792458.0)**3
        e_nu_joules = neutrino_energy_mev * 1e6 * 1.602176634e-19
        delta_m2_joules2 = delta_m2_ev2 * (1.602176634e-19 ** 2)
        c = 299792458.0
        
        n_e_res = (delta_m2_joules2 * (c ** 4) * cos_2theta) / (2.0 * math.sqrt(2.0) * g_f_si * 2.0 * e_nu_joules * (c**2))
        return {
            "delta_m2_eV2": delta_m2_ev2,
            "neutrino_energy_MeV": neutrino_energy_mev,
            "theta_vacuum_deg": theta_vacuum_deg,
            "resonance_electron_density_m3": f"{abs(n_e_res):.6e}"
        }

    @staticmethod
    def matter_effective_mixing_angle(theta_vacuum_deg: float, matter_potential_a_ev: float, delta_m2_ev2: float, energy_ev: float) -> dict:
        """sin^2(2*theta_m) = sin^2(2*theta) / ( (cos(2*theta) - A*2E/Delta_m^2)^2 + sin^2(2*theta) )"""
        theta_rad = math.radians(theta_vacuum_deg)
        sin_2theta = math.sin(2.0 * theta_rad)
        cos_2theta = math.cos(2.0 * theta_rad)
        
        denom = ((cos_2theta - (matter_potential_a_ev * 2.0 * energy_ev / delta_m2_ev2)) ** 2) + (sin_2theta ** 2)
        sin2_2theta_m = (sin_2theta ** 2) / denom
        sin2_2theta_m = min(1.0, max(0.0, sin2_2theta_m))
        theta_m_deg = 0.5 * math.degrees(math.asin(math.sqrt(sin2_2theta_m)))
        return {
            "vacuum_angle_deg": theta_vacuum_deg,
            "matter_effective_sin2_2theta": round(sin2_2theta_m, 6),
            "matter_mixing_angle_deg": round(theta_m_deg, 4)
        }
