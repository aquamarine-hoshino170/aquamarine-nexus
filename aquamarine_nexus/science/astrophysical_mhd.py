import math

class AstrophysicalMHDCore:
    MU_0 = 1.25663706212e-6
    G_CONST = 6.67430e-11

    @staticmethod
    def magnetic_energy_density(b_field_tesla: float) -> dict:
        """u_B = B^2 / (2 * mu_0)"""
        if b_field_tesla < 0:
            raise ValueError("B field magnitude must be non-negative.")
        u_b = (b_field_tesla ** 2) / (2.0 * AstrophysicalMHDCore.MU_0)
        return {"b_field_Tesla": b_field_tesla, "magnetic_energy_density_J_m3": f"{u_b:.6e}"}

    @staticmethod
    def chandrasekhar_fermi_virial_equilibrium(kinetic_energy_t: float, thermal_energy_u: float, magnetic_energy_m: float, gravitational_potential_w: float) -> dict:
        """2T + 2U + M + W = 0 (Tensor Virial Equilibrium)"""
        virial_sum = 2.0 * kinetic_energy_t + 2.0 * thermal_energy_u + magnetic_energy_m + gravitational_potential_w
        return {
            "kinetic_2T": 2.0 * kinetic_energy_t,
            "thermal_2U": 2.0 * thermal_energy_u,
            "magnetic_M": magnetic_energy_m,
            "gravitational_W": gravitational_potential_w,
            "virial_residual": round(virial_sum, 6),
            "is_dynamically_stable": abs(virial_sum) < 1e-5
        }
