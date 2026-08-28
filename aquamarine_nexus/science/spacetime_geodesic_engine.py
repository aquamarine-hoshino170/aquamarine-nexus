import math
from typing import Dict, Any, List

class SpacetimeGeodesicCore:
    @staticmethod
    def integrate_schwarzschild_geodesic(
        black_hole_mass_m: float,
        initial_radius_r: float,
        initial_phi_rad: float,
        specific_angular_momentum_l: float,
        specific_energy_e: float,
        particle_type: str = "photon",
        d_lambda: float = 0.01,
        max_steps: int = 2000
    ) -> Dict[str, Any]:
        """
        Integrates general relativistic geodesic equations in 4D Schwarzschild spacetime:
        ds^2 = - (1 - 2M/r) dt^2 + (1 - 2M/r)^-1 dr^2 + r^2 dphi^2 (equatorial plane theta = pi/2)
        
        epsilon = 0 for Null Geodesics (Photons), epsilon = 1 for Timelike Geodesics (Massive particles)
        """
        if black_hole_mass_m <= 0 or initial_radius_r <= 2.0 * black_hole_mass_m:
            raise ValueError("Mass must be > 0 and initial radius outside event horizon (r > 2M).")

        r_s = 2.0 * black_hole_mass_m
        r_isco = 6.0 * black_hole_mass_m
        r_photon_sphere = 3.0 * black_hole_mass_m

        epsilon = 0.0 if particle_type.lower() == "photon" else 1.0

        r = initial_radius_r
        phi = initial_phi_rad
        l_ang = specific_angular_momentum_l
        e_energy = specific_energy_e

        # Initial radial velocity: (dr/dlambda)^2 = E^2 - (1 - 2M/r) * (epsilon + L^2 / r^2)
        v_eff_init = (1.0 - (r_s / r)) * (epsilon + (l_ang ** 2) / (r ** 2))
        radial_kinetic_sq = (e_energy ** 2) - v_eff_init

        if radial_kinetic_sq < 0:
            raise ValueError(f"Energy E={e_energy} is less than effective barrier V_eff={v_eff_init:.4f}. Trajectory forbidden.")

        # Infalling initial radial momentum
        p_r = - math.sqrt(radial_kinetic_sq)

        trajectory_points = []
        status = "ORBITING"

        for step in range(max_steps):
            trajectory_points.append({
                "step": step,
                "r": round(r, 5),
                "phi": round(phi, 5),
                "x": round(r * math.cos(phi), 5),
                "y": round(r * math.sin(phi), 5)
            })

            # Check Event Horizon Crossing (r <= 2M)
            if r <= r_s * 1.001:
                status = "CAPTURED_BY_EVENT_HORIZON"
                break

            # Effective Potential Derivative: dV_eff/dr
            # V_eff = (1 - 2M/r) * (epsilon + L^2/r^2)
            dv_eff_dr = (r_s / (r ** 2)) * (epsilon + (l_ang ** 2) / (r ** 2)) + (1.0 - (r_s / r)) * (- 2.0 * (l_ang ** 2) / (r ** 3))

            # Geodesic Acceleration: d^2 r / dlambda^2 = - 0.5 * dV_eff/dr
            acc_r = - 0.5 * dv_eff_dr

            # Velocity Verlet symplectic update
            p_r_half = p_r + 0.5 * d_lambda * acc_r
            r_next = r + d_lambda * p_r_half

            if r_next <= r_s:
                r = r_next
                status = "CAPTURED_BY_EVENT_HORIZON"
                break

            dv_eff_dr_next = (r_s / (r_next ** 2)) * (epsilon + (l_ang ** 2) / (r_next ** 2)) + (1.0 - (r_s / r_next)) * (- 2.0 * (l_ang ** 2) / (r_next ** 3))
            acc_r_next = - 0.5 * dv_eff_dr_next
            p_r = p_r_half + 0.5 * d_lambda * acc_r_next

            # Angular coordinate update: dphi/dlambda = L / r^2
            dphi_dlambda = l_ang / (r ** 2)
            phi += d_lambda * dphi_dlambda

            r = r_next

            # Escape to asymptotic infinity check
            if r > initial_radius_r * 3.0:
                status = "DEFLECTED_TO_INFINITY"
                break

        # Calculate final periapsis / closest approach
        min_r = min(pt["r"] for pt in trajectory_points)

        return {
            "spacetime_geometry": "Schwarzschild 4D Spacetime",
            "black_hole_parameters": {
                "mass_M": black_hole_mass_m,
                "schwarzschild_radius_r_s": round(r_s, 4),
                "photon_sphere_radius_r_ph": round(r_photon_sphere, 4),
                "isco_radius": round(r_isco, 4)
            },
            "particle_properties": {
                "type": particle_type,
                "null_timelike_epsilon": epsilon,
                "specific_energy_E": e_energy,
                "specific_angular_momentum_L": l_ang
            },
            "geodesic_summary": {
                "total_integration_steps": len(trajectory_points),
                "closest_approach_radius_r_min": round(min_r, 4),
                "final_radial_coordinate": round(r, 4),
                "final_angular_deflection_deg": round(math.degrees(phi - initial_phi_rad), 2),
                "trajectory_fate": status
            }
        }
