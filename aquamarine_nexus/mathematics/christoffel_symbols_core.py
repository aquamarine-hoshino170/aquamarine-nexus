class ChristoffelSymbolsCore:
    @staticmethod
    def polar_coordinates_christoffel(radius_r: float) -> dict:
        """Gamma^r_{theta theta} = -r, Gamma^{theta}_{r theta} = Gamma^{theta}_{theta r} = 1/r for metric ds^2 = dr^2 + r^2 dtheta^2"""
        if radius_r <= 0:
            raise ValueError("Radius r must be strictly positive to avoid coordinate singularity.")
            
        gamma_r_thetatheta = -radius_r
        gamma_theta_rtheta = 1.0 / radius_r
        
        return {
            "radius_r": radius_r,
            "Gamma^r_{theta,theta}": round(gamma_r_thetatheta, 6),
            "Gamma^{theta}_{r,theta}": round(gamma_theta_rtheta, 6),
            "Gamma^{theta}_{theta,r}": round(gamma_theta_rtheta, 6),
            "all_other_components": 0.0
        }
