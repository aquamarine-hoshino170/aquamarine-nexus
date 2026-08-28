import math

class AcousticLevitationGorkovCore:
    @staticmethod
    def gorkov_acoustic_potential_1d(pressure_amplitude_pa: float, particle_radius_m: float, fluid_density_kg_m3: float, fluid_sound_speed_m_s: float, particle_density_kg_m3: float, particle_sound_speed_m_s: float, k_wavenumber: float, z_pos_m: float) -> dict:
        """U = V_0 * [ (f_1 / (2*rho_0*c_0^2)) * <p^2> - (3*f_2*rho_0 / 4) * <v^2> ]"""
        if particle_radius_m <= 0 or fluid_density_kg_m3 <= 0 or fluid_sound_speed_m_s <= 0 or particle_density_kg_m3 <= 0 or particle_sound_speed_m_s <= 0:
            raise ValueError("Physical parameters must be strictly positive.")
            
        v_particle = (4.0 / 3.0) * math.pi * (particle_radius_m ** 3)
        
        # Monopole and dipole compressibility/density contrast factors
        f1 = 1.0 - (fluid_density_kg_m3 * (fluid_sound_speed_m_s ** 2)) / (particle_density_kg_m3 * (particle_sound_speed_m_s ** 2))
        f2 = 2.0 * (particle_density_kg_m3 - fluid_density_kg_m3) / (2.0 * particle_density_kg_m3 + fluid_density_kg_m3)
        
        e_acoustic = (pressure_amplitude_pa ** 2) / (4.0 * fluid_density_kg_m3 * (fluid_sound_speed_m_s ** 2))
        
        # Potential profile in 1D standing wave along z
        # p(z) = P0 * cos(k*z) => <p^2> = 0.5 * P0^2 * cos^2(k*z), <v^2> = 0.5 * (P0 / rho0*c0)^2 * sin^2(k*z)
        u_z = v_particle * e_acoustic * (f1 * (math.cos(k_wavenumber * z_pos_m) ** 2) - 1.5 * f2 * (math.sin(k_wavenumber * z_pos_m) ** 2))
        
        # Acoustic force F_z = - dU/dz
        f_z = v_particle * e_acoustic * k_wavenumber * math.sin(2.0 * k_wavenumber * z_pos_m) * (f1 + 1.5 * f2)
        
        return {
            "particle_volume_m3": f"{v_particle:.6e}",
            "monopole_factor_f1": round(f1, 4),
            "dipole_factor_f2": round(f2, 4),
            "gorkov_potential_Joules": f"{u_z:.6e}",
            "acoustic_radiation_force_N": f"{f_z:.6e}"
        }
