import math

class MolecularMotorRatchetCore:
    K_BOLTZ = 1.380649e-23

    @staticmethod
    def brownian_ratchet_drift_velocity(asymmetry_ratio: float, barrier_height_kt: float, cycle_rate_hz: float, step_size_nm: float, load_force_pn: float = 0.0, temp_k: float = 300.0) -> dict:
        """v = L * nu * (P_forward - P_backward * exp(-F * L / (k_B * T)))"""
        if asymmetry_ratio <= 0 or barrier_height_kt <= 0 or cycle_rate_hz <= 0 or step_size_nm <= 0 or temp_k <= 0:
            raise ValueError("All parameters must be strictly positive.")
            
        kb_t_j = MolecularMotorRatchetCore.K_BOLTZ * temp_k
        step_m = step_size_nm * 1e-9
        load_j = (load_force_pn * 1e-12) * step_m
        
        p_fwd = asymmetry_ratio / (1.0 + asymmetry_ratio)
        p_back = 1.0 / (1.0 + asymmetry_ratio)
        
        work_ratio = math.exp(-load_j / kb_t_j) if (-load_j / kb_t_j) > -700 else 0.0
        effective_net_prob = p_fwd - (p_back * work_ratio)
        velocity_m_s = step_m * cycle_rate_hz * effective_net_prob
        velocity_nm_s = velocity_m_s * 1e9
        
        # Stall force estimate where effective net prob becomes 0
        stall_force_pn = (kb_t_j * math.log(p_fwd / p_back) / step_m) * 1e12 if p_fwd > p_back else 0.0
        
        return {
            "step_size_nm": step_size_nm,
            "cycling_frequency_Hz": cycle_rate_hz,
            "forward_stepping_velocity_nm_s": round(velocity_nm_s, 4),
            "estimated_stall_force_pN": round(stall_force_pn, 4),
            "motor_regime": "Forward Processive" if velocity_nm_s > 0 else ("Stalled" if velocity_nm_s == 0 else "Forced Reverse Drift")
        }
