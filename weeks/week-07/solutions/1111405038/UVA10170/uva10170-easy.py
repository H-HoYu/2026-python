import sys

# ============================================================
# UVA 10170 — The Hotel with Infinite Rooms（簡單易記版）
#
# 記憶口訣：
#   「前 k 團總天數 = k*S + k*(k-1)//2，二分找最小 k 使總數 >= D」
#
# 三步驟：
#   1. 定義 total(k) = k*S + k*(k-1)//2  ← 前 k 個旅行團的總天數
#   2. 二分搜尋最小的 k，使 total(k) >= D
#   3. 答案 = S + k - 1（第 k 個旅行團的人數）
# ============================================================


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        S, D = map(int, line.split())

        # ── 二分搜尋 ──────────────────────────────────────────
        # 找最小的 k 使「前 k 個旅行團的總天數 >= D」
        lo, hi = 1, 2 * 10**15 + 2

        while lo < hi:
            mid = (lo + hi) // 2
            # total(mid) = mid*S + mid*(mid-1)//2
            if mid * S + mid * (mid - 1) // 2 >= D:
                hi = mid      # mid 可行，試看看更小的
            else:
                lo = mid + 1  # mid 不夠大，往右找

        # lo 就是第幾個旅行團，人數 = S + lo - 1
        print(S + lo - 1)


if __name__ == '__main__':
    main()
