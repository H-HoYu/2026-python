import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    l = data[0]
    s = data[1]
    t = data[2]
    m = data[3]
    stones = sorted(data[4:4 + m])
    if s == t:
        print(sum(1 for stone in stones if stone % s == 0))
        return
    limit = t * (t - 1)
    compressed = []
    current = 0
    last = 0
    for stone in stones:
        current += min(stone - last, limit)
        compressed.append(current)
        last = stone
    end = current + min(l - last, limit)
    marks = [0] * (end + t + 1)
    for stone in compressed:
        marks[stone] = 1
    inf = 10**9
    dp = [inf] * (end + t + 1)
    dp[0] = 0
    for i in range(1, end + t + 1):
        add = marks[i]
        for jump in range(s, t + 1):
            prev = i - jump
            if prev >= 0 and dp[prev] + add < dp[i]:
                dp[i] = dp[prev] + add
    print(min(dp[end:end + t + 1]))


if __name__ == "__main__":
    main()