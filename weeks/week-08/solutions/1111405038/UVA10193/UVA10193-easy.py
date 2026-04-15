"""
UVA 10193 - 反正切公式 簡易版本

核心思路：
  arctan(1/a) = arctan(1/b) + arctan(1/c)
  推導出：(b-a)(c-a) = 1 + a²

  把 1+a² 分解成兩個因數 d1 × d2
  則 b = d1+a, c = d2+a
  最小化 b+c ⟺ 最小化 d1+d2 ⟺ d1, d2 越接近 √(1+a²) 越好
"""

import math


def solve(a):
    """找 b + c 的最小值"""
    n = 1 + a * a  # 需分解的數：(b-a)(c-a) = n

    # 從大到小枚舉 d1（越大越接近 √n，d1+d2 越小）
    for d1 in range(int(math.isqrt(n)), 0, -1):
        if n % d1 == 0:
            d2 = n // d1
            return (d1 + a) + (d2 + a)  # 第一個找到的就是最小的
