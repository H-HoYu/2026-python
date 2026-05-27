"""UVA 12019 - Doom's Day Algorithm
一般解題版本
"""

import sys


# 2012 年每月天數（閏年）
DAYS_IN_MONTH = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# 題目要求輸出英文全名
WEEKDAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]


def get_weekday_2012(month: int, day: int) -> str:
    """回傳 2012 年該日期對應的星期。"""
    # 2012-01-01 是 Sunday，先算從 1/1 經過幾天
    offset = sum(DAYS_IN_MONTH[: month - 1]) + (day - 1)
    return WEEKDAYS[offset % 7]


def main() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []

    for _ in range(t):
        m = int(data[idx])
        d = int(data[idx + 1])
        idx += 2
        out.append(get_weekday_2012(m, d))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
