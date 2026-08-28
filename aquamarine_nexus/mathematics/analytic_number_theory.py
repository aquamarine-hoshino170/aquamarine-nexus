import math

class AnalyticNumberTheoryCore:
    """Pure Mathematics: Riemann Zeta Function, Logarithmic Integrals & Prime Asymptotics"""

    @staticmethod
    def riemann_zeta_real(s_param: float, num_terms: int = 10000) -> dict:
        """
        Computes the Riemann Zeta function zeta(s) for real s > 1 via Dirichlet Series:
        zeta(s) = sum_{n=1}^N (1 / n^s)
        """
        if s_param <= 1.0:
            raise ValueError("Direct Dirichlet series strictly converges for Real(s) > 1.")

        zeta_sum = sum(1.0 / (n ** s_param) for n in range(1, num_terms + 1))

        return {
            "s_param": s_param,
            "terms_evaluated": num_terms,
            "zeta_approximation": round(zeta_sum, 10),
            "exact_pi_squared_over_6": round((math.pi ** 2) / 6.0, 10) if s_param == 2.0 else None
        }

    @staticmethod
    def logarithmic_integral_li(x_bound: float, steps: int = 1000) -> dict:
        """
        Numerical integration of Li(x) = int_2^x (1 / ln(t)) dt using Trapezoidal Rule:
        Asymptotic estimate for Prime-Counting Function pi(x).
        """
        if x_bound <= 2.0:
            raise ValueError("Bound x must be strictly greater than 2.")

        a, b = 2.0, x_bound
        h = (b - a) / steps
        total = 0.5 * (1.0 / math.log(a) + 1.0 / math.log(b))

        for i in range(1, steps):
            t = a + i * h
            total += 1.0 / math.log(t)

        li_val = total * h
        pnt_x_over_lnx = x_bound / math.log(x_bound)

        return {
            "x_bound": x_bound,
            "logarithmic_integral_Li": round(li_val, 4),
            "prime_number_theorem_x_over_lnx": round(pnt_x_over_lnx, 4)
        }
