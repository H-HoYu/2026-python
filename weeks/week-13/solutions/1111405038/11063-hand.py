import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    n = data[0]
    total_y = 0.0
    count = n * n
    lines = []
    index = 1
    for _ in range(count):
        r = data[index]
        g = data[index + 1]
        b = data[index + 2]
        index += 3
        x = 0.5149 * r + 0.3244 * g + 0.1607 * b
        y = 0.2654 * r + 0.6704 * g + 0.0642 * b
        z = 0.0248 * r + 0.1248 * g + 0.8504 * b
        total_y += y
        lines.append(f"{x:.4f} {y:.4f} {z:.4f}")
    lines.append(f"The average of Y is {total_y / count:.4f}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()