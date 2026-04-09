import sys

# ============================================================
# UVA 10093 — 炮兵佈陣（Artillery Deployment）
#
# 解題策略：位元遮罩動態規劃（Bitmask DP）
#
# 核心觀察：
#   - M ≤ 10，每一行的放置狀態可用一個 M-bit 整數（遮罩）表示。
#     bit j = 1 表示第 j 格放了炮兵。
#   - 衝突條件：
#       水平：同行兩炮距離 ≤ 2 → mask & (mask<<1) 或 mask & (mask<<2)
#       垂直：同列兩炮所在行距離 ≤ 2 → cur & prev1 或 cur & prev2
#
# 演算法：
#   1. 先枚舉所有「行內合法」遮罩（無水平衝突）。
#   2. DP 狀態：dp[(prev1, prev2)] = 到目前行為止最多能放的炮兵數
#      prev1 = 前一行遮罩，prev2 = 前兩行遮罩。
#   3. 每行轉移時，針對所有合法的當前行遮罩 cur，
#      要求 cur & prev1 == 0 且 cur & prev2 == 0（無垂直衝突）。
#
# 時間複雜度：O(N × |valid|³)，M=10 時 |valid|≈60，非常快。
# ============================================================


def main() -> None:
    # ── 讀取輸入 ──────────────────────────────────────────────
    data = sys.stdin.read().split()
    ptr = 0

    N = int(data[ptr]); ptr += 1  # 地圖行數
    M = int(data[ptr]); ptr += 1  # 地圖列數

    # 把每行地形轉成「禁放遮罩」：bit j=1 表示該格是 H，不能放炮兵
    forbidden: list[int] = []
    for _ in range(N):
        row = data[ptr]; ptr += 1
        mask = 0
        for j, ch in enumerate(row):
            if ch == 'H':
                mask |= (1 << j)
        forbidden.append(mask)

    # ── 預計算行內合法遮罩 ────────────────────────────────────
    # 合法條件：不存在兩個 1-bit 相距 ≤ 2
    #   mask & (mask << 1) == 0  →  沒有相鄰的 1
    #   mask & (mask << 2) == 0  →  沒有距離 2 的兩個 1
    valid: list[int] = [
        m for m in range(1 << M)
        if (m & (m << 1)) == 0 and (m & (m << 2)) == 0
    ]

    # 預算每個遮罩中有幾個 1（= 炮兵數）
    pc: list[int] = [bin(i).count('1') for i in range(1 << M)]

    # ── 動態規劃初始化 ────────────────────────────────────────
    # dp[(prev1, prev2)] = 目前最多炮兵數
    # 第 0 行：虛擬「前兩行」都是 0（空行，不衝突）
    dp: dict[tuple[int, int], int] = {}
    for m in valid:
        if (m & forbidden[0]) == 0:  # 不踩山地
            dp[(m, 0)] = pc[m]

    # ── 逐行轉移 ──────────────────────────────────────────────
    for i in range(1, N):
        forb = forbidden[i]
        new_dp: dict[tuple[int, int], int] = {}

        for cur in valid:
            # 當前行放置不能踩山地
            if cur & forb:
                continue

            # 遍歷所有來自上一行的 DP 狀態
            for (prev1, prev2), cnt in dp.items():
                # 當前行與前一行、前兩行都不能有同列衝突
                if (cur & prev1) or (cur & prev2):
                    continue

                key = (cur, prev1)
                val = cnt + pc[cur]
                # 保留最大值
                if key not in new_dp or new_dp[key] < val:
                    new_dp[key] = val

        dp = new_dp

    # ── 輸出最大炮兵數 ────────────────────────────────────────
    print(max(dp.values()) if dp else 0)


if __name__ == "__main__":
    main()
