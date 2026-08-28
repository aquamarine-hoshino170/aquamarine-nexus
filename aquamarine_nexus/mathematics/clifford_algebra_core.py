class CliffordAlgebraCore:
    @staticmethod
    def pauli_clifford_geometric_product(v1_x: float, v1_y: float, v1_z: float, v2_x: float, v2_y: float, v2_z: float) -> dict:
        """u * v = u . v + u ^ v (Scalar + Bivector)"""
        scalar_dot = (v1_x * v2_x) + (v1_y * v2_y) + (v1_z * v2_z)
        
        # Bivector components (e23, e31, e12)
        bivector_e23 = (v1_y * v2_z) - (v1_z * v2_y)
        bivector_e31 = (v1_z * v2_x) - (v1_x * v2_z)
        bivector_e12 = (v1_x * v2_y) - (v1_y * v2_x)
        
        return {
            "scalar_grade_0_dot": round(scalar_dot, 6),
            "bivector_grade_2_e23": round(bivector_e23, 6),
            "bivector_grade_2_e31": round(bivector_e31, 6),
            "bivector_grade_2_e12": round(bivector_e12, 6),
            "is_orthogonal": abs(scalar_dot) < 1e-9,
            "is_parallel": (bivector_e23**2 + bivector_e31**2 + bivector_e12**2) < 1e-9
        }
