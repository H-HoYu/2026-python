from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path
from textwrap import dedent


# 測試檔與解答檔放在同一個資料夾，這樣搬移時不用額外修改路徑。
BASE_DIR = Path(__file__).resolve().parent


def find_solution_file() -> Path | None:
    """尋找同資料夾中的 UVA 10019 解答程式。"""

    # 若要明確指定某個檔名來測試，可用環境變數覆寫。
    override_name = os.environ.get("UVA10019_SOLUTION", "").strip()
    if override_name:
        override_path = BASE_DIR / override_name
        if override_path.exists():
            return override_path

    preferred_names = [
        "uva10019.py",
        "solution.py",
        "UVA10019.py",
        "answer.py",
        "main.py",
    ]

    for file_name in preferred_names:
        candidate = BASE_DIR / file_name
        if candidate.exists():
            return candidate

    # 若使用其他檔名，就抓第一個非測試檔的 Python 檔。
    python_files = sorted(
        path
        for path in BASE_DIR.glob("*.py")
        if path.name != Path(__file__).name and not path.name.startswith("test_")
    )
    return python_files[0] if python_files else None


class TestUVA10019(unittest.TestCase):
    """針對題目檔目前描述的整數差值問題進行標準輸入輸出測試。"""

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

    def test_single_case_difference(self) -> None:
        """最基本情況：一組資料輸出兩數的正差值。"""

        test_input = "10 12\n"
        expected_output = "2"

        self.assert_output(test_input, expected_output)

    def test_multiple_cases_until_eof(self) -> None:
        """輸入沒有測資數量，必須一路讀到 EOF 為止。"""

        test_input = dedent(
            """
            10 12
            10 14
            100 200
            """
        ).lstrip()
        expected_output = dedent(
            """
            2
            4
            100
            """
        ).strip()

        self.assert_output(test_input, expected_output)

    def test_input_order_can_be_reversed(self) -> None:
        """題目允許兩個數的順序顛倒，因此必須取絕對值。"""

        test_input = "300 20\n"
        expected_output = "280"

        self.assert_output(test_input, expected_output)

    def test_equal_numbers_should_output_zero(self) -> None:
        """若兩個整數相同，差值應輸出 0。"""

        test_input = "999999999 999999999\n"
        expected_output = "0"

        self.assert_output(test_input, expected_output)

    def test_large_integers_should_work(self) -> None:
        """大整數測資也應能正確計算，不可因型別範圍出錯。"""

        test_input = "9223372036854775807 0\n"
        expected_output = "9223372036854775807"

        self.assert_output(test_input, expected_output)


if __name__ == "__main__":
    unittest.main()