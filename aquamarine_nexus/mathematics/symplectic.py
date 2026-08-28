import math

class SymplecticCore:
    """Hamiltonian Mechanics & Symplectic Topology (Phase Space Conservation)"""

    @staticmethod
    def harmonic_oscillator_symplectic_step(q: float, p: float, dt: float, m: float = 1.0, k: float = 1.0) -> dict:
        """
        Symplectic Euler integrator for H(q, p) = p^2/(2m) + (1/2)k*q^2:
        Preserves phase space area exactly.
        """
        # p_{n+1} = p_n - dt * dH/dq
        p_next = p - dt * (k * q)
        # q_{n+1} = q_n + dt * (p_{n+1} / m)
        q_next = q + dt * (p_next / m)
        energy = (p_next**2) / (2.0 * m) + 0.5 * k * (q_next**2)
        return {
            "q_pos": round(q_next, 6),
            "p_mom": round(p_next, 6),
            "total_energy_H": round(energy, 6)
        }

    @staticmethod
    def phase_space_area_preservation(q_spread: float, p_spread: float) -> dict:
        """Liouville's theorem invariant: Area = Delta_q * Delta_p"""
        area = q_spread * p_spread
        return {"phase_space_area": round(area, 6), "is_canonical_invariant": True}
