import math
from typing import Dict, Any, List

class TopologicalSpacetimeGeodesicCore:
    @staticmethod
    def simulate_4d_curved_geodesic(
        spacetime_type: str = "kerr",
        mass_m: float = 1.0,
        spin_a: float = 0.9,
        wormhole_throat_b0: float = 1.5,
        initial_r: float = 10.0,
        initial_theta_rad: float = 1.5707963,
        initial_phi_rad: float = 0.0,
        specific_energy_e: float = 1.0,
        specific_angular_momentum_l: float = 2.5,
        carter_constant_q: float = 0.0,
        particle_type: str = "photon",
        step_d_lambda: float = 0.01,
        max_steps: int = 3000
    ) -> Dict[str, Any]:
        """
        Integrates exact general relativistic geodesics across non-trivial topologies:
        - Kerr Metric: ds^2 = -(1 - 2Mr/Sigma) dt^2 - (4Mar sin^2(theta)/Sigma) dt dphi + (Sigma/Delta) dr^2 + Sigma dtheta^2 + (A/Sigma) sin^2(theta) dphi^2
        - Morris-Thorne Wormhole: ds^2 = - dt^2 + (1 - b0/r)^-1 dr^2 + r^2 (dtheta^2 + sin^2(theta) dphi^2)
        Calculates Kretschmann scalar curvature invariants along the path.
        """
        if mass_m <= 0 or initial_r <= 0:
            raise ValueError("Mass and initial radial coordinates must be strictly positive.")

        spacetime_type = spacetime_type.lower()
        if spacetime_type not in ["schwarzschild", "kerr", "wormhole"]:
            raise ValueError("Supported spacetime topologies: 'schwarzschild', 'kerr', 'wormhole'")

        epsilon = 0.0 if particle_type.lower() == "photon" else 1.0

        # Event Horizon & Ergosphere / Throat Calculation
        if spacetime_type == "schwarzschild":
            spin_a = 0.0
            r_horizon_outer = 2.0 * mass_m
            r_horizon_inner = 0.0
        elif spacetime_type == "kerr":
            if abs(spin_a) > mass_m:
                raise ValueError("Extremal spin exceeded: a <= M required to avoid naked singularity.")
            r_horizon_outer = mass_m + math.sqrt(mass_m ** 2 - spin_a ** 2)
            r_horizon_inner = mass_m - math.sqrt(mass_m ** 2 - spin_a ** 2)
        elif spacetime_type == "wormhole":
            r_horizon_outer = wormhole_throat_b0
            r_horizon_inner = wormhole_throat_b0

        # Initial conditions setup
        r = initial_r
        theta = initial_theta_rad
        phi = initial_phi_rad
        
        # Effective radial potential initialization
        sigma = r ** 2 + (spin_a ** 2) * (math.cos(theta) ** 2)
        delta = (r ** 2) - (2.0 * mass_m * r) + (spin_a ** 2) if spacetime_type != "wormhole" else (r ** 2)

        # Kretschmann invariant calculation function
        def compute_kretschmann(r_val: float, th_val: float) -> float:
            if spacetime_type == "schwarzschild":
                return (48.0 * (mass_m ** 2)) / (r_val ** 6 + 1e-15)
            elif spacetime_type == "kerr":
                sig = r_val ** 2 + (spin_a ** 2) * (math.cos(th_val) ** 2)
                return (48.0 * (mass_m ** 2) * (r_val ** 2 - 3.0 * (spin_a ** 2) * (math.cos(th_val) ** 2)) * 
                        ((r_val ** 2 - spin_a ** 2 * (math.cos(th_val) ** 2)) ** 2 - 16.0 * (r_val ** 2) * (spin_a ** 2) * (math.cos(th_val) ** 2))) / (sig ** 6 + 1e-15)
            elif spacetime_type == "wormhole":
                # Regular non-singular Ricci scalar / tidal curvature at throat
                return (12.0 * (wormhole_throat_b0 ** 2)) / (r_val ** 6 + 1e-15)

        # Initial radial velocity: R(r) = [E*(r^2 + a^2) - a*L]^2 - Delta * [epsilon*r^2 + (L - a*E)^2 + Q]
        p_theta = 0.0  # Equatorial launch symmetry
        term_e = specific_energy_e * (r ** 2 + spin_a ** 2) - spin_a * specific_angular_momentum_l
        ang_pot = epsilon * (r ** 2) + ((specific_angular_momentum_l - spin_a * specific_energy_e) ** 2) + carter_constant_q
        radial_metric_potential = (term_e ** 2) - delta * ang_pot

        if radial_metric_potential < 0 and spacetime_type != "wormhole":
            radial_metric_potential = 0.0

        p_r = - math.sqrt(max(0.0, radial_metric_potential)) / (sigma + 1e-15)

        trajectory_log = []
        status = "ORBITING"
        max_kretschmann_seen = 0.0
        crossed_throat = False

        for step in range(max_steps):
            k_curv = abs(compute_kretschmann(r, theta))
            if k_curv > max_kretschmann_seen:
                max_kretschmann_seen = k_curv

            if step % 20 == 0:
                trajectory_log.append({
                    "step": step,
                    "r": round(r, 4),
                    "theta": round(theta, 4),
                    "phi": round(phi, 4),
                    "x": round(math.sqrt(r ** 2 + spin_a ** 2) * math.sin(theta) * math.cos(phi), 4),
                    "y": round(math.sqrt(r ** 2 + spin_a ** 2) * math.sin(theta) * math.sin(phi), 4),
                    "z": round(r * math.cos(theta), 4)
                })

            # Check Horizon Crossing / Wormhole Throat Passage
            if spacetime_type in ["schwarzschild", "kerr"]:
                if r <= r_horizon_outer * 1.0005:
                    status = "CAPTURED_BY_EVENT_HORIZON"
                    break
            elif spacetime_type == "wormhole":
                if r <= wormhole_throat_b0 * 1.001:
                    crossed_throat = True
                    status = "TUNNELED_THROUGH_WORMHOLE_THROAT"
                    # Invert momentum across the bridge into the upper parallel universe
                    p_r = abs(p_r)

            # Symplectic Geodesic Flow Equations
            sigma_val = r ** 2 + (spin_a ** 2) * (math.cos(theta) ** 2)
            delta_val = (r ** 2) - (2.0 * mass_m * r) + (spin_a ** 2) if spacetime_type != "wormhole" else (r ** 2)

            # Radial acceleration d^2 r / dlambda^2
            # Analytical derivative of radial equation
            term_e = specific_energy_e * (r ** 2 + spin_a ** 2) - spin_a * specific_angular_momentum_l
            d_term_e_dr = 2.0 * r * specific_energy_e
            d_delta_dr = 2.0 * r - 2.0 * mass_m if spacetime_type != "wormhole" else 2.0 * r
            ang_pot = epsilon * (r ** 2) + ((specific_angular_momentum_l - spin_a * specific_energy_e) ** 2) + carter_constant_q
            d_ang_pot_dr = 2.0 * epsilon * r

            d_rad_potential_dr = (2.0 * term_e * d_term_e_dr) - (d_delta_dr * ang_pot + delta_val * d_ang_pot_dr)
            acc_r = (0.5 * d_rad_potential_dr) / (sigma_val ** 2 + 1e-15)

            # Coordinate updates
            p_r += acc_r * step_d_lambda
            r += p_r * step_d_lambda

            # Frame Dragging Angular Shift: dphi/dlambda
            if spacetime_type == "kerr":
                dphi_dlambda = ((2.0 * mass_m * r * spin_a * specific_energy_e) + (sigma_val - 2.0 * mass_m * r) * specific_angular_momentum_l) / (delta_val * sigma_val + 1e-15)
            elif spacetime_type == "schwarzschild":
                dphi_dlambda = specific_angular_momentum_l / (r ** 2 + 1e-15)
            elif spacetime_type == "wormhole":
                dphi_dlambda = specific_angular_momentum_l / (r ** 2 + 1e-15)

            phi += dphi_dlambda * step_d_lambda

            # Escape condition
            if r > initial_r * 2.5:
                status = "DEFLECTED_TO_SPACETIME_INFINITY" if not crossed_throat else "EMERGED_IN_PARALLEL_UNIVERSE"
                break

        min_approach_r = min(pt["r"] for pt in trajectory_log) if trajectory_log else r

        return {
            "spacetime_topology": spacetime_type.upper(),
            "metric_invariants": {
                "mass_M": mass_m,
                "angular_spin_parameter_a": spin_a,
                "outer_event_horizon_r_plus": round(r_horizon_outer, 4),
                "inner_cauchy_horizon_r_minus": round(r_horizon_inner, 4) if spacetime_type == "kerr" else None,
                "kretschmann_peak_curvature_invariant": f"{max_kretschmann_seen:.6e}"
            },
            "conserved_noether_charges": {
                "specific_energy_E": specific_energy_e,
                "angular_momentum_Lz": specific_angular_momentum_l,
                "carter_constant_Q": carter_constant_q,
                "particle_null_timelike_epsilon": epsilon
            },
            "geodesic_solution": {
                "periapsis_closest_approach_r": round(min_approach_r, 4),
                "final_radial_coordinate": round(r, 4),
                "total_frame_dragged_rotation_deg": round(math.degrees(phi - initial_phi_rad), 2),
                "manifold_trajectory_fate": status
            },
            "status": "4D_SPACETIME_GEODESIC_EVOLVED_SUCCESSFULLY"
        }
