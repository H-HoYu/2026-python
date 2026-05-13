import subprocess
import sys
from pathlib import Path
import unittest


SCRIPT = Path(__file__).with_name("UVA10908-hand.py")


def run_case(input_text: str) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=input_text,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


SAMPLE_INPUT = (
    "1\n"
    "7 10 4\n"
    "abbbaaaaaa\n"
    "abbbaaaaaa\n"
    "abbbaaaaaa\n"
    "aaaaaaaaaa\n"
    "aaaaaaaaaa\n"
    "aaccaaaaaa\n"
    "aaccaaaaaa\n"
    "1 2\n"
    "2 4\n"
    "4 6\n"
    "5 2\n"
)


class TestUVA10908Hand(unittest.TestCase):
    def test_sample(self) -> None:
        self.assertEqual(
            run_case(SAMPLE_INPUT),
            "7 10 4\n3\n1\n5\n1",
        )

    def test_single_cell(self) -> None:
        inp = "1\n1 1 1\na\n0 0\n"
        self.assertEqual(run_case(inp), "1 1 1\n1")

    def test_corner_query(self) -> None:
        inp = "1\n3 3 1\naaa\naaa\naaa\n0 0\n"
        self.assertEqual(run_case(inp), "3 3 1\n1")

    def test_center_all_same(self) -> None:
        inp = "1\n3 3 1\naaa\naaa\naaa\n1 1\n"
        self.assertEqual(run_case(inp), "3 3 1\n3")


if __name__ == "__main__":
    unittest.main()
