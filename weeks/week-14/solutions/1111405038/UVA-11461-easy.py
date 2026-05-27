"""UVA 11461 - Square Numbers
簡短易懂版本
"""

import math
import sys


ans = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    a, b = map(int, line.split())
    if a == 0 and b == 0:
        break

    # [a, b] 內平方數個數 = floor(sqrt(b)) - ceil(sqrt(a)) + 1
    l = math.isqrt(a)
    if l * l < a:
        l += 1
    r = math.isqrt(b)

    ans.append(str(max(0, r - l + 1)))

print("\n".join(ans))
