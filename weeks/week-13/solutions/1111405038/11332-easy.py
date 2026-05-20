import heapq
import math
import sys
from collections import defaultdict


EPS = 1e-10
TWO_PI = 2.0 * math.pi
INF = 1e100


def cross(ax, ay, bx, by):
    return ax * by - ay * bx


def ang(v):
    x = math.atan2(v[1], v[0]) % TWO_PI
    return x


def intervals(seg):
    sx, sy, ex, ey = seg
    a1 = ang((sx, sy))
    a2 = ang((ex, ey))
    diff = (a2 - a1) % TWO_PI
    if diff < EPS or abs(diff - TWO_PI) < EPS:
        return []
    if diff <= math.pi:
        l, r = a1, a1 + diff
    else:
        l, r = a2, a2 + (TWO_PI - diff)
    if r <= TWO_PI + EPS:
        return [(l, min(r, TWO_PI))]
    return [(l, TWO_PI), (0.0, r - TWO_PI)]


def dist(seg, a):
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


def solve(segments):
    n = len(segments)
    vis = [0] * n
    add = defaultdict(list)
    rem = defaultdict(list)
    events = {0.0, TWO_PI}

    for i, seg in enumerate(segments):
        for l, r in intervals(seg):
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
        heapq.heappush(heap, (dist(segments[i], a), i, ver[i]))

    def top(a):
        while heap:
            d, i, v = heap[0]
            if (not active[i]) or v != ver[i]:
                heapq.heappop(heap)
                continue
            nd = dist(segments[i], a)
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
        mid = (a + b) * 0.5
        i = top(mid)
        if i is not None:
            vis[i] = 1
    return vis


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    out = []
    idx = 0
    while idx < len(data):
        n = data[idx]
        idx += 1
        if n <= 0:
            break
        segs = []
        for _ in range(n):
            segs.append(tuple(data[idx:idx + 4]))
            idx += 4
        out.append(" ".join(map(str, solve(segs))))
    print("\n".join(out))


if __name__ == "__main__":
    main()