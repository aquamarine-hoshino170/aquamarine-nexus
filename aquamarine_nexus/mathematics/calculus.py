import math

class CalculusEngine:
    """Numerical Calculus & Dynamical Systems Engine"""
    @staticmethod
    def numerical_derivative(func, x: float, h: float = 1e-7) -> float:
        """Central Difference Method (O(h^2) accuracy)"""
        return (func(x + h) - func(x - h)) / (2.0 * h)

    @staticmethod
    def adaptive_simpson_integral(func, a: float, b: float, n: int = 1000) -> float:
        """Composite Simpson's 1/3 Rule for Numerical Integration"""
        if n % 2 != 0:
            n += 1
        h = (b - a) / n
        s = func(a) + func(b)
        for i in range(1, n, 2):
            s += 4.0 * func(a + i * h)
        for i in range(2, n - 1, 2):
            s += 2.0 * func(a + i * h)
        return round(s * (h / 3.0), 8)

    @staticmethod
    def rk4_ode_step(func, t: float, y: float, dt: float) -> float:
        """Runge-Kutta 4th Order ODE Step"""
        k1 = func(t, y)
        k2 = func(t + 0.5 * dt, y + 0.5 * dt * k1)
        k3 = func(t + 0.5 * dt, y + 0.5 * dt * k2)
        k4 = func(t + dt, y + dt * k3)
        return y + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
