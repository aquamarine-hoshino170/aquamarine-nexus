import math

class DualNumber:
    """Forward-mode automatic differentiation element: x + eps * dx"""
    def __init__(self, val: float, der: float = 0.0):
        self.val = float(val)
        self.der = float(der)

    def __add__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other, 0.0)
        return DualNumber(self.val + other.val, self.der + other.der)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other, 0.0)
        return DualNumber(self.val - other.val, self.der - other.der)

    def __rsub__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other, 0.0)
        return DualNumber(other.val - self.val, other.der - self.der)

    def __mul__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other, 0.0)
        return DualNumber(self.val * other.val, (self.val * other.der) + (self.der * other.val))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other, 0.0)
        return DualNumber(self.val / other.val, (self.der * other.val - self.val * other.der) / (other.val ** 2))

    def __pow__(self, power: float):
        return DualNumber(self.val ** power, power * (self.val ** (power - 1.0)) * self.der)


class ManifoldAutoDiffRicciFlowCore:
    @staticmethod
    def riemannian_gradient_and_christoffel_flow(theta: float, phi: float, radius: float = 1.0, flow_dt: float = 0.01) -> dict:
        """
        1. Evaluates scalar potential f(theta, phi) = cos(theta) * sin(phi) on 2-Sphere S^2.
        2. Computes Euclidean gradients via DualNumber Forward-mode Automatic Differentiation.
        3. Computes Riemannian Gradient: Grad_M f = g^{ij} * (df / dx^j) where g = diag(r^2, r^2 * sin^2(theta)).
        4. Calculates Christoffel Symbols Gamma^k_ij on curved manifold.
        5. Computes Ricci Curvature Tensor R_ij and evolves metric: g_ij(t+dt) = g_ij(t) - 2 * dt * R_ij.
        """
        if radius <= 0 or theta <= 0 or theta >= math.pi:
            raise ValueError("Radius must be > 0 and theta in (0, pi) to avoid spherical coordinate singularity.")

        # --- Forward-Mode AD for Euclidean Partial Derivatives ---
        # df/dtheta
        t_dual = DualNumber(theta, 1.0)
        f_theta_dual = DualNumber(math.cos(t_dual.val), -math.sin(t_dual.val) * t_dual.der) * DualNumber(math.sin(phi), 0.0)
        df_dtheta = f_theta_dual.der

        # df/dphi
        p_dual = DualNumber(phi, 1.0)
        f_phi_dual = DualNumber(math.cos(theta), 0.0) * DualNumber(math.sin(p_dual.val), math.cos(p_dual.val) * p_dual.der)
        df_dphi = f_phi_dual.der

        # --- Metric Tensor g_ij and Inverse g^{ij} on S^2 ---
        g_11 = radius ** 2
        g_22 = (radius ** 2) * (math.sin(theta) ** 2)
        inv_g11 = 1.0 / g_11
        inv_g22 = 1.0 / g_22

        # --- Riemannian Manifold Gradient: Grad^M f = g^{ij} * \partial_j f ---
        grad_manifold_theta = inv_g11 * df_dtheta
        grad_manifold_phi = inv_g22 * df_dphi
        riemannian_norm_sq = (g_11 * (grad_manifold_theta ** 2)) + (g_22 * (grad_manifold_phi ** 2))

        # --- Christoffel Symbols of the Second Kind for Sphere S^2 ---
        # Gamma^1_22 = -sin(theta)*cos(theta)
        # Gamma^2_12 = Gamma^2_21 = cot(theta)
        gamma_1_22 = - math.sin(theta) * math.cos(theta)
        gamma_2_12 = 1.0 / math.tan(theta)

        # --- Ricci Curvature Tensor R_ij on S^2 with radius R ---
        # Scalar curvature K = 1 / R^2 => R_ij = K * g_ij
        ricci_11 = 1.0
        ricci_22 = math.sin(theta) ** 2
        scalar_curvature_r = 2.0 / (radius ** 2)

        # --- Hamilton's Ricci Flow Step: g_ij' = g_ij - 2 * dt * R_ij ---
        g11_evolved = g_11 - (2.0 * flow_dt * ricci_11)
        g22_evolved = g_22 - (2.0 * flow_dt * ricci_22)
        evolved_radius_approx = math.sqrt(max(0.0, g11_evolved))

        return {
            "manifold_point": {"theta_rad": round(theta, 4), "phi_rad": round(phi, 4), "manifold_type": "2-Sphere (S^2)"},
            "autodiff_euclidean_gradient": {
                "df_dtheta": round(df_dtheta, 6),
                "df_dphi": round(df_dphi, 6)
            },
            "riemannian_manifold_gradient": {
                "grad_M_theta": round(grad_manifold_theta, 6),
                "grad_M_phi": round(grad_manifold_phi, 6),
                "riemannian_gradient_norm": round(math.sqrt(riemannian_norm_sq), 6)
            },
            "christoffel_connections": {
                "Gamma^theta_phi_phi": round(gamma_1_22, 6),
                "Gamma^phi_theta_phi": round(gamma_2_12, 6)
            },
            "ricci_flow_evolution": {
                "initial_g_theta_theta": round(g_11, 4),
                "evolved_g_theta_theta": round(g11_evolved, 4),
                "ricci_scalar_curvature_R": round(scalar_curvature_r, 4),
                "evolved_metric_radius": round(evolved_radius_approx, 4),
                "flow_step_dt": flow_dt
            }
        }
