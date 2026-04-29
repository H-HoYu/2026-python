import sys
from collections import deque


def scc_kosaraju(n, g, rg):
    seen = [False] * n
    order = []

    # 第一趟：算後序。
    for st in range(n):
        if seen[st]:
            continue
        stack = [(st, 0)]
        seen[st] = True

        while stack:
            u, i = stack[-1]
            if i < len(g[u]):
                v = g[u][i]
                stack[-1] = (u, i + 1)
                if not seen[v]:
                    seen[v] = True
                    stack.append((v, 0))
            else:
                order.append(u)
                stack.pop()

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
    # 這題只有單筆測資，直接按整數序列讀完。
    a = list(map(int, text.split()))
    it = iter(a)

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

    # 把同一 SCC 的 ATM 金額加總，之後在 SCC DAG 上做 DP。
    cmoney = [0] * cc
    cbar = [False] * cc
    for u in range(n):
        cmoney[comp[u]] += money[u]
    for b in bars:
        cbar[comp[b]] = True

    dag = [set() for _ in range(cc)]
    for u in range(n):
        cu = comp[u]
        for v in g[u]:
            cv = comp[v]
            if cu != cv:
                dag[cu].add(cv)

    st = comp[s]

    # 只保留起點可達 SCC。
    reach = [False] * cc
    q = deque([st])
    reach[st] = True
    while q:
        u = q.popleft()
        for v in dag[u]:
            if not reach[v]:
                reach[v] = True
                q.append(v)

    indeg = [0] * cc
    for u in range(cc):
        if not reach[u]:
            continue
        for v in dag[u]:
            if reach[v]:
                indeg[v] += 1

    NEG = -10**30
    # dp[c]：從起點 SCC 走到 c 時，最多可搶金額。
    dp = [NEG] * cc
    dp[st] = cmoney[st]

    topo = deque([u for u in range(cc) if reach[u] and indeg[u] == 0])
    while topo:
        u = topo.popleft()
        for v in dag[u]:
            if not reach[v]:
                continue
            if dp[u] != NEG:
                dp[v] = max(dp[v], dp[u] + cmoney[v])
            indeg[v] -= 1
            if indeg[v] == 0:
                topo.append(v)

    ans = 0
    for c in range(cc):
        if reach[c] and cbar[c] and dp[c] != NEG:
            ans = max(ans, dp[c])

    return str(ans)


def main():
    # 使用 buffer 讀入可避免大量資料下的 I/O 瓶頸。
    data = sys.stdin.buffer.read().decode()
    sys.stdout.write(solve(data))


if __name__ == "__main__":
    main()