class OrthogonalPolynomialsCore:
    """Chebyshev & Legendre Orthogonal Polynomial Evaluation Engine"""

    @staticmethod
    def chebyshev_t_eval(n_degree: int, x_val: float) -> dict:
        """
        Evaluates Chebyshev polynomial of the first kind T_n(x) via 3-term recurrence:
        T_0(x) = 1, T_1(x) = x, T_{n+1}(x) = 2x*T_n(x) - T_{n-1}(x)
        """
        if n_degree < 0:
            raise ValueError("Degree n must be non-negative.")

        if n_degree == 0:
            return {"degree_n": 0, "x": x_val, "T_n_x": 1.0}
        if n_degree == 1:
            return {"degree_n": 1, "x": x_val, "T_n_x": x_val}

        t_prev2 = 1.0
        t_prev1 = x_val
        t_curr = 0.0

        for _ in range(2, n_degree + 1):
            t_curr = (2.0 * x_val * t_prev1) - t_prev2
            t_prev2 = t_prev1
            t_prev1 = t_curr

        return {
            "degree_n": n_degree,
            "x": x_val,
            "T_n_x": round(t_curr, 8)
        }

    @staticmethod
    def legendre_p_eval(n_degree: int, x_val: float) -> dict:
        """
        Evaluates Legendre polynomial P_n(x) via Bonnet's recurrence formula:
        (n+1)*P_{n+1}(x) = (2n+1)*x*P_n(x) - n*P_{n-1}(x)
        """
        if n_degree < 0:
            raise ValueError("Degree n must be non-negative.")

        if n_degree == 0:
            return {"degree_n": 0, "x": x_val, "P_n_x": 1.0}
        if n_degree == 1:
            return {"degree_n": 1, "x": x_val, "P_n_x": x_val}

        p_prev2 = 1.0
        p_prev1 = x_val
        p_curr = 0.0

        for n in range(1, n_degree):
            p_curr = (((2.0 * n + 1.0) * x_val * p_prev1) - (n * p_prev2)) / (n + 1.0)
            p_prev2 = p_prev1
            p_prev1 = p_curr

        return {
            "degree_n": n_degree,
            "x": x_val,
            "P_n_x": round(p_curr, 8)
        }
