import math

class QuaternionAlgebraCore:
    @staticmethod
    def quaternion_product(q1: list, q2: list) -> dict:
        """Hamilton product: q1 * q2 = (w1*w2 - v1.v2, w1*v2 + w2*v1 + v1 x v2)"""
        if len(q1) != 4 or len(q2) != 4:
            raise ValueError("Quaternions must be 4D vectors [w, x, y, z].")
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2

        w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        y = w1*y2 - x1*z2 + y1*w2 + z1*x2
        z = w1*z2 + x1*y2 - y1*x2 + z1*w2

        norm = math.sqrt(w**2 + x**2 + y**2 + z**2)
        return {
            "quaternion_product": [round(w, 6), round(x, 6), round(y, 6), round(z, 6)],
            "result_norm": round(norm, 6)
        }

    @staticmethod
    def quaternion_rotate_vector_3d(vector_v: list, axis_u: list, angle_rad: float) -> dict:
        """v' = q * v * q^-1 where q = [cos(theta/2), sin(theta/2) * u_hat]"""
        if len(vector_v) != 3 or len(axis_u) != 3:
            raise ValueError("Vector and rotation axis must be 3D.")
        axis_norm = math.sqrt(sum(a**2 for a in axis_u))
        if axis_norm == 0:
            raise ValueError("Rotation axis cannot be zero vector.")
        
        ux, uy, uz = [a / axis_norm for a in axis_u]
        half_theta = angle_rad / 2.0
        qw = math.cos(half_theta)
        qx = ux * math.sin(half_theta)
        qy = uy * math.sin(half_theta)
        qz = uz * math.sin(half_theta)

        # q * [0, vx, vy, vz]
        vx, vy, vz = vector_v
        t_w = - qx*vx - qy*vy - qz*vz
        t_x =   qw*vx + qy*vz - qz*vy
        t_y =   qw*vy - qx*vz + qz*vx
        t_z =   qw*vz + qx*vy - qy*vx

        # t * q_conjugate [qw, -qx, -qy, -qz]
        rx = t_w*(-qx) + t_x*qw - t_y*(-qz) + t_z*(-qy)
        ry = t_w*(-qy) + t_y*qw - t_z*(-qx) + t_x*(-qz)
        rz = t_w*(-qz) + t_z*qw - t_x*(-qy) + t_y*(-qx)

        return {
            "original_vector": vector_v,
            "rotation_angle_rad": round(angle_rad, 6),
            "rotated_vector": [round(rx, 6), round(ry, 6), round(rz, 6)]
        }
