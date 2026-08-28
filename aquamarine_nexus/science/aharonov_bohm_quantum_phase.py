import math

class AharonovBohmQuantumPhaseCore:
    E_CHARGE = 1.602176634e-19
    H_BAR = 1.054571817e-34

    @staticmethod
    def magnetic_aharonov_bohm_phase(magnetic_flux_webers: float) -> dict:
        """Delta_phi = (q / hbar) * Phi_B = 2*pi * (Phi_B / Phi_0) where Phi_0 = h/e"""
        e = AharonovBohmQuantumPhaseCore.E_CHARGE
        hbar = AharonovBohmQuantumPhaseCore.H_BAR
        
        phase_shift_rad = (e * magnetic_flux_webers) / hbar
        flux_quantum_phi0 = (2.0 * math.pi * hbar) / e
        
        fractional_flux = magnetic_flux_webers / flux_quantum_phi0
        
        return {
            "magnetic_flux_Wb": f"{magnetic_flux_webers:.6e}",
            "fundamental_flux_quantum_Phi0_Wb": f"{flux_quantum_phi0:.6e}",
            "phase_shift_rad": round(phase_shift_rad, 6),
            "phase_shift_deg": round(math.degrees(phase_shift_rad) % 360.0, 3),
            "interference_modulation": round(math.cos(phase_shift_rad / 2.0) ** 2, 6)
        }
