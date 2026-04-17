from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path
from textwrap import dedent


# 測試檔與解答檔放在同一個資料夾，之後搬移時不用改路徑。
BASE_DIR = Path(__file__).resolve().parent


def find_solution_file() -> Path | None:
    """尋找同資料夾中的 UVA 10038 解答程式。"""

    # 若要指定測試某個檔名，可先設定環境變數。
    override_name = os.environ.get("UVA10038_SOLUTION", "").strip()
    if override_name:
        override_path = BASE_DIR / override_name
        if override_path.exists():
            return override_path

    preferred_names = [
        "uva10038.py",
        "solution.py",
        "UVA10038.py",
        "answer.py",
        "main.py",
    ]

    for file_name in preferred_names:
        candidate = BASE_DIR / file_name
        if candidate.exists():
            return candidate

    # 若解答使用其他名稱，就抓第一個非測試檔的 Python 檔。
    python_files = sorted(
        path
        for path in BASE_DIR.glob("*.py")
        if path.name != Path(__file__).name and not path.name.startswith("test_")
    )
    return python_files[0] if python_files else None


class TestUVA10038(unittest.TestCase):
    """針對 UVA 10038 jolly jumper 題目的標準輸入輸出測試。"""

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
        """比較實際輸出與預期輸出是否一致。"""

        actual_output = self.run_solution(test_input)
        self.assertEqual(actual_output, expected_output.strip())

    def test_single_number_sequence_is_jolly(self) -> None:
        """只有一個數字時，沒有缺少的差值，因此應視為 Jolly。"""

        test_input = "1 5\n"
        expected_output = "Jolly"

        self.assert_output(test_input, expected_output)

    def test_sample_jolly_case(self) -> None:
        """題目中的經典範例應判定為 Jolly。"""

        test_input = "4 1 4 2 3\n"
        expected_output = "Jolly"

        self.assert_output(test_input, expected_output)

    def test_sample_not_jolly_case(self) -> None:
        """題目中的反例應判定為 Not jolly。"""

        test_input = "5 1 4 2 -1 6\n"
        expected_output = "Not jolly"

        self.assert_output(test_input, expected_output)

    def test_repeated_difference_is_not_jolly(self) -> None:
        """若差值重複，代表無法完整涵蓋 1 到 n-1。"""

        test_input = "4 1 4 7 10\n"
        expected_output = "Not jolly"

        self.assert_output(test_input, expected_output)

    def test_multiple_cases_until_eof(self) -> None:
        """輸入有多列測資時，必須一路處理到 EOF。"""

        test_input = dedent(
            """
            4 1 4 2 3
            5 1 4 2 -1 6
            1 9
            4 1 4 7 10
            """
        ).lstrip()
        expected_output = dedent(
            """
            Jolly
            Not jolly
            Jolly
            Not jolly
            """
        ).strip()

        self.assert_output(test_input, expected_output)


if __name__ == "__main__":
    unittest.main()