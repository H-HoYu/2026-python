import math
import sys


def solve(s, a, unit):
    r = 6440.0 + s


    deg = a / 60.0 if unit == "min" else a


    if deg > 180.0:
        deg = 360.0 - deg

    rad = math.radians(deg)
    arc = r * rad
    chord = 2.0 * r * math.sin(rad / 2.0)
    return arc, chord


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        s, a, unit = line.split()
        arc, chord = solve(float(s), float(a), unit)

        print(f"{arc:.6f} {chord:.6f}")


if __name__ == "__main__":
    main()
