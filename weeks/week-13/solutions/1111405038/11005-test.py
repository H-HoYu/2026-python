from __future__ import annotations

import argparse
import random
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SOLVERS = [
    ("standard", BASE_DIR / "11005.py"),
    ("easy", BASE_DIR / "11005-easy.py"),
    ("hand", BASE_DIR / "11005-hand.py"),
]


def digit_cost(number: int, base: int, costs: list[int]) -> int:
    """計算十進位數字在指定進位下的總印刷成本。"""
    if number == 0:
        return costs[0]

    total = 0
    current = number
    while current > 0:
        total += costs[current % base]
        current //= base
    return total


def cheapest_bases(number: int, costs: list[int]) -> list[int]:
    """用直接枚舉的方式求出所有最低成本的進位。"""
    best_cost = None
    best_bases: list[int] = []

    for base in range(2, 37):
        current_cost = digit_cost(number, base, costs)
        if best_cost is None or current_cost < best_cost:
            best_cost = current_cost
            best_bases = [base]
        elif current_cost == best_cost:
            best_bases.append(base)

    return best_bases


def build_expected_output(cases: list[tuple[list[int], list[int]]]) -> str:
    """依照題目格式產生正確答案，作為測試基準。"""
    lines: list[str] = []

    for case_index, (costs, queries) in enumerate(cases, start=1):
        lines.append(f"Case {case_index}:")
        for number in queries:
            bases = cheapest_bases(number, costs)
            bases_text = " ".join(str(base) for base in bases)
            lines.append(f"Cheapest base(s) for number {number}: {bases_text}")
        if case_index != len(cases):
            lines.append("")

    return "\n".join(lines) + "\n"


def build_input_text(cases: list[tuple[list[int], list[int]]]) -> str:
    """把測試案例組裝成題目輸入格式。"""
    lines = [str(len(cases))]

    for costs, queries in cases:
        for offset in range(0, 36, 9):
            lines.append(" ".join(str(value) for value in costs[offset : offset + 9]))
        lines.append(str(len(queries)))
        lines.extend(str(number) for number in queries)

    return "\n".join(lines) + "\n"


def generate_cases() -> list[tuple[list[int], list[int]]]:
    """建立固定案例與隨機案例，兼顧邊界值與一般情況。"""
    cases: list[tuple[list[int], list[int]]] = [
        ([1] * 36, [0, 1, 10, 31, 32, 255, 1024]),
        (list(range(1, 37)), [0, 2, 35, 36, 12345, 2_000_000_000]),
        (list(range(36, 0, -1)), [0, 7, 15, 255, 4096, 999_999_937]),
    ]

    rng = random.Random(11005)
    for _ in range(12):
        costs = [rng.randint(1, 30) for _ in range(36)]
        queries = [rng.randint(0, 2_000_000_000) for _ in range(6)]
        cases.append((costs, queries))

    return cases


def normalize_output(text: str) -> str:
    """統一行尾並忽略檔尾多餘空白，避免平台差異。"""
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").strip().split("\n"))


def run_solver(script_path: Path, input_text: str) -> tuple[int, str, str]:
    """執行指定解題程式並回傳結束碼、標準輸出、標準錯誤。"""
    completed = subprocess.run(
        [sys.executable, str(script_path)],
        input=input_text,
        text=True,
        capture_output=True,
        encoding="utf-8",
        cwd=BASE_DIR,
        check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr


def build_report() -> tuple[bool, str]:
    """產生完整測試報告。"""
    cases = generate_cases()
    input_text = build_input_text(cases)
    expected_output = build_expected_output(cases)

    report_lines = [
        "11005 測試報告",
        f"測試資料組數: {len(cases)}",
        f"查詢總數: {sum(len(queries) for _, queries in cases)}",
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

        return_code, stdout_text, stderr_text = run_solver(script_path, input_text)
        if return_code != 0:
            all_passed = False
            report_lines.append(f"結果: 執行失敗，exit code = {return_code}")
            if stderr_text.strip():
                report_lines.append("stderr:")
                report_lines.append(stderr_text.rstrip())
            report_lines.append("")
            continue

        if normalize_output(stdout_text) != normalize_output(expected_output):
            all_passed = False
            report_lines.append("結果: 輸出不一致")
            report_lines.append("預期輸出前 20 行:")
            report_lines.extend(expected_output.rstrip().splitlines()[:20])
            report_lines.append("實際輸出前 20 行:")
            report_lines.extend(stdout_text.rstrip().splitlines()[:20])
            report_lines.append("")
            continue

        report_lines.append("結果: 通過")
        report_lines.append("")

    report_lines.append("總結: " + ("全部通過" if all_passed else "有失敗項目"))
    report_text = "\n".join(report_lines) + "\n"
    return all_passed, report_text


def main() -> int:
    """執行測試，必要時同步寫出 log 檔。"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=Path, help="把測試結果另外寫入指定檔案")
    args = parser.parse_args()

    all_passed, report_text = build_report()
    print(report_text, end="")

    if args.log is not None:
        args.log.write_text(report_text, encoding="utf-8")

    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())