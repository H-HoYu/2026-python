"""UVA 11417 - GCD
一般解題版本（使用預處理加速）
"""

import sys


def build_prefix(limit: int) -> list[int]:
    """預先計算每個 n 的題目答案 G(n)。"""
    # 先用線性概念做 phi 篩
    phi = list(range(limit + 1))
    for i in range(2, limit + 1):
        if phi[i] == i:
            for j in range(i, limit + 1, i):
                phi[j] -= phi[j] // i

    # f[j] = sum_{i=1}^{j-1} gcd(i, j)
    f = [0] * (limit + 1)
    for i in range(1, limit + 1):
        for k in range(2, (limit // i) + 1):
            j = i * k
            f[j] += i * phi[k]

    # 題目要的是 sum_{1<=a<b<=n} gcd(a,b) = f[2] + ... + f[n]
    g = [0] * (limit + 1)
    for n in range(2, limit + 1):
        g[n] = g[n - 1] + f[n]

    return g


def main() -> None:
    nums = [int(x.strip()) for x in sys.stdin.read().split()]
    if not nums:
        return

    queries = [x for x in nums if x != 0]
    if not queries:
        return

    limit = max(queries)
    g = build_prefix(limit)

    out = []
    for n in nums:
        if n == 0:
            break
        out.append(str(g[n]))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
