import math

class PlasmaSolitonsCore:
    @staticmethod
    def ion_acoustic_soliton_velocity(amplitude_delta_n: float, sound_speed_c_s: float) -> dict:
        """v_soliton = c_s * (1 + delta_n / (3 * n_0)) for small amplitude KdV solitons"""
        if sound_speed_c_s <= 0 or amplitude_delta_n < 0:
            raise ValueError("Parameters must be positive.")
        mach_number = 1.0 + (amplitude_delta_n / 3.0)
        soliton_v = sound_speed_c_s * mach_number
        return {
            "soliton_mach_number": round(mach_number, 6),
            "soliton_velocity_m_s": round(soliton_v, 4)
        }

    @staticmethod
    def bohm_sheath_criterion(electron_temp_ev: float, ion_mass_kg: float) -> dict:
        """u_bohm = sqrt( (k_B * T_e) / m_i )"""
        if electron_temp_ev <= 0 or ion_mass_kg <= 0:
            raise ValueError("Invalid plasma temperature or ion mass.")
        e_charge = 1.602176634e-19
        v_bohm = math.sqrt((electron_temp_ev * e_charge) / ion_mass_kg)
        return {
            "electron_temp_eV": electron_temp_ev,
            "bohm_velocity_m_s": round(v_bohm, 2)
        }
