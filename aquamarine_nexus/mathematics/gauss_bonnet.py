import math

class GaussBonnetCore:
    @staticmethod
    def euler_characteristic_from_curvature(total_integrated_gaussian_curvature: float) -> dict:
        """integral_M K dA = 2 * pi * chi(M)"""
        chi_float = total_integrated_gaussian_curvature / (2.0 * math.pi)
        chi_int = round(chi_float)
        # For orientable closed 2-manifolds: chi = 2 - 2g => g = (2 - chi) / 2
        genus = (2 - chi_int) / 2.0
        return {
            "integrated_curvature": total_integrated_gaussian_curvature,
            "euler_characteristic_chi": chi_int,
            "topological_genus_g": int(genus) if genus >= 0 and genus.is_integer() else "Non-orientable/Boundary"
        }

    @staticmethod
    def geodesic_curvature_step(tangent_angle_turn_rad: float, arc_length_ds: float) -> dict:
        """k_g = d(phi)/ds"""
        if arc_length_ds <= 0:
            raise ValueError("Arc length ds must be positive.")
        k_g = tangent_angle_turn_rad / arc_length_ds
        return {
            "tangent_turn_rad": round(tangent_angle_turn_rad, 6),
            "arc_length_ds": arc_length_ds,
            "geodesic_curvature_k_g": round(k_g, 6)
        }
