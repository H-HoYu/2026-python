import random
import subprocess
import sys
from pathlib import Path
import unittest


class TestUVA10041(unittest.TestCase):
    # 這份測試假設解答程式會放在與測試檔相同的資料夾中。
    # 測試會直接以命令列執行解答程式，驗證標準輸入與標準輸出。

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
                "找不到待測解答程式。請將解答 .py 檔放在與 test_uva10041.py 相同的資料夾。"
            )

        preferred_names = [
            "main.py",
            "solution.py",
            "uva10041.py",
            "UVA10041.py",
            "answer.py",
        ]

        for name in preferred_names:
            for candidate in candidates:
                if candidate.name == name:
                    return candidate

        if len(candidates) == 1:
            return candidates[0]

        raise RuntimeError(
            "偵測到多個可能的解答檔，請只保留一個，或使用慣例檔名 main.py / solution.py / uva10041.py。"
        )

    def _run_program(self, input_data: str) -> list[int]:
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

        output_lines = stdout.splitlines()
        try:
            return [int(line.strip()) for line in output_lines]
        except ValueError as exc:
            self.fail(f"輸出必須每行都是整數，實際輸出為：{output_lines}\n原始錯誤：{exc}")

    @staticmethod
    def _expected_min_distance(addresses: list[int]) -> int:
        # 以暴力法枚舉所有可能門牌，作為測試端的獨立正解。
        # 這樣可以避免測試直接複製題目的標準解法而降低驗證價值。
        return min(
            sum(abs(candidate - address) for address in addresses)
            for candidate in range(min(addresses), max(addresses) + 1)
        )

    def _assert_cases(self, cases: list[list[int]]):
        input_lines = [str(len(cases))]
        expected = []

        for addresses in cases:
            input_lines.append(
                " ".join([str(len(addresses))] + [str(address) for address in addresses])
            )
            expected.append(self._expected_min_distance(addresses))

        actual = self._run_program("\n".join(input_lines) + "\n")
        self.assertEqual(
            len(actual),
            len(expected),
            msg=f"輸出行數錯誤，預期 {len(expected)} 行，實際得到 {len(actual)} 行。",
        )
        self.assertEqual(actual, expected)

    def test_single_relative_returns_zero(self):
        self._assert_cases([[17]])

    def test_duplicate_addresses_returns_zero(self):
        self._assert_cases([[5, 5, 5, 5]])

    def test_even_number_of_relatives(self):
        self._assert_cases([[2, 4, 6, 8]])

    def test_unsorted_addresses(self):
        self._assert_cases([[30, 1, 20, 10, 2]])

    def test_multiple_cases_in_one_input(self):
        self._assert_cases(
            [
                [2, 4],
                [2, 4, 6],
                [1, 2, 2, 8, 10],
                [100, 200, 300, 400],
            ]
        )

    def test_random_small_cases_match_bruteforce_reference(self):
        # 使用固定亂數種子，讓測試可重現且涵蓋多組不同分布。
        random.seed(10041)
        cases = []
        for _ in range(40):
            relative_count = random.randint(1, 8)
            addresses = [random.randint(1, 40) for _ in range(relative_count)]
            cases.append(addresses)

        self._assert_cases(cases)


if __name__ == "__main__":
    unittest.main()