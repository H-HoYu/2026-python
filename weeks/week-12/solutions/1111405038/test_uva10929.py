import subprocess
import sys
from pathlib import Path
import unittest


SCRIPT = Path(__file__).with_name("UVA10929-hand.py")


def run_case(input_text: str) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=input_text,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


class TestUVA10929Hand(unittest.TestCase):
    def test_multiple_11(self) -> None:
        self.assertEqual(run_case("11\n0\n"), "11 is a multiple of 11.\n")

    def test_multiple_22(self) -> None:
        self.assertEqual(run_case("22\n0\n"), "22 is a multiple of 11.\n")

    def test_not_multiple(self) -> None:
        self.assertEqual(run_case("10\n0\n"), "10 is not a multiple of 11.\n")

    def test_large_multiple(self) -> None:
        self.assertEqual(run_case("121\n0\n"), "121 is a multiple of 11.\n")

    def test_multiple_cases(self) -> None:
        inp = "11\n22\n10\n121\n0\n"
        expected = (
            "11 is a multiple of 11.\n"
            "22 is a multiple of 11.\n"
            "10 is not a multiple of 11.\n"
            "121 is a multiple of 11.\n"
        )
        self.assertEqual(run_case(inp), expected)


if __name__ == "__main__":
    unittest.main()
