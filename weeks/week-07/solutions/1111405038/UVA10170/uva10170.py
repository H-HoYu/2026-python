import sys
from math import isqrt

# ============================================================
# UVA 10170 — The Hotel with Infinite Rooms
#
# 解題核心：二分搜尋
#
# 旅行團規律：
#   第 k 個旅行團（k 從 1 開始）有 S+k-1 人，住 S+k-1 天。
#
# 前 k 個旅行團合計佔用天數：
#   total(k) = S + (S+1) + ... + (S+k-1)
#            = k*S + 0+1+...+(k-1)
#            = k*S + k*(k-1)//2
#
# 問第 D 天是哪個旅行團：
#   找最小的 k 使 total(k) >= D
#   → 答案 = S + k - 1（第 k 個旅行團的人數）
#
# 二分搜尋範圍：
#   k 最大約 2*D/S，但 D 可達 10^15，直接用 2*10^15+2 當上界。
# ============================================================


def find_group(S: int, D: int) -> int:
    """找第 D 天住宿的旅行團人數。

    使用二分搜尋找最小的 k，使前 k 個旅行團總天數 >= D。
    """
    lo, hi = 1, 2 * (10**15) + 2

    while lo < hi:
        mid = (lo + hi) // 2
        # 前 mid 個旅行團的總天數
        total = mid * S + mid * (mid - 1) // 2
        if total >= D:
            hi = mid
        else:
            lo = mid + 1

    # lo 即為所在的旅行團編號，人數為 S + lo - 1
    return S + lo - 1


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        S = int(parts[0])   # 起始旅行團人數
        D = int(parts[1])   # 查詢天數
        print(find_group(S, D))


if __name__ == '__main__':
    main()
