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

    # 如果每次都只能跳固定距離，會落在哪些點其實已經完全決定了。
    if s == t:
        ans = 0
        for stone in stones:
            if stone % s == 0:
                ans += 1
        print(ans)
        return

    limit = t * (t - 1)
    new_stones = []
    now = 0
    last = 0

    # 把太長的空白區間縮短，因為中間沒有石頭，保留很長的距離沒有意義。
    for stone in stones:
        gap = stone - last
        now += min(gap, limit)
        new_stones.append(now)
        last = stone

    end = now + min(l - last, limit)
    road = [0] * (end + t + 1)
    for stone in new_stones:
        road[stone] = 1

    inf = 10**9
    dp = [inf] * (end + t + 1)
    dp[0] = 0

    for i in range(1, end + t + 1):
        for jump in range(s, t + 1):
            prev = i - jump
            if prev >= 0:
                dp[i] = min(dp[i], dp[prev] + road[i])

    print(min(dp[end:end + t + 1]))


if __name__ == "__main__":
    main()