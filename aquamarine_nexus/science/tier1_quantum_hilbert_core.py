import math

class Tier1QuantumHilbertCore:
    @staticmethod
    def von_neumann_entropy_qubit_density(rho_00: float, rho_11: float, rho_01_real: float, rho_01_imag: float = 0.0) -> dict:
        """S(rho) = - lambda_1 * ln(lambda_1) - lambda_2 * ln(lambda_2)"""
        if abs(rho_00 + rho_11 - 1.0) > 1e-6 or rho_00 < 0 or rho_11 < 0:
            raise ValueError("Density matrix must have trace = 1 and non-negative diagonal elements.")
            
        det_rho = (rho_00 * rho_11) - (rho_01_real**2 + rho_01_imag**2)
        if det_rho < -1e-9:
            raise ValueError("Invalid quantum density matrix (negative eigenvalues).")
        det_rho = max(0.0, det_rho)
        
        # Eigenvalues of 2x2 density matrix
        disc = math.sqrt(max(0.0, ((rho_00 - rho_11) ** 2) + 4.0 * (rho_01_real**2 + rho_01_imag**2)))
        l1 = 0.5 * (1.0 + disc)
        l2 = 0.5 * (1.0 - disc)
        
        def term(val):
            return 0.0 if val <= 1e-15 else val * math.log(val)
            
        s_entropy = - (term(l1) + term(l2))
        purity = (rho_00 ** 2) + (rho_11 ** 2) + 2.0 * (rho_01_real**2 + rho_01_imag**2)
        
        return {
            "eigenvalue_1": round(l1, 6),
            "eigenvalue_2": round(l2, 6),
            "purity_gamma": round(purity, 6),
            "von_neumann_entropy_nats": round(s_entropy, 6),
            "quantum_state": "Pure State" if purity >= 0.999999 else "Mixed State (Entangled/Decohered)"
        }
