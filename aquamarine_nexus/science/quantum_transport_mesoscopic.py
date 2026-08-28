class QuantumTransportMesoscopicCore:
    E_CHARGE = 1.602176634e-19
    H_PLANCK = 6.62607015e-34

    @staticmethod
    def landauer_conductance(transmission_probabilities: list) -> dict:
        """G = (2 * e^2 / h) * sum( T_n )"""
        if not transmission_probabilities or any(t < 0 or t > 1 for t in transmission_probabilities):
            raise ValueError("Transmission probabilities must be in range [0, 1].")
        g0 = (2.0 * (QuantumTransportMesoscopicCore.E_CHARGE ** 2)) / QuantumTransportMesoscopicCore.H_PLANCK
        trans_sum = sum(transmission_probabilities)
        g_conductance = g0 * trans_sum
        return {
            "conductance_quantum_G0_Siemens": f"{g0:.6e}",
            "channels_open": len(transmission_probabilities),
            "conductance_Siemens": f"{g_conductance:.6e}",
            "conductance_G0_units": round(trans_sum, 4)
        }

    @staticmethod
    def shot_noise_fano_factor(transmission_probabilities: list) -> dict:
        """F = sum( T_n * (1 - T_n) ) / sum( T_n )"""
        if not transmission_probabilities or sum(transmission_probabilities) == 0:
            raise ValueError("At least one non-zero channel required.")
        t_sum = sum(transmission_probabilities)
        f_num = sum(t * (1.0 - t) for t in transmission_probabilities)
        fano = f_num / t_sum
        return {
            "fano_factor_F": round(fano, 6),
            "is_poissonian": round(fano, 4) == 1.0,
            "is_noiseless": round(fano, 4) == 0.0
        }
