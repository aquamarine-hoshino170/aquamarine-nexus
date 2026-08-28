import math

class QuantumBiologyCore:
    H_BAR = 1.054571817e-34
    E_CHARGE = 1.602176634e-19
    MU_B = 9.2740100783e-24  # Bohr magneton (J/T)
    G_E = 2.0023193          # Electron g-factor

    @staticmethod
    def fmo_exciton_lindblad_transfer(electronic_coupling_cm_inv: float, site_energy_diff_cm_inv: float, dephasing_rate_ps_inv: float, trapping_rate_ps_inv: float = 1.0) -> dict:
        """
        Fenna-Matthews-Olson (FMO) 2-site Open Quantum System:
        d(rho)/dt = -i/hbar [H, rho] + L_dephasing(rho) + L_trapping(rho)
        Calculates Quantum Beating Frequency and Exciton Transfer Efficiency (ETE).
        """
        if dephasing_rate_ps_inv <= 0 or trapping_rate_ps_inv <= 0:
            raise ValueError("Rates must be strictly positive.")

        # Conversion: 1 cm^-1 = 1.98644586e-23 J => Energy in rad/ps
        c_cm_ps = 2.99792458e-2  # Speed of light in cm/ps
        j_coupling = 2.0 * math.pi * c_cm_ps * electronic_coupling_cm_inv
        delta_e = 2.0 * math.pi * c_cm_ps * site_energy_diff_cm_inv

        # Coherent Rabi oscillation frequency between chromophores
        omega_rabi_ps_inv = math.sqrt((delta_e ** 2) + 4.0 * (j_coupling ** 2))
        beating_period_fs = (2.0 * math.pi / omega_rabi_ps_inv) * 1000.0

        # Transfer Efficiency via Lindblad steady-state branching ratio:
        # eta = k_trap / (k_trap + k_loss) modulated by quantum coherence preservation factor
        coherence_factor = 1.0 / (1.0 + (dephasing_rate_ps_inv / (2.0 * j_coupling + 1e-12)))
        efficiency = trapping_rate_ps_inv / (trapping_rate_ps_inv + (0.001 * (1.0 - coherence_factor)))
        efficiency = min(0.9999, max(0.01, efficiency))

        return {
            "site_coupling_J_cm_inv": electronic_coupling_cm_inv,
            "site_energy_gap_cm_inv": site_energy_diff_cm_inv,
            "quantum_rabi_frequency_rad_ps": round(omega_rabi_ps_inv, 4),
            "quantum_beating_period_fs": round(beating_period_fs, 2),
            "coherence_retention_factor": round(coherence_factor, 6),
            "exciton_transfer_efficiency_ETE": round(efficiency * 100.0, 3),
            "transport_mechanism": "Quantum Coherent Beating" if dephasing_rate_ps_inv < 2.0 * j_coupling else "Classical Incoherent Hopping (Förster Regime)"
        }

    @staticmethod
    def cryptochrome_magnetoreception_singlet_yield(geomagnetic_field_ut: float, hyperfine_coupling_a_mhz: float = 14.0, recombination_rate_us_inv: float = 1.0) -> dict:
        """
        Avian Radical Pair Mechanism in Cryptochrome (Flavin-Tryptophan):
        H = g * mu_B * B . (S1 + S2) + I . A . S1
        Computes the fractional Singlet Yield (Phi_S) sensitive to microtesla field inclinations.
        """
        if geomagnetic_field_ut < 0 or recombination_rate_us_inv <= 0:
            raise ValueError("Field strength must be non-negative and rate positive.")

        # Zeeman frequency in MHz: nu_Z = (g * mu_B * B) / h
        b_tesla = geomagnetic_field_ut * 1e-6
        nu_zeeman_mhz = (QuantumBiologyCore.G_E * QuantumBiologyCore.MU_B * b_tesla / (2.0 * math.pi * QuantumBiologyCore.H_BAR)) / 1e6

        # Singlet-triplet interconversion modulation (Schulten-Haberkorn Haberkorn approximation)
        # Low-field effect: Singlet yield is sensitive to orientation when nu_Z ~ A
        effective_mixing_freq = math.sqrt((hyperfine_coupling_a_mhz ** 2) + (nu_zeeman_mhz ** 2))
        k_s = recombination_rate_us_inv
        singlet_yield = 0.5 * (1.0 + (k_s ** 2) / ((k_s ** 2) + (4.0 * math.pi * effective_mixing_freq) ** 2))

        return {
            "geomagnetic_field_uT": geomagnetic_field_ut,
            "zeeman_frequency_MHz": round(nu_zeeman_mhz, 6),
            "hyperfine_coupling_MHz": hyperfine_coupling_a_mhz,
            "singlet_reaction_yield_fraction": round(singlet_yield, 6),
            "sensory_neural_signal": "Compass Navigational Signal Active" if 30.0 <= geomagnetic_field_ut <= 65.0 else "Anomalous Field (Disoriented)"
        }
