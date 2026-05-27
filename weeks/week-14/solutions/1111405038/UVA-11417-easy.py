"""UVA 11417 - GCD
簡短直觀版本
"""

import math
import sys


# 逐筆讀入 N，直到遇到 0
nums = [int(x) for x in sys.stdin.read().split()]
ans = []

for n in nums:
    if n == 0:
        break

    total = 0

    # 直接雙迴圈列舉所有 i < j
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            total += math.gcd(i, j)

    ans.append(str(total))

sys.stdout.write("\n".join(ans))
