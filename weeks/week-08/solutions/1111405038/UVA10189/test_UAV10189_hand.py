"""
UVA 10189 - Minesweeper 手打版本測試程式
"""

import unittest
import importlib.util
import sys

# 動態導入含減號的模組
spec = importlib.util.spec_from_file_location("hand_module", "UAV10189-hand.py")
hand_module = importlib.util.module_from_spec(spec)
sys.modules["hand_module"] = hand_module
spec.loader.exec_module(hand_module)

solve_minesweeper = hand_module.solve_minesweeper
solve = hand_module.solve


class TestUAV10189Hand(unittest.TestCase):
    """手打版本的測試"""
    
    def test_01_basic(self):
        """測試基礎案例"""
        grid = [['*', '.', '.'], ['.', '.', '.'], ['.', '*', '.']]
        result = solve_minesweeper(grid)
        expected = [['*', '1', '0'], ['2', '2', '1'], ['1', '*', '1']]
        self.assertEqual(result, expected)
    
    def test_02_no_mines(self):
        """沒有地雷"""
        grid = [['.', '.'], ['.', '.']]
        result = solve_minesweeper(grid)
        expected = [['0', '0'], ['0', '0']]
        self.assertEqual(result, expected)
    
    def test_03_full_mines(self):
        """全是地雷"""
        grid = [['*', '*'], ['*', '*']]
        result = solve_minesweeper(grid)
        self.assertEqual(result, grid)
    
    def test_04_surrounded(self):
        """被完全包圍"""
        grid = [['*', '*', '*'], ['*', '.', '*'], ['*', '*', '*']]
        result = solve_minesweeper(grid)
        self.assertEqual(result[1][1], '8')
    
    def test_05_full_solve(self):
        """完整解題"""
        test_input = [
            "2 2",
            "*.",
            "..",
            "0 0"
        ]
        output = solve(test_input)
        self.assertIn("Field #1:", output)
        self.assertIn("*1", output)
        self.assertIn("11", output)
    
    def test_06_single(self):
        """單個格子"""
        grid = [['.']]
        result = solve_minesweeper(grid)
        self.assertEqual(result, [['0']])
    
    def test_07_edge_mine(self):
        """邊緣地雷"""
        grid = [['.', '*', '.'], ['.', '.', '.'], ['.', '.', '.']]
        result = solve_minesweeper(grid)
        self.assertEqual(result[0][0], '1')
        self.assertEqual(result[0][2], '1')
    
    def test_08_multiple_cases(self):
        """多個測試案例"""
        test_input = [
            "4 4",
            "*...",
            "....",
            ".*...",
            "....",
            "3 5",
            "**...",
            ".....",
            ".*...",
            "0 0"
        ]
        output = solve(test_input)
        self.assertIn("Field #1:", output)
        self.assertIn("Field #2:", output)
        # 驗證兩個案例之間有空行
        lines = output.split('\n')
        field_indices = [i for i, line in enumerate(lines) if line.startswith("Field #")]
        self.assertGreaterEqual(len(field_indices), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
