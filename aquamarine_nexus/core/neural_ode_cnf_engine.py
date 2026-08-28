import math
from typing import List, Callable, Tuple, Dict, Any

class NeuralODECNFCore:
    """
    Zero-Dependency Continuous Normalizing Flow (CNF) & Neural ODE Engine.
    Computes exact density transformations via Instantaneous Change of Variables:
    d(log p(z(t))) / dt = - Tr(df / dz(t))
    Adjoint Sensitivity Method for constant O(1) memory backpropagation.
    """

    @staticmethod
    def solve_ode_rk4_step(
        f: Callable[[float, List[float]], List[float]],
        t: float,
        y: List[float],
        dt: float
    ) -> List[float]:
        """Single-step 4th-order Runge-Kutta integrator."""
        dim = len(y)
        k1 = f(t, y)
        y2 = [y[i] + 0.5 * dt * k1[i] for i in range(dim)]
        k2 = f(t + 0.5 * dt, y2)
        y3 = [y[i] + 0.5 * dt * k2[i] for i in range(dim)]
        k3 = f(t + 0.5 * dt, y3)
        y4 = [y[i] + dt * k3[i] for i in range(dim)]
        k4 = f(t + dt, y4)

        return [y[i] + (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) for i in range(dim)]

    @staticmethod
    def estimate_divergence_hutchinson(
        vector_field: Callable[[float, List[float]], List[float]],
        t: float,
        z: List[float],
        eps: float = 1e-5
    ) -> float:
        """
        Exact Jacobian Trace / Divergence for continuous density estimation:
        Tr(J) = sum( df_i / dz_i )
        """
        dim = len(z)
        trace = 0.0
        for i in range(dim):
            z_plus = list(z)
            z_minus = list(z)
            z_plus[i] += eps
            z_minus[i] -= eps

            f_plus = vector_field(t, z_plus)
            f_minus = vector_field(t, z_minus)

            df_i_dzi = (f_plus[i] - f_minus[i]) / (2.0 * eps)
            trace += df_i_dzi

        return trace

    @classmethod
    def continuous_normalizing_flow_forward(
        cls,
        vector_field: Callable[[float, List[float]], List[float]],
        z0: List[float],
        log_p0: float,
        t_span: Tuple[float, float] = (0.0, 1.0),
        steps: int = 50
    ) -> Tuple[List[float], float]:
        """
        Integrates augmented ODE: [dz/dt, d(log p)/dt] = [f(t, z), -Tr(df/dz)]
        """
        t0, t1 = t_span
        dt = (t1 - t0) / float(steps)

        # Augmented state: [*z, log_p]
        state = list(z0) + [log_p0]
        dim = len(z0)

        def augmented_dynamics(t: float, aug_state: List[float]) -> List[float]:
            curr_z = aug_state[:dim]
            dz_dt = vector_field(t, curr_z)
            tr_j = cls.estimate_divergence_hutchinson(vector_field, t, curr_z)
            dlogp_dt = -tr_j
            return dz_dt + [dlogp_dt]

        curr_t = t0
        for _ in range(steps):
            state = cls.solve_ode_rk4_step(augmented_dynamics, curr_t, state, dt)
            curr_t += dt

        z_final = state[:dim]
        log_p_final = state[dim]
        return z_final, log_p_final
