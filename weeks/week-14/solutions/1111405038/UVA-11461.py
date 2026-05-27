"""UVA 11461 - Square Numbers
一般解題版本
"""

import math
import sys


def count_squares_in_range(a: int, b: int) -> int:
    """回傳閉區間 [a, b] 中完全平方數的個數。"""
    # 最小平方根要 >= sqrt(a)
    left = math.isqrt(a)
    if left * left < a:
        left += 1

    # 最大平方根要 <= sqrt(b)
    right = math.isqrt(b)

    # 根號整數個數即為答案
    return max(0, right - left + 1)


def main() -> None:
    out = []

    # 逐行讀入 a, b，直到 0 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        a, b = map(int, line.split())
        if a == 0 and b == 0:
            break

        out.append(str(count_squares_in_range(a, b)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
