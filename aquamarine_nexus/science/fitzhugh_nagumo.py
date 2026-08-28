class FitzHughNagumoCore:
    @staticmethod
    def fitzhugh_nagumo_vector_field(v_voltage: float, w_recovery: float, i_stimulus: float, a: float = 0.7, b: float = 0.8, tau: float = 12.5) -> dict:
        """
        dv/dt = v - (v^3 / 3) - w + I
        dw/dt = (v + a - b*w) / tau
        """
        dv_dt = v_voltage - ((v_voltage ** 3) / 3.0) - w_recovery + i_stimulus
        dw_dt = (v_voltage + a - (b * w_recovery)) / tau
        return {
            "voltage_v": v_voltage,
            "recovery_w": w_recovery,
            "stimulus_I": i_stimulus,
            "dv_dt": round(dv_dt, 6),
            "dw_dt": round(dw_dt, 6),
            "is_depolarizing": dv_dt > 0
        }
