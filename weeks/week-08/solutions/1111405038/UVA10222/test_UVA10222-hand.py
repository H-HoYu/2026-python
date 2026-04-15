import importlib.util
import sys
import unittest
from pathlib import Path


# 動態載入帶減號的 hand 版檔案
MODULE_PATH = Path(__file__).with_name("UVA10222-hand.py")
SPEC = importlib.util.spec_from_file_location("uva10222_hand", MODULE_PATH)
UVA10222_HAND = importlib.util.module_from_spec(SPEC)
sys.modules["uva10222_hand"] = UVA10222_HAND
if SPEC.loader is not None:
    SPEC.loader.exec_module(UVA10222_HAND)


class TestUVA10222Hand(unittest.TestCase):
    """UVA10222 hand 版本測試"""

    def test_01_single_letter(self):
        """R -> E"""
        self.assertEqual(UVA10222_HAND.decode("R"), "E")

    def test_02_lowercase(self):
        """小寫輸入也能解碼"""
        self.assertEqual(UVA10222_HAND.decode("r"), "E")

    def test_03_number_and_symbol(self):
        """數字與符號：4 -> 3, = -> -"""
        self.assertEqual(UVA10222_HAND.decode("4="), "3-")

    def test_04_keep_space(self):
        """空白應保留"""
        self.assertEqual(UVA10222_HAND.decode("R U"), "E Y")

    def test_05_word(self):
        """YJR -> THE"""
        self.assertEqual(UVA10222_HAND.decode("YJR"), "THE")

    def test_06_sentence(self):
        """整句範例"""
        self.assertEqual(UVA10222_HAND.decode("O S, GOMR YPFSU/"), "I AM FINE TODAY.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
