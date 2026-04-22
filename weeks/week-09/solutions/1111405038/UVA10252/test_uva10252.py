import os
import random
import subprocess
import sys
import unittest
from pathlib import Path


def build_input(cases):
    rows = [str(len(cases))]
    for pts in cases:
        rows.append(str(len(pts)))
        for x, y in pts:
            rows.append(f"{x} {y}")
    return "\n".join(rows) + "\n"


def brute_force_case(points):
    """小資料暴力：枚舉整數點找最小總曼哈頓距離與解數。"""
    xs = [x for x, _ in points]
    ys = [y for _, y in points]

    lx = min(xs) - 2
    rx = max(xs) + 2
    ly = min(ys) - 2
    ry = max(ys) + 2

    best = None
    cnt = 0

    for px in range(lx, rx + 1):
        for py in range(ly, ry + 1):
            val = 0
            for x, y in points:
                val += abs(px - x) + abs(py - y)

            if best is None or val < best:
                best = val
                cnt = 1
            elif val == best:
                cnt += 1

    return best, cnt


def reference_case(points):
    """參考解：L1 距離可分成 x 與 y 兩個一維中位數問題。"""
    n = len(points)
    xs = sorted(x for x, _ in points)
    ys = sorted(y for _, y in points)

    if n % 2 == 1:
        mx = xs[n // 2]
        my = ys[n // 2]
        cntx = 1
        cnty = 1
    else:
        lx, rx = xs[n // 2 - 1], xs[n // 2]
        ly, ry = ys[n // 2 - 1], ys[n // 2]
        mx = lx
        my = ly
        cntx = rx - lx + 1
        cnty = ry - ly + 1

    best = sum(abs(x - mx) for x, _ in points) + sum(abs(y - my) for _, y in points)
    return best, cntx * cnty


def reference_solve(raw):
    arr = list(map(int, raw.split()))
    it = iter(arr)
    t = next(it)
    out = []

    for _ in range(t):
        n = next(it)
        pts = [(next(it), next(it)) for _ in range(n)]
        best, cnt = reference_case(pts)
        out.append(f"{best} {cnt}")

    return "\n".join(out)


def find_target_script():
    base = Path(__file__).resolve().parent

    env_target = os.environ.get("TARGET_SCRIPT")
    if env_target:
        p = Path(env_target)
        if p.exists() and p.is_file():
            return p

    for name in ["main.py", "solution.py", "uva10252.py", "UVA10252.py"]:
        p = base / name
        if p.exists() and p.is_file():
            return p

    return None


def run_script(target, input_data):
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
    return "\n".join(line.rstrip() for line in proc.stdout.strip().splitlines())


class TestReference(unittest.TestCase):
    def test_story_example_like(self):
        pts = [(0, 0), (1, 1), (2, 2)]
        self.assertEqual(reference_case(pts), (4, 1))

    def test_even_case_has_multiple_answers(self):
        pts = [(0, 0), (2, 0)]
        self.assertEqual(reference_case(pts), (2, 3))

    def test_bruteforce_match_random(self):
        rng = random.Random(10252)
        for _ in range(60):
            n = rng.randint(1, 7)
            pts = [(rng.randint(-4, 4), rng.randint(-4, 4)) for _ in range(n)]
            self.assertEqual(reference_case(pts), brute_force_case(pts))


class TestCandidateProgram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target = find_target_script()
        if cls.target is None:
            raise unittest.SkipTest(
                "找不到受測程式。請在同資料夾提供 main.py/solution.py/uva10252.py，"
                "或設定環境變數 TARGET_SCRIPT。"
            )

    def test_fixed_cases(self):
        cases = [
            [(0, 0), (1, 1), (2, 2)],
            [(0, 0), (2, 0)],
            [(-1, -1), (1, 1), (1, -1), (-1, 1)],
            [(3, 5)],
        ]
        data = build_input(cases)
        expected = reference_solve(data)
        actual = run_script(self.target, data)
        self.assertEqual(actual, expected)

    def test_random_cases(self):
        rng = random.Random(252)
        cases = []
        for _ in range(35):
            n = rng.randint(1, 12)
            pts = [(rng.randint(-8, 8), rng.randint(-8, 8)) for _ in range(n)]
            cases.append(pts)

        data = build_input(cases)
        expected = reference_solve(data)
        actual = run_script(self.target, data)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
