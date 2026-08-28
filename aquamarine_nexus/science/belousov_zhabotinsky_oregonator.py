class BelousovZhabotinskyOregonatorCore:
    @staticmethod
    def oregonator_reaction_derivatives(alpha_x: float, beta_y: float, gamma_z: float, q_param: float = 8.375e-6, f_stoich: float = 1.0, epsilon: float = 0.04, epsilon_prime: float = 0.0004) -> dict:
        """
        eps * dx/dt = q*y - x*y + x*(1 - x)
        eps' * dy/dt = -q*y - x*y + 2*f*z
        dz/dt = x - z
        """
        if any(v < 0 for v in [alpha_x, beta_y, gamma_z, q_param, f_stoich, epsilon, epsilon_prime]):
            raise ValueError("State variables and dimensionless parameters must be non-negative.")
            
        dx_dt = (q_param * beta_y - alpha_x * beta_y + alpha_x * (1.0 - alpha_x)) / epsilon
        dy_dt = (-q_param * beta_y - alpha_x * beta_y + 2.0 * f_stoich * gamma_z) / epsilon_prime
        dz_dt = alpha_x - gamma_z
        
        return {
            "dx_dt_hbro2": round(dx_dt, 4),
            "dy_dt_br_minus": round(dy_dt, 4),
            "dz_dt_ce_iv": round(dz_dt, 4),
            "oscillation_state": "Limit Cycle Active" if abs(dx_dt) + abs(dy_dt) > 1e-3 else "Steady State Quenched"
        }
