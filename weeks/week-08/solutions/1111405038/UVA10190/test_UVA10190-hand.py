"""
UVA 10190 手打版本測試程式
"""

import unittest
import importlib.util
import sys

# 動態導入帶減號的模組
spec = importlib.util.spec_from_file_location("hand_module", "UVA10190-hand.py")
hand_module = importlib.util.module_from_spec(spec)
sys.modules["hand_module"] = hand_module
spec.loader.exec_module(hand_module)

solve = hand_module.solve


class TestUVA10190Hand(unittest.TestCase):
    """手打版本的測試"""

    def test_01_single_static(self):
        """單把靜止傘"""
        result = solve(1, 10, 1, 1, [(0, 5, 0)])
        self.assertAlmostEqual(result, 50.0, places=2)

    def test_02_two_no_overlap(self):
        """兩把傘不重疊"""
        result = solve(2, 10, 1, 1, [(0, 2, 0), (3, 2, 0)])
        self.assertAlmostEqual(result, 40.0, places=2)

    def test_03_two_overlap(self):
        """兩把傘部分重疊"""
        result = solve(2, 10, 1, 1, [(0, 3, 0), (2, 3, 0)])
        self.assertAlmostEqual(result, 50.0, places=2)

    def test_04_moving_right(self):
        """向右移動的傘"""
        result = solve(1, 10, 2, 0.5, [(0, 2, 2)])
        self.assertAlmostEqual(result, 60.0, places=2)

    def test_05_moving_left(self):
        """向左移動的傘"""
        result = solve(1, 10, 2, 0.5, [(5, 1, -1)])
        self.assertAlmostEqual(result, 30.0, places=2)

    def test_06_boundary_right(self):
        """傘超出右邊界"""
        result = solve(1, 10, 1, 1, [(8, 4, 0)])
        self.assertGreater(result, 0)

    def test_07_multiple_rain(self):
        """降雨速率加倍，體積應加倍"""
        umbrellas = [(0, 5, 0)]
        result1 = solve(1, 10, 1, 1, umbrellas)
        result2 = solve(1, 10, 1, 2, umbrellas)
        self.assertAlmostEqual(result2, result1 * 2, places=2)

    def test_08_three_umbrellas(self):
        """三把傘複雜合併"""
        umbrellas = [(0, 2, 0), (1.5, 2, 0), (4, 2, 0)]
        result = solve(3, 10, 1, 1, umbrellas)
        self.assertAlmostEqual(result, 55.0, places=1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
