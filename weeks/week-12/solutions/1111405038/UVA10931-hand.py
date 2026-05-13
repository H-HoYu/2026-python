import sys


def solve() -> None:
    for line in sys.stdin:
        value = int(line.strip())
        if value == 0:
            break

        binary = bin(value)[2:]
        ones = binary.count("1")
        print(f"The parity of {binary} is {ones} (mod 2).")


if __name__ == "__main__":
    solve()
