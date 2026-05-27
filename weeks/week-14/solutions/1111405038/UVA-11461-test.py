"""UVA 11461 測試程式
自動比對一般版、easy、hand 輸出，並寫入 txt log。
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import math
import random
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent
TARGETS = [
    "UVA-11461.py",
    "UVA-11461-easy.py",
    "UVA-11461-hand.py",
]
LOG_FILE = BASE_DIR / "UVA-11461-test-log.txt"


def expected_count(a: int, b: int) -> int:
    left = math.isqrt(a)
    if left * left < a:
        left += 1
    right = math.isqrt(b)
    return max(0, right - left + 1)


def run_target(script_name: str, input_data: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, str(BASE_DIR / script_name)],
        input=input_data,
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def main() -> int:
    random.seed(11461)

    tests: list[tuple[int, int]] = [
        (1, 4),
        (1, 10),
        (1, 100000),
        (81, 81),
        (82, 99),
        (99999, 100000),
    ]

    for _ in range(30):
        a = random.randint(1, 100000)
        b = random.randint(a, 100000)
        tests.append((a, b))

    input_data = "\n".join(f"{a} {b}" for a, b in tests) + "\n0 0\n"
    expected = "\n".join(str(expected_count(a, b)) for a, b in tests)

    lines = [
        f"[Time] {datetime.now().isoformat(timespec='seconds')}",
        f"[Test Count] {len(tests)}",
        "",
    ]

    all_pass = True

    for target in TARGETS:
        code, out, err = run_target(target, input_data)
        ok = (code == 0 and out == expected)
        all_pass = all_pass and ok

        lines.append(f"[Target] {target}")
        lines.append(f"[Exit Code] {code}")
        lines.append(f"[Result] {'PASS' if ok else 'FAIL'}")

        if not ok:
            lines.append("[Expected]")
            lines.append(expected)
            lines.append("[Actual]")
            lines.append(out)
            if err:
                lines.append("[Stderr]")
                lines.append(err)

        lines.append("")

    LOG_FILE.write_text("\n".join(lines), encoding="utf-8")

    print("PASS" if all_pass else "FAIL")
    print(f"log: {LOG_FILE}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
