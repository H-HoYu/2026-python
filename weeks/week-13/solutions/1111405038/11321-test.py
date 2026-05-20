from __future__ import annotations

import argparse
import random
import subprocess
from collections import deque
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PYTHON = Path("c:/Users/nvaw1/OneDrive/Desktop/python/2026-python/.venv/Scripts/python.exe")
SOLVERS = [
    ("standard", BASE_DIR / "11321.py"),
    ("easy", BASE_DIR / "11321-easy.py"),
    ("hand", BASE_DIR / "11321-hand.py"),
]
PASS = "<(_ _)>"
FAIL = ">_<"
DIR4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def has_left_to_right_path(rows: int, cols: int, blocked: set[tuple[int, int]]) -> bool:
    """用 BFS 檢查目前是否仍有從左邊界到右邊界的可行路徑。"""
    queue: deque[tuple[int, int]] = deque()
    visited: set[tuple[int, int]] = set()

    for row in range(rows):
        start = (row, 0)
        if start not in blocked:
            queue.append(start)
            visited.add(start)

    while queue:
        row, col = queue.popleft()
        if col == cols - 1:
            return True

        for dr, dc in DIR4:
            nr = row + dr
            nc = col + dc
            nxt = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols and nxt not in blocked and nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)

    return False


def brute_force_answer(rows: int, cols: int, operations: list[tuple[int, int]]) -> list[str]:
    """逐次嘗試放陷阱，若封死道路就回退。"""
    blocked: set[tuple[int, int]] = set()
    results: list[str] = []

    for point in operations:
        blocked.add(point)
        if has_left_to_right_path(rows, cols, blocked):
            results.append(PASS)
        else:
            blocked.remove(point)
            results.append(FAIL)

    return results


def build_cases() -> list[tuple[int, int, list[tuple[int, int]]]]:
    """建立固定案例與隨機案例，讓暴力解能完整驗證。"""
    cases = [
        (3, 3, [(0, 1), (1, 1), (2, 1)]),
        (2, 2, [(0, 0), (1, 1), (0, 1), (1, 0)]),
        (4, 5, [(0, 2), (1, 1), (2, 2), (3, 1), (1, 3)]),
    ]

    rng = random.Random(11321)
    for _ in range(25):
        rows = rng.randint(2, 6)
        cols = rng.randint(2, 6)
        cells = [(r, c) for r in range(rows) for c in range(cols)]
        rng.shuffle(cells)
        op_count = rng.randint(1, min(len(cells), 12))
        operations = cells[:op_count]
        cases.append((rows, cols, operations))

    return cases


def build_input_text(rows: int, cols: int, operations: list[tuple[int, int]]) -> str:
    """依題目格式組出輸入。"""
    lines = [f"{rows} {cols} {len(operations)}"]
    lines.extend(f"{x} {y}" for x, y in operations)
    return "\n".join(lines) + "\n"


def normalize_output(text: str) -> str:
    """統一換行與尾端空白，避免平台差異。"""
    return text.replace("\r\n", "\n").strip()


def run_solver(script_path: Path, input_text: str) -> tuple[int, str, str]:
    """執行指定解題程式。"""
    completed = subprocess.run(
        [str(PYTHON), str(script_path)],
        input=input_text,
        text=True,
        capture_output=True,
        encoding="utf-8",
        cwd=BASE_DIR,
        check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr


def build_report() -> tuple[bool, str]:
    """執行全部測試並整理成報告。"""
    cases = build_cases()
    report_lines = [
        "11321 測試報告",
        f"測試案例數: {len(cases)}",
        "",
    ]
    all_passed = True

    for label, script_path in SOLVERS:
        report_lines.append(f"[{label}] {script_path.name}")
        if not script_path.exists():
            all_passed = False
            report_lines.append("結果: 缺少檔案")
            report_lines.append("")
            continue

        passed = True
        for case_number, (rows, cols, operations) in enumerate(cases, start=1):
            input_text = build_input_text(rows, cols, operations)
            expected = "\n".join(brute_force_answer(rows, cols, operations))
            return_code, stdout_text, stderr_text = run_solver(script_path, input_text)

            if return_code != 0:
                all_passed = False
                passed = False
                report_lines.append(f"案例 {case_number}: 執行失敗，exit code = {return_code}")
                if stderr_text.strip():
                    report_lines.append("stderr:")
                    report_lines.append(stderr_text.rstrip())
                break

            if normalize_output(stdout_text) != expected:
                all_passed = False
                passed = False
                report_lines.append(f"案例 {case_number}: 輸出不一致")
                report_lines.append(f"輸入: rows={rows}, cols={cols}, operations={operations}")
                report_lines.append("預期:")
                report_lines.append(expected)
                report_lines.append("實際:")
                report_lines.append(normalize_output(stdout_text))
                break

        if passed:
            report_lines.append("結果: 通過")
        report_lines.append("")

    report_lines.append("總結: " + ("全部通過" if all_passed else "有失敗項目"))
    return all_passed, "\n".join(report_lines) + "\n"


def main() -> int:
    """執行測試並可選擇寫出 log。"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=Path, help="把測試結果寫入指定文字檔")
    args = parser.parse_args()

    all_passed, report_text = build_report()
    print(report_text, end="")

    if args.log is not None:
        args.log.write_text(report_text, encoding="utf-8")

    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())