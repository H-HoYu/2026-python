import importlib.util
import math
import sys
import unittest
from pathlib import Path


# 動態載入帶減號檔名的模組
MODULE_PATH = Path(__file__).with_name("UVA10221-hand.py")
SPEC = importlib.util.spec_from_file_location("uva10221_hand", MODULE_PATH)
UVA10221_HAND = importlib.util.module_from_spec(SPEC)
sys.modules["uva10221_hand"] = UVA10221_HAND
if SPEC.loader is not None:
    SPEC.loader.exec_module(UVA10221_HAND)


class TestUVA10221Hand(unittest.TestCase):
    """UVA10221 hand 版本測試"""

    def _reference(self, s, a, unit):
        r = 6440.0 + s
        if unit == "min":
            a /= 60.0
        if a > 180.0:
            a = 360.0 - a

        rad = math.radians(a)
        return r * rad, 2.0 * r * math.sin(rad / 2.0)

    def _assert_case(self, s, a, unit, expected=None):
        actual = UVA10221_HAND.solve(s, a, unit)
        if expected is None:
            expected = self._reference(s, a, unit)

        self.assertAlmostEqual(actual[0], expected[0], places=6)
        self.assertAlmostEqual(actual[1], expected[1], places=6)

    def test_01_sample_1(self):
        self._assert_case(500, 30, "deg", (3633.775503, 3592.408346))

    def test_02_sample_2(self):
        self._assert_case(700, 60, "min", (124.616509, 124.614927))

    def test_03_sample_3(self):
        self._assert_case(200, 45, "deg", (5215.043805, 5082.035982))

    def test_04_over_180(self):
        a1 = UVA10221_HAND.solve(0, 300, "deg")
        a2 = UVA10221_HAND.solve(0, 60, "deg")
        self.assertAlmostEqual(a1[0], a2[0], places=6)
        self.assertAlmostEqual(a1[1], a2[1], places=6)

    def test_05_min_to_deg(self):
        a1 = UVA10221_HAND.solve(123, 60, "min")
        a2 = UVA10221_HAND.solve(123, 1, "deg")
        self.assertAlmostEqual(a1[0], a2[0], places=6)
        self.assertAlmostEqual(a1[1], a2[1], places=6)

    def test_06_straight_angle(self):
        r = 6440.0 + 10
        self._assert_case(10, 180, "deg", (math.pi * r, 2.0 * r))


if __name__ == "__main__":
    unittest.main(verbosity=2)
