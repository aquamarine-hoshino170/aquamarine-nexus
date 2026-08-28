import math

class AdvancedCosmologyCore:
    G_CONST = 6.67430e-11
    C_LIGHT = 299792458.0
    MPC_TO_METERS = 3.085677581e22

    @staticmethod
    def critical_density_universe(h0_km_s_mpc: float = 70.0) -> dict:
        """rho_c = (3 * H_0^2) / (8 * pi * G)"""
        if h0_km_s_mpc <= 0: raise ValueError("H0 must be positive.")
        h0_si = (h0_km_s_mpc * 1000.0) / AdvancedCosmologyCore.MPC_TO_METERS
        rho_c = (3.0 * (h0_si ** 2)) / (8.0 * math.pi * AdvancedCosmologyCore.G_CONST)
        return {"H0_km_s_Mpc": h0_km_s_mpc, "H0_SI_inv_s": f"{h0_si:.6e}", "critical_density_kg_m3": f"{rho_c:.6e}"}

    @staticmethod
    def cosmological_deceleration_parameter(omega_matter: float, omega_lambda: float, omega_radiation: float = 0.0) -> dict:
        """q_0 = Omega_r + 0.5 * Omega_m - Omega_Lambda"""
        q0 = omega_radiation + 0.5 * omega_matter - omega_lambda
        return {"Omega_m": omega_matter, "Omega_Lambda": omega_lambda, "deceleration_parameter_q0": round(q0, 4), "is_accelerating": q0 < 0}

    @staticmethod
    def horizon_distance_conformal(redshift_z: float, h0_km_s_mpc: float = 70.0, omega_m: float = 0.3, omega_l: float = 0.7) -> dict:
        """Hubble Horizon Distance d_H = c / H(z)"""
        h_z = h0_km_s_mpc * math.sqrt(omega_m * ((1.0 + redshift_z)**3) + omega_l)
        h_z_si = (h_z * 1000.0) / AdvancedCosmologyCore.MPC_TO_METERS
        d_h_meters = AdvancedCosmologyCore.C_LIGHT / h_z_si
        d_h_mpc = d_h_meters / AdvancedCosmologyCore.MPC_TO_METERS
        return {"redshift_z": redshift_z, "H_z_km_s_Mpc": round(h_z, 3), "hubble_horizon_Mpc": round(d_h_mpc, 3)}
