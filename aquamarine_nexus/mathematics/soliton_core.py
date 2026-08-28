import math

class SolitonDynamicsCore:
    """Nonlinear Wave Solitons & Exact Solutions (KdV Engine)"""

    @staticmethod
    def kdv_single_soliton(x: float, t: float, velocity: float) -> dict:
        """
        KdV 1-Soliton analytical profile:
        eta(x, t) = (v / 2) * sech^2( (sqrt(v)/2) * (x - v*t) )
        """
        if velocity <= 0:
            raise ValueError("Soliton velocity must be positive.")
        
        arg = 0.5 * math.sqrt(velocity) * (x - velocity * t)
        # sech(u) = 1 / cosh(u)
        cosh_val = math.cosh(arg) if abs(arg) < 700 else float('inf')
        sech_sq = (1.0 / cosh_val)**2 if cosh_val != float('inf') else 0.0
        amplitude = 0.5 * velocity * sech_sq
        
        # Conserved Soliton Mass Invariant M = integral(eta dx) = 2 * sqrt(v)
        invariant_mass = 2.0 * math.sqrt(velocity)
        return {
            "x_pos": x,
            "time_t": t,
            "velocity": velocity,
            "soliton_amplitude": round(amplitude, 6),
            "conserved_soliton_mass": round(invariant_mass, 6)
        }
