import bisect
import sys


def axis_cost(sorted_vals, prefix, m):
    # 以 prefix sum + 二分求 sum |x - m|，避免逐點 abs 迴圈。
    n = len(sorted_vals)
    k = bisect.bisect_right(sorted_vals, m)
    left_sum = prefix[k]
    right_sum = prefix[n] - left_sum
    return m * k - left_sum + right_sum - m * (n - k)


def solve_one(xs, ys):
    n = len(xs)
    xs.sort()
    ys.sort()

    px = [0] * (n + 1)
    py = [0] * (n + 1)
    for i, v in enumerate(xs, 1):
        px[i] = px[i - 1] + v
    for i, v in enumerate(ys, 1):
        py[i] = py[i - 1] + v

    if n & 1:
        mx = xs[n // 2]
        my = ys[n // 2]
        cnt = 1
    else:
        lx, rx = xs[n // 2 - 1], xs[n // 2]
        ly, ry = ys[n // 2 - 1], ys[n // 2]
        mx = lx
        my = ly
        cnt = (rx - lx + 1) * (ry - ly + 1)

    best = axis_cost(xs, px, mx) + axis_cost(ys, py, my)
    return best, cnt


def solve(text):
    vals = list(map(int, text.split()))
    it = iter(vals)
    t = next(it)

    out = []
    for _ in range(t):
        n = next(it)
        xs = [0] * n
        ys = [0] * n
        for i in range(n):
            xs[i] = next(it)
            ys[i] = next(it)

        best, cnt = solve_one(xs, ys)
        out.append(f"{best} {cnt}")

    return "\n".join(out)


def main():
    data = sys.stdin.buffer.read().decode()
    ans = solve(data)
    if ans:
        sys.stdout.write(ans)


if __name__ == "__main__":
    main()
