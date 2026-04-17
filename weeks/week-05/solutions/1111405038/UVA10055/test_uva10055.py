import random
import subprocess
import sys
from pathlib import Path
import unittest


class TestUVA10055(unittest.TestCase):
    # 這份測試假設解答程式會放在與測試檔相同的資料夾中，
    # 並使用 UVA 常見的標準輸入 / 標準輸出格式。

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
                "找不到待測解答程式。請將解答 .py 檔放在與 test_uva10055.py 相同的資料夾。"
            )

        preferred_names = [
            "uva10055.py",
            "UVA10055.py",
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
            "偵測到多個可能的解答檔，請只保留一個，或使用慣例檔名 uva10055.py / solution.py。"
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
            self.fail(f"輸出必須每行都是 0 或 1，實際輸出為：{stdout!r}\n原始錯誤：{exc}")

    @staticmethod
    def _expected_answers(n: int, operations: list[tuple[int, ...]]) -> list[int]:
        # 以最直接的模擬法作為測試端的獨立正解。
        # False 代表增函數，True 代表減函數。
        states = [False] * (n + 1)
        answers = []

        for operation in operations:
            if operation[0] == 1:
                index = operation[1]
                states[index] = not states[index]
            else:
                left, right = operation[1], operation[2]
                decreasing_count = sum(states[left:right + 1])
                answers.append(decreasing_count % 2)

        return answers

    def _assert_case(self, n: int, operations: list[tuple[int, ...]]):
        input_lines = [f"{n} {len(operations)}"]

        for operation in operations:
            input_lines.append(" ".join(map(str, operation)))

        expected = self._expected_answers(n, operations)
        actual = self._run_program("\n".join(input_lines) + "\n")

        self.assertEqual(
            len(actual),
            len(expected),
            msg=f"輸出行數錯誤，預期 {len(expected)} 行，實際得到 {len(actual)} 行。",
        )
        self.assertEqual(actual, expected)

    def test_all_increasing_initially(self):
        # 一開始全部都是增函數，因此任何區間查詢都應輸出 0。
        self._assert_case(5, [(2, 1, 5), (2, 2, 4), (2, 3, 3)])

    def test_single_flip_changes_parity(self):
        # 單點翻轉後，包含該位置的區間奇偶性會改變。
        self._assert_case(4, [(1, 2), (2, 1, 4), (2, 2, 2), (2, 3, 4)])

    def test_double_flip_restores_original_state(self):
        # 同一位置翻轉兩次，等於回到原本的增函數狀態。
        self._assert_case(3, [(1, 1), (1, 1), (2, 1, 3), (2, 1, 1)])

    def test_mixed_updates_and_queries(self):
        self._assert_case(
            6,
            [
                (1, 2),
                (1, 5),
                (2, 1, 6),
                (2, 2, 5),
                (1, 2),
                (2, 1, 3),
                (2, 5, 6),
            ],
        )

    def test_query_single_position_range(self):
        # 區間只有一個函數時，答案就是該函數目前是否為減函數。
        self._assert_case(5, [(1, 4), (2, 4, 4), (1, 4), (2, 4, 4)])

    def test_random_operations_match_reference_simulation(self):
        # 使用固定亂數種子，確保測試可重現。
        random.seed(10055)

        for _ in range(20):
            n = random.randint(1, 20)
            operation_count = random.randint(10, 40)
            operations = []
            has_query = False

            for _ in range(operation_count):
                if random.randint(0, 1) == 0:
                    operations.append((1, random.randint(1, n)))
                else:
                    left = random.randint(1, n)
                    right = random.randint(left, n)
                    operations.append((2, left, right))
                    has_query = True

            if not has_query:
                operations.append((2, 1, n))

            self._assert_case(n, operations)


if __name__ == "__main__":
    unittest.main()