import sys
from collections import deque


def scc_kosaraju(n, g, rg):
    seen = bytearray(n)
    order = []

    # 第一趟：算後序（iterative DFS，避免遞迴深度問題）。
    for st in range(n):
        if seen[st]:
            continue

        seen[st] = 1
        stack = [st]
        it_idx = [0]

        while stack:
            u = stack[-1]
            i = it_idx[-1]
            gu = g[u]

            if i < len(gu):
                v = gu[i]
                it_idx[-1] = i + 1
                if not seen[v]:
                    seen[v] = 1
                    stack.append(v)
                    it_idx.append(0)
            else:
                order.append(u)
                stack.pop()
                it_idx.pop()

    # 第二趟：在反圖收 SCC。
    comp = [-1] * n
    cc = 0
    for st in reversed(order):
        if comp[st] != -1:
            continue
        comp[st] = cc
        stack = [st]
        while stack:
            u = stack.pop()
            for v in rg[u]:
                if comp[v] == -1:
                    comp[v] = cc
                    stack.append(v)
        cc += 1

    return comp, cc


def solve(text):
    nums = list(map(int, text.split()))
    it = iter(nums)

    n = next(it)
    m = next(it)

    g = [[] for _ in range(n)]
    rg = [[] for _ in range(n)]
    for _ in range(m):
        u = next(it) - 1
        v = next(it) - 1
        g[u].append(v)
        rg[v].append(u)

    money = [next(it) for _ in range(n)]

    s = next(it) - 1
    p = next(it)
    bars = [next(it) - 1 for _ in range(p)]

    comp, cc = scc_kosaraju(n, g, rg)

    # 把同一 SCC 的 ATM 金額加總。
    cmoney = [0] * cc
    cbar = bytearray(cc)
    nodes_in_comp = [[] for _ in range(cc)]

    for u in range(n):
        cu = comp[u]
        cmoney[cu] += money[u]
        nodes_in_comp[cu].append(u)

    for b in bars:
        cbar[comp[b]] = 1

    # 建 SCC DAG（去掉 set，改用時間戳記陣列去重，降低 hash 開銷）。
    dag = [[] for _ in range(cc)]
    seen_to = [0] * cc
    stamp = 0

    for cu in range(cc):
        stamp += 1
        out = dag[cu]
        for u in nodes_in_comp[cu]:
            for v in g[u]:
                cv = comp[v]
                if cv != cu and seen_to[cv] != stamp:
                    seen_to[cv] = stamp
                    out.append(cv)

    st = comp[s]

    # 只保留起點可達 SCC。
    reach = bytearray(cc)
    q = deque([st])
    reach[st] = 1
    while q:
        u = q.popleft()
        for v in dag[u]:
            if not reach[v]:
                reach[v] = 1
                q.append(v)

    indeg = [0] * cc
    for u in range(cc):
        if not reach[u]:
            continue
        for v in dag[u]:
            if reach[v]:
                indeg[v] += 1

    NEG = -10**30
    dp = [NEG] * cc
    dp[st] = cmoney[st]

    topo = deque([u for u in range(cc) if reach[u] and indeg[u] == 0])
    while topo:
        u = topo.popleft()
        du = dp[u]
        if du != NEG:
            for v in dag[u]:
                if reach[v]:
                    nv = du + cmoney[v]
                    if nv > dp[v]:
                        dp[v] = nv
        else:
            for v in dag[u]:
                if not reach[v]:
                    continue
                indeg[v] -= 1
                if indeg[v] == 0:
                    topo.append(v)
            continue

        for v in dag[u]:
            if not reach[v]:
                continue
            indeg[v] -= 1
            if indeg[v] == 0:
                topo.append(v)

    ans = 0
    for c in range(cc):
        if reach[c] and cbar[c] and dp[c] > ans:
            ans = dp[c]

    return str(ans)


def main():
    data = sys.stdin.buffer.read().decode()
    sys.stdout.write(solve(data))


if __name__ == "__main__":
    main()
