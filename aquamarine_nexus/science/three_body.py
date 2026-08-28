import math

class ThreeBodyCore:
    """Planar 3-Body Gravitational Dynamics Integrator"""

    G_CONST = 6.67430e-11

    @staticmethod
    def step_3body_planar(m1: float, m2: float, m3: float,
                          r1: list, r2: list, r3: list,
                          v1: list, v2: list, v3: list,
                          dt: float = 1.0) -> dict:
        """
        Calculates gravitational acceleration for 3 bodies in 2D and updates positions/velocities via Symplectic Euler.
        r = [x, y], v = [vx, vy]
        """
        G = ThreeBodyCore.G_CONST

        def compute_acc(r_self, r_other, m_other):
            dx = r_other[0] - r_self[0]
            dy = r_other[1] - r_self[1]
            dist = math.sqrt(dx**2 + dy**2)
            if dist < 1e-3:
                dist = 1e-3 # Softening parameter to prevent division by zero
            f = (G * m_other) / (dist**3)
            return f * dx, f * dy

        # Total acceleration for each body
        a1x_2, a1y_2 = compute_acc(r1, r2, m2)
        a1x_3, a1y_3 = compute_acc(r1, r3, m3)
        a1 = [a1x_2 + a1x_3, a1y_2 + a1y_3]

        a2x_1, a2y_1 = compute_acc(r2, r1, m1)
        a2x_3, a2y_3 = compute_acc(r2, r3, m3)
        a2 = [a2x_1 + a2x_3, a2y_1 + a2y_3]

        a3x_1, a3y_1 = compute_acc(r3, r1, m1)
        a3x_2, a3y_2 = compute_acc(r3, r2, m2)
        a3 = [a3x_1 + a3x_2, a3y_1 + a3y_2]

        # Velocity update
        v1_next = [v1[0] + a1[0] * dt, v1[1] + a1[1] * dt]
        v2_next = [v2[0] + a2[0] * dt, v2[1] + a2[1] * dt]
        v3_next = [v3[0] + a3[0] * dt, v3[1] + a3[1] * dt]

        # Position update
        r1_next = [r1[0] + v1_next[0] * dt, r1[1] + v1_next[1] * dt]
        r2_next = [r2[0] + v2_next[0] * dt, r2[1] + v2_next[1] * dt]
        r3_next = [r3[0] + v3_next[0] * dt, r3[1] + v3_next[1] * dt]

        return {
            "body1_r": [round(x, 3) for x in r1_next],
            "body2_r": [round(x, 3) for x in r2_next],
            "body3_r": [round(x, 3) for x in r3_next],
            "body1_v": [round(x, 5) for x in v1_next],
            "body2_v": [round(x, 5) for x in v2_next],
            "body3_v": [round(x, 5) for x in v3_next]
        }
