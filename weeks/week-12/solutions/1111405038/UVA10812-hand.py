import sys


def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return

    count = int(data[0])
    index = 1
    results = []

    for _ in range(count):
        total = int(data[index])
        diff = int(data[index + 1])
        index += 2

        if total < diff or (total + diff) % 2 != 0:
            results.append("impossible")
            continue

        big = (total + diff) // 2
        small = (total - diff) // 2

        if small < 0:
            results.append("impossible")
        else:
            results.append(f"{big} {small}")

    sys.stdout.write("\n".join(results))


if __name__ == "__main__":
    solve()