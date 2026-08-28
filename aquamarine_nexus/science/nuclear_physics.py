import math

class NuclearPhysicsCore:
    @staticmethod
    def weizsacker_semi_empirical_mass(protons_z: int, mass_number_a: int) -> dict:
        """Bethe-Weizsäcker Liquid Drop Binding Energy Formula: B(A, Z)"""
        if protons_z <= 0 or mass_number_a <= protons_z: raise ValueError("Invalid A or Z.")
        n = mass_number_a - protons_z
        a_v, a_s, a_c, a_a = 15.75, 17.8, 0.711, 23.7
        # Pairing term delta
        if protons_z % 2 != 0 and n % 2 != 0: delta = -11.18 / (mass_number_a ** 0.5)
        elif protons_z % 2 == 0 and n % 2 == 0: delta = 11.18 / (mass_number_a ** 0.5)
        else: delta = 0.0

        b_vol = a_v * mass_number_a
        b_surf = a_s * (mass_number_a ** (2.0 / 3.0))
        b_coul = a_c * (protons_z * (protons_z - 1)) / (mass_number_a ** (1.0 / 3.0))
        b_asym = a_a * ((mass_number_a - 2 * protons_z) ** 2) / mass_number_a
        
        binding_energy_mev = b_vol - b_surf - b_coul - b_asym + delta
        binding_per_nucleon = binding_energy_mev / mass_number_a
        return {"A": mass_number_a, "Z": protons_z, "N": n, "binding_energy_MeV": round(binding_energy_mev, 4), "binding_per_nucleon_MeV": round(binding_per_nucleon, 4)}

    @staticmethod
    def radioactive_decay_activity(n0_nuclei: float, half_life_seconds: float, elapsed_time_seconds: float) -> dict:
        """A(t) = lambda * N(t) = lambda * N0 * exp(-lambda * t)"""
        if n0_nuclei <= 0 or half_life_seconds <= 0 or elapsed_time_seconds < 0: raise ValueError("Invalid inputs.")
        decay_constant = math.log(2.0) / half_life_seconds
        remaining_n = n0_nuclei * math.exp(-decay_constant * elapsed_time_seconds)
        activity_becquerel = decay_constant * remaining_n
        return {"decay_constant_inv_s": f"{decay_constant:.6e}", "remaining_nuclei": f"{remaining_n:.6e}", "activity_Bq": f"{activity_becquerel:.6e}"}

    @staticmethod
    def q_value_nuclear_reaction(masses_reactants_amu: list, masses_products_amu: list) -> dict:
        """Q = (sum(m_reactants) - sum(m_products)) * 931.494 MeV"""
        dm = sum(masses_reactants_amu) - sum(masses_products_amu)
        q_mev = dm * 931.4940954
        return {"delta_mass_amu": round(dm, 6), "Q_value_MeV": round(q_mev, 6), "is_exothermic": q_mev > 0}
