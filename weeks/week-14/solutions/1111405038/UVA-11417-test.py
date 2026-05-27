"""UVA 11417 測試程式
比對一般版、easy 版、hand 版輸出是否一致，並將結果寫入 txt log。
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
    "UVA-11417.py",
    "UVA-11417-easy.py",
    "UVA-11417-hand.py",
]
LOG_FILE = BASE_DIR / "UVA-11417-test-log.txt"


def expected_for_n(n: int) -> int:
    """用直觀方式計算標準答案。"""
    s = 0
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            s += math.gcd(i, j)
    return s


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
    random.seed(11417)

    # 含題目範例 + 隨機小測資（讓 easy 版也能快速跑完）
    tests = [10, 100, 500]
    tests.extend(random.randint(2, 120) for _ in range(20))

    input_data = "\n".join(map(str, tests + [0])) + "\n"
    expected = "\n".join(str(expected_for_n(n)) for n in tests)

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
