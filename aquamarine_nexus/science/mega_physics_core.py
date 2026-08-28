import math

class MegaPhysicsCore:
    C_LIGHT = 299792458.0
    H_BAR = 1.054571817e-34
    K_BOLTZ = 1.380649e-23
    U_AMU_KG = 1.66053906660e-27

    @staticmethod
    def carnot_heat_engine_efficiency(t_hot_k: float, t_cold_k: float) -> dict:
        """eta = 1 - (T_cold / T_hot)"""
        if t_cold_k <= 0 or t_hot_k <= t_cold_k:
            raise ValueError("Temperatures must be positive and T_hot > T_cold.")
        eta = 1.0 - (t_cold_k / t_hot_k)
        return {
            "T_hot_K": t_hot_k,
            "T_cold_K": t_cold_k,
            "carnot_efficiency": round(eta, 6),
            "efficiency_percentage": round(eta * 100.0, 2)
        }

    @staticmethod
    def bethe_weizsacker_semi_empirical_mass(a_mass_number: int, z_atomic_number: int) -> dict:
        """B(A, Z) = a_v*A - a_s*A^(2/3) - a_c*Z^2/A^(1/3) - a_sym*(A - 2Z)^2/A + delta(A, Z)"""
        if a_mass_number <= 0 or z_atomic_number <= 0 or z_atomic_number > a_mass_number:
            raise ValueError("Invalid nucleon count.")
            
        a, z = a_mass_number, z_atomic_number
        n = a - z
        av, asurf, ac, asym, ap = 15.75, 17.8, 0.711, 23.7, 11.18
        
        # Pairing term delta
        if a % 2 != 0: delta = 0.0
        elif z % 2 == 0: delta = ap / (a ** 0.5)
        else: delta = - ap / (a ** 0.5)
        
        binding_energy_mev = (av * a) - (asurf * (a ** (2.0 / 3.0))) - (ac * (z ** 2) / (a ** (1.0 / 3.0))) - (asym * ((a - 2 * z) ** 2) / a) + delta
        binding_per_nucleon = binding_energy_mev / a
        
        return {
            "mass_number_A": a,
            "atomic_number_Z": z,
            "total_binding_energy_MeV": round(binding_energy_mev, 4),
            "binding_energy_per_nucleon_MeV": round(binding_per_nucleon, 4)
        }

    @staticmethod
    def richardson_dushman_thermionic_current(temp_k: float, work_function_ev: float, richardsons_constant_a: float = 1.20173e6) -> dict:
        """J = A * T^2 * exp(-Phi / (k_B * T))"""
        if temp_k <= 0 or work_function_ev <= 0: raise ValueError("Invalid inputs.")
        e_charge = 1.602176634e-19
        kb = MegaPhysicsCore.K_BOLTZ
        phi_joules = work_function_ev * e_charge
        
        exponent = - phi_joules / (kb * temp_k)
        j_current = richardsons_constant_a * (temp_k ** 2) * math.exp(exponent) if exponent > -700 else 0.0
        
        return {
            "temperature_K": temp_k,
            "work_function_eV": work_function_ev,
            "emission_current_density_A_m2": f"{j_current:.6e}"
        }
