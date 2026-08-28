import math
from typing import Dict, Any, List

class DrugLikenessFilterEngine:
    """
    Pure-Python deterministic drug-likeness & physicochemical filter suite.
    Zero third-party chemistry dependencies.
    """

    @staticmethod
    def evaluate_lipinski_rule_of_five(mw: float, logp: float, hbd: int, hba: int) -> Dict[str, Any]:
        """
        Lipinski's Rule of 5:
        - Molecular Weight < 500 Da
        - logP <= 5.0
        - HBD (Hydrogen Bond Donors: -OH, -NH) <= 5
        - HBA (Hydrogen Bond Acceptors: O, N) <= 10
        """
        violations = []
        if mw >= 500.0:
            violations.append(f"Molecular Weight ({mw} Da >= 500 Da)")
        if logp > 5.0:
            violations.append(f"Lipophilicity logP ({logp} > 5.0)")
        if hbd > 5:
            violations.append(f"H-Bond Donors ({hbd} > 5)")
        if hba > 10:
            violations.append(f"H-Bond Acceptors ({hba} > 10)")

        is_accepted = len(violations) <= 1  # Standard criterion allows at most 1 violation

        return {
            "filter_name": "Lipinski_Rule_of_5",
            "violations_count": len(violations),
            "violation_details": violations,
            "passed": is_accepted,
            "orally_bioavailable": is_accepted
        }

    @staticmethod
    def evaluate_veber_rule(rotatable_bonds: int, tpsa: float) -> Dict[str, Any]:
        """
        Veber's Rule for Oral Bioavailability:
        - Rotatable Bonds <= 10 (Flexibility constraint)
        - TPSA (Topological Polar Surface Area) <= 140.0 Å²
        """
        violations = []
        if rotatable_bonds > 10:
            violations.append(f"Rotatable Bonds ({rotatable_bonds} > 10)")
        if tpsa > 140.0:
            violations.append(f"Polar Surface Area TPSA ({tpsa} Å² > 140.0 Å²)")

        return {
            "filter_name": "Veber_Rule",
            "rotatable_bonds": rotatable_bonds,
            "tpsa_angstrom_sq": tpsa,
            "violations_count": len(violations),
            "violation_details": violations,
            "passed": len(violations) == 0
        }

    @staticmethod
    def evaluate_rule_of_three(mw: float, logp: float, hbd: int, hba: int, rotatable_bonds: int = 0) -> Dict[str, Any]:
        """
        Congreve's Rule of 3 (Fragment Screening):
        - Molecular Weight < 300 Da
        - logP <= 3.0
        - HBD <= 3
        - HBA <= 3
        - Rotatable Bonds <= 3
        """
        violations = []
        if mw >= 300.0:
            violations.append(f"Molecular Weight ({mw} Da >= 300 Da)")
        if logp > 3.0:
            violations.append(f"logP ({logp} > 3.0)")
        if hbd > 3:
            violations.append(f"HBD ({hbd} > 3)")
        if hba > 3:
            violations.append(f"HBA ({hba} > 3)")
        if rotatable_bonds > 3:
            violations.append(f"Rotatable Bonds ({rotatable_bonds} > 3)")

        return {
            "filter_name": "Rule_of_3_Fragment",
            "violations_count": len(violations),
            "violation_details": violations,
            "passed": len(violations) == 0
        }

    @staticmethod
    def evaluate_ghose_filter(mw: float, logp: float, molar_refractivity: float, atom_count: int) -> Dict[str, Any]:
        """
        Ghose Quantitative Filter:
        - 160 Da <= Molecular Weight <= 480 Da
        - -0.4 <= logP <= 5.6
        - 40 <= Molar Refractivity (MR) <= 130
        - 20 <= Total Atom Count <= 70
        """
        violations = []
        if not (160.0 <= mw <= 480.0):
            violations.append(f"Molecular Weight ({mw} Da not in [160, 480])")
        if not (-0.4 <= logp <= 5.6):
            violations.append(f"logP ({logp} not in [-0.4, 5.6])")
        if not (40.0 <= molar_refractivity <= 130.0):
            violations.append(f"Molar Refractivity ({molar_refractivity} not in [40, 130])")
        if not (20 <= atom_count <= 70):
            violations.append(f"Atom Count ({atom_count} not in [20, 70])")

        return {
            "filter_name": "Ghose_Filter",
            "violations_count": len(violations),
            "violation_details": violations,
            "passed": len(violations) == 0
        }

    @classmethod
    def evaluate_comprehensive_druglikeness(
        cls, 
        mw: float, 
        logp: float, 
        hbd: int, 
        hba: int, 
        rotatable_bonds: int, 
        tpsa: float, 
        molar_refractivity: float, 
        atom_count: int
    ) -> Dict[str, Any]:
        """
        Runs unified evaluation across Lipinski, Veber, Rule-of-3, and Ghose filters.
        """
        lipinski = cls.evaluate_lipinski_rule_of_five(mw, logp, hbd, hba)
        veber = cls.evaluate_veber_rule(rotatable_bonds, tpsa)
        ro3 = cls.evaluate_rule_of_three(mw, logp, hbd, hba, rotatable_bonds)
        ghose = cls.evaluate_ghose_filter(mw, logp, molar_refractivity, atom_count)

        all_passed = lipinski["passed"] and veber["passed"] and ghose["passed"]

        return {
            "molecular_profile": {
                "MW": mw, "logP": logp, "HBD": hbd, "HBA": hba,
                "Rotatable_Bonds": rotatable_bonds, "TPSA": tpsa,
                "Molar_Refractivity": molar_refractivity, "Atom_Count": atom_count
            },
            "lipinski_ro5": lipinski,
            "veber_rule": veber,
            "rule_of_3": ro3,
            "ghose_filter": ghose,
            "consensus_druglike": all_passed,
            "status": "EVALUATION_SUCCESS"
        }
