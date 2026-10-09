import unittest
from fractions import Fraction as F

from paradox.collision import collide, object_speed_ratio
from paradox.limits import along_ratio, iterated, path_table
from paradox.plot import chart
from paradox.proof import check_definitions, find_contradiction


class CollisionTests(unittest.TestCase):
    def test_momentum_is_conserved_exactly(self):
        for m, M, e in ((1, 1, 1), (3, 7, F(1, 2)), (10**200, 1, 0), (2, 10**200, 1)):
            o = collide(m, M, 5, e)
            self.assertEqual(m * 5, m * o.v_force + M * o.v_object)

    def test_restitution_sets_the_separation_speed(self):
        o = collide(3, 7, 10, F(1, 2))
        self.assertEqual(o.v_object - o.v_force, F(1, 2) * 10)

    def test_elastic_loses_no_energy_sticky_loses_some(self):
        self.assertEqual(collide(3, 7, 10, 1).energy_lost, 0)
        self.assertGreater(collide(3, 7, 10, 0).energy_lost, 0)

    def test_equal_masses_elastic_swap_velocities(self):  # the Newton's cradle case
        o = collide(4, 4, 6, 1)
        self.assertEqual((o.v_force, o.v_object), (0, 6))

    def test_bad_inputs(self):
        for args in ((0, 1, 1, 1), (1, -1, 1, 1), (1, 1, 1, 2)):
            with self.assertRaises(ValueError):
                collide(*args)


class LimitTests(unittest.TestCase):
    def test_only_the_ratio_matters(self):
        values = {v for _k, v in along_ratio(F(2), 1)}
        self.assertEqual(values, {object_speed_ratio(2, 1)})  # identical at 10^0 and 10^300
        self.assertEqual(object_speed_ratio(2, 1), F(4, 3))

    def test_any_answer_between_0_and_1_plus_e(self):
        table = dict(path_table([F(1, 10**6), F(1), F(10**6)], 1))
        self.assertLess(table[F(1, 10**6)], F(1, 10**5))     # immovable side wins
        self.assertEqual(table[F(1)], 1)                      # a draw
        self.assertGreater(table[F(10**6)], F(1999, 1000))    # unstoppable side wins

    def test_iterated_limits_disagree(self):
        force_first, object_first = iterated(1)
        self.assertAlmostEqual(float(force_first), 2.0, places=12)
        self.assertAlmostEqual(float(object_first), 0.0, places=12)


class ProofTests(unittest.TestCase):
    def test_the_definitions_cannot_all_hold(self):
        self.assertIn("contradict", find_contradiction())

    def test_the_rule_checker(self):
        rules = check_definitions(F(1), F(1), F(0))  # what both objects existing would require
        self.assertEqual(rules, {"immovable (v_O = 0)": True, "unstoppable (v_F = u)": True,
                                 "no passing through (v_F <= v_O)": False})


class PlotTests(unittest.TestCase):
    def test_svg_is_well_formed_text(self):
        import xml.etree.ElementTree as ET  # parse it back: proves the hand-written XML is valid
        root = ET.fromstring(chart())
        self.assertTrue(root.tag.endswith("svg"))
        self.assertEqual(len(root.findall("{http://www.w3.org/2000/svg}polyline")), 3)


if __name__ == "__main__":
    unittest.main()
