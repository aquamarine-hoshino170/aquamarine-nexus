import math

class HomotopyTopologyCore:
    """Pure Mathematics: Algebraic Topology, Homotopy Classes & Winding Numbers"""

    @staticmethod
    def discrete_winding_number(polygon_vertices: list, origin_point: list = [0.0, 0.0]) -> dict:
        """
        Computes the topological winding number W(gamma, z_0) for a closed discrete 2D loop gamma:
        W = (1 / 2pi) * sum [ delta_theta_i ]
        """
        if len(polygon_vertices) < 3:
            raise ValueError("Closed loop requires at least 3 vertices.")

        ox, oy = origin_point[0], origin_point[1]
        pts = [[p[0] - ox, p[1] - oy] for p in polygon_vertices]
        
        # Close loop if open
        if pts[0] != pts[-1]:
            pts.append(pts[0])

        total_angle = 0.0
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]

            # Check for origin intersection
            if (x1 == 0 and y1 == 0) or (x2 == 0 and y2 == 0):
                raise ValueError("Curve passes strictly through the origin singularity.")

            # Cross product and dot product for angle delta
            dot = x1 * x2 + y1 * y2
            cross = x1 * y2 - y1 * x2
            delta_theta = math.atan2(cross, dot)
            total_angle += delta_theta

        winding = round(total_angle / (2.0 * math.pi))
        return {
            "origin_point": origin_point,
            "total_angle_radians": round(total_angle, 6),
            "winding_number_invariant": winding,
            "is_contractible_in_punctured_plane": winding == 0
        }
