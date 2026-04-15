import math
import sys


def solve(s, a, unit):
    # 地心到衛星距離 = 地球半徑 + 高度
    r = 6440.0 + s

    # 輸入若是分(min)先換成度(deg)
    deg = a / 60.0 if unit == "min" else a

    # 取較小夾角（題目要求）
    if deg > 180.0:
        deg = 360.0 - deg

    # 角度轉弧度後，依公式計算弧長與弦長
    rad = math.radians(deg)
    arc = r * rad
    chord = 2.0 * r * math.sin(rad / 2.0)
    return arc, chord


def main():
    # 逐行讀到 EOF，每行格式: s a unit
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        s, a, unit = line.split()
        arc, chord = solve(float(s), float(a), unit)
        # 輸出固定到小數點後六位
        print(f"{arc:.6f} {chord:.6f}")


if __name__ == "__main__":
    main()
