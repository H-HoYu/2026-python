"""UVA 11349 測試程式
自動產生測資並比對三個版本的輸出，結果寫入 log。
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import random
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent
TARGETS = [
    "UVA-11349.py",
    "UVA-11349-easy.py",
    "UVA-11349-hand.py",
]
LOG_FILE = BASE_DIR / "UVA-11349-test.log"


def parse_and_judge(input_data: str) -> str:
    """參考判斷器：直接依題意計算正確輸出。"""
    lines = input_data.strip().splitlines()
    t = int(lines[0].strip())
    idx = 1
    out = []

    for case_no in range(1, t + 1):
        n = int(lines[idx].split("=")[1].strip())
        idx += 1

        m = []
        for _ in range(n):
            m.append(list(map(int, lines[idx].split())))
            idx += 1

        ok = True
        for i in range(n):
            for j in range(n):
                if m[i][j] < 0 or m[i][j] != m[n - 1 - i][n - 1 - j]:
                    ok = False
                    break
            if not ok:
                break

        out.append(f"Test #{case_no}: {'Symmetric.' if ok else 'Non-symmetric.'}")

    return "\n".join(out)


def make_case(n: int, should_be_symmetric: bool) -> list[list[int]]:
    """產生一組 n x n 測資。"""
    if should_be_symmetric:
        m = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                ni, nj = n - 1 - i, n - 1 - j
                if i > ni or (i == ni and j > nj):
                    continue
                val = random.randint(0, 30)
                m[i][j] = val
                m[ni][nj] = val
        return m

    m = [[random.randint(0, 30) for _ in range(n)] for _ in range(n)]
    mode = random.choice(["negative", "mismatch"])
    if mode == "negative":
        i, j = random.randrange(n), random.randrange(n)
        m[i][j] = -random.randint(1, 30)
    else:
        i, j = random.randrange(n), random.randrange(n)
        ni, nj = n - 1 - i, n - 1 - j
        m[i][j] = 7
        m[ni][nj] = 11
    return m


def build_input(cases: list[list[list[int]]]) -> str:
    lines = [str(len(cases))]
    for m in cases:
        n = len(m)
        lines.append(f"N = {n}")
        for row in m:
            lines.append(" ".join(map(str, row)))
    return "\n".join(lines) + "\n"


def run_target(script_name: str, test_input: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, str(BASE_DIR / script_name)],
        input=test_input,
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def main() -> int:
    random.seed(11349)

    cases = []
    # 題目範例
    cases.append([[5, 1, 3], [2, 0, 2], [3, 1, 5]])
    cases.append([[5, 1, 3], [2, 0, 2], [0, 1, 5]])

    # 隨機測資
    for _ in range(40):
        n = random.randint(1, 8)
        cases.append(make_case(n, should_be_symmetric=random.choice([True, False])))

    test_input = build_input(cases)
    expected = parse_and_judge(test_input)

    log_lines = [
        f"[Time] {datetime.now().isoformat(timespec='seconds')}",
        f"[Total Cases] {len(cases)}",
        "",
    ]

    all_pass = True

    for name in TARGETS:
        code, out, err = run_target(name, test_input)
        ok = code == 0 and out == expected
        all_pass = all_pass and ok

        log_lines.append(f"[Target] {name}")
        log_lines.append(f"[Exit Code] {code}")
        log_lines.append(f"[Result] {'PASS' if ok else 'FAIL'}")

        if not ok:
            log_lines.append("[Expected]")
            log_lines.append(expected)
            log_lines.append("[Actual]")
            log_lines.append(out)
            if err:
                log_lines.append("[Stderr]")
                log_lines.append(err)
        log_lines.append("")

    LOG_FILE.write_text("\n".join(log_lines), encoding="utf-8")

    print("PASS" if all_pass else "FAIL")
    print(f"log: {LOG_FILE}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
