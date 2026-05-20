from __future__ import annotations

import argparse
import random
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PYTHON = Path("c:/Users/nvaw1/OneDrive/Desktop/python/2026-python/.venv/Scripts/python.exe")
SOLVERS = [
    ("standard", BASE_DIR / "11150.py"),
    ("easy", BASE_DIR / "11150-easy.py"),
    ("hand", BASE_DIR / "11150-hand.py"),
]
INF = 10**9


def brute_force_answer(length: int, min_jump: int, max_jump: int, stones: list[int]) -> int:
    """直接在完整數線上做 DP，作為小測資的正解。"""
    stone_set = set(stones)
    dp = [INF] * (length + max_jump + 1)
    dp[0] = 0

    for position in range(length):
        if dp[position] == INF:
            continue
        for jump in range(min_jump, max_jump + 1):
            next_position = position + jump
            if next_position >= length:
                continue
            cost = 1 if next_position in stone_set else 0
            if dp[position] + cost < dp[next_position]:
                dp[next_position] = dp[position] + cost

    answer = INF
    for position in range(length, length + max_jump + 1):
        if position < len(dp):
            answer = min(answer, dp[position])

    for position in range(length):
        if dp[position] == INF:
            continue
        for jump in range(min_jump, max_jump + 1):
            if position + jump >= length:
                answer = min(answer, dp[position])

    return answer


def build_cases() -> list[tuple[int, int, int, list[int]]]:
    """建立固定與隨機案例，讓暴力驗證可以完整覆蓋。"""
    cases = [
        (10, 2, 3, [2, 4, 7]),
        (12, 3, 3, [3, 6, 9]),
        (15, 2, 4, [1, 5, 6, 10, 14]),
        (20, 1, 2, [2, 3, 5, 8, 13]),
        (25, 3, 5, [4, 7, 8, 11, 17, 20]),
    ]

    rng = random.Random(11150)
    for _ in range(25):
        length = rng.randint(5, 40)
        min_jump = rng.randint(1, 5)
        max_jump = rng.randint(min_jump, 6)
        max_stones = min(length - 1, 10)
        stone_count = rng.randint(1, max_stones)
        stones = sorted(rng.sample(range(1, length), stone_count))
        cases.append((length, min_jump, max_jump, stones))

    return cases


def build_input_text(length: int, min_jump: int, max_jump: int, stones: list[int]) -> str:
    """依題目格式組出單筆測資輸入。"""
    lines = [str(length), f"{min_jump} {max_jump} {len(stones)}", " ".join(str(value) for value in stones)]
    return "\n".join(lines) + "\n"


def normalize_output(text: str) -> str:
    """統一輸出格式，避免行尾差異造成誤判。"""
    return text.replace("\r\n", "\n").strip()


def run_solver(script_path: Path, input_text: str) -> tuple[int, str, str]:
    """執行指定解題程式並回傳結果。"""
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
    """執行所有測試並產生報告。"""
    cases = build_cases()
    report_lines = [
        "11150 測試報告",
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
        for case_number, (length, min_jump, max_jump, stones) in enumerate(cases, start=1):
            input_text = build_input_text(length, min_jump, max_jump, stones)
            expected = str(brute_force_answer(length, min_jump, max_jump, stones))
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
                report_lines.append(f"輸入: L={length}, S={min_jump}, T={max_jump}, stones={stones}")
                report_lines.append(f"預期: {expected}")
                report_lines.append(f"實際: {normalize_output(stdout_text)}")
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