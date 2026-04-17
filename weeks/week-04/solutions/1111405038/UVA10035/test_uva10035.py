from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path
from textwrap import dedent


# 測試檔與解答檔放在同一個資料夾，搬移資料夾時不用改路徑。
BASE_DIR = Path(__file__).resolve().parent


def find_solution_file() -> Path | None:
    """尋找同資料夾中的 UVA 10035 解答程式。"""

    # 若想指定要測哪一個檔名，可先設定環境變數。
    override_name = os.environ.get("UVA10035_SOLUTION", "").strip()
    if override_name:
        override_path = BASE_DIR / override_name
        if override_path.exists():
            return override_path

    preferred_names = [
        "uva10035.py",
        "solution.py",
        "UVA10035.py",
        "answer.py",
        "main.py",
    ]

    for file_name in preferred_names:
        candidate = BASE_DIR / file_name
        if candidate.exists():
            return candidate

    # 若使用其他檔名，則抓第一個非測試檔的 Python 檔。
    python_files = sorted(
        path
        for path in BASE_DIR.glob("*.py")
        if path.name != Path(__file__).name and not path.name.startswith("test_")
    )
    return python_files[0] if python_files else None


class TestUVA10035(unittest.TestCase):
    """針對 UVA 10035 carry operation 題目的標準輸入輸出測試。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.solution_file = find_solution_file()

    def run_solution(self, test_input: str) -> str:
        """執行解答程式並回傳去除首尾空白後的輸出。"""

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

        return completed.stdout.strip()

    def assert_output(self, test_input: str, expected_output: str) -> None:
        """比較實際輸出與預期輸出。"""

        actual_output = self.run_solution(test_input)
        self.assertEqual(actual_output, expected_output.strip())

    def test_no_carry_operation(self) -> None:
        """若每一位相加都不到 10，就應輸出沒有進位。"""

        test_input = dedent(
            """
            123 456
            0 0
            """
        ).lstrip()
        expected_output = "No carry operation."

        self.assert_output(test_input, expected_output)

    def test_one_carry_operation(self) -> None:
        """剛好一次進位時，輸出必須使用單數 operation。"""

        test_input = dedent(
            """
            123 594
            0 0
            """
        ).lstrip()
        expected_output = "1 carry operation."

        self.assert_output(test_input, expected_output)

    def test_multiple_carry_operations(self) -> None:
        """進位超過一次時，輸出必須使用複數 operations。"""

        test_input = dedent(
            """
            555 555
            0 0
            """
        ).lstrip()
        expected_output = "3 carry operations."

        self.assert_output(test_input, expected_output)

    def test_previous_carry_affects_next_digit(self) -> None:
        """前一位的進位必須正確帶入下一位計算。"""

        test_input = dedent(
            """
            95 17
            0 0
            """
        ).lstrip()
        expected_output = "2 carry operations."

        self.assert_output(test_input, expected_output)

    def test_multiple_cases_stop_at_zero_zero(self) -> None:
        """多筆測資需依序輸出，且讀到 0 0 後必須停止。"""

        test_input = dedent(
            """
            123 456
            555 555
            123 594
            0 0
            999 1
            """
        ).lstrip()
        expected_output = dedent(
            """
            No carry operation.
            3 carry operations.
            1 carry operation.
            """
        ).strip()

        self.assert_output(test_input, expected_output)


if __name__ == "__main__":
    unittest.main()