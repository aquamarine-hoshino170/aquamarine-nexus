import unittest
import math
from aquamarine_nexus.mathematics import BasicAlgebra, CalculusEngine
from aquamarine_nexus.geometry import EuclideanGeometry, NonEuclideanGeometry
from aquamarine_nexus.topology import PointSetTopology, AlgebraicTopology

class TestNexusCore(unittest.TestCase):
    def test_shoelace_area(self):
        poly = [(0, 0), (4, 0), (0, 3)]
        self.assertAlmostEqual(EuclideanGeometry.polygon_area_shoelace(poly), 6.0)

    def test_poincare_distance(self):
        dist = NonEuclideanGeometry.poincare_disk_distance((0, 0), (0.5, 0))
        self.assertAlmostEqual(dist, math.log(3), places=4)

    def test_valid_topology(self):
        u = {1, 2}
        t = [set(), {1, 2}, {1}]
        self.assertTrue(PointSetTopology.is_valid_topology(u, t))

    def test_euler_characteristic(self):
        res = AlgebraicTopology.euler_characteristic(8, 12, 6)
        self.assertEqual(res["euler_characteristic"], 2)
        self.assertEqual(res["orientable_genus"], 0)

if __name__ == "__main__":
    unittest.main()
