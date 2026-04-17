import random
import subprocess
import sys
from pathlib import Path
import unittest


class TestUVA10057(unittest.TestCase):
    # 這份測試假設解答程式會放在與測試檔相同的資料夾中，
    # 並且使用 UVA 常見的標準輸入 / 標準輸出格式。

    @classmethod
    def setUpClass(cls):
        cls.solution_path = cls._find_solution_file()

    @classmethod
    def _find_solution_file(cls) -> Path:
        current_dir = Path(__file__).resolve().parent
        candidates = sorted(
            path for path in current_dir.glob("*.py") if path.name != Path(__file__).name
        )

        if not candidates:
            raise FileNotFoundError(
                "找不到待測解答程式。請將解答 .py 檔放在與 test_uva10057.py 相同的資料夾。"
            )

        preferred_names = [
            "uva10057.py",
            "UVA10057.py",
            "solution.py",
            "main.py",
            "answer.py",
        ]

        for name in preferred_names:
            for candidate in candidates:
                if candidate.name == name:
                    return candidate

        if len(candidates) == 1:
            return candidates[0]

        raise RuntimeError(
            "偵測到多個可能的解答檔，請只保留一個，或使用慣例檔名 uva10057.py / solution.py。"
        )

    def _run_program(self, input_data: str) -> list[tuple[int, int, int]]:
        completed = subprocess.run(
            [sys.executable, str(self.solution_path)],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )

        self.assertEqual(
            completed.returncode,
            0,
            msg=(
                "程式執行失敗。\n"
                f"return code: {completed.returncode}\n"
                f"stderr:\n{completed.stderr}"
            ),
        )

        stdout = completed.stdout.strip()
        if not stdout:
            return []

        results = []
        for line in stdout.splitlines():
            parts = line.strip().split()
            self.assertEqual(parts.__len__(), 3, msg=f"每行輸出必須正好有 3 個整數，實際為：{line!r}")

            try:
                results.append(tuple(int(part) for part in parts))
            except ValueError as exc:
                self.fail(f"輸出必須是整數，實際輸出為：{line!r}\n原始錯誤：{exc}")

        return results

    @staticmethod
    def _expected_result(numbers: list[int]) -> tuple[int, int, int]:
        # 用暴力法枚舉所有可能的 A，作為測試端的獨立正解。
        # 對小型測資而言，這樣能避免測試直接複製正式解法。
        minimum_cost = min(
            sum(abs(value - candidate) for value in numbers)
            for candidate in range(min(numbers), max(numbers) + 1)
        )

        minimizers = [
            candidate
            for candidate in range(min(numbers), max(numbers) + 1)
            if sum(abs(value - candidate) for value in numbers) == minimum_cost
        ]

        best_a = minimizers[0]
        count_in_range = sum(1 for value in numbers if minimizers[0] <= value <= minimizers[-1])
        possible_count = len(minimizers)
        return best_a, count_in_range, possible_count

    def _assert_cases(self, cases: list[list[int]]):
        input_lines = []
        expected = []

        for numbers in cases:
            input_lines.append(str(len(numbers)))
            input_lines.append(" ".join(str(number) for number in numbers))
            expected.append(self._expected_result(numbers))

        actual = self._run_program("\n".join(input_lines) + "\n")

        self.assertEqual(
            len(actual),
            len(expected),
            msg=f"輸出行數錯誤，預期 {len(expected)} 行，實際得到 {len(actual)} 行。",
        )
        self.assertEqual(actual, expected)

    def test_odd_count_has_single_best_a(self):
        # 奇數筆資料時，最佳 A 會唯一落在中位數。
        self._assert_cases([[1, 2, 3, 4, 5]])

    def test_even_count_has_multiple_possible_a(self):
        # 偶數筆資料時，最佳 A 可能是一整段連續整數區間。
        self._assert_cases([[1, 2, 8, 9]])

    def test_duplicate_values_increase_count(self):
        self._assert_cases([[10, 10, 10, 20, 20]])

    def test_all_values_same(self):
        self._assert_cases([[7, 7, 7, 7]])

    def test_multiple_datasets_until_eof(self):
        # 題目是讀到 EOF 為止，因此同一份輸入中會有多組資料。
        self._assert_cases(
            [
                [1, 2, 3],
                [5, 5, 5, 6],
                [0, 10, 20, 30, 40, 50],
            ]
        )

    def test_random_small_cases_match_bruteforce_reference(self):
        # 使用固定亂數種子，確保測試可重現。
        random.seed(10057)
        cases = []

        for _ in range(30):
            count = random.randint(1, 8)
            numbers = [random.randint(0, 30) for _ in range(count)]
            cases.append(numbers)

        self._assert_cases(cases)


if __name__ == "__main__":
    unittest.main()