class MetricGeometryCaratheodoryCore:
    @staticmethod
    def conformal_modulus_rectangle(width_a: float, height_b: float) -> dict:
        """Modulus M(R) = a / b, Extremal Length Lambda(Gamma) = 1 / M(R)"""
        if width_a <= 0 or height_b <= 0:
            raise ValueError("Dimensions must be strictly positive.")
            
        modulus = width_a / height_b
        extremal_length = height_b / width_a
        
        return {
            "conformal_width_a": width_a,
            "conformal_height_b": height_b,
            "conformal_modulus_M": round(modulus, 6),
            "extremal_length_Lambda": round(extremal_length, 6),
            "is_conformal_square": abs(modulus - 1.0) < 1e-9
        }
