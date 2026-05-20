from __future__ import annotations

import argparse
import math
import random
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PYTHON = Path("c:/Users/nvaw1/OneDrive/Desktop/python/2026-python/.venv/Scripts/python.exe")
SOLVERS = [
    ("standard", BASE_DIR / "11063.py"),
    ("easy", BASE_DIR / "11063-easy.py"),
    ("hand", BASE_DIR / "11063-hand.py"),
]


def convert_xyz(red: int, green: int, blue: int) -> tuple[float, float, float]:
    """依題目公式把 RGB 轉成 XYZ。"""
    x_value = 0.5149 * red + 0.3244 * green + 0.1607 * blue
    y_value = 0.2654 * red + 0.6704 * green + 0.0642 * blue
    z_value = 0.0248 * red + 0.1248 * green + 0.8504 * blue
    return x_value, y_value, z_value


def build_cases() -> list[list[tuple[int, int, int]]]:
    """建立固定與隨機測資，涵蓋黑白、邊界值與一般像素。"""
    cases = [
        [(0, 0, 0)],
        [(255, 255, 255)],
        [(255, 3, 192), (10, 20, 30), (7, 8, 9), (100, 150, 200)],
    ]

    rng = random.Random(11063)
    for size in [2, 3, 4, 5]:
        pixels: list[tuple[int, int, int]] = []
        for _ in range(size * size):
            pixels.append((rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255)))
        cases.append(pixels)

    return cases


def build_input_text(pixels: list[tuple[int, int, int]]) -> str:
    """將一張 n x n 影像組成題目輸入。"""
    size = int(math.isqrt(len(pixels)))
    lines = [str(size)]

    for row in range(size):
        parts: list[str] = []
        for column in range(size):
            red, green, blue = pixels[row * size + column]
            parts.extend([str(red), str(green), str(blue)])
        lines.append(" ".join(parts))

    return "\n".join(lines) + "\n"


def build_expected_output(pixels: list[tuple[int, int, int]]) -> str:
    """依題意格式輸出每個像素的 XYZ 與平均 Y。"""
    lines: list[str] = []
    total_y = 0.0

    for red, green, blue in pixels:
        x_value, y_value, z_value = convert_xyz(red, green, blue)
        total_y += y_value
        lines.append(f"{x_value:.4f} {y_value:.4f} {z_value:.4f}")

    average_y = total_y / len(pixels)
    lines.append(f"The average of Y is {average_y:.4f}")
    return "\n".join(lines) + "\n"


def normalize_output(text: str) -> str:
    """統一行尾與末尾空白，避免平台差異影響比對。"""
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").strip().split("\n"))


def run_solver(script_path: Path, input_text: str) -> tuple[int, str, str]:
    """執行解題程式並收集輸出。"""
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
    """執行所有測試並整理成文字報告。"""
    cases = build_cases()
    report_lines = [
        "11063 測試報告",
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
        for case_number, pixels in enumerate(cases, start=1):
            input_text = build_input_text(pixels)
            expected = build_expected_output(pixels)
            return_code, stdout_text, stderr_text = run_solver(script_path, input_text)

            if return_code != 0:
                all_passed = False
                passed = False
                report_lines.append(f"案例 {case_number}: 執行失敗，exit code = {return_code}")
                if stderr_text.strip():
                    report_lines.append("stderr:")
                    report_lines.append(stderr_text.rstrip())
                break

            if normalize_output(stdout_text) != normalize_output(expected):
                all_passed = False
                passed = False
                report_lines.append(f"案例 {case_number}: 輸出不一致")
                report_lines.append("預期輸出:")
                report_lines.extend(expected.rstrip().splitlines()[:10])
                report_lines.append("實際輸出:")
                report_lines.extend(stdout_text.rstrip().splitlines()[:10])
                break

        if passed:
            report_lines.append("結果: 通過")
        report_lines.append("")

    report_lines.append("總結: " + ("全部通過" if all_passed else "有失敗項目"))
    return all_passed, "\n".join(report_lines) + "\n"


def main() -> int:
    """執行測試，並可選擇寫出 log 檔。"""
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