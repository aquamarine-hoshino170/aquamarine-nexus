from aquamarine_nexus.core.tensor_array_pure import PureNDArray
from aquamarine_nexus.core.symbolic_cas_pure import Symbol, Const, Sin, Cos, Exp, Ln, _simplify

class Tier1FoundationCore:
    @staticmethod
    def pure_tensor_matrix_multiplication(m1_rows: list, m2_rows: list) -> dict:
        """NumPy-Grade Pure Vectorized Matrix Dot Product"""
        a = PureNDArray(m1_rows)
        b = PureNDArray(m2_rows)
        c = a.dot(b)
        return {
            "matrix_A_shape": list(a.shape),
            "matrix_B_shape": list(b.shape),
            "product_shape": list(c.shape),
            "result_matrix": c.to_list(),
            "frobenius_norm": round(c.norm(), 6)
        }

    @staticmethod
    def pure_symbolic_exact_differentiation(expression_type: str, x_eval: float) -> dict:
        """SymPy-Grade Exact Closed-Form Symbolic Differentiation"""
        x = Symbol('x')
        if expression_type == "polynomial":
            expr = (x ** 3) - (Const(4.0) * (x ** 2)) + (Const(7.0) * x) - Const(5.0)
        elif expression_type == "transcendental":
            expr = Exp(x) * Sin(x)
        elif expression_type == "rational":
            expr = Ln(x) / x
        else:
            raise ValueError("Supported types: 'polynomial', 'transcendental', 'rational'")

        derivative = expr.diff(x)
        val_f = expr.eval({'x': x_eval})
        val_df = derivative.eval({'x': x_eval})

        return {
            "expression": str(expr),
            "symbolic_derivative": str(_simplify(derivative)),
            "evaluation_point_x": x_eval,
            "f_x": round(val_f, 6),
            "df_dx_exact": round(val_df, 6)
        }
