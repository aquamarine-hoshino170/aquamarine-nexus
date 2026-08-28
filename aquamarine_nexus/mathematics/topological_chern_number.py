import math

class TopologicalChernNumberCore:
    @staticmethod
    def discrete_chern_number_proxy(berry_flux_plaquettes: list) -> dict:
        """C = (1 / 2*pi) * sum( Berry_flux_plaquette )"""
        if not berry_flux_plaquettes:
            raise ValueError("Plaquette flux list cannot be empty.")
            
        total_flux = sum(berry_flux_plaquettes)
        chern_exact = total_flux / (2.0 * math.pi)
        chern_int = round(chern_exact)
        
        return {
            "total_plaquettes": len(berry_flux_plaquettes),
            "total_berry_flux_rad": round(total_flux, 6),
            "computed_chern_fractional": round(chern_exact, 6),
            "quantized_chern_number": chern_int,
            "topological_classification": "Trivial Band (C = 0)" if chern_int == 0 else f"Non-Trivial Quantum Hall Phase (C = {chern_int})"
        }
