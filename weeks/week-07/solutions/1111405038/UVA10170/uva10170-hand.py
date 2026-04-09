import sys


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        S, D = map(int, line.split())

        lo, hi = 1, 2 * 10**15 + 2

        while lo < hi:
            mid = (lo + hi) // 2
            if mid * S + mid * (mid - 1) // 2 >= D:
                hi = mid
            else:
                lo = mid + 1

        print(S + lo - 1)


if __name__ == '__main__':
    main()
