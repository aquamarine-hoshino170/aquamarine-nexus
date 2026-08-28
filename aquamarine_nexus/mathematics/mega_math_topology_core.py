import math

class MegaMathTopologyCore:
    @staticmethod
    def euler_characteristic_polyhedron(vertices_v: int, edges_e: int, faces_f: int) -> dict:
        """chi = V - E + F (Euler-Poincaré Formula)"""
        if vertices_v <= 0 or edges_e <= 0 or faces_f <= 0:
            raise ValueError("Elements must be positive integers.")
        chi = vertices_v - edges_e + faces_f
        genus_g = (2 - chi) // 2 if (2 - chi) % 2 == 0 else (2 - chi) / 2.0
        return {
            "vertices_V": vertices_v,
            "edges_E": edges_e,
            "faces_F": faces_f,
            "euler_characteristic_chi": chi,
            "topological_genus_g": genus_g,
            "is_sphere_homeomorphic": chi == 2
        }

    @staticmethod
    def mobius_inversion_term(n: int) -> dict:
        """mu(n) = 1 if square-free with even prime factors, -1 if odd, 0 if square factor"""
        if n <= 0: raise ValueError("n must be a positive integer.")
        if n == 1: return {"n": 1, "mobius_mu": 1}
        
        factors = 0
        temp = n
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                factors += 1
                temp //= d
                if temp % d == 0:
                    return {"n": n, "mobius_mu": 0, "is_square_free": False}
            d += 1
        if temp > 1:
            factors += 1
            
        mu_val = -1 if factors % 2 != 0 else 1
        return {"n": n, "mobius_mu": mu_val, "prime_factors_count": factors, "is_square_free": True}

    @staticmethod
    def cauchy_simple_pole_residue(numerator_at_z0: float, denominator_derivative_at_z0: float) -> dict:
        """Res(f, z_0) = g(z_0) / h'(z_0) for f(z) = g(z)/h(z)"""
        if abs(denominator_derivative_at_z0) < 1e-15:
            raise ValueError("Denominator derivative must be non-zero at simple pole.")
        residue = numerator_at_z0 / denominator_derivative_at_z0
        integral_contour = 2.0 * math.pi * residue
        return {
            "simple_pole_residue": round(residue, 8),
            "contour_integral_2pi_i_scaled": round(integral_contour, 8)
        }
