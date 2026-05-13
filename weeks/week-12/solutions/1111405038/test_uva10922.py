import subprocess
import sys
from pathlib import Path
import unittest


SCRIPT = Path(__file__).with_name("UVA10922-hand.py")


def run_case(input_text: str) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=input_text,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


class TestUVA10922Hand(unittest.TestCase):
    def test_single_9(self) -> None:
        self.assertEqual(run_case("9\n0\n"), "9-degree of 9 is 1.\n")

    def test_depth_1(self) -> None:
        self.assertEqual(run_case("18\n0\n"), "9-degree of 18 is 1.\n")

    def test_depth_2(self) -> None:
        self.assertEqual(run_case("99\n0\n"), "9-degree of 99 is 2.\n")

    def test_not_multiple(self) -> None:
        self.assertEqual(run_case("10\n0\n"), "10 is not a multiple of 9.\n")

    def test_multiple_cases(self) -> None:
        inp = "9\n18\n99\n10\n0\n"
        expected = (
            "9-degree of 9 is 1.\n"
            "9-degree of 18 is 1.\n"
            "9-degree of 99 is 2.\n"
            "10 is not a multiple of 9.\n"
        )
        self.assertEqual(run_case(inp), expected)


if __name__ == "__main__":
    unittest.main()
