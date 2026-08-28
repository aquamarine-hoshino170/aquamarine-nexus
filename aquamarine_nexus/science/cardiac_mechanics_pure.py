class CardiacMechanicsPureCore:
    @staticmethod
    def stroke_work_and_efficiency(end_diastolic_vol_ml: float, end_systolic_vol_ml: float, mean_arterial_pressure_mmhg: float) -> dict:
        """Stroke Volume = EDV - ESV, Stroke Work approx SV * MAP * conversion_factor"""
        if end_diastolic_vol_ml <= end_systolic_vol_ml or end_systolic_vol_ml <= 0 or mean_arterial_pressure_mmhg <= 0:
            raise ValueError("EDV must be strictly greater than ESV and pressures positive.")
        
        stroke_vol_ml = end_diastolic_vol_ml - end_systolic_vol_ml
        ejection_fraction = (stroke_vol_ml / end_diastolic_vol_ml) * 100.0
        
        # 1 mmHg * mL = 1.33322e-4 Joules
        stroke_work_joules = stroke_vol_ml * mean_arterial_pressure_mmhg * 1.33322e-4
        
        return {
            "end_diastolic_volume_mL": end_diastolic_vol_ml,
            "end_systolic_volume_mL": end_systolic_vol_ml,
            "stroke_volume_mL": round(stroke_vol_ml, 2),
            "ejection_fraction_percent": round(ejection_fraction, 2),
            "stroke_work_Joules": round(stroke_work_joules, 4),
            "ventricular_state": "Normal Function" if ejection_fraction >= 50.0 else "Reduced Ejection Fraction"
        }

    @staticmethod
    def frank_starling_preload_recruitment(resting_sarcomere_length_um: float, max_isometric_tension_kpa: float = 120.0) -> dict:
        """Normalized active force based on optimal actin-myosin overlap (L_opt approx 2.0 - 2.2 um)"""
        if resting_sarcomere_length_um <= 1.5 or resting_sarcomere_length_um >= 3.6:
            return {"sarcomere_length_um": resting_sarcomere_length_um, "active_tension_fraction": 0.0, "tension_kPa": 0.0}
        
        if resting_sarcomere_length_um < 2.0:
            fraction = (resting_sarcomere_length_um - 1.5) / 0.5
        elif resting_sarcomere_length_um <= 2.2:
            fraction = 1.0
        else:
            fraction = (3.6 - resting_sarcomere_length_um) / 1.4
            
        tension = fraction * max_isometric_tension_kpa
        return {
            "sarcomere_length_um": resting_sarcomere_length_um,
            "active_force_fraction": round(fraction, 4),
            "active_tension_kPa": round(tension, 3)
        }
