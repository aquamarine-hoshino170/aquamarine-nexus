class NexusPoly:
    """Symbolic Polynomial Manipulation & Evaluation Core (SymPy Extension)"""
    @staticmethod
    def poly_eval(coeffs: list, x: float) -> float:
        """Evaluates P(x) = c0 + c1*x + c2*x^2 + ... via Horner's Method"""
        res = 0.0
        for c in reversed(coeffs):
            res = res * x + c
        return round(res, 6)

    @staticmethod
    def poly_add(p1: list, p2: list) -> list:
        """Adds two polynomials represented as coefficient lists"""
        max_len = max(len(p1), len(p2))
        res = [0.0] * max_len
        for i in range(max_len):
            v1 = p1[i] if i < len(p1) else 0.0
            v2 = p2[i] if i < len(p2) else 0.0
            res[i] = v1 + v2
        return res

    @staticmethod
    def poly_mul(p1: list, p2: list) -> list:
        """Multiplies two polynomials (Cauchy Product)"""
        res = [0.0] * (len(p1) + len(p2) - 1)
        for i, c1 in enumerate(p1):
            for j, c2 in enumerate(p2):
                res[i + j] += c1 * c2
        return [round(c, 4) for c in res]
