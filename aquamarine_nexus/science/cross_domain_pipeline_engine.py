import math

class CrossDomainPipelineCore:
    E_CHARGE = 1.602176634e-19
    H_BAR = 1.054571817e-34
    C_LIGHT = 299792458.0
    K_BOLTZ = 1.380649e-23
    R_GAS = 8.314462618
    F_FARADAY = 96485.33212

    @staticmethod
    def quantum_to_cellular_action_potential(plate_gap_nm: float, reorganization_lambda_ev: float = 0.8, hab_coupling_ev: float = 0.05, temp_k: float = 310.15) -> dict:
        """
        Multi-Scale Cross-Domain Pipeline:
        1. [Quantum Field Scale]: Compute Casimir Vacuum Energy Density between lipid nanodomains.
        2. [Molecular Chemistry Scale]: Couple Casimir shift into Marcus Electron Transfer driving force (Delta G0).
        3. [Biophysical Membrane Scale]: Modulate ion gate permeability (P_Na / P_K) from Marcus charge rate and solve Goldman-Hodgkin-Katz (GHK) membrane potential.
        """
        if plate_gap_nm <= 0 or reorganization_lambda_ev <= 0 or hab_coupling_ev <= 0 or temp_k <= 0:
            raise ValueError("All physical dimensions and parameters must be strictly positive.")

        # ----------------------------------------------------------------------
        # Stage 1: Quantum Vacuum Fluctuations (Casimir Force & Energy Density)
        # ----------------------------------------------------------------------
        d_m = plate_gap_nm * 1e-9
        hbar = CrossDomainPipelineCore.H_BAR
        c = CrossDomainPipelineCore.C_LIGHT
        e = CrossDomainPipelineCore.E_CHARGE
        kb = CrossDomainPipelineCore.K_BOLTZ

        # Pressure P = - (pi^2 * hbar * c) / (240 * d^4)
        casimir_pressure_pa = - (math.pi ** 2 * hbar * c) / (240.0 * (d_m ** 4))
        # Energy per unit surface area (J/m^2)
        casimir_energy_density_j_m2 = - (math.pi ** 2 * hbar * c) / (720.0 * (d_m ** 3))
        # Scaled conformational energy shift in molecular scale (~1 nm^2 cross section)
        molecular_area_m2 = 1.0e-18
        delta_g_quantum_j = casimir_energy_density_j_m2 * molecular_area_m2
        delta_g_quantum_ev = delta_g_quantum_j / e

        # ----------------------------------------------------------------------
        # Stage 2: Marcus Molecular Electron Transfer Dynamics
        # ----------------------------------------------------------------------
        # Drive Delta_G0 via quantum-induced conformational displacement
        delta_g_0_ev = -0.4 + delta_g_quantum_ev
        
        lambda_j = reorganization_lambda_ev * e
        hab_j = hab_coupling_ev * e
        dg0_j = delta_g_0_ev * e
        kb_t_j = kb * temp_k

        prefactor = (2.0 * math.pi / hbar) * (hab_j ** 2) / math.sqrt(4.0 * math.pi * lambda_j * kb_t_j)
        activation_barrier_j = ((dg0_j + lambda_j) ** 2) / (4.0 * lambda_j)
        exponent = - activation_barrier_j / kb_t_j
        marcus_k_et = prefactor * math.exp(exponent) if exponent > -700 else 0.0

        # ----------------------------------------------------------------------
        # Stage 3: Biophysical GHK Membrane Potential & Action Potential Trigger
        # ----------------------------------------------------------------------
        # Baseline physiological concentrations (mM)
        k_in, k_out = 140.0, 5.0
        na_in, na_out = 15.0, 145.0
        cl_in, cl_out = 10.0, 110.0

        # Permeability modulation driven by electron transfer kinetic rate
        # Normalized against baseline transfer rate ~ 1e6 s^-1
        normalized_rate = min(100.0, max(0.01, marcus_k_et / 1.0e6))
        p_k = 1.0
        p_na = 0.04 * normalized_rate
        p_cl = 0.45

        rt_over_f = (CrossDomainPipelineCore.R_GAS * temp_k) / CrossDomainPipelineCore.F_FARADAY
        num = (p_k * k_out) + (p_na * na_out) + (p_cl * cl_in)
        den = (p_k * k_in) + (p_na * na_in) + (p_cl * cl_out)
        ghk_v_m = rt_over_f * math.log(num / den)
        ghk_v_mv = ghk_v_m * 1000.0

        # Action potential threshold check (~ -55 mV)
        ap_triggered = ghk_v_mv >= -55.0

        return {
            "stage_1_quantum": {
                "plate_gap_nm": plate_gap_nm,
                "casimir_pressure_Pa": f"{casimir_pressure_pa:.6e}",
                "quantum_energy_shift_eV": f"{delta_g_quantum_ev:.6e}"
            },
            "stage_2_chemical": {
                "effective_delta_G0_eV": round(delta_g_0_ev, 6),
                "marcus_transfer_rate_k_ET_s_inv": f"{marcus_k_et:.6e}",
                "reorganization_lambda_eV": reorganization_lambda_ev
            },
            "stage_3_biophysical": {
                "induced_P_Na_over_P_K": round(p_na / p_k, 6),
                "membrane_potential_Vm_mV": round(ghk_v_mv, 2),
                "action_potential_depolarized": ap_triggered,
                "cellular_response": "Action Potential Fired (Spike Generated)" if ap_triggered else "Sub-threshold Resting Potential"
            },
            "pipeline_status": "Closed-Loop Multi-Scale Execution Successful"
        }
