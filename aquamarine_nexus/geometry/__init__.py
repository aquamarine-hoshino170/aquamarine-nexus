import math

class EuclideanGeometry:
    """Foundational Euclidean Plane & Solid Geometry"""
    @staticmethod
    def polygon_area_shoelace(vertices: list) -> float:
        """Shoelace formula for any 2D polygon: vertices = [(x1, y1), (x2, y2), ...]"""
        n = len(vertices)
        if n < 3:
            raise ValueError("Polygon must have at least 3 vertices.")
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += vertices[i][0] * vertices[j][1]
            area -= vertices[j][0] * vertices[i][1]
        return round(abs(area) / 2.0, 6)

    @staticmethod
    def triangle_inradius_circumradius(a: float, b: float, c: float) -> dict:
        """Heron's Formula based Inradius (r) & Circumradius (R)"""
        s = (a + b + c) / 2.0
        area_sq = s * (s - a) * (s - b) * (s - c)
        if area_sq <= 0:
            raise ValueError("Degenerate or invalid triangle sides.")
        area = math.sqrt(area_sq)
        r = area / s
        R = (a * b * c) / (4.0 * area)
        return {"area": round(area, 4), "inradius": round(r, 4), "circumradius": round(R, 4)}

class NonEuclideanGeometry:
    """Hyperbolic & Spherical Manifold Geometry"""
    @staticmethod
    def spherical_triangle_excess(A_deg: float, B_deg: float, C_deg: float, radius: float = 1.0) -> dict:
        """Girard's Theorem: Area = R^2 * E where E = (A + B + C - π) in radians"""
        A_rad, B_rad, C_rad = math.radians(A_deg), math.radians(B_deg), math.radians(C_deg)
        excess = (A_rad + B_rad + C_rad) - math.pi
        if excess <= 0:
            raise ValueError("Sum of angles on a spherical triangle must exceed 180 degrees.")
        area = (radius ** 2) * excess
        return {"excess_radians": round(excess, 5), "spherical_area": round(area, 5)}

    @staticmethod
    def poincare_disk_distance(u: tuple, v: tuple) -> float:
        """Hyperbolic distance in Poincare Disk model: d = arcosh(1 + 2|u-v|^2 / ((1-|u|^2)(1-|v|^2)))"""
        norm_u_sq = u[0]**2 + u[1]**2
        norm_v_sq = v[0]**2 + v[1]**2
        if norm_u_sq >= 1.0 or norm_v_sq >= 1.0:
            raise ValueError("Points must lie strictly inside the open unit disk |z| < 1.")
        diff_sq = (u[0] - v[0])**2 + (u[1] - v[1])**2
        delta = 1.0 + 2.0 * diff_sq / ((1.0 - norm_u_sq) * (1.0 - norm_v_sq))
        return round(math.acosh(delta), 6)
