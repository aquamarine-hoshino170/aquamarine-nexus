class RiemannGeometryCore:
    @staticmethod
    def ricci_scalar_from_diagonal_metric(metric_diag: list, d2_metric_diag: list) -> dict:
        """R approx (1/2) * sum( g^ii * d2_g_ii ) for diagonal weak-field metric"""
        if len(metric_diag) != 4 or len(d2_metric_diag) != 4: raise ValueError("4D Spacetime metric required.")
        r_scalar = 0.5 * sum((1.0 / metric_diag[i]) * d2_metric_diag[i] for i in range(4))
        return {"metric_signature": metric_diag, "ricci_scalar_R": round(r_scalar, 8)}

    @staticmethod
    def kretschmann_scalar_schwarzschild(mass_kg: float, radius_meters: float) -> dict:
        """K = R^{abcd} R_{abcd} = 48 * G^2 * M^2 / (c^4 * r^6)"""
        g, c = 6.67430e-11, 299792458.0
        if radius_meters <= 0 or mass_kg <= 0: raise ValueError("Invalid parameters.")
        k = (48.0 * (g ** 2) * (mass_kg ** 2)) / ((c ** 4) * (radius_meters ** 6))
        return {"radius_m": f"{radius_meters:.6e}", "kretschmann_scalar_inv_m4": f"{k:.6e}"}
