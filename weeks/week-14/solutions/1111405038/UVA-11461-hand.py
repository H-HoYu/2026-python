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

    l = math.isqrt(a)
    if l * l < a:
        l += 1
    r = math.isqrt(b)

    ans.append(str(max(0, r - l + 1)))

print("\n".join(ans))
