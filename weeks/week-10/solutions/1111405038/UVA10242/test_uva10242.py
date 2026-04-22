import os
import random
import subprocess
import sys
import unittest
from collections import deque
from pathlib import Path


def build_input(n, edges, money, s, bars):
    rows = [f"{n} {len(edges)}"]
    for u, v in edges:
        rows.append(f"{u} {v}")
    for x in money:
        rows.append(str(x))
    rows.append(f"{s} {len(bars)}")
    rows.append(" ".join(map(str, bars)))
    return "\n".join(rows) + "\n"


def reference_bruteforce(n, edges, money, s, bars):
    """小規模暴力：狀態為 (當前點, 已搶集合 mask)。"""
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u - 1].append(v - 1)

    s -= 1
    bar_set = {b - 1 for b in bars}

    start_mask = 1 << s
    start_money = money[s]

    best = {}
    q = deque([(s, start_mask, start_money)])
    best[(s, start_mask)] = start_money

    ans = -1

    while q:
        u, mask, val = q.popleft()

        if u in bar_set:
            ans = max(ans, val)

        for v in g[u]:
            nmask = mask
            gain = 0
            bit = 1 << v
            if (mask & bit) == 0:
                nmask |= bit
                gain = money[v]

            nval = val + gain
            key = (v, nmask)
            if nval > best.get(key, -1):
                best[key] = nval
                q.append((v, nmask, nval))

    return max(ans, 0)


def find_target_script():
    base = Path(__file__).resolve().parent

    env_target = os.environ.get("TARGET_SCRIPT")
    if env_target:
        p = Path(env_target)
        if p.exists() and p.is_file():
            return p

    for name in ["main.py", "solution.py", "uva10242.py", "UVA10242.py"]:
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
    return proc.stdout.strip()


class TestReferenceBruteforce(unittest.TestCase):
    def test_simple_line(self):
        n = 3
        edges = [(1, 2), (2, 3)]
        money = [5, 10, 7]
        s = 1
        bars = [3]
        self.assertEqual(reference_bruteforce(n, edges, money, s, bars), 22)

    def test_cycle_collect_once(self):
        n = 3
        edges = [(1, 2), (2, 1), (2, 3)]
        money = [8, 9, 4]
        s = 1
        bars = [3]
        self.assertEqual(reference_bruteforce(n, edges, money, s, bars), 21)


class TestCandidateProgram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target = find_target_script()
        if cls.target is None:
            raise unittest.SkipTest(
                "找不到受測程式。請在同資料夾提供 main.py/solution.py/uva10242.py，"
                "或設定環境變數 TARGET_SCRIPT。"
            )

    def test_fixed_cases(self):
        cases = [
            (3, [(1, 2), (2, 3)], [5, 10, 7], 1, [3]),
            (3, [(1, 2), (2, 1), (2, 3)], [8, 9, 4], 1, [3]),
            (4, [(1, 2), (2, 3), (3, 2), (3, 4)], [2, 5, 6, 10], 1, [4]),
            (4, [(1, 2), (2, 1), (3, 4)], [7, 8, 20, 30], 1, [4, 2]),
        ]

        for n, edges, money, s, bars in cases:
            data = build_input(n, edges, money, s, bars)
            expected = str(reference_bruteforce(n, edges, money, s, bars))
            actual = run_script(self.target, data)
            self.assertEqual(actual, expected)

    def test_random_small_cases(self):
        # 小規模隨機圖，用暴力結果交叉驗證。
        rng = random.Random(10242)

        for _ in range(25):
            n = rng.randint(2, 8)
            max_edges = n * n
            m = rng.randint(n - 1, min(max_edges, 18))

            edges = []
            used = set()
            while len(edges) < m:
                u = rng.randint(1, n)
                v = rng.randint(1, n)
                if (u, v) in used:
                    continue
                used.add((u, v))
                edges.append((u, v))

            money = [rng.randint(1, 20) for _ in range(n)]
            s = rng.randint(1, n)
            p = rng.randint(1, n)
            bars = rng.sample(list(range(1, n + 1)), p)

            data = build_input(n, edges, money, s, bars)
            expected = str(reference_bruteforce(n, edges, money, s, bars))
            actual = run_script(self.target, data)
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
