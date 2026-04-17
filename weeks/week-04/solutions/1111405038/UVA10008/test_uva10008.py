from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path
from textwrap import dedent


# 測試檔與解答檔預期放在同一個資料夾中，這樣搬移資料夾時不需要修改路徑。
BASE_DIR = Path(__file__).resolve().parent


def find_solution_file() -> Path | None:
    """尋找同資料夾中的 UVA 10008 解答程式。"""

    # 若想指定要測哪一個檔案，可先設定環境變數。
    override_name = os.environ.get("UVA10008_SOLUTION", "").strip()
    if override_name:
        override_path = BASE_DIR / override_name
        if override_path.exists():
            return override_path

    preferred_names = [
        "uva10008.py",
        "solution.py",
        "UVA10008.py",
        "answer.py",
        "main.py",
    ]

    for file_name in preferred_names:
        candidate = BASE_DIR / file_name
        if candidate.exists():
            return candidate

    # 若使用其他檔名，就退而求其次抓同資料夾內第一個非測試檔的 Python 檔。
    python_files = sorted(
        path
        for path in BASE_DIR.glob("*.py")
        if path.name != Path(__file__).name and not path.name.startswith("test_")
    )
    return python_files[0] if python_files else None


class TestUVA10008(unittest.TestCase):
    """針對 UVA 10008 字母統計題目的標準輸入輸出測試。"""

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
        """比對實際輸出與預期輸出是否一致。"""

        actual_output = self.run_solution(test_input)
        self.assertEqual(actual_output, expected_output.strip())

    def test_case_insensitive_counting(self) -> None:
        """大小寫應視為同一個字母一起累計。"""

        test_input = dedent(
            """
            2
            AaBb
            aA!!c
            """
        ).lstrip()
        expected_output = dedent(
            """
            A 4
            B 2
            C 1
            """
        ).strip()

        self.assert_output(test_input, expected_output)

    def test_same_frequency_should_sort_alphabetically(self) -> None:
        """若出現次數相同，必須依照字母順序輸出。"""

        test_input = dedent(
            """
            3
            AB
            ba
            cc
            """
        ).lstrip()
        expected_output = dedent(
            """
            A 2
            B 2
            C 2
            """
        ).strip()

        self.assert_output(test_input, expected_output)

    def test_non_letters_should_be_ignored(self) -> None:
        """數字、空白與標點符號都不應列入統計。"""

        test_input = dedent(
            """
            2
            123 !?
            zZ y-Y
            """
        ).lstrip()
        expected_output = dedent(
            """
            Y 2
            Z 2
            """
        ).strip()

        self.assert_output(test_input, expected_output)

    def test_only_existing_letters_should_be_printed(self) -> None:
        """沒有出現的字母不能輸出，完全沒有字母時應為空輸出。"""

        test_input = dedent(
            """
            2
            12345
               !@#$%
            """
        ).lstrip()
        expected_output = ""

        self.assert_output(test_input, expected_output)

    def test_frequency_descending_then_alphabetical(self) -> None:
        """先比次數高低，再用字母順序處理同分情況。"""

        test_input = dedent(
            """
            3
            The Day is Here.
            aAAb
            bbb
            """
        ).lstrip()
        expected_output = dedent(
            """
            A 4
            B 4
            E 3
            H 2
            D 1
            I 1
            R 1
            S 1
            T 1
            Y 1
            """
        ).strip()

        self.assert_output(test_input, expected_output)


if __name__ == "__main__":
    unittest.main()