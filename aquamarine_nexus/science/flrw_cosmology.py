import math

class FLRWCosmologyCore:
    """Friedmann-Lemaître-Robertson-Walker (FLRW) Spacetime Dynamics"""

    @staticmethod
    def hubble_parameter_z(redshift_z: float, h0_kms_mpc: float = 70.0, 
                           omega_m: float = 0.3, omega_lambda: float = 0.7, 
                           omega_r: float = 8.4e-5) -> dict:
        """
        Calculates Hubble parameter H(z) in Lambda-CDM Cosmology:
        H(z) = H0 * sqrt( Omega_r*(1+z)^4 + Omega_m*(1+z)^3 + Omega_k*(1+z)^2 + Omega_Lambda )
        where Omega_k = 1 - (Omega_r + Omega_m + Omega_Lambda)
        """
        if redshift_z < -1.0:
            raise ValueError("Redshift z must be >= -1.0.")

        zp1 = 1.0 + redshift_z
        omega_k = 1.0 - (omega_r + omega_m + omega_lambda)

        e_z_sq = (omega_r * (zp1 ** 4) 
                  + omega_m * (zp1 ** 3) 
                  + omega_k * (zp1 ** 2) 
                  + omega_lambda)

        if e_z_sq <= 0:
            raise ValueError("Unphysical cosmological parameters resulting in imaginary H(z).")

        e_z = math.sqrt(e_z_sq)
        h_z = h0_kms_mpc * e_z

        # Deceleration parameter q(z)
        # q = (Omega_r*(1+z)^4 + 0.5*Omega_m*(1+z)^3 - Omega_Lambda) / E(z)^2
        q_z = (omega_r * (zp1 ** 4) + 0.5 * omega_m * (zp1 ** 3) - omega_lambda) / e_z_sq

        return {
            "redshift_z": redshift_z,
            "H_z_kms_Mpc": round(h_z, 4),
            "scale_factor_a": round(1.0 / zp1, 6),
            "deceleration_q_z": round(q_z, 5),
            "is_accelerating": q_z < 0
        }
