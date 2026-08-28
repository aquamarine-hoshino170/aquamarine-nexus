import math

class NeuronalCableTheoryCore:
    @staticmethod
    def cable_length_and_time_constants(membrane_resistance_ohm_cm2: float, axial_resistance_ohm_cm: float, fiber_radius_cm: float, membrane_capacitance_uf_cm2: float = 1.0) -> dict:
        """lambda = sqrt( (r_m / r_a) * (a / 2) ), tau_m = r_m * c_m"""
        if membrane_resistance_ohm_cm2 <= 0 or axial_resistance_ohm_cm <= 0 or fiber_radius_cm <= 0 or membrane_capacitance_uf_cm2 <= 0:
            raise ValueError("All electrical parameters and radius must be strictly positive.")
            
        space_constant_lambda_cm = math.sqrt((membrane_resistance_ohm_cm2 * fiber_radius_cm) / (2.0 * axial_resistance_ohm_cm))
        c_m_farads = membrane_capacitance_uf_cm2 * 1e-6
        time_constant_tau_s = membrane_resistance_ohm_cm2 * c_m_farads
        
        return {
            "fiber_radius_um": round(fiber_radius_cm * 1e4, 2),
            "space_constant_lambda_mm": round(space_constant_lambda_cm * 10.0, 4),
            "membrane_time_constant_tau_ms": round(time_constant_tau_s * 1000.0, 4),
            "electrotonic_length_at_1mm": round(0.1 / space_constant_lambda_cm, 4)
        }

    @staticmethod
    def electrotonic_voltage_decay(v_soma_mv: float, distance_x_cm: float, space_constant_lambda_cm: float) -> dict:
        """V(x) = V_0 * exp(-x / lambda)"""
        if space_constant_lambda_cm <= 0 or distance_x_cm < 0:
            raise ValueError("Invalid spatial dimensions.")
        v_x = v_soma_mv * math.exp(-distance_x_cm / space_constant_lambda_cm)
        return {
            "soma_voltage_mV": v_soma_mv,
            "distance_x_mm": round(distance_x_cm * 10.0, 2),
            "voltage_at_x_mV": round(v_x, 4),
            "attenuation_percentage": round((1.0 - (v_x / v_soma_mv)) * 100.0, 2)
        }
