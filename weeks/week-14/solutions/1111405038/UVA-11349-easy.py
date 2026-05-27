"""UVA 11349 - Symmetric Matrix
簡化易懂版本
"""

import sys


# 讀完整份輸入，方便用索引逐行處理
lines = sys.stdin.read().strip().splitlines()
t = int(lines[0])
pos = 1
out = []

for case_no in range(1, t + 1):
    # 解析 "N = n"
    n = int(lines[pos].split("=")[1])
    pos += 1

    # 讀入 n x n 矩陣
    m = [list(map(int, lines[pos + i].split())) for i in range(n)]
    pos += n

    ok = True

    # 同時檢查：非負 + 中心對稱
    for i in range(n):
        for j in range(n):
            if m[i][j] < 0 or m[i][j] != m[n - 1 - i][n - 1 - j]:
                ok = False
                break
        if not ok:
            break

    out.append(f"Test #{case_no}: {'Symmetric.' if ok else 'Non-symmetric.'}")

print("\n".join(out))
