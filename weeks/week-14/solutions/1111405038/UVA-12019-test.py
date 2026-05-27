"""UVA 12019 測試程式
驗證一般版、easy、hand 輸出一致，並寫入 txt log。
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import random
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent
TARGETS = [
    "UVA-12019.py",
    "UVA-12019-easy.py",
    "UVA-12019-hand.py",
]
LOG_FILE = BASE_DIR / "UVA-12019-test-log.txt"


def expected_weekday(m: int, d: int) -> str:
    return date(2012, m, d).strftime("%A")


def run_target(script_name: str, input_data: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, str(BASE_DIR / script_name)],
        input=input_data,
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def random_date_2012() -> tuple[int, int]:
    month = random.randint(1, 12)
    mdays = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]
    day = random.randint(1, mdays)
    return month, day


def main() -> int:
    random.seed(12019)

    tests: list[tuple[int, int]] = [
        (1, 1),
        (2, 29),
        (12, 31),
        (3, 7),
        (10, 10),
    ]
    tests.extend(random_date_2012() for _ in range(40))

    input_data = str(len(tests)) + "\n" + "\n".join(f"{m} {d}" for m, d in tests) + "\n"
    expected = "\n".join(expected_weekday(m, d) for m, d in tests)

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
