import os
import random
import subprocess
import sys
import unittest
from pathlib import Path

MOD = 1_000_000_007


def parse_grid_line(line: str) -> str:
    # 支援 "0101" 或 "0 1 0 1" 兩種輸入。
    s = line.strip()
    parts = s.split()
    if len(parts) > 1:
        return "".join(parts)
    return s


def build_input(cases):
    rows = [str(len(cases))]
    for n, m, grid in cases:
        rows.append(f"{n} {m}")
        rows.extend(grid)
    return "\n".join(rows) + "\n"


def reference_count_bruteforce(grid):
    """小規模暴力解：枚舉邊是否選用，驗證每個可用格子度數恰為 2。"""
    n = len(grid)
    m = len(grid[0]) if n else 0

    idx = {}
    verts = []
    for r in range(n):
        for c in range(m):
            if grid[r][c] == "1":
                idx[(r, c)] = len(verts)
                verts.append((r, c))

    vcnt = len(verts)
    if vcnt == 0:
        # 可以一條蛇都不擺，空集合視為合法。
        return 1

    edges = []
    incident = [[] for _ in range(vcnt)]

    for r, c in verts:
        u = idx[(r, c)]
        if r + 1 < n and grid[r + 1][c] == "1":
            v = idx[(r + 1, c)]
            eid = len(edges)
            edges.append((u, v))
            incident[u].append(eid)
            incident[v].append(eid)
        if c + 1 < m and grid[r][c + 1] == "1":
            v = idx[(r, c + 1)]
            eid = len(edges)
            edges.append((u, v))
            incident[u].append(eid)
            incident[v].append(eid)

    # 若某點在完整圖中度數不足 2，不可能形成環。
    for u in range(vcnt):
        if len(incident[u]) < 2:
            return 0

    e = len(edges)
    deg = [0] * vcnt
    ans = 0

    # 預先算每個頂點在每個步驟之後最多還有幾條邊可用，做剪枝。
    remain = [[0] * (e + 1) for _ in range(vcnt)]
    for u in range(vcnt):
        seen = [0] * e
        for eid in incident[u]:
            seen[eid] = 1
        for i in range(e - 1, -1, -1):
            remain[u][i] = remain[u][i + 1] + seen[i]

    def dfs(i):
        nonlocal ans

        # 度數過大或即使全拿也補不到 2，直接剪枝。
        for u in range(vcnt):
            if deg[u] > 2:
                return
            if deg[u] + remain[u][i] < 2:
                return

        if i == e:
            if all(d == 2 for d in deg):
                ans += 1
            return

        u, v = edges[i]

        # 不選這條邊。
        dfs(i + 1)

        # 選這條邊。
        deg[u] += 1
        deg[v] += 1
        dfs(i + 1)
        deg[u] -= 1
        deg[v] -= 1

    dfs(0)
    return ans % MOD


def reference_solve(raw: str) -> str:
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if not lines:
        return ""

    t = int(lines[0])
    idx = 1
    out = []

    for case_id in range(1, t + 1):
        n, m = map(int, lines[idx].split())
        idx += 1

        grid = []
        for _ in range(n):
            grid.append(parse_grid_line(lines[idx]))
            idx += 1

        val = reference_count_bruteforce(grid)
        out.append(f"Case {case_id}: {val}")

    return "\n".join(out)


def normalize_output(s: str) -> str:
    return "\n".join(line.rstrip() for line in s.strip().splitlines()) if s.strip() else ""


def find_target_script() -> Path | None:
    base = Path(__file__).resolve().parent

    env_target = os.environ.get("TARGET_SCRIPT")
    if env_target:
        p = Path(env_target)
        if p.exists() and p.is_file():
            return p

    for name in ["main.py", "solution.py", "uva10235.py", "UVA10235.py"]:
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


class TestReferenceSolver(unittest.TestCase):
    def test_empty_grid(self):
        raw = "1\n1 1\n0\n"
        self.assertEqual(reference_solve(raw), "Case 1: 1")

    def test_single_cell_open(self):
        raw = "1\n1 1\n1\n"
        self.assertEqual(reference_solve(raw), "Case 1: 0")

    def test_small_square(self):
        raw = "1\n2 2\n11\n11\n"
        self.assertEqual(reference_solve(raw), "Case 1: 1")


class TestCandidateProgram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target = find_target_script()
        if cls.target is None:
            raise unittest.SkipTest(
                "找不到受測程式。請在同資料夾提供 main.py/solution.py/uva10235.py，"
                "或設定環境變數 TARGET_SCRIPT。"
            )

    def test_fixed_cases(self):
        cases = [
            (1, 1, ["0"]),
            (1, 1, ["1"]),
            (2, 2, ["11", "11"]),
            (2, 3, ["111", "111"]),
            (3, 3, ["111", "101", "111"]),
        ]
        data = build_input(cases)
        expected = reference_solve(data)
        actual = run_script(self.target, data)
        self.assertEqual(normalize_output(actual), normalize_output(expected))

    def test_random_small_cases(self):
        # 隨機小圖用暴力解交叉驗證，固定 seed 可重現。
        rng = random.Random(10235)
        cases = []
        for _ in range(20):
            n = rng.randint(1, 3)
            m = rng.randint(1, 3)
            grid = []
            for _r in range(n):
                row = "".join("1" if rng.random() < 0.7 else "0" for _c in range(m))
                grid.append(row)
            cases.append((n, m, grid))

        data = build_input(cases)
        expected = reference_solve(data)
        actual = run_script(self.target, data)
        self.assertEqual(normalize_output(actual), normalize_output(expected))


if __name__ == "__main__":
    unittest.main()
