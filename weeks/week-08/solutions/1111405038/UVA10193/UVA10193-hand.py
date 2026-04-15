import math


def solve(a):
    n = 1 + a * a

    for d1 in range(int(math.isqrt(n)), 0, -1):
        if n % d1 == 0:
            d2 = n // d1
            return (d1 + a) + (d2 + a)
import math


def solve(a):
    n = 1 + a * a

    for d1 in range(int(math.isqrt(n)), 0, -1):
        if n % d1 == 0:
            d2 = n // d1
            return (d1 + a) + (d2 + a)
