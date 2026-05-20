from __future__ import annotations

import argparse
import math
import random
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PYTHON = Path("c:/Users/nvaw1/OneDrive/Desktop/python/2026-python/.venv/Scripts/python.exe")
SOLVERS = [
    ("standard", BASE_DIR / "11332.py"),
    ("easy", BASE_DIR / "11332-easy.py"),
    ("hand", BASE_DIR / "11332-hand.py"),
]
EPS = 1e-10
INF = 1e100
TWO_PI = 2.0 * math.pi


def cross(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx


def distance_on_ray(seg: tuple[int, int, int, int], angle: float) -> float:
    sx, sy, ex, ey = seg
    dx = ex - sx
    dy = ey - sy
    rx = math.cos(angle)
    ry = math.sin(angle)
    den = cross(rx, ry, dx, dy)
    if abs(den) < EPS:
        return INF
    t_value = cross(sx, sy, dx, dy) / den
    u_value = cross(sx, sy, rx, ry) / den
    if t_value <= EPS or u_value < -EPS or u_value > 1.0 + EPS:
        return INF
    return t_value


def brute_visible(segments: list[tuple[int, int, int, int]]) -> list[int]:
    """以高密度角度採樣建立小測資 oracle。"""
    n = len(segments)
    visible = [0] * n
    angles = []

    endpoint_angles = []
    for sx, sy, ex, ey in segments:
        endpoint_angles.append(math.atan2(sy, sx) % TWO_PI)
        endpoint_angles.append(math.atan2(ey, ex) % TWO_PI)

    endpoint_angles.sort()
    angles.extend(endpoint_angles)
    for i in range(len(endpoint_angles)):
        a = endpoint_angles[i]
        b = endpoint_angles[(i + 1) % len(endpoint_angles)]
        if i + 1 == len(endpoint_angles):
            b += TWO_PI
        mid = (a + b) * 0.5
        if mid >= TWO_PI:
            mid -= TWO_PI
        angles.append(mid)

    rng = random.Random(11332)
    for _ in range(1200):
        angles.append(rng.random() * TWO_PI)

    for angle in angles:
        best_id = -1
        best_dist = INF
        for i, seg in enumerate(segments):
            d = distance_on_ray(seg, angle)
            if d < best_dist:
                best_dist = d
                best_id = i
        if best_id != -1 and best_dist < INF / 2:
            visible[best_id] = 1
    return visible


def build_cases() -> list[list[tuple[int, int, int, int]]]:
    """建立可控案例：包含重疊角度遮擋與分離角度可見。"""
    cases = [
        [
            (1, 1, 2, 1),
            (3, 3, 6, 3),
            (1, -2, 2, -2),
        ],
        [
            (2, 1, 2, 3),
            (4, 2, 4, 6),
            (-3, 1, -3, 4),
            (-6, 2, -6, 8),
        ],
        [
            (2, 2, 3, 1),
            (5, 5, 7, 3),
            (2, -1, 4, -2),
            (6, -3, 8, -4),
        ],
    ]

    rng = random.Random(332113)
    for _ in range(18):
        segs: list[tuple[int, int, int, int]] = []
        count = rng.randint(4, 10)
        base_angles = sorted(rng.random() * TWO_PI for _ in range(count))
        for angle in base_angles:
            radius1 = rng.uniform(2.0, 9.0)
            radius2 = radius1 + rng.uniform(0.5, 2.5)
            width = rng.uniform(0.02, 0.18)
            a1 = angle - width
            a2 = angle + width
            sx = int(round(radius1 * math.cos(a1) * 6))
            sy = int(round(radius1 * math.sin(a1) * 6))
            ex = int(round(radius2 * math.cos(a2) * 6))
            ey = int(round(radius2 * math.sin(a2) * 6))
            if sx == 0 and sy == 0:
                sx = 1
            if ex == 0 and ey == 0:
                ex = 1
            segs.append((sx, sy, ex, ey))
        cases.append(segs)

    return cases


def build_input_text(cases: list[list[tuple[int, int, int, int]]]) -> str:
    lines = []
    for segs in cases:
        lines.append(str(len(segs)))
        lines.extend(f"{sx} {sy} {ex} {ey}" for sx, sy, ex, ey in segs)
    lines.append("0")
    return "\n".join(lines) + "\n"


def build_expected_output(cases: list[list[tuple[int, int, int, int]]]) -> str:
    lines = []
    for segs in cases:
        lines.append(" ".join(map(str, brute_visible(segs))))
    return "\n".join(lines) + "\n"


def normalize_output(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").strip().split("\n"))


def run_solver(script_path: Path, input_text: str) -> tuple[int, str, str]:
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
    cases = build_cases()
    input_text = build_input_text(cases)
    expected = build_expected_output(cases)
    report_lines = [
        "11332 測試報告",
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

        code, out, err = run_solver(script_path, input_text)
        if code != 0:
            all_passed = False
            report_lines.append(f"結果: 執行失敗，exit code = {code}")
            if err.strip():
                report_lines.append("stderr:")
                report_lines.append(err.rstrip())
            report_lines.append("")
            continue

        if normalize_output(out) != normalize_output(expected):
            all_passed = False
            report_lines.append("結果: 輸出不一致")
            report_lines.append("預期前 20 行:")
            report_lines.extend(expected.rstrip().splitlines()[:20])
            report_lines.append("實際前 20 行:")
            report_lines.extend(out.rstrip().splitlines()[:20])
            report_lines.append("")
            continue

        report_lines.append("結果: 通過")
        report_lines.append("")

    report_lines.append("總結: " + ("全部通過" if all_passed else "有失敗項目"))
    return all_passed, "\n".join(report_lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=Path, help="把測試結果寫入指定文字檔")
    args = parser.parse_args()

    ok, text = build_report()
    print(text, end="")
    if args.log is not None:
        args.log.write_text(text, encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())