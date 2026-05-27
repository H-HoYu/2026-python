import math
import sys


nums = [int(x) for x in sys.stdin.read().split()]
ans = []

for n in nums:
    if n == 0:
        break

    total = 0

    for i in range(1, n):
        for j in range(i + 1, n + 1):
            total += math.gcd(i, j)

    ans.append(str(total))

sys.stdout.write("\n".join(ans))
