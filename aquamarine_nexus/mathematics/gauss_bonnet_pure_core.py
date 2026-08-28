import math

class GaussBonnetPureCore:
    @staticmethod
    def verify_gauss_bonnet_closed_surface(gaussian_curvature_integral: float, boundary_geodesic_integral: float = 0.0) -> dict:
        """iint_M K dA + int_{partial M} k_g ds = 2 * pi * chi(M)"""
        total_curvature = gaussian_curvature_integral + boundary_geodesic_integral
        chi_exact = total_curvature / (2.0 * math.pi)
        chi_integer = round(chi_exact)
        
        genus_g = (2 - chi_integer) // 2 if (2 - chi_integer) % 2 == 0 else (2 - chi_integer) / 2.0
        
        residual = abs(total_curvature - (2.0 * math.pi * chi_integer))
        
        return {
            "gaussian_curvature_integral": round(gaussian_curvature_integral, 6),
            "boundary_geodesic_integral": round(boundary_geodesic_integral, 6),
            "total_topological_flux": round(total_curvature, 6),
            "euler_characteristic_chi": chi_integer,
            "topological_genus_g": genus_g,
            "residual_error": f"{residual:.10e}",
            "gauss_bonnet_satisfied": residual < 1e-4
        }
