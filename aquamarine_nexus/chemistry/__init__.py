import math

class ReactionNexus:
    """Chemical Equilibrium & Electrochemistry"""
    @staticmethod
    def gibbs_cell_potential(e_cell_v: float, n_electrons: int, temp_k: float = 298.15) -> dict:
        """Computes Delta G0 = -n * F * E_cell and Equilibrium Constant K"""
        F = 96485.33212
        R = 8.314462618
        dg_joules = -n_electrons * F * e_cell_v
        k_eq = math.exp(-dg_joules / (R * temp_k)) if (-dg_joules / (R * temp_k)) < 700 else float('inf')
        return {"dG0_kJ_mol": round(dg_joules / 1000.0, 3), "equilibrium_K": f"{k_eq:.4e}"}

    @staticmethod
    def clausius_clapeyron_p2(p1_bar: float, t1_k: float, t2_k: float, dh_vap_kj_mol: float) -> dict:
        """Vapor pressure at T2 via integrated Clausius-Clapeyron equation"""
        R = 8.314462618e-3
        p2 = p1_bar * math.exp(-(dh_vap_kj_mol / R) * ((1.0 / t2_k) - (1.0 / t1_k)))
        return {"P1_bar": p1_bar, "T1_K": t1_k, "T2_K": t2_k, "P2_bar": round(p2, 4)}
