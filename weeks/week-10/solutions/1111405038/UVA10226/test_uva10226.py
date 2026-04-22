import itertools
import os
import random
import subprocess
import sys
import unittest
from pathlib import Path


class UVA10226Reference:
    """題目規則的參考實作：只用於測試比對，不追求最佳效能。"""

    @staticmethod
    def parse_cases(raw: str):
        # 題目輸入是多筆測資，直到 EOF；空白行可忽略。
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        idx = 0
        cases = []
        while idx < len(lines):
            n = int(lines[idx])
            idx += 1

            forbidden = []
            for _ in range(n):
                nums = [int(x) for x in lines[idx].split()]
                idx += 1

                blocked = set()
                for v in nums:
                    if v == 0:
                        break
                    blocked.add(v)
                forbidden.append(blocked)

            cases.append((n, forbidden))

        return cases

    @staticmethod
    def valid_permutations(n: int, forbidden):
        # 以字典序列舉 A.. 對應的人員排列（排列字串代表每個位置站的人）。
        people = [chr(ord("A") + i) for i in range(n)]
        results = []

        for perm in itertools.permutations(people):
            ok = True
            for i, p in enumerate(people):
                pos = perm.index(p) + 1  # 題目位置從 1 開始
                if pos in forbidden[i]:
                    ok = False
                    break
            if ok:
                results.append("".join(perm))

        return results

    @staticmethod
    def compress_lines(perms):
        # 第一個答案輸出完整字串；後續僅輸出與前一個答案不同的後綴。
        if not perms:
            return []

        out = [perms[0]]
        prev = perms[0]

        for cur in perms[1:]:
            lcp = 0
            while lcp < len(cur) and cur[lcp] == prev[lcp]:
                lcp += 1
            out.append(cur[lcp:])
            prev = cur

        return out

    @classmethod
    def solve(cls, raw: str) -> str:
        lines = []
        for n, forbidden in cls.parse_cases(raw):
            perms = cls.valid_permutations(n, forbidden)
            lines.extend(cls.compress_lines(perms))

        return "\n".join(lines)


def normalize_output(s: str) -> str:
    # 比對時忽略每行尾端空白與最後多一個換行的差異。
    if not s:
        return ""
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


def find_target_script() -> Path | None:
    """嘗試定位受測程式檔案。可用 TARGET_SCRIPT 覆蓋。"""
    base = Path(__file__).resolve().parent

    env_target = os.environ.get("TARGET_SCRIPT")
    if env_target:
        p = Path(env_target)
        if p.exists() and p.is_file():
            return p

    for name in ["main.py", "solution.py", "uva10226.py", "UVA10226.py"]:
        p = base / name
        if p.exists() and p.is_file():
            return p

    return None


def run_script(target: Path, input_data: str) -> str:
    proc = subprocess.run(
        [sys.executable, str(target)],
        input=input_data,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(
            "受測程式執行失敗。\n"
            f"檔案: {target}\n"
            f"return code: {proc.returncode}\n"
            f"stderr:\n{proc.stderr}"
        )
    return proc.stdout


def build_input(cases):
    rows = []
    for n, forbidden in cases:
        rows.append(str(n))
        for blocked in forbidden:
            if blocked:
                row = " ".join(str(x) for x in sorted(blocked)) + " 0"
            else:
                row = "0"
            rows.append(row)
    return "\n".join(rows) + "\n"


class TestReferenceSolver(unittest.TestCase):
    """先驗證測試用參考邏輯本身，避免錯把測試寫錯。"""

    def test_single_person(self):
        raw = "1\n0\n"
        self.assertEqual(UVA10226Reference.solve(raw), "A")

    def test_two_people_with_forbidden(self):
        # A 不可站 1 號位，B 無限制，唯一可行解是 BA。
        raw = "2\n1 0\n0\n"
        self.assertEqual(UVA10226Reference.solve(raw), "BA")

    def test_multi_case_parsing(self):
        raw = "1\n0\n2\n0\n0\n"
        self.assertEqual(UVA10226Reference.solve(raw), "A\nAB\nBA")


class TestCandidateProgram(unittest.TestCase):
    """實際測受測者程式（若尚未提供解答檔，會自動略過）。"""

    @classmethod
    def setUpClass(cls):
        cls.target = find_target_script()
        if cls.target is None:
            raise unittest.SkipTest(
                "找不到受測程式。請在同資料夾提供 main.py/solution.py/uva10226.py，"
                "或設定環境變數 TARGET_SCRIPT。"
            )

    def test_small_fixed_case(self):
        # 固定小案例：可快速檢查基本輸入、合法過濾、壓縮輸出流程。
        cases = [
            (
                3,
                [
                    {1},  # A 不可在 1
                    set(),
                    set(),
                ],
            )
        ]
        data = build_input(cases)
        expected = UVA10226Reference.solve(data)
        actual = run_script(self.target, data)
        self.assertEqual(normalize_output(actual), normalize_output(expected))

    def test_random_cases(self):
        # 隨機測資用來提高覆蓋率；固定 seed 讓結果可重現。
        rng = random.Random(10226)
        cases = []

        for _ in range(20):
            n = rng.randint(2, 7)
            forbidden = []
            for _ in range(n):
                blocked = {pos for pos in range(1, n + 1) if rng.random() < 0.25}
                forbidden.append(blocked)
            cases.append((n, forbidden))

        data = build_input(cases)
        expected = UVA10226Reference.solve(data)
        actual = run_script(self.target, data)
        self.assertEqual(normalize_output(actual), normalize_output(expected))


if __name__ == "__main__":
    unittest.main()
