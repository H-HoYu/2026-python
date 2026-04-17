import random
import subprocess
import sys
from pathlib import Path
import unittest


class TestUVA10050(unittest.TestCase):
    # 這份測試假設解答程式會放在與測試檔相同的資料夾中，
    # 並且是標準 UVA 類型的 stdin / stdout 程式。

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
                "找不到待測解答程式。請將解答 .py 檔放在與 test_uva10050.py 相同的資料夾。"
            )

        preferred_names = [
            "uva10050.py",
            "UVA10050.py",
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
            "偵測到多個可能的解答檔，請只保留一個，或使用慣例檔名 uva10050.py / solution.py。"
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

        try:
            return [int(line.strip()) for line in stdout.splitlines()]
        except ValueError as exc:
            self.fail(f"輸出必須每行都是整數，實際輸出為：{stdout!r}\n原始錯誤：{exc}")

    @staticmethod
    def _expected_lost_days(total_days: int, hartals: list[int]) -> int:
        # 用測試端自己的模擬器當獨立正解：
        # 逐天檢查是否有任一政黨在該日發動罷會，且排除星期五與星期六。
        lost_days = 0

        for day in range(1, total_days + 1):
            weekday = day % 7

            # 依題意，模擬從星期天開始：
            # day % 7 == 6 代表星期五，day % 7 == 0 代表星期六。
            if weekday in (6, 0):
                continue

            if any(day % hartal == 0 for hartal in hartals):
                lost_days += 1

        return lost_days

    def _assert_cases(self, cases: list[tuple[int, list[int]]]):
        input_lines = [str(len(cases))]
        expected = []

        for total_days, hartals in cases:
            input_lines.append(str(total_days))
            input_lines.append(str(len(hartals)))
            input_lines.extend(str(hartal) for hartal in hartals)
            expected.append(self._expected_lost_days(total_days, hartals))

        actual = self._run_program("\n".join(input_lines) + "\n")

        self.assertEqual(
            len(actual),
            len(expected),
            msg=f"輸出行數錯誤，預期 {len(expected)} 行，實際得到 {len(actual)} 行。",
        )
        self.assertEqual(actual, expected)

    def test_problem_statement_example(self):
        # 題目敘述中的經典範例：14 天、參數 3、4、8，答案應為 5。
        self._assert_cases([(14, [3, 4, 8])])

    def test_holiday_days_are_not_counted(self):
        # 7 天內若只有參數 6，代表只會落在第 6 天星期五，答案應為 0。
        self._assert_cases([(7, [6])])

    def test_overlapping_hartals_count_once(self):
        # 同一天被多個政黨同時罷會時，只能算損失一天，不能重複累加。
        self._assert_cases([(15, [3, 3, 5])])

    def test_multiple_cases_in_one_input(self):
        self._assert_cases(
            [
                (14, [3, 4, 8]),
                (7, [2]),
                (30, [2, 3, 4]),
                (21, [5, 6, 8]),
            ]
        )

    def test_single_party_longer_period(self):
        self._assert_cases([(100, [13])])

    def test_random_small_cases_match_reference_simulation(self):
        # 使用固定亂數種子，確保測試可重現。
        random.seed(10050)
        cases = []

        for _ in range(40):
            total_days = random.randint(7, 60)
            party_count = random.randint(1, 6)

            # 題目保證 hartal 參數不會是 7 的倍數。
            hartals = []
            while len(hartals) < party_count:
                value = random.randint(1, 20)
                if value % 7 != 0:
                    hartals.append(value)

            cases.append((total_days, hartals))

        self._assert_cases(cases)


if __name__ == "__main__":
    unittest.main()