class VariationalCalculusCore:
    @staticmethod
    def discrete_action_integral(kinetic_energies: list, potential_energies: list, dt: float) -> dict:
        """Action S = integral (T - V) dt approx sum (T_i - V_i) * dt"""
        if len(kinetic_energies) != len(potential_energies) or len(kinetic_energies) < 1 or dt <= 0:
            raise ValueError("Arrays must match and dt > 0.")
        lagrangian = [t - v for t, v in zip(kinetic_energies, potential_energies)]
        action_s = sum(lagrangian) * dt
        return {"steps": len(kinetic_energies), "time_step_dt": dt, "action_integral_Joules_s": round(action_s, 8)}

    @staticmethod
    def euler_lagrange_residual_1d(d_lagrangian_dq: float, d_lagrangian_dv_dot: float) -> dict:
        """Residual = (d/dt)(dL/dv) - dL/dq"""
        res = d_lagrangian_dv_dot - d_lagrangian_dq
        return {"residual_euler_lagrange": round(res, 8), "is_stationary": abs(res) < 1e-10}
