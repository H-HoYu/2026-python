import heapq
import math
import sys
from collections import defaultdict

EPS = 1e-10
TWO_PI = 2.0 * math.pi
INF = 1e100


def cross(ax, ay, bx, by):
    return ax * by - ay * bx


def angle(x, y):
    return math.atan2(y, x) % TWO_PI


def get_intervals(seg):
    sx, sy, ex, ey = seg
    a = angle(sx, sy)
    b = angle(ex, ey)
    d = (b - a) % TWO_PI
    if d < EPS or abs(d - TWO_PI) < EPS:
        return []
    if d <= math.pi:
        l, r = a, a + d
    else:
        l, r = b, b + (TWO_PI - d)
    if r <= TWO_PI + EPS:
        return [(l, min(r, TWO_PI))]
    return [(l, TWO_PI), (0.0, r - TWO_PI)]


def distance(seg, a):
    sx, sy, ex, ey = seg
    dx = ex - sx
    dy = ey - sy
    rx = math.cos(a)
    ry = math.sin(a)
    den = cross(rx, ry, dx, dy)
    if abs(den) < EPS:
        return INF
    t = cross(sx, sy, dx, dy) / den
    u = cross(sx, sy, rx, ry) / den
    if t <= EPS or u < -EPS or u > 1.0 + EPS:
        return INF
    return t


def solve_case(segs):
    n = len(segs)
    vis = [0] * n
    add = defaultdict(list)
    rem = defaultdict(list)
    events = {0.0, TWO_PI}
    for i, seg in enumerate(segs):
        for l, r in get_intervals(seg):
            if r - l < EPS:
                continue
            add[l].append(i)
            rem[r].append(i)
            events.add(l)
            events.add(r)
    angles = sorted(events)
    active = [False] * n
    ver = [0] * n
    heap = []

    def push(i, a):
        ver[i] += 1
        heapq.heappush(heap, (distance(segs[i], a), i, ver[i]))

    def best(a):
        while heap:
            d, i, v = heap[0]
            if (not active[i]) or v != ver[i]:
                heapq.heappop(heap)
                continue
            nd = distance(segs[i], a)
            if abs(nd - d) > 1e-9:
                heapq.heappop(heap)
                heapq.heappush(heap, (nd, i, v))
                continue
            return i
        return None

    for k in range(len(angles) - 1):
        a = angles[k]
        for i in rem.get(a, []):
            active[i] = False
            ver[i] += 1
        p = a + 1e-7
        if p >= TWO_PI:
            p -= TWO_PI
        for i in add.get(a, []):
            active[i] = True
            push(i, p)
        b = angles[k + 1]
        if b - a < EPS:
            continue
        m = (a + b) * 0.5
        i = best(m)
        if i is not None:
            vis[i] = 1
    return vis


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    idx = 0
    out = []
    while idx < len(data):
        n = data[idx]
        idx += 1
        if n <= 0:
            break
        segs = []
        for _ in range(n):
            segs.append(tuple(data[idx:idx + 4]))
            idx += 4
        out.append(" ".join(map(str, solve_case(segs))))
    print("\n".join(out))


if __name__ == "__main__":
    main()