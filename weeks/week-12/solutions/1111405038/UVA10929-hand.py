import sys


def solve() -> None:
    for line in sys.stdin:
        x = line.strip()
        if x == "0":
            break

        if int(x) % 11 == 0:
            print(f"{x} is a multiple of 11.")
        else:
            print(f"{x} is not a multiple of 11.")


if __name__ == "__main__":
    solve()
