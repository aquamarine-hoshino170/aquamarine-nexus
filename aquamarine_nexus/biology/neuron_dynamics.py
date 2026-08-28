class FitzHughNagumoNeuronCore:
    """Biophysical Neuron Action Potential & Spiking Dynamics (FitzHugh-Nagumo Model)"""

    @staticmethod
    def neuron_spike_step(v: float, w: float, i_ext: float = 0.5, a: float = 0.7, b: float = 0.8, tau: float = 12.5, dt: float = 0.1) -> dict:
        """
        Integrates membrane voltage (v) and recovery variable (w):
        dv/dt = v - (v^3)/3 - w + I_ext
        dw/dt = (v + a - b*w) / tau
        """
        dv = v - ((v ** 3) / 3.0) - w + i_ext
        dw = (v + a - b * w) / tau

        v_next = v + dv * dt
        w_next = w + dw * dt

        return {
            "v_membrane_voltage": round(v_next, 6),
            "w_recovery_variable": round(w_next, 6),
            "is_spiking": v_next > 1.0
        }
