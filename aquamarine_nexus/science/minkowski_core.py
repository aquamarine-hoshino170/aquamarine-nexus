import math

class MinkowskiSpacetimeCore:
    """Special Relativity 4-Vectors & Invariant Metric Tensor (- + + +)"""

    C_LIGHT = 299792458.0

    @staticmethod
    def spacetime_interval(dt_s: float, dx_m: float, dy_m: float, dz_m: float) -> dict:
        """
        Minkowski invariant interval:
        ds^2 = -(c * dt)^2 + dx^2 + dy^2 + dz^2
        """
        c = MinkowskiSpacetimeCore.C_LIGHT
        c_dt_sq = (c * dt_s)**2
        spatial_sq = dx_m**2 + dy_m**2 + dz_m**2
        ds_sq = -c_dt_sq + spatial_sq
        
        if ds_sq < 0:
            nature = "Timelike (Causally Connected)"
            proper_time = math.sqrt(-ds_sq) / c
        elif ds_sq > 0:
            nature = "Spacelike (Acausal Separation)"
            proper_time = None
        else:
            nature = "Null / Lightlike (Photon Trajectory)"
            proper_time = 0.0

        return {
            "ds_squared_m2": f"{ds_sq:.4e}",
            "interval_nature": nature,
            "proper_time_seconds": f"{proper_time:.6e}" if proper_time is not None else "Undefined"
        }

    @staticmethod
    def relativistic_invariant_mass(total_energy_joules: float, px: float, py: float, pz: float) -> dict:
        """
        Computes invariant rest mass:
        m0^2 * c^4 = E^2 - (p_x^2 + p_y^2 + p_z^2) * c^2
        """
        c = MinkowskiSpacetimeCore.C_LIGHT
        p_sq = px**2 + py**2 + pz**2
        p_c_sq = p_sq * (c**2)
        inv_sq = total_energy_joules**2 - p_c_sq
        
        if inv_sq < 0:
            raise ValueError("Unphysical state: p*c exceeds total energy E.")
            
        m0_kg = math.sqrt(inv_sq) / (c**2)
        return {
            "invariant_rest_mass_kg": f"{m0_kg:.6e}",
            "rest_energy_eV": f"{(m0_kg * (c**2)) / 1.602176634e-19:.4e}"
        }
