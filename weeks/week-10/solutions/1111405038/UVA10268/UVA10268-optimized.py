import sys


def solve_one(k, n):
    if n <= 0:
        return "0"

    # 只有一顆球時只能線性掃描。
    if k == 1:
        return str(n) if n <= 63 else "More than 63 trials needed."

    # 在最多 63 次試驗的限制下，球數超過 63 對答案不再有幫助。
    eggs = min(k, 63)

    # dp[e] = 目前 t 次試驗、e 顆球可確定的最大樓層數。
    dp = [0] * (eggs + 1)

    for t in range(1, 64):
        # 需完整更新到 eggs，讓高球數狀態在每一輪都正確累積。
        for e in range(eggs, 0, -1):
            dp[e] = dp[e] + dp[e - 1] + 1

        if dp[eggs] >= n:
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
