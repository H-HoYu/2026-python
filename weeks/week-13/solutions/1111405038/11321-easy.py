import sys


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.rows = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return a
        if self.rank[a] < self.rank[b]:
            a, b = b, a
        self.parent[b] = a
        self.rows[a] |= self.rows[b]
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1
        return a


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return

    n, m, t = data[0], data[1], data[2]
    ops = [(data[i], data[i + 1]) for i in range(3, 3 + 2 * t, 2)]
    dsu = DSU(n * m)
    blocked = [False] * (n * m)
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    ans = []

    def idx(x, y):
        return x * m + y

    full = (1 << n) - 1

    for x, y in ops:
        p = idx(x, y)
        roots = set()
        mask = 1 << x
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < n and 0 <= ny < m:
                q = idx(nx, ny)
                if blocked[q]:
                    root = dsu.find(q)
                    if root not in roots:
                        roots.add(root)
                        mask |= dsu.rows[root]

        if mask == full:
            blocked[p] = False
            ans.append(">_<")
        else:
            blocked[p] = True
            dsu.rows[p] = 1 << x
            root = p
            for q_root in roots:
                root = dsu.union(root, q_root)
            ans.append("<(_ _)>")

    print("\n".join(ans))


if __name__ == "__main__":
    main()