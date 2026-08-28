import unittest
import math
from aquamarine_nexus.mathematics import BasicAlgebra, CalculusEngine, AdvancedAnalysis

class TestNexusMathematics(unittest.TestCase):
    def test_extended_gcd(self):
        gcd, x, y = BasicAlgebra.extended_gcd(240, 46)
        self.assertEqual(gcd, 2)
        self.assertEqual(240 * x + 46 * y, 2)

    def test_prime_factorization(self):
        factors = BasicAlgebra.prime_factorization(360)
        self.assertEqual(factors, {2: 3, 3: 2, 5: 1})

    def test_simpson_integral(self):
        val = CalculusEngine.adaptive_simpson_integral(math.sin, 0, math.pi)
        self.assertAlmostEqual(val, 2.0, places=4)

    def test_derivative(self):
        d = CalculusEngine.numerical_derivative(lambda x: x**3, 2.0)
        self.assertAlmostEqual(d, 12.0, places=3)

if __name__ == "__main__":
    unittest.main()
