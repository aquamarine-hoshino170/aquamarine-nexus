import math

class CasimirVacuumPhysicsCore:
    H_BAR = 1.054571817e-34
    C_LIGHT = 299792458.0

    @staticmethod
    def casimir_force_parallel_plates(plate_separation_m: float, plate_area_m2: float = 1.0) -> dict:
        """F / A = - (pi^2 * hbar * c) / (240 * d^4)"""
        if plate_separation_m <= 0 or plate_area_m2 <= 0:
            raise ValueError("Plate separation and area must be strictly positive.")
            
        hbar = CasimirVacuumPhysicsCore.H_BAR
        c = CasimirVacuumPhysicsCore.C_LIGHT
        
        pressure = (math.pi ** 2 * hbar * c) / (240.0 * (plate_separation_m ** 4))
        total_force = pressure * plate_area_m2
        
        return {
            "separation_nm": round(plate_separation_m * 1e9, 3),
            "plate_area_m2": plate_area_m2,
            "casimir_pressure_Pa": f"{-pressure:.6e}",
            "casimir_force_N": f"{-total_force:.6e}",
            "nature": "Attractive Quantum Vacuum Pressure"
        }
