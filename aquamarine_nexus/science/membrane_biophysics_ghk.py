import math

class MembraneBiophysicsGHKCore:
    R_GAS = 8.314462618
    F_FARADAY = 96485.33212

    @staticmethod
    def ghk_resting_membrane_potential(k_in: float, k_out: float, na_in: float, na_out: float, cl_in: float, cl_out: float, p_k: float = 1.0, p_na: float = 0.04, p_cl: float = 0.45, temp_k: float = 310.15) -> dict:
        """V_m = (R*T / F) * ln( (P_K*[K+]_out + P_Na*[Na+]_out + P_Cl*[Cl-]_in) / (P_K*[K+]_in + P_Na*[Na+]_in + P_Cl*[Cl-]_out) )"""
        if any(c <= 0 for c in [k_in, k_out, na_in, na_out, cl_in, cl_out, p_k, p_na, p_cl, temp_k]):
            raise ValueError("All ion concentrations, relative permeabilities, and temperature must be positive.")
        
        rt_over_f = (MembraneBiophysicsGHKCore.R_GAS * temp_k) / MembraneBiophysicsGHKCore.F_FARADAY
        
        num = (p_k * k_out) + (p_na * na_out) + (p_cl * cl_in)
        denom = (p_k * k_in) + (p_na * na_in) + (p_cl * cl_out)
        
        v_m_volts = rt_over_f * math.log(num / denom)
        v_m_mv = v_m_volts * 1000.0
        
        return {
            "temperature_K": temp_k,
            "membrane_potential_V": round(v_m_volts, 6),
            "membrane_potential_mV": round(v_m_mv, 2),
            "state": "Resting Polarized" if v_m_mv < -50.0 else "Depolarized/Active"
        }

    @staticmethod
    def nernst_equilibrium_potential_single_ion(conc_inside_mm: float, conc_outside_mm: float, valence_z: int, temp_k: float = 310.15) -> dict:
        """E_ion = (R*T / (z*F)) * ln([ion]_out / [ion]_in)"""
        if conc_inside_mm <= 0 or conc_outside_mm <= 0 or valence_z == 0 or temp_k <= 0:
            raise ValueError("Invalid parameters.")
        
        rt_over_zf = (MembraneBiophysicsGHKCore.R_GAS * temp_k) / (valence_z * MembraneBiophysicsGHKCore.F_FARADAY)
        e_ion_mv = rt_over_zf * math.log(conc_outside_mm / conc_inside_mm) * 1000.0
        
        return {
            "valence_z": valence_z,
            "reversal_potential_E_mV": round(e_ion_mv, 2)
        }
