import sys


def solve_one(k, n):
    if n == 0:
        return "0"

    dp = [0] * (k + 1)

    for t in range(1, 64):
        for e in range(k, 0, -1):
            dp[e] = dp[e] + dp[e - 1] + 1
        if dp[k] >= n:
            return str(t)

    return "More than 63 trials needed."


def solve(text):
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        k, n = map(int, line.split())
        if k == 0:
            break

        out.append(solve_one(k, n))

    return "\n".join(out)


def main():
    data = sys.stdin.buffer.read().decode()
    ans = solve(data)
    if ans:
        sys.stdout.write(ans)


if __name__ == "__main__":
    main()
