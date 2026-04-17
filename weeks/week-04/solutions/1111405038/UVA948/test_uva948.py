from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path
from textwrap import dedent


# 測試檔與解答檔預期放在同一個資料夾中。
BASE_DIR = Path(__file__).resolve().parent


def find_solution_file() -> Path | None:
    """尋找同資料夾中的解答程式檔案。"""

    override_name = os.environ.get("UVA948_SOLUTION", "").strip()
    if override_name:
        override_path = BASE_DIR / override_name
        if override_path.exists():
            return override_path

    preferred_names = [
        "uva948.py",
        "solution.py",
        "UVA948.py",
        "answer.py",
        "main.py",
    ]

    for file_name in preferred_names:
        candidate = BASE_DIR / file_name
        if candidate.exists():
            return candidate

    python_files = sorted(
        path
        for path in BASE_DIR.glob("*.py")
        if path.name != Path(__file__).name and not path.name.startswith("test_")
    )
    return python_files[0] if python_files else None


class TestUVA948(unittest.TestCase):
    """針對 UVA 948 假幣問題的標準輸入輸出測試。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.solution_file = find_solution_file()

    def run_solution(self, test_input: str) -> str:
        """執行解答程式並回傳標準輸出結果。"""

        if self.solution_file is None:
            self.skipTest("尚未找到解答檔，請將解答程式放在同資料夾中。")

        completed = subprocess.run(
            [sys.executable, str(self.solution_file)],
            input=test_input,
            text=True,
            capture_output=True,
            cwd=BASE_DIR,
            check=False,
        )

        if completed.returncode != 0:
            self.fail(
                "解答程式執行失敗。\n"
                f"exit code: {completed.returncode}\n"
                f"stderr:\n{completed.stderr}"
            )

        # 題目只在乎輸出內容，這裡去除首尾多餘空白行，避免換行風格影響判斷。
        return completed.stdout.strip()

    def assert_output(self, test_input: str, expected_output: str) -> None:
        """比較實際輸出與預期輸出。"""

        actual_output = self.run_solution(test_input)
        self.assertEqual(actual_output, expected_output.strip())

    def test_unique_fake_coin_after_multiple_weighings(self) -> None:
        """多次秤重後可唯一鎖定第 4 枚是假幣。"""

        test_input = dedent(
            """
            1

            4 3
            1 1 2
            =
            1 3 4
            <
            1 3 1
            =
            """
        ).lstrip()
        expected_output = "4"

        self.assert_output(test_input, expected_output)

    def test_equal_weighing_can_directly_identify_fake_coin(self) -> None:
        """若秤平後只剩下一枚未被證明為真幣，應直接輸出該編號。"""

        test_input = dedent(
            """
            1

            3 1
            1 1 2
            =
            """
        ).lstrip()
        expected_output = "3"

        self.assert_output(test_input, expected_output)

    def test_ambiguous_result_should_output_zero(self) -> None:
        """若秤重結果仍無法唯一判定假幣，必須輸出 0。"""

        test_input = dedent(
            """
            1

            4 1
            1 1 2
            <
            """
        ).lstrip()
        expected_output = "0"

        self.assert_output(test_input, expected_output)

    def test_conflicting_heavy_light_assumptions_should_output_zero(self) -> None:
        """同一枚硬幣若無法同時滿足前後秤重方向，也不能視為答案。"""

        test_input = dedent(
            """
            1

            3 2
            1 1 2
            <
            1 1 3
            >
            """
        ).lstrip()
        expected_output = "0"

        self.assert_output(test_input, expected_output)

    def test_multiple_cases_need_blank_line_between_answers(self) -> None:
        """多組測資之間需要保留一個空白行。"""

        test_input = dedent(
            """
            2

            3 1
            1 1 2
            =

            4 1
            1 1 2
            <
            """
        ).lstrip()
        expected_output = dedent(
            """
            3

            0
            """
        ).strip()

        self.assert_output(test_input, expected_output)


if __name__ == "__main__":
    unittest.main()