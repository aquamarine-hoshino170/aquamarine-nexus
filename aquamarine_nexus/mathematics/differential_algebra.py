class DifferentialAlgebraCore:
    @staticmethod
    def wronskian_2x2(y1_val: float, dy1_val: float, y2_val: float, dy2_val: float) -> dict:
        """W(y1, y2) = y1 * dy2 - y2 * dy1"""
        w = (y1_val * dy2_val) - (y2_val * dy1_val)
        return {
            "wronskian_value": round(w, 8),
            "are_linearly_independent": abs(w) > 1e-10
        }

    @staticmethod
    def casoratian_sequence_step(x_n: list, y_n: list, idx: int) -> dict:
        """C(n) = x(n)*y(n+1) - x(n+1)*y(n) for discrete difference equations"""
        if idx < 0 or idx >= len(x_n) - 1 or len(x_n) != len(y_n):
            raise ValueError("Index out of bounds or sequence length mismatch.")
        c_val = (x_n[idx] * y_n[idx + 1]) - (x_n[idx + 1] * y_n[idx])
        return {
            "step_index_n": idx,
            "casoratian_value": round(c_val, 8),
            "is_discrete_independent": abs(c_val) > 1e-10
        }
