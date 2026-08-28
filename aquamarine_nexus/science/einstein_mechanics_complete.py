import math

class EinsteinMechanicsCompleteCore:
    C_LIGHT = 299792458.0
    H_PLANCK = 6.62607015e-34
    K_BOLTZ = 1.380649e-23
    EV_TO_JOULE = 1.602176634e-19

    @staticmethod
    def mass_energy_equivalence(mass_kg: float) -> dict:
        """E = m * c^2"""
        if mass_kg < 0: raise ValueError("Mass must be non-negative.")
        c = EinsteinMechanicsCompleteCore.C_LIGHT
        energy_joules = mass_kg * (c ** 2)
        energy_ev = energy_joules / EinsteinMechanicsCompleteCore.EV_TO_JOULE
        return {
            "mass_kg": f"{mass_kg:.6e}",
            "energy_Joules": f"{energy_joules:.6e}",
            "energy_eV": f"{energy_ev:.6e}",
            "energy_MeV": f"{(energy_ev / 1e6):.6e}"
        }

    @staticmethod
    def photoelectric_kinetic_energy(photon_freq_hz: float, work_function_ev: float) -> dict:
        """K_max = h * nu - Phi"""
        if photon_freq_hz <= 0 or work_function_ev < 0: raise ValueError("Invalid parameters.")
        h = EinsteinMechanicsCompleteCore.H_PLANCK
        e_photon_joules = h * photon_freq_hz
        phi_joules = work_function_ev * EinsteinMechanicsCompleteCore.EV_TO_JOULE
        
        k_max_joules = e_photon_joules - phi_joules
        k_max_ev = k_max_joules / EinsteinMechanicsCompleteCore.EV_TO_JOULE
        cutoff_freq = phi_joules / h
        
        return {
            "photon_frequency_Hz": f"{photon_freq_hz:.6e}",
            "work_function_eV": work_function_ev,
            "threshold_frequency_Hz": f"{cutoff_freq:.6e}",
            "kinetic_energy_max_eV": round(max(0.0, k_max_ev), 4),
            "electron_emitted": k_max_joules > 0
        }

    @staticmethod
    def einstein_brownian_diffusion_coefficient(temp_k: float, particle_radius_m: float, dynamic_viscosity_pa_s: float) -> dict:
        """D = (k_B * T) / (6 * pi * eta * r) (Stokes-Einstein Relation)"""
        if temp_k <= 0 or particle_radius_m <= 0 or dynamic_viscosity_pa_s <= 0:
            raise ValueError("Invalid physical dimensions.")
        kb = EinsteinMechanicsCompleteCore.K_BOLTZ
        denom = 6.0 * math.pi * dynamic_viscosity_pa_s * particle_radius_m
        d_diff = (kb * temp_k) / denom
        return {
            "temperature_K": temp_k,
            "particle_radius_m": f"{particle_radius_m:.6e}",
            "diffusion_coefficient_m2_s": f"{d_diff:.6e}"
        }

    @staticmethod
    def bose_einstein_condensation_temp(particle_density_m3: float, atomic_mass_kg: float) -> dict:
        """T_c = (2 * pi * hbar^2 / (m * k_B)) * (n / zeta(3/2))^(2/3), zeta(3/2) approx 2.612"""
        if particle_density_m3 <= 0 or atomic_mass_kg <= 0:
            raise ValueError("Density and mass must be strictly positive.")
        hbar = EinsteinMechanicsCompleteCore.H_PLANCK / (2.0 * math.pi)
        kb = EinsteinMechanicsCompleteCore.K_BOLTZ
        zeta_3_2 = 2.612375
        
        prefactor = (2.0 * math.pi * (hbar ** 2)) / (atomic_mass_kg * kb)
        density_factor = (particle_density_m3 / zeta_3_2) ** (2.0 / 3.0)
        tc_kelvin = prefactor * density_factor
        return {
            "particle_density_m3": f"{particle_density_m3:.6e}",
            "atomic_mass_kg": f"{atomic_mass_kg:.6e}",
            "critical_temperature_Tc_Kelvin": f"{tc_kelvin:.6e}",
            "critical_temperature_nK": round(tc_kelvin * 1e9, 4)
        }
