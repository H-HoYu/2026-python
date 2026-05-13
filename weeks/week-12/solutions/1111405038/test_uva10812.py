import subprocess
import sys
from pathlib import Path
import unittest


SCRIPT = Path(__file__).with_name("UVA10812-hand.py")


def run_case(input_text: str) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=input_text,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


class TestUVA10812Hand(unittest.TestCase):
    def test_sample_cases(self) -> None:
        self.assertEqual(
            run_case("2\n40 20\n20 40\n"),
            "30 10\nimpossible",
        )

    def test_even_and_negative_guard(self) -> None:
        self.assertEqual(
            run_case("3\n10 2\n9 2\n4 6\n"),
            "6 4\nimpossible\nimpossible",
        )

    def test_zero_inputs(self) -> None:
        self.assertEqual(run_case("1\n0 0\n"), "0 0")

    def test_equal_scores(self) -> None:
        self.assertEqual(run_case("1\n10 0\n"), "5 5")


if __name__ == "__main__":
    unittest.main()
