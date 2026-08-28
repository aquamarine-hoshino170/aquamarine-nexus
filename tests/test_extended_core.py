import unittest
import math
from aquamarine_nexus.science import ClassicalMechanics, RelativisticPhysics
from aquamarine_nexus.biology import AllostericKinetics, PopulationGenetics
from aquamarine_nexus.chemistry import QuantumChemistry, ReactionEquilibrium

class TestExtendedNexus(unittest.TestCase):
    def test_escape_velocity(self):
        # Earth: M = 5.972e24 kg, R = 6.371e6 m -> ~11186 m/s
        v_esc = ClassicalMechanics.gravitational_escape_velocity(5.972e24, 6.371e6)
        self.assertAlmostEqual(v_esc, 11186.0, delta=100.0)

    def test_four_momentum(self):
        res = RelativisticPhysics.four_momentum_invariant(1.0, 0.6 * 299792458.0)
        self.assertAlmostEqual(res["gamma"], 1.25, places=2)

    def test_mwc_allosteric(self):
        res = AllostericKinetics.mwc_allosteric_fraction(substrate=2.0)
        self.assertTrue(0.0 <= res["fractional_saturation"] <= 1.0)

    def test_slater_zeff(self):
        res = QuantumChemistry.slaters_effective_nuclear_charge(6, "2p") # Carbon 2p
        self.assertTrue(res["Z_effective"] > 0)

if __name__ == "__main__":
    unittest.main()
