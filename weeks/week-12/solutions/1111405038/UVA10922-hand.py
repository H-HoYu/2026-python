import sys


def solve() -> None:
    for line in sys.stdin:
        x = line.strip()
        if x == "0":
            break

        s = x
        degree = 0
        while True:
            s = str(sum(int(c) for c in s))
            degree += 1
            if len(s) == 1:
                break

        if s == "9":
            print(f"9-degree of {x} is {degree}.")
        else:
            print(f"{x} is not a multiple of 9.")


if __name__ == "__main__":
    solve()
