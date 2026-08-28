class LotkaVolterraEcologyCore:
    @staticmethod
    def predator_prey_derivatives(prey_x: float, predator_y: float, alpha_birth: float, beta_predation: float, gamma_death: float, delta_growth: float) -> dict:
        """
        dx/dt = alpha * x - beta * x * y
        dy/dt = delta * x * y - gamma * y
        """
        if prey_x < 0 or predator_y < 0 or alpha_birth <= 0 or beta_predation <= 0 or gamma_death <= 0 or delta_growth <= 0:
            raise ValueError("Populations and rate parameters must be strictly positive.")
        
        dx_dt = alpha_birth * prey_x - beta_predation * prey_x * predator_y
        dy_dt = delta_growth * prey_x * predator_y - gamma_death * predator_y
        
        # Non-trivial equilibrium (x*, y*) = (gamma / delta, alpha / beta)
        eq_x = gamma_death / delta_growth
        eq_y = alpha_birth / beta_predation
        
        return {
            "prey_dx_dt": round(dx_dt, 6),
            "predator_dy_dt": round(dy_dt, 6),
            "coexistence_equilibrium_prey": round(eq_x, 4),
            "coexistence_equilibrium_predator": round(eq_y, 4)
        }

    @staticmethod
    def lotka_volterra_jacobian_determinant(alpha_birth: float, gamma_death: float) -> dict:
        """At equilibrium (x*, y*): J = [[0, -beta*x*], [delta*y*, 0]] => det(J) = alpha * gamma, Tr(J) = 0"""
        det_j = alpha_birth * gamma_death
        return {
            "jacobian_trace": 0.0,
            "jacobian_determinant": round(det_j, 6),
            "eigenvalues": f"+- {round(det_j**0.5, 6)} i",
            "stability": "Marginally Stable (Center Orbit)"
        }
