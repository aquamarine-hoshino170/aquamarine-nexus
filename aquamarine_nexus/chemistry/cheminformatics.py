import re

class NexusCheminformatics:
    """Molecular Stoichiometry & Formula Analysis (RDKit/ChemPy Alternative)"""
    PERIODIC_TABLE = {
        'H': 1.008, 'He': 4.0026, 'Li': 6.94, 'Be': 9.0122, 'B': 10.81,
        'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
        'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.085, 'P': 30.974,
        'S': 32.06, 'Cl': 35.45, 'K': 39.098, 'Ar': 39.948, 'Ca': 40.078,
        'Fe': 55.845, 'Cu': 63.546, 'Zn': 65.38, 'Br': 79.904, 'Ag': 107.87,
        'I': 126.90, 'Au': 196.97, 'Pb': 207.2
    }

    @staticmethod
    def parse_formula(formula: str) -> dict:
        """Parses chemical formula e.g. C6H12O6, H2SO4, Fe2O3"""
        tokens = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
        counts = {}
        for elem, count in tokens:
            if elem not in NexusCheminformatics.PERIODIC_TABLE:
                raise ValueError(f"Unknown chemical element: {elem}")
            c = int(count) if count else 1
            counts[elem] = counts.get(elem, 0) + c
        return counts

    @staticmethod
    def molecular_weight(formula: str) -> dict:
        """Calculates molecular mass and mass fraction of elements"""
        counts = NexusCheminformatics.parse_formula(formula)
        total_mw = 0.0
        for elem, count in counts.items():
            total_mw += NexusCheminformatics.PERIODIC_TABLE[elem] * count
        
        mass_fractions = {
            elem: round((NexusCheminformatics.PERIODIC_TABLE[elem] * count / total_mw) * 100.0, 2)
            for elem, count in counts.items()
        }
        return {"formula": formula, "molecular_weight_g_mol": round(total_mw, 3), "mass_percentages": mass_fractions}
