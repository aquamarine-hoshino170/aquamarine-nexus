import math

class MembraneBiophysicsCore:
    R_GAS = 8.314462618
    F_FARADAY = 96485.33212
    T_PHYSIO = 310.15

    @staticmethod
    def nernst_equilibrium_potential(valence_z: int, c_outside_mm: float, c_inside_mm: float, temp_k: float = 310.15) -> dict:
        """E = (R * T) / (z * F) * ln([C]_out / [C]_in)"""
        if valence_z == 0 or c_outside_mm <= 0 or c_inside_mm <= 0:
            raise ValueError("Invalid concentration or valence.")
        e_volts = ((MembraneBiophysicsCore.R_GAS * temp_k) / (valence_z * MembraneBiophysicsCore.F_FARADAY)) * math.log(c_outside_mm / c_inside_mm)
        return {"valence_z": valence_z, "equilibrium_potential_mV": round(e_volts * 1000.0, 3)}

    @staticmethod
    def goldman_hodgkin_katz_voltage(p_k: float, k_out: float, k_in: float, p_na: float, na_out: float, na_in: float, p_cl: float, cl_out: float, cl_in: float, temp_k: float = 310.15) -> dict:
        """V_m = (RT/F) * ln( (P_K[K]o + P_Na[Na]o + P_Cl[Cl]i) / (P_K[K]i + P_Na[Na]i + P_Cl[Cl]o) )"""
        numerator = p_k * k_out + p_na * na_out + p_cl * cl_in
        denominator = p_k * k_in + p_na * na_in + p_cl * cl_out
        if numerator <= 0 or denominator <= 0:
            raise ValueError("Invalid Goldman parameters.")
        v_m = ((MembraneBiophysicsCore.R_GAS * temp_k) / MembraneBiophysicsCore.F_FARADAY) * math.log(numerator / denominator)
        return {"membrane_potential_mV": round(v_m * 1000.0, 3)}
