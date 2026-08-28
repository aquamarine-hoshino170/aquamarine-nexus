import math

class SymbolicCore:
    """Symbolic Expression Engine (SymPy Alternative)"""
    @staticmethod
    def symbolic_poly_derivative(poly_coeffs: list) -> list:
        """Differentiates polynomial represented by coefficient list [a_0, a_1, a_2, ...] (a0 + a1*x + a2*x^2)"""
        if len(poly_coeffs) <= 1:
            return [0.0]
        return [i * poly_coeffs[i] for i in range(1, len(poly_coeffs))]

    @staticmethod
    def taylor_expansion_exp(x: float, order: int = 10) -> dict:
        """Symbolic-numeric Taylor series for e^x = sum(x^k / k!)"""
        approx = 0.0
        terms = []
        for k in range(order + 1):
            term = (x ** k) / math.factorial(k)
            approx += term
            terms.append(f"x^{k}/{k}!")
        return {"order": order, "approximation": round(approx, 8), "exact_math": round(math.exp(x), 8)}

    @staticmethod
    def taylor_expansion_sin(x: float, order: int = 5) -> dict:
        """Taylor series for sin(x) = sum((-1)^k * x^(2k+1) / (2k+1)!)"""
        approx = 0.0
        for k in range(order):
            term = ((-1) ** k) * (x ** (2 * k + 1)) / math.factorial(2 * k + 1)
            approx += term
        return {"order_terms": order, "sin_approx": round(approx, 8), "exact_sin": round(math.sin(x), 8)}
