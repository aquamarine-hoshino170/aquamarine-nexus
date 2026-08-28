class NuclearFusionLawsonCore:
    K_EV_TO_JOULE = 1.602176634e-16  # 1 keV = 1.602e-16 J

    @staticmethod
    def lawson_triple_product(density_m3: float, temp_kev: float, confinement_time_s: float) -> dict:
        """n * T * tau_E >= 3 * 10^21 keV s m^-3 for D-T ignition"""
        if density_m3 <= 0 or temp_kev <= 0 or confinement_time_s <= 0:
            raise ValueError("All parameters must be strictly positive.")
        triple_prod = density_m3 * temp_kev * confinement_time_s
        ignition_threshold = 3.0e21
        q_ratio_proxy = triple_prod / ignition_threshold
        return {
            "density_m3": f"{density_m3:.4e}",
            "temp_keV": temp_kev,
            "confinement_time_s": confinement_time_s,
            "triple_product_keV_s_m3": f"{triple_prod:.4e}",
            "ignition_reached": triple_prod >= ignition_threshold,
            "q_ignition_ratio": round(q_ratio_proxy, 4)
        }

    @staticmethod
    def fusion_power_density_dt(density_deuterium: float, density_tritium: float, reactivity_sigma_v: float) -> dict:
        """P_fusion = n_D * n_T * <sigma*v> * E_DT (E_DT = 17.6 MeV = 2.818e-12 J)"""
        e_dt_joules = 17.6 * 1e6 * 1.602176634e-19
        if density_deuterium <= 0 or density_tritium <= 0 or reactivity_sigma_v <= 0:
            raise ValueError("Densities and reactivity must be positive.")
        p_vol = density_deuterium * density_tritium * reactivity_sigma_v * e_dt_joules
        return {
            "power_density_W_m3": f"{p_vol:.6e}",
            "power_density_MW_m3": f"{p_vol / 1e6:.6e}"
        }
