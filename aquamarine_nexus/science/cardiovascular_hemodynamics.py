import math

class CardiovascularHemodynamicsCore:
    @staticmethod
    def two_element_windkessel_decay(p_systolic: float, p_diastolic: float, total_peripheral_resistance: float, compliance_c: float, t_diastole: float) -> dict:
        """P(t) = P_sys * exp(-t / (R * C))"""
        if total_peripheral_resistance <= 0 or compliance_c <= 0 or p_systolic <= 0 or t_diastole <= 0:
            raise ValueError("Hemodynamic variables and resistance/compliance must be strictly positive.")
            
        tau_decay = total_peripheral_resistance * compliance_c
        p_t = p_systolic * math.exp(-t_diastole / tau_decay)
        mean_arterial_pressure = (2.0 * p_diastolic + p_systolic) / 3.0
        
        return {
            "systolic_pressure_mmHg": p_systolic,
            "diastolic_pressure_mmHg": p_diastolic,
            "mean_arterial_pressure_mmHg": round(mean_arterial_pressure, 2),
            "windkessel_time_constant_tau_s": round(tau_decay, 4),
            "estimated_end_diastolic_pressure_mmHg": round(p_t, 2)
        }

    @staticmethod
    def poiseuille_vascular_resistance(blood_viscosity_pa_s: float, vessel_length_m: float, vessel_radius_m: float) -> dict:
        """R_hyd = (8 * eta * L) / (pi * r^4)"""
        if blood_viscosity_pa_s <= 0 or vessel_length_m <= 0 or vessel_radius_m <= 0:
            raise ValueError("Physical dimensions and viscosity must be positive.")
            
        r_hyd = (8.0 * blood_viscosity_pa_s * vessel_length_m) / (math.pi * (vessel_radius_m ** 4))
        return {
            "vessel_length_mm": round(vessel_length_m * 1e3, 3),
            "vessel_radius_mm": round(vessel_radius_m * 1e3, 4),
            "hydraulic_resistance_Pa_s_m3": f"{r_hyd:.6e}"
        }
