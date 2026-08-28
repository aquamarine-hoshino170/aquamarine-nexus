import math

class ParticleQFTCore:
    C_LIGHT = 299792458.0
    H_BAR = 1.054571817e-34
    G_FERMI = 1.1663787e-5  # GeV^-2
    ALPHA_EM = 1.0 / 137.035999084

    @staticmethod
    def rutherford_differential_cross_section(energy_mev: float, scattering_angle_deg: float, z_target: int = 79) -> dict:
        """dsigma/dOmega = ( (z1*z2*e^2) / (4*E) )^2 * (1 / sin^4(theta/2))"""
        if scattering_angle_deg <= 0 or scattering_angle_deg >= 180 or energy_mev <= 0: raise ValueError("Invalid parameters.")
        theta_rad = math.radians(scattering_angle_deg)
        sin_half = math.sin(theta_rad / 2.0)
        # In femtometers/barns scaling: proportionality proxy
        diff_cs = ((z_target * 2.0 * 1.44) / (4.0 * energy_mev))**2 * (1.0 / (sin_half ** 4))
        return {"energy_MeV": energy_mev, "angle_deg": scattering_angle_deg, "target_Z": z_target, "diff_cross_section_fm2_sr": round(diff_cs, 4)}

    @staticmethod
    def yukawa_potential(r_meters: float, exchange_boson_mass_ev: float) -> dict:
        """V(r) = -g^2 * exp(-m*c*r / hbar) / (4*pi*r)"""
        if r_meters <= 0 or exchange_boson_mass_ev <= 0: raise ValueError("Invalid inputs.")
        mass_kg = (exchange_boson_mass_ev * 1.602176634e-19) / (ParticleQFTCore.C_LIGHT ** 2)
        mu = (mass_kg * ParticleQFTCore.C_LIGHT) / ParticleQFTCore.H_BAR
        screening = math.exp(-mu * r_meters)
        return {"radius_m": f"{r_meters:.6e}", "range_parameter_mu_inv_m": f"{mu:.6e}", "screening_factor_exp": round(screening, 8)}

    @staticmethod
    def muon_decay_lifetime(muon_mass_mev: float = 105.658) -> dict:
        """Gamma = (G_F^2 * m_mu^5) / (192 * pi^3) -> tau = hbar / Gamma"""
        g_f = 1.1663787e-5
        m_gev = muon_mass_mev / 1000.0
        width_gev = (g_f**2 * (m_gev**5)) / (192.0 * (math.pi**3))
        hbar_gev_s = 6.582119569e-25
        lifetime_s = hbar_gev_s / width_gev
        return {"muon_mass_MeV": muon_mass_mev, "decay_width_GeV": f"{width_gev:.6e}", "muon_lifetime_seconds": f"{lifetime_s:.6e}"}
