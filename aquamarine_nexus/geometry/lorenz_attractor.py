class LorenzChaosCore:
    """Lorenz Strange Attractor & 3D Phase Space Trajectories"""

    @staticmethod
    def lorenz_rk4_step(x: float, y: float, z: float, dt: float = 0.01, sigma: float = 10.0, rho: float = 28.0, beta: float = 8.0/3.0) -> dict:
        """
        Integrates Lorenz ODEs by one step dt via Runge-Kutta 4th Order:
        dx/dt = sigma * (y - x)
        dy/dt = x * (rho - z) - y
        dz/dt = x * y - beta * z
        """
        def f(cx, cy, cz):
            dx = sigma * (cy - cx)
            dy = cx * (rho - cz) - cy
            dz = cx * cy - beta * cz
            return dx, dy, dz

        # RK4 Slopes
        k1x, k1y, k1z = f(x, y, z)
        k2x, k2y, k2z = f(x + 0.5 * dt * k1x, y + 0.5 * dt * k1y, z + 0.5 * dt * k1z)
        k3x, k3y, k3z = f(x + 0.5 * dt * k2x, y + 0.5 * dt * k2y, z + 0.5 * dt * k2z)
        k4x, k4y, k4z = f(x + dt * k3x, y + dt * k3y, z + dt * k3z)

        x_next = x + (dt / 6.0) * (k1x + 2.0 * k2x + 2.0 * k3x + k4x)
        y_next = y + (dt / 6.0) * (k1y + 2.0 * k2y + 2.0 * k3y + k4y)
        z_next = z + (dt / 6.0) * (k1z + 2.0 * k2z + 2.0 * k3z + k4z)

        return {
            "x_next": round(x_next, 6),
            "y_next": round(y_next, 6),
            "z_next": round(z_next, 6)
        }
