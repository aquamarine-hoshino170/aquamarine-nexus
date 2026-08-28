import math

class CardiacElectrophysiologyPhaseCore:
    @staticmethod
    def sinoatrial_pacemaker_phase_reset(initial_phase_rad: float, perturbation_magnitude: float, coupling_strength: float = 0.5) -> dict:
        """Phase Response Curve (PRC): Theta_new = Theta_old + epsilon * sin(Theta_old)"""
        if not (0.0 <= initial_phase_rad <= 2.0 * math.pi):
            raise ValueError("Phase must be within [0, 2*pi] radians.")
            
        phase_shift = coupling_strength * perturbation_magnitude * math.sin(initial_phase_rad)
        new_phase = (initial_phase_rad + phase_shift) % (2.0 * math.pi)
        
        return {
            "initial_phase_rad": round(initial_phase_rad, 4),
            "phase_shift_Delta_theta": round(phase_shift, 4),
            "reset_phase_rad": round(new_phase, 4),
            "cardiac_response": "Phase Advanced (Tachy-shift)" if phase_shift > 0 else ("Phase Delayed (Brady-shift)" if phase_shift < 0 else "Phase Invariant")
        }
