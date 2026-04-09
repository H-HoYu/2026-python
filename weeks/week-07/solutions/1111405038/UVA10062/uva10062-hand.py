import sys


def main() -> None:
    

    data = sys.stdin.read().strip().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))

    smaller = [0] * (n + 1)
    for pos in range(2, n + 1):
        try:
            smaller[pos] = int(next(it))
        except StopIteration:
            smaller[pos] = 0

    available = list(range(1, n + 1))

    result = [0] * (n + 1)

    for pos in range(n, 1, -1):
        k = smaller[pos]
        result[pos] = available.pop(k)

    if n >= 1:
        result[1] = available.pop(0)

    out = "\n".join(str(result[pos]) for pos in range(1, n + 1))
    sys.stdout.write(out)


if __name__ == "__main__":
    main()
