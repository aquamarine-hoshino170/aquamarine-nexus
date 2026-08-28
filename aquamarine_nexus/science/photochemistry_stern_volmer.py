class PhotochemistrySternVolmerCore:
    @staticmethod
    def stern_volmer_fluorescence_quenching(i0_intensity: float, quencher_conc_molar: float, k_sv_molar_inv: float) -> dict:
        """I_0 / I = 1 + K_SV * [Q]"""
        if i0_intensity <= 0 or quencher_conc_molar < 0 or k_sv_molar_inv <= 0:
            raise ValueError("Intensity, concentration, and quenching constant must be non-negative/positive.")
            
        ratio = 1.0 + (k_sv_molar_inv * quencher_conc_molar)
        i_quenched = i0_intensity / ratio
        
        return {
            "initial_fluorescence_I0": i0_intensity,
            "quencher_concentration_M": quencher_conc_molar,
            "stern_volmer_constant_KSV": k_sv_molar_inv,
            "quenched_fluorescence_I": round(i_quenched, 4),
            "quenching_efficiency": round((1.0 - (1.0 / ratio)) * 100.0, 2)
        }

    @staticmethod
    def photochemical_quantum_yield(molecules_reacted: float, photons_absorbed: float) -> dict:
        """Phi = N_molecules / N_photons"""
        if molecules_reacted < 0 or photons_absorbed <= 0:
            raise ValueError("Molecules and photons count must be valid.")
        phi = molecules_reacted / photons_absorbed
        return {
            "molecules_reacted": f"{molecules_reacted:.6e}",
            "photons_absorbed": f"{photons_absorbed:.6e}",
            "quantum_yield_Phi": round(phi, 6),
            "is_chain_reaction": phi > 1.0
        }
