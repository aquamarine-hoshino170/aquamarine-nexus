import math

class CosmicRaysGZKCore:
    M_PROTON_GEV = 0.938272
    M_PION0_GEV = 0.134976
    K_BOLTZ_EV = 8.617333262e-5
    C_LIGHT = 299792458.0

    @staticmethod
    def gzk_threshold_energy(cmb_photon_energy_ev: float = 6.0e-4) -> dict:
        """E_p,th = (m_pi * (2 * m_p + m_pi)) / (4 * epsilon_gamma)"""
        if cmb_photon_energy_ev <= 0:
            raise ValueError("Photon energy must be strictly positive.")
        eps_gev = cmb_photon_energy_ev * 1e-9
        mp = CosmicRaysGZKCore.M_PROTON_GEV
        mpi = CosmicRaysGZKCore.M_PION0_GEV
        
        e_th_gev = (mpi * (2.0 * mp + mpi)) / (4.0 * eps_gev)
        e_th_ev = e_th_gev * 1e9
        return {
            "cmb_photon_energy_eV": cmb_photon_energy_ev,
            "gzk_threshold_GeV": f"{e_th_gev:.6e}",
            "gzk_threshold_eV": f"{e_th_ev:.6e}",
            "is_uhecr_regime": e_th_ev >= 5.0e19
        }

    @staticmethod
    def relativistic_mandelstam_s(energy_1_gev: float, energy_2_gev: float, mass_1_gev: float, mass_2_gev: float, collision_angle_deg: float = 180.0) -> dict:
        """s = (p1 + p2)^2 = m1^2 + m2^2 + 2*(E1*E2 - |p1|*|p2|*cos(theta))"""
        p1 = math.sqrt(max(0.0, energy_1_gev**2 - mass_1_gev**2))
        p2 = math.sqrt(max(0.0, energy_2_gev**2 - mass_2_gev**2))
        theta_rad = math.radians(collision_angle_deg)
        
        s_val = (mass_1_gev ** 2) + (mass_2_gev ** 2) + 2.0 * (energy_1_gev * energy_2_gev - p1 * p2 * math.cos(theta_rad))
        sqrt_s = math.sqrt(max(0.0, s_val))
        return {
            "mandelstam_s_GeV2": round(s_val, 4),
            "center_of_mass_energy_sqrt_s_GeV": round(sqrt_s, 4)
        }
