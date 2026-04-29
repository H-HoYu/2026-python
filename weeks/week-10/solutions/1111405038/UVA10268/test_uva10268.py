import os
import subprocess
import sys
import unittest
from functools import lru_cache
from pathlib import Path


def build_input(cases):
    rows = [f"{k} {n}" for k, n in cases]
    rows.append("0 0")
    return "\n".join(rows) + "\n"


def min_trials_reference(k, n):
    """參考解：用可測樓層數 DP，最多試到 63 次。"""
    if n == 0:
        return "0"

    dp = [0] * (k + 1)

    for t in range(1, 64):
        for e in range(k, 0, -1):
            # f[t][e] = f[t-1][e-1] + f[t-1][e] + 1
            dp[e] = dp[e] + dp[e - 1] + 1
        if dp[k] >= n:
            return str(t)

    return "More than 63 trials needed."


def reference_solve(raw):
    out = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        k, n = map(int, line.split())
        if k == 0:
            break
        out.append(min_trials_reference(k, n))
    return "\n".join(out)


@lru_cache(maxsize=None)
def brute_small(k, n):
    """小資料暴力：回傳最少最壞次數。"""
    if n <= 0:
        return 0
    if k == 0:
        return 10**9
    if k == 1:
        return n

    best = 10**9
    for x in range(1, n + 1):
        # 破：樓下 x-1；不破：樓上 n-x
        need = 1 + max(brute_small(k - 1, x - 1), brute_small(k, n - x))
        if need < best:
            best = need

    return best


def find_target_script():
    base = Path(__file__).resolve().parent

    env_target = os.environ.get("TARGET_SCRIPT")
    if env_target:
        p = Path(env_target)
        if p.exists() and p.is_file():
            return p

    for name in ["main.py", "solution.py", "uva10268.py", "UVA10268.py"]:
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
    def test_known_small(self):
        self.assertEqual(min_trials_reference(1, 10), "10")
        self.assertEqual(min_trials_reference(2, 10), "4")
        self.assertEqual(min_trials_reference(2, 100), "14")

    def test_over_63(self):
        self.assertEqual(min_trials_reference(1, 64), "More than 63 trials needed.")

    def test_bruteforce_crosscheck(self):
        # 用小範圍暴力交叉驗證參考解。
        for k in range(1, 6):
            for n in range(0, 25):
                brute = brute_small(k, n)
                ref = min_trials_reference(k, n)
                if brute > 63:
                    self.assertEqual(ref, "More than 63 trials needed.")
                else:
                    self.assertEqual(ref, str(brute))


class TestCandidateProgram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target = find_target_script()
        if cls.target is None:
            raise unittest.SkipTest(
                "找不到受測程式。請在同資料夾提供 main.py/solution.py/uva10268.py，"
                "或設定環境變數 TARGET_SCRIPT。"
            )

    def test_fixed_cases(self):
        cases = [
            (1, 10),
            (2, 10),
            (2, 100),
            (3, 1000),
            (1, 64),
            (100, 9223372036854775807),
        ]
        data = build_input(cases)
        expected = reference_solve(data)
        actual = run_script(self.target, data)
        self.assertEqual(actual, expected)

    def test_many_cases(self):
        cases = []
        for k in [1, 2, 3, 5, 10, 50, 100]:
            for n in [0, 1, 2, 3, 10, 50, 100, 1000, 10**6, 10**12]:
                cases.append((k, n))

        data = build_input(cases)
        expected = reference_solve(data)
        actual = run_script(self.target, data)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()