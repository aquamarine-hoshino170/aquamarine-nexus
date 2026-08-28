import math

class PhaseTransitionsCore:
    K_BOLTZ = 1.380649e-23

    @staticmethod
    def ising_1d_partition_function(num_spins_n: int, coupling_j: float, external_field_h: float, temp_k: float) -> dict:
        """Z_N = lambda_plus^N + lambda_minus^N via Transfer Matrix method"""
        if temp_k <= 0 or num_spins_n <= 0: raise ValueError("Invalid parameters.")
        beta = 1.0 / (PhaseTransitionsCore.K_BOLTZ * temp_k)
        k = beta * coupling_j
        b = beta * external_field_h
        
        disc = math.sinh(b)**2 + math.exp(-4.0 * k)
        lambda_plus = math.exp(k) * math.cosh(b) + math.sqrt(math.exp(2.0*k) * (math.cosh(b)**2) - 2.0 * math.sinh(2.0*k)) if disc < 0 else math.exp(k) * math.cosh(b) + math.sqrt(math.exp(2.0*k) * (math.sinh(b)**2) + math.exp(-2.0*k))
        free_energy_f = - (1.0 / beta) * math.log(lambda_plus)
        return {"num_spins": num_spins_n, "beta": f"{beta:.6e}", "free_energy_per_spin_J": f"{free_energy_f:.6e}"}

    @staticmethod
    def curie_weiss_magnetization(coupling_z_j: float, temp_k: float, max_iter: int = 100) -> dict:
        """Self-consistent mean-field equation: m = tanh( (z*J / k_B*T) * m )"""
        if temp_k <= 0 or coupling_z_j <= 0: raise ValueError("Invalid parameters.")
        tc = coupling_z_j / PhaseTransitionsCore.K_BOLTZ
        if temp_k >= tc:
            return {"Curie_Temp_K": round(tc, 2), "spontaneous_magnetization_m": 0.0, "state": "Paramagnetic"}
        
        m = 0.5
        for _ in range(max_iter):
            m = math.tanh((tc / temp_k) * m)
        return {"Curie_Temp_K": round(tc, 2), "spontaneous_magnetization_m": round(m, 6), "state": "Ferromagnetic"}
