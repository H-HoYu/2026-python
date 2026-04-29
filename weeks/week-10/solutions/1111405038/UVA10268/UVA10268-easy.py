import sys


def solve_one(k, n):
    if n == 0:
        return "0"

    # dp[e]：目前丟了 t 次時，e 顆球最多能測的樓層數。
    dp = [0] * (k + 1)

    for t in range(1, 64):
        for e in range(k, 0, -1):
            # 遞推：破掉看下方（e-1），沒破看上方（e），再加當前這層。
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
        # k=0 是結束標記，不處理。
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