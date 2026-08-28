import math

class GenomicsNexus:
    """Sequence Analysis & Biophysical Formalisms"""
    @staticmethod
    def gc_skew_profile(dna_seq: str) -> dict:
        """Computes GC-Skew = (G - C) / (G + C) for DNA strand asymmetry"""
        seq = dna_seq.upper()
        g = seq.count('G')
        c = seq.count('C')
        skew = (g - c) / (g + c) if (g + c) > 0 else 0.0
        return {"sequence_len": len(seq), "G_count": g, "C_count": c, "gc_skew": round(skew, 4)}

    @staticmethod
    def hill_langmuir_fraction(ligand_conc: float, kd: float, n_cooperativity: float = 1.0) -> dict:
        """Fractional receptor occupancy theta = [L]^n / (Kd^n + [L]^n)"""
        num = ligand_conc ** n_cooperativity
        den = (kd ** n_cooperativity) + num
        return {"fractional_occupancy": round(num / den, 5)}
