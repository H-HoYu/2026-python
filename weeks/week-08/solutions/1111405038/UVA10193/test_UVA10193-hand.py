"""
UVA 10193 手打版本測試程式
"""

import unittest
import importlib.util
import sys

# 動態導入帶減號的模組
spec = importlib.util.spec_from_file_location("hand_module", "UVA10193-hand.py")
hand_module = importlib.util.module_from_spec(spec)
sys.modules["hand_module"] = hand_module
spec.loader.exec_module(hand_module)

solve = hand_module.solve


class TestUVA10193Hand(unittest.TestCase):
    """手打版本的測試"""

    def test_01_a_1(self):
        """a=1 → b=2, c=3 → b+c=5"""
        self.assertEqual(solve(1), 5)

    def test_02_a_2(self):
        """a=2 → b=3, c=7 → b+c=10"""
        self.assertEqual(solve(2), 10)

    def test_03_a_3(self):
        """a=3 → b=5, c=8 → b+c=13"""
        self.assertEqual(solve(3), 13)

    def test_04_a_4(self):
        """a=4 → b=5, c=21 → b+c=26"""
        self.assertEqual(solve(4), 26)

    def test_05_a_5(self):
        """a=5 → b=7, c=18 → b+c=25"""
        self.assertEqual(solve(5), 25)

    def test_06_a_7(self):
        """a=7 → b=12, c=17 → b+c=29"""
        self.assertEqual(solve(7), 29)

    def test_07_range_1_to_20(self):
        """a=1~20 與正確答案比對"""
        def brute(a):
            n = 1 + a * a
            best = None
            for d1 in range(1, n + 1):
                if n % d1 == 0:
                    s = (d1 + a) + (n // d1 + a)
                    if best is None or s < best:
                        best = s
            return best

        for a in range(1, 21):
            self.assertEqual(solve(a), brute(a), f"a={a} 結果不符")

    def test_08_large_a(self):
        """大數 a=60000 應能正常運算"""
        result = solve(60000)
        self.assertIsNotNone(result)
        self.assertGreater(result, 2 * 60000)


if __name__ == '__main__':
    unittest.main(verbosity=2)
