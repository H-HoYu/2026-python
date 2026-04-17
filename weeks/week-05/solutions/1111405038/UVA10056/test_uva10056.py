import math
import random
import re
import subprocess
import sys
from pathlib import Path
import unittest


class TestUVA10056(unittest.TestCase):
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
                "找不到待測解答程式。請將解答 .py 檔放在與 test_uva10056.py 相同的資料夾。"
            )

        preferred_names = [
            "uva10056.py",
            "UVA10056.py",
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
            "偵測到多個可能的解答檔，請只保留一個，或使用慣例檔名 uva10056.py / solution.py。"
        )

    def _run_program(self, input_data: str) -> list[str]:
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

        output_lines = [line.strip() for line in stdout.splitlines()]
        for line in output_lines:
            # 題目要求固定輸出到小數點後四位，因此這裡直接驗證格式。
            self.assertRegex(line, r"^\d+\.\d{4}$")
        return output_lines

    @staticmethod
    def _expected_probability(player_count: int, success_probability: float, player_index: int) -> str:
        # 第 i 位玩家第一次能嘗試成功的機率為：
        # (1 - p)^(i - 1) * p
        # 若前面整輪都沒人成功，機率會再乘上 ((1 - p)^N)^k。
        # 因此總和是一個等比級數。
        if success_probability == 0:
            return "0.0000"

        first_win_probability = ((1 - success_probability) ** (player_index - 1)) * success_probability
        full_round_failure = (1 - success_probability) ** player_count
        probability = first_win_probability / (1 - full_round_failure)
        return f"{probability:.4f}"

    def _assert_cases(self, cases: list[tuple[int, float, int]]):
        input_lines = [str(len(cases))]
        expected = []

        for player_count, success_probability, player_index in cases:
            input_lines.append(f"{player_count} {success_probability} {player_index}")
            expected.append(
                self._expected_probability(player_count, success_probability, player_index)
            )

        actual = self._run_program("\n".join(input_lines) + "\n")

        self.assertEqual(
            len(actual),
            len(expected),
            msg=f"輸出行數錯誤，預期 {len(expected)} 行，實際得到 {len(actual)} 行。",
        )
        self.assertEqual(actual, expected)

    def test_zero_probability_always_outputs_zero(self):
        self._assert_cases([(3, 0.0, 1), (5, 0.0, 4)])

    def test_first_player_with_certain_success(self):
        self._assert_cases([(4, 1.0, 1), (7, 1.0, 1)])

    def test_non_first_player_with_certain_success(self):
        # 當 p = 1 時，只有第一位玩家可能獲勝，其他玩家應為 0.0000。
        self._assert_cases([(4, 1.0, 2), (9, 1.0, 5)])

    def test_multiple_cases_in_one_input(self):
        self._assert_cases(
            [
                (3, 0.1666666667, 1),
                (3, 0.1666666667, 2),
                (10, 0.25, 3),
                (5, 0.5, 5),
            ]
        )

    def test_known_sample_style_values(self):
        self._assert_cases([(2, 0.5, 1), (2, 0.5, 2), (5, 0.2, 3)])

    def test_random_cases_match_reference_formula(self):
        # 使用固定亂數種子，確保測試可重現。
        random.seed(10056)
        cases = []

        for _ in range(40):
            player_count = random.randint(1, 20)
            success_probability = random.choice(
                [0.0, 1.0, random.randint(1, 999) / 1000]
            )
            player_index = random.randint(1, player_count)
            cases.append((player_count, success_probability, player_index))

        self._assert_cases(cases)


if __name__ == "__main__":
    unittest.main()