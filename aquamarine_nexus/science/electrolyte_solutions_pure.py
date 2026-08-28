import math

class ElectrolyteSolutionsPureCore:
    @staticmethod
    def ionic_strength_solution(molalities: list, charges_z: list) -> dict:
        """I = 0.5 * sum( m_i * z_i^2 )"""
        if len(molalities) != len(charges_z) or not molalities:
            raise ValueError("Molalities and charges list dimension mismatch.")
        
        i_strength = 0.5 * sum(m * (z ** 2) for m, z in zip(molalities, charges_z))
        return {
            "ionic_strength_mol_kg": round(i_strength, 6),
            "is_dilute_regime": i_strength <= 0.01
        }

    @staticmethod
    def debye_huckel_activity_coefficient(z_pos: int, z_neg: int, ionic_strength: float, a_debye: float = 0.509) -> dict:
        """log10(gamma_plus_minus) = - A * |z_+ * z_-| * sqrt(I)"""
        if ionic_strength < 0:
            raise ValueError("Ionic strength must be non-negative.")
        
        abs_charge_prod = abs(z_pos * z_neg)
        log_gamma = - a_debye * abs_charge_prod * math.sqrt(ionic_strength)
        gamma_pm = 10.0 ** log_gamma
        
        return {
            "z_positive": z_pos,
            "z_negative": z_neg,
            "ionic_strength": ionic_strength,
            "log10_gamma_mean": round(log_gamma, 6),
            "mean_ionic_activity_coefficient": round(gamma_pm, 6)
        }
