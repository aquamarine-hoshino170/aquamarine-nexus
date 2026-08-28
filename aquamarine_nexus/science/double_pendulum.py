import math

class DoublePendulumCore:
    """Chaotic Double Pendulum Lagrangian Dynamic Integrator"""

    @staticmethod
    def step_state(theta1: float, theta2: float, omega1: float, omega2: float, 
                   m1: float = 1.0, m2: float = 1.0, l1: float = 1.0, l2: float = 1.0, 
                   g: float = 9.80665, dt: float = 0.01) -> dict:
        """
        Calculates angular accelerations (alpha1, alpha2) and integrates 1 time-step dt.
        """
        delta = theta1 - theta2

        d1 = (m1 + m2) * l1 - m2 * l1 * (math.cos(delta) ** 2)
        d2 = (l2 / l1) * d1

        # Angular acceleration 1
        num1 = (-g * (2 * m1 + m2) * math.sin(theta1) 
                - m2 * g * math.sin(theta1 - 2 * theta2) 
                - 2 * math.sin(delta) * m2 * (omega2**2 * l2 + omega1**2 * l1 * math.cos(delta)))
        alpha1 = num1 / (l1 * (2 * m1 + m2 - m2 * math.cos(2 * theta1 - 2 * theta2)))

        # Angular acceleration 2
        num2 = (2 * math.sin(delta) * (omega1**2 * l1 * (m1 + m2) 
                + g * (m1 + m2) * math.cos(theta1) 
                + omega2**2 * l2 * m2 * math.cos(delta)))
        alpha2 = num2 / (l2 * (2 * m1 + m2 - m2 * math.cos(2 * theta1 - 2 * theta2)))

        omega1_next = omega1 + alpha1 * dt
        omega2_next = omega2 + alpha2 * dt
        theta1_next = theta1 + omega1_next * dt
        theta2_next = theta2 + omega2_next * dt

        # Total Energy (Kinetic + Potential)
        t1 = 0.5 * m1 * (l1 * omega1_next)**2
        t2 = 0.5 * m2 * ((l1 * omega1_next)**2 + (l2 * omega2_next)**2 + 2 * l1 * l2 * omega1_next * omega2_next * math.cos(delta))
        v1 = -(m1 + m2) * g * l1 * math.cos(theta1_next)
        v2 = -m2 * g * l2 * math.cos(theta2_next)
        total_energy = t1 + t2 + v1 + v2

        return {
            "theta1_rad": round(theta1_next, 5),
            "theta2_rad": round(theta2_next, 5),
            "omega1_rad_s": round(omega1_next, 5),
            "omega2_rad_s": round(omega2_next, 5),
            "total_energy_J": round(total_energy, 5)
        }
