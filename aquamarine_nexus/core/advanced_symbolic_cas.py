import math
from aquamarine_nexus.core.symbolic_cas_pure import Symbol, Const, Expr, Add, Sub, Mul, Div, Pow, Sin, Cos, Exp, Ln, _simplify, _to_expr

class AdvancedSymbolicCAS:
    @staticmethod
    def symbolic_integrate_polynomial_terms(coefficients_dict: dict, var_name: str = 'x') -> str:
        """
        Integrates polynomials analytically: \int c * x^n dx = c/(n+1) * x^(n+1)
        Input format: {"power": coefficient} e.g., {2: 3.0, 1: -4.0, 0: 5.0} for 3x^2 - 4x + 5
        """
        integrated_terms = []
        for p_str, coeff in sorted(coefficients_dict.items(), key=lambda item: -int(item[0])):
            p = int(p_str)
            c = float(coeff)
            if c == 0:
                continue
            if p == -1:
                integrated_terms.append(f"{c:g}*ln(|{var_name}|)" if c != 1.0 else f"ln(|{var_name}|)")
            else:
                new_power = p + 1
                new_coeff = c / new_power
                if new_power == 1:
                    term = f"{new_coeff:g}*{var_name}" if new_coeff != 1.0 else var_name
                else:
                    term = f"{new_coeff:g}*{var_name}^{new_power}" if new_coeff != 1.0 else f"{var_name}^{new_power}"
                integrated_terms.append(term)
                
        result_str = " + ".join(integrated_terms).replace("+ -", "- ")
        return f"{result_str} + C" if result_str else "C"

    @staticmethod
    def taylor_series_expansion(expr_type: str, x0: float, order: int = 4, var_name: str = 'x') -> dict:
        """Computes analytical Taylor Series: \sum_{k=0}^n (f^(k)(x0) / k!) * (x - x0)^k"""
        x = Symbol(var_name)
        if expr_type == "exp":
            base_expr = Exp(x)
        elif expr_type == "sin":
            base_expr = Sin(x)
        elif expr_type == "cos":
            base_expr = Cos(x)
        elif expr_type == "ln":
            base_expr = Ln(x)
        else:
            raise ValueError("Supported expr_type: 'exp', 'sin', 'cos', 'ln'")

        terms = []
        poly_coefficients = []
        current_deriv = base_expr

        for k in range(order + 1):
            val_at_x0 = current_deriv.eval({var_name: x0})
            coeff = val_at_x0 / math.factorial(k)
            poly_coefficients.append(coeff)
            
            if abs(coeff) > 1e-12:
                if k == 0:
                    terms.append(f"{coeff:.6g}")
                elif k == 1:
                    shift = f"({var_name} - {x0:g})" if x0 != 0 else var_name
                    terms.append(f"{coeff:.6g}*{shift}")
                else:
                    shift = f"({var_name} - {x0:g})^{k}" if x0 != 0 else f"{var_name}^{k}"
                    terms.append(f"{coeff:.6g}*{shift}")
                    
            current_deriv = _simplify(current_deriv.diff(x))

        expansion_str = " + ".join(terms).replace("+ -", "- ")
        return {
            "function": str(base_expr),
            "expansion_point_x0": x0,
            "order": order,
            "taylor_polynomial": expansion_str,
            "coefficients": [round(c, 8) for c in poly_coefficients]
        }

    @staticmethod
    def evaluate_symbolic_limit_lhopital(numerator_type: str, denominator_type: str, limit_point: float, var_name: str = 'x') -> dict:
        """Solves indeterminate forms 0/0 using automatic symbolic L'Hôpital's differentiation."""
        x = Symbol(var_name)
        
        # Build numerator
        if numerator_type == "sin(x)": num_expr = Sin(x)
        elif numerator_type == "exp(x)-1": num_expr = Exp(x) - Const(1.0)
        elif numerator_type == "1-cos(x)": num_expr = Const(1.0) - Cos(x)
        else: raise ValueError("Unsupported numerator form.")

        # Build denominator
        if denominator_type == "x": den_expr = x
        elif denominator_type == "x^2": den_expr = x ** Const(2.0)
        else: raise ValueError("Unsupported denominator form.")

        num_val = num_expr.eval({var_name: limit_point})
        den_val = den_expr.eval({var_name: limit_point})

        # Apply L'Hôpital if 0/0
        if abs(num_val) < 1e-9 and abs(den_val) < 1e-9:
            num_diff = _simplify(num_expr.diff(x))
            den_diff = _simplify(den_expr.diff(x))
            
            num_val2 = num_diff.eval({var_name: limit_point})
            den_val2 = den_diff.eval({var_name: limit_point})
            
            if abs(den_val2) < 1e-9 and abs(num_val2) < 1e-9:
                num_diff2 = _simplify(num_diff.diff(x))
                den_diff2 = _simplify(den_diff.diff(x))
                limit_result = num_diff2.eval({var_name: limit_point}) / den_diff2.eval({var_name: limit_point})
                rule_applied = "Double L'Hopital Rule"
            else:
                limit_result = num_val2 / den_val2
                rule_applied = "Single L'Hopital Rule"
        else:
            limit_result = num_val / den_val
            rule_applied = "Direct Substitution"

        return {
            "expression": f"({num_expr}) / ({den_expr})",
            "limit_point": limit_point,
            "evaluation_method": rule_applied,
            "exact_limit_value": round(limit_result, 8)
        }

    @staticmethod
    def symbolic_newton_raphson_solve(equation_type: str, initial_guess: float, tolerance: float = 1e-12, max_iter: int = 100) -> dict:
        """Solves f(x) = 0 analytically generating exact symbolic derivatives for quadratic convergence."""
        x = Symbol('x')
        if equation_type == "kepler_transcendental":
            # x - 0.5 * sin(x) - 1.0 = 0
            expr = x - (Const(0.5) * Sin(x)) - Const(1.0)
        elif equation_type == "cubic_depressed":
            # x^3 - 2*x - 5 = 0
            expr = (x ** Const(3.0)) - (Const(2.0) * x) - Const(5.0)
        elif equation_type == "exponential_cross":
            # exp(x) - 3*x = 0 (finds positive root)
            expr = Exp(x) - (Const(3.0) * x)
        else:
            raise ValueError("Unsupported equation type.")

        df = _simplify(expr.diff(x))
        curr_x = initial_guess

        for i in range(max_iter):
            f_val = expr.eval({'x': curr_x})
            df_val = df.eval({'x': curr_x})
            if abs(df_val) < 1e-15:
                break
            delta = f_val / df_val
            curr_x -= delta
            if abs(delta) < tolerance:
                return {
                    "equation": f"{expr} = 0",
                    "symbolic_derivative": str(df),
                    "converged_root": round(curr_x, 12),
                    "residual_f_x": f"{expr.eval({'x': curr_x}):.6e}",
                    "iterations": i + 1,
                    "status": "CONVERGED_EXACT"
                }

        raise RuntimeError("Newton-Raphson failed to converge within tolerance.")
