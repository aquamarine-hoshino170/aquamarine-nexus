import math

class DonnanMembraneEquilibriumCore:
    R_GAS = 8.314462618

    @staticmethod
    def donnan_ion_distribution(impermeable_polyion_conc_molar: float, polyion_charge_z: int, external_nacl_conc_molar: float, temp_k: float = 298.15) -> dict:
        """[Na+]_in * [Cl-]_in = [Na+]_out * [Cl-]_out, [Na+]_in = z*[P^z-] + [Cl-]_in"""
        if external_nacl_conc_molar <= 0 or impermeable_polyion_conc_molar <= 0 or polyion_charge_z == 0 or temp_k <= 0:
            raise ValueError("All concentrations and absolute charge must be strictly positive.")
            
        c_poly_charge = abs(polyion_charge_z) * impermeable_polyion_conc_molar
        c_out = external_nacl_conc_molar
        
        # Solving x * (x + c_poly_charge) = c_out^2 => x^2 + c_poly_charge*x - c_out^2 = 0 where x = [Cl-]_in
        disc = math.sqrt((c_poly_charge ** 2) + 4.0 * (c_out ** 2))
        cl_in = (-c_poly_charge + disc) / 2.0
        na_in = cl_in + c_poly_charge
        
        # Donnan ratio r = [Na+]_in / [Na+]_out = [Cl-]_out / [Cl-]_in
        donnan_ratio_r = na_in / c_out
        
        # Excess osmotic pressure Pi = R * T * sum(Delta C_ions)
        delta_osmolarity = (na_in + cl_in + impermeable_polyion_conc_molar) - (2.0 * c_out)
        excess_osmotic_pressure_pa = delta_osmolarity * DonnanMembraneEquilibriumCore.R_GAS * temp_k * 1000.0
        
        return {
            "internal_Na_M": round(na_in, 6),
            "internal_Cl_M": round(cl_in, 6),
            "external_Na_Cl_M": c_out,
            "donnan_ratio_r": round(donnan_ratio_r, 4),
            "excess_osmotic_pressure_Pa": round(excess_osmotic_pressure_pa, 2),
            "excess_osmotic_pressure_kPa": round(excess_osmotic_pressure_pa / 1000.0, 3)
        }
