import sys


def solve_one(pts):
    n = len(pts)
    xs = sorted(x for x, _ in pts)
    ys = sorted(y for _, y in pts)

    if n % 2:
        mx = xs[n // 2]
        my = ys[n // 2]
        cx = 1
        cy = 1
    else:
        lx, rx = xs[n // 2 - 1], xs[n // 2]
        ly, ry = ys[n // 2 - 1], ys[n // 2]
        mx = lx
        my = ly
        cx = rx - lx + 1
        cy = ry - ly + 1

    best = sum(abs(x - mx) for x, _ in pts) + sum(abs(y - my) for _, y in pts)
    return best, cx * cy


def solve(text):
    a = list(map(int, text.split()))
    it = iter(a)
    t = next(it)

    out = []
    for _ in range(t):
        n = next(it)
        pts = [(next(it), next(it)) for _ in range(n)]
        best, cnt = solve_one(pts)
        out.append(f"{best} {cnt}")

    return "\n".join(out)


def main():
    data = sys.stdin.buffer.read().decode()
    ans = solve(data)
    if ans:
        sys.stdout.write(ans)


if __name__ == "__main__":
    main()
