import math

class Tier1LyapunovChaosCore:
    @staticmethod
    def logistic_map_lyapunov_exponent(r_param: float, iterations: int = 2000, x0: float = 0.5) -> dict:
        """lambda = lim (1/N) * sum( ln|r * (1 - 2*x_n)| )"""
        if not (0.0 < r_param <= 4.0) or not (0.0 < x0 < 1.0) or iterations < 100:
            raise ValueError("r must be in (0, 4], x0 in (0, 1), and iterations >= 100.")
            
        x = x0
        # Warmup
        for _ in range(500):
            x = r_param * x * (1.0 - x)
            
        total_lyap = 0.0
        for _ in range(iterations):
            x = r_param * x * (1.0 - x)
            deriv = abs(r_param * (1.0 - 2.0 * x))
            total_lyap += math.log(deriv) if deriv > 1e-15 else -30.0
            
        lyap_exp = total_lyap / iterations
        
        return {
            "parameter_r": r_param,
            "iterations_evaluated": iterations,
            "lyapunov_exponent_lambda": round(lyap_exp, 6),
            "dynamics_regime": "Deterministic Chaos" if lyap_exp > 0 else ("Periodic Orbit" if lyap_exp < 0 else "Bifurcation Criticality")
        }
