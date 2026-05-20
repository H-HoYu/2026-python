import sys


def main():
    # 先把所有數字都讀進來，第一個是 n，後面每 3 個一組是 RGB。
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return

    n = data[0]
    total_y = 0.0
    count = n * n
    ans = []
    i = 1

    # 每次拿 3 個數字，分別代表一個像素的 R、G、B。
    for _ in range(count):
        r = data[i]
        g = data[i + 1]
        b = data[i + 2]
        i += 3

        x = 0.5149 * r + 0.3244 * g + 0.1607 * b
        y = 0.2654 * r + 0.6704 * g + 0.0642 * b
        z = 0.0248 * r + 0.1248 * g + 0.8504 * b

        total_y += y
        ans.append(f"{x:.4f} {y:.4f} {z:.4f}")

    average_y = total_y / count
    ans.append(f"The average of Y is {average_y:.4f}")
    print("\n".join(ans))


if __name__ == "__main__":
    main()