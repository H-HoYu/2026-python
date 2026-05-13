import subprocess
import sys
from pathlib import Path
import unittest


SCRIPT = Path(__file__).with_name("UVA10931-hand.py")


def run_case(input_text: str) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=input_text,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


class TestUVA10931Hand(unittest.TestCase):
    def test_sample_cases(self) -> None:
        inp = "1\n2\n10\n21\n0\n"
        expected = (
            "The parity of 1 is 1 (mod 2).\n"
            "The parity of 10 is 1 (mod 2).\n"
            "The parity of 1010 is 2 (mod 2).\n"
            "The parity of 10101 is 3 (mod 2).\n"
        )
        self.assertEqual(run_case(inp), expected)

    def test_power_of_two(self) -> None:
        self.assertEqual(run_case("8\n0\n"), "The parity of 1000 is 1 (mod 2).\n")

    def test_all_ones(self) -> None:
        self.assertEqual(run_case("7\n0\n"), "The parity of 111 is 3 (mod 2).\n")

    def test_large_value(self) -> None:
        self.assertEqual(
            run_case("2147483647\n0\n"),
            "The parity of 1111111111111111111111111111111 is 31 (mod 2).\n",
        )

    def test_multiple_lines(self) -> None:
        inp = "3\n4\n5\n0\n"
        expected = (
            "The parity of 11 is 2 (mod 2).\n"
            "The parity of 100 is 1 (mod 2).\n"
            "The parity of 101 is 2 (mod 2).\n"
        )
        self.assertEqual(run_case(inp), expected)


if __name__ == "__main__":
    unittest.main()
