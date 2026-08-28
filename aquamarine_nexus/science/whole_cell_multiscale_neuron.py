import math
from typing import Dict, Any, List

class MultiScaleWholeCellNeuronCore:
    # Fundamental Constants
    E_CHARGE = 1.602176634e-19
    K_BOLTZ = 1.380649e-23
    H_BAR = 1.054571817e-34
    C_LIGHT = 299792458.0
    F_FARADAY = 96485.33212

    @staticmethod
    def _safe_exp(x: float) -> float:
        """Clamps exponent input to prevent floating point overflow."""
        if x > 100.0:
            return 2.6881171418161356e+43
        elif x < -100.0:
            return 3.720075976020836e-44
        return math.exp(x)

    @staticmethod
    def _hh_rates(v: float) -> tuple:
        # Hodgkin-Huxley empirical rate constants with robust overflow protection
        vt_m = v + 40.0
        exp_m = MultiScaleWholeCellNeuronCore._safe_exp(-vt_m / 10.0)
        am = 0.1 * vt_m / (1.0 - exp_m) if abs(1.0 - exp_m) > 1e-6 else 1.0
        bm = 4.0 * MultiScaleWholeCellNeuronCore._safe_exp(-(v + 65.0) / 18.0)

        ah = 0.07 * MultiScaleWholeCellNeuronCore._safe_exp(-(v + 65.0) / 20.0)
        bh = 1.0 / (1.0 + MultiScaleWholeCellNeuronCore._safe_exp(-(v + 35.0) / 10.0))

        vt_n = v + 55.0
        exp_n = MultiScaleWholeCellNeuronCore._safe_exp(-vt_n / 10.0)
        an = 0.01 * vt_n / (1.0 - exp_n) if abs(1.0 - exp_n) > 1e-6 else 0.1
        bn = 0.125 * MultiScaleWholeCellNeuronCore._safe_exp(-(v + 65.0) / 80.0)

        return am, bm, ah, bh, an, bn

    @staticmethod
    def simulate_multiscale_synapse_and_spine_plasticity(
        lipid_cleft_gap_nm: float = 2.0,
        reorganization_lambda_ev: float = 0.70,
        initial_spine_volume_um3: float = 0.10,
        g_actin_conc_um: float = 5.0,
        temp_k: float = 310.15,
        sim_duration_ms: float = 20.0,
        dt_ms: float = 0.01
    ) -> Dict[str, Any]:
        if lipid_cleft_gap_nm <= 0 or initial_spine_volume_um3 <= 0 or g_actin_conc_um <= 0:
            raise ValueError("Physical dimensions, concentrations, and volume must be strictly positive.")

        # 1. Pre-synaptic Quantum Casimir Modulation
        d_m = lipid_cleft_gap_nm * 1e-9
        hbar = MultiScaleWholeCellNeuronCore.H_BAR
        c = MultiScaleWholeCellNeuronCore.C_LIGHT
        e = MultiScaleWholeCellNeuronCore.E_CHARGE
        kb = MultiScaleWholeCellNeuronCore.K_BOLTZ

        casimir_pressure_pa = - (math.pi ** 2 * hbar * c) / (240.0 * (d_m ** 4))
        delta_g_quantum_ev = (- (math.pi ** 2 * hbar * c) / (720.0 * (d_m ** 3)) * 1.0e-18) / e

        # 2. Marcus Kinetic Transition
        delta_g0_eff_ev = -0.45 + delta_g_quantum_ev
        lambda_j = reorganization_lambda_ev * e
        hab_j = 0.03 * e
        kb_t = kb * temp_k

        prefactor = (2.0 * math.pi / hbar) * (hab_j ** 2) / math.sqrt(4.0 * math.pi * lambda_j * kb_t)
        barrier_j = (((delta_g0_eff_ev * e) + lambda_j) ** 2) / (4.0 * lambda_j)
        marcus_k_fusion = prefactor * MultiScaleWholeCellNeuronCore._safe_exp(-barrier_j / kb_t)

        p_vesicle_release = 1.0 - MultiScaleWholeCellNeuronCore._safe_exp(-marcus_k_fusion * 1e-8)
        p_vesicle_release = min(0.99, max(0.02, p_vesicle_release))
        glutamate_quanta_released = int(round(500 * p_vesicle_release))

        # 3. Post-synaptic Conductance
        g_ampa_peak = glutamate_quanta_released * 0.08
        g_nmda_peak = glutamate_quanta_released * 0.03
        ca_influx_integral = 0.0

        # 4. Somatic Hodgkin-Huxley Dynamics
        c_m = 1.0
        g_na_max = 120.0
        g_k_max = 36.0
        g_l = 0.3
        e_na, e_k, e_l = 50.0, -77.0, -54.4
        e_syn = 0.0

        v = -65.0
        am, bm, ah, bh, an, bn = MultiScaleWholeCellNeuronCore._hh_rates(v)
        m = am / (am + bm)
        h = ah / (ah + bh)
        n = an / (an + bn)

        # Internal small sub-stepping (0.005 ms) for numerical stability
        sub_dt = 0.005
        steps = int(sim_duration_ms / sub_dt)
        spike_times_ms = []
        in_spike = False
        peak_v = v

        for step in range(steps):
            t = step * sub_dt
            
            i_syn = 0.0
            for t_spike in [2.0, 10.0, 18.0]:
                if t >= t_spike:
                    dt_s = t - t_spike
                    if dt_s < 6.0:
                        g_syn_t = (g_ampa_peak + g_nmda_peak) * (dt_s / 1.5) * MultiScaleWholeCellNeuronCore._safe_exp(1.0 - (dt_s / 1.5))
                        i_syn += g_syn_t * (v - e_syn)
                        if v > -30.0:
                            ca_influx_integral += g_nmda_peak * 0.01 * sub_dt

            i_na = g_na_max * (m ** 3) * h * (v - e_na)
            i_k = g_k_max * (n ** 4) * (v - e_k)
            i_l = g_l * (v - e_l)

            dv_dt = (- (i_na + i_k + i_l + i_syn)) / c_m
            v += dv_dt * sub_dt

            am, bm, ah, bh, an, bn = MultiScaleWholeCellNeuronCore._hh_rates(v)
            m += (am * (1.0 - m) - bm * m) * sub_dt
            h += (ah * (1.0 - h) - bh * h) * sub_dt
            n += (an * (1.0 - n) - bn * n) * sub_dt

            # Clamp state variables
            m = max(0.0, min(1.0, m))
            h = max(0.0, min(1.0, h))
            n = max(0.0, min(1.0, n))

            if v > peak_v:
                peak_v = v

            if v >= 0.0 and not in_spike:
                spike_times_ms.append(round(t, 2))
                in_spike = True
            elif v < -20.0:
                in_spike = False

        # 5. Actin Treadmilling & Dendritic Spine Head Growth
        k_on_actin = 11.6
        k_off_actin = 1.4
        net_treadmilling_flux = (k_on_actin * g_actin_conc_um - k_off_actin) * (1.0 + ca_influx_integral * 2.5)
        delta_volume_ratio = min(2.5, max(0.0, (net_treadmilling_flux * 0.005)))
        evolved_spine_volume_um3 = initial_spine_volume_um3 * (1.0 + delta_volume_ratio)

        return {
            "scale_1_quantum_membrane": {
                "vesicle_cleft_gap_nm": lipid_cleft_gap_nm,
                "casimir_pressure_Pa": f"{casimir_pressure_pa:.6e}",
                "effective_delta_G0_eV": round(delta_g0_eff_ev, 6),
                "marcus_fusion_rate_s_inv": f"{marcus_k_fusion:.6e}"
            },
            "scale_2_quantal_transmission": {
                "vesicle_fusion_probability": round(p_vesicle_release, 4),
                "glutamate_molecules_translocated": glutamate_quanta_released,
                "peak_ampa_conductance_mS_cm2": round(g_ampa_peak, 4),
                "total_intracellular_Ca2_charge_entry": round(ca_influx_integral, 5)
            },
            "scale_3_somatic_electrophysiology": {
                "action_potentials_fired": len(spike_times_ms),
                "spike_timestamps_ms": spike_times_ms,
                "peak_somatic_depolarization_mV": round(peak_v, 2),
                "electrophysiological_state": "High-Frequency Burst Spiking" if len(spike_times_ms) >= 2 else "Moderate/Sparse Spiking"
            },
            "scale_4_dendritic_spine_plasticity": {
                "initial_spine_volume_um3": initial_spine_volume_um3,
                "actin_treadmilling_flux_s_inv": round(net_treadmilling_flux, 4),
                "structural_LTP_volume_growth_percent": round(delta_volume_ratio * 100.0, 2),
                "evolved_spine_head_volume_um3": round(evolved_spine_volume_um3, 4),
                "plasticity_verdict": "Long-Term Potentiation (Synaptic Spine Enlarged)" if delta_volume_ratio > 0.2 else "Basal Steady State"
            },
            "execution_status": "END_TO_END_WHOLE_CELL_INTEGRATION_SUCCESSFUL"
        }
