import math

class WindingNumberHomotopyCore:
    @staticmethod
    def discrete_winding_number(polygon_vertices_2d: list, point_z0: list = [0.0, 0.0]) -> dict:
        """W = (1 / 2*pi) * sum( Delta_theta_k ) along closed polygonal loop"""
        n = len(polygon_vertices_2d)
        if n < 3:
            raise ValueError("At least 3 vertices required to define a closed loop.")
        
        x0, y0 = point_z0
        total_angle = 0.0
        
        for i in range(n):
            x1, y1 = polygon_vertices_2d[i][0] - x0, polygon_vertices_2d[i][1] - y0
            x2, y2 = polygon_vertices_2d[(i + 1) % n][0] - x0, polygon_vertices_2d[(i + 1) % n][1] - y0
            
            dot = (x1 * x2) + (y1 * y2)
            cross = (x1 * y2) - (y1 * x2)
            
            d_theta = math.atan2(cross, dot)
            total_angle += d_theta
            
        winding_index = total_angle / (2.0 * math.pi)
        winding_int = round(winding_index)
        
        return {
            "probe_point_z0": point_z0,
            "polygon_vertex_count": n,
            "accumulated_angle_rad": round(total_angle, 6),
            "topological_winding_number": winding_int,
            "is_point_enclosed": winding_int != 0
        }
