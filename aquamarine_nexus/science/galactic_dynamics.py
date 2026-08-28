import math

class GalacticDynamicsCore:
    @staticmethod
    def oort_constants_and_rotation(v_rot_km_s: float, r_radius_kpc: float, dv_dr_km_s_kpc: float) -> dict:
        """
        A = - 0.5 * ( dV/dR - V/R )
        B = - 0.5 * ( dV/dR + V/R )
        Omega = A - B = V / R
        """
        if r_radius_kpc <= 0:
            raise ValueError("Galactocentric radius must be positive.")
        
        v_over_r = v_rot_km_s / r_radius_kpc
        a_const = -0.5 * (dv_dr_km_s_kpc - v_over_r)
        b_const = -0.5 * (dv_dr_km_s_kpc + v_over_r)
        omega = a_const - b_const
        
        # Epicyclic frequency kappa = sqrt( -4 * B * (A - B) )
        kappa_sq = -4.0 * b_const * (a_const - b_const)
        kappa = math.sqrt(kappa_sq) if kappa_sq >= 0 else 0.0
        
        return {
            "radius_kpc": r_radius_kpc,
            "Oort_A_km_s_kpc": round(a_const, 4),
            "Oort_B_km_s_kpc": round(b_const, 4),
            "angular_speed_Omega_km_s_kpc": round(omega, 4),
            "epicyclic_frequency_kappa_km_s_kpc": round(kappa, 4)
        }

    @staticmethod
    def toomre_q_stability_criterion(velocity_dispersion_km_s: float, epicyclic_freq_km_s_kpc: float, surface_density_msun_pc2: float) -> dict:
        """Q = (sigma_r * kappa) / (3.36 * G * Sigma)"""
        if surface_density_msun_pc2 <= 0 or velocity_dispersion_km_s <= 0 or epicyclic_freq_km_s_kpc <= 0:
            raise ValueError("Invalid parameters.")
        
        # G in (km/s)^2 * kpc / M_sun -> G approx 4.30091e-6
        # Converting Msun/pc^2 to Msun/kpc^2 -> multiply by 1e6
        g_unit = 4.30091e-6
        sigma_kpc2 = surface_density_msun_pc2 * 1e6
        q_val = (velocity_dispersion_km_s * epicyclic_freq_km_s_kpc) / (3.36 * g_unit * sigma_kpc2)
        
        return {
            "toomre_Q_parameter": round(q_val, 4),
            "is_locally_stable_to_gravitational_collapse": q_val > 1.0
        }
