import math

class YangMillsGaugeCore:
    @staticmethod
    def instanton_topological_charge_density(trace_f_fdual: float) -> dict:
        """q = (1 / (32 * pi^2)) * Tr(F_{mu nu} * Fdual^{mu nu})"""
        denom = 32.0 * (math.pi ** 2)
        q_density = trace_f_fdual / denom
        return {
            "trace_F_Fdual": trace_f_fdual,
            "topological_charge_density": f"{q_density:.8e}",
            "integrated_instanton_number_approx": round(q_density, 4)
        }

    @staticmethod
    def chromoelectric_magnetic_invariants(e_color_squared: float, b_color_squared: float, eb_color_dot: float) -> dict:
        """I_1 = B^2 - E^2, I_2 = E . B"""
        i1 = b_color_squared - e_color_squared
        i2 = eb_color_dot
        return {
            "invariant_I1_B2_minus_E2": round(i1, 6),
            "invariant_I2_E_dot_B": round(i2, 6),
            "is_self_dual_proxy": abs(i1) < 1e-6 and abs(i2) > 0
        }
