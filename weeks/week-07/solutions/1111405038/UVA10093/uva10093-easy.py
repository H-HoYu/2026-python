import sys

# ============================================================
# UVA 10093 — 炮兵佈陣（簡單易記版）
#
# 核心想法（用一句話記住）：
#   「每行用一個整數遮罩代表放炮位置，
#     用 3 層迴圈（當前行、前一行、前兩行）做 DP。」
#
# 記憶口訣：
#   1. valid[]   → 列出同行不互攻的所有放法（水平安全）
#   2. dp[a][b]  → 前一行用 valid[a]、前兩行用 valid[b] 時的最多炮兵數
#   3. 換行時：若遮罩 cur 與 valid[a] 或 valid[b] 沒有同列衝突，就可轉移
# ============================================================


def main() -> None:
    data = sys.stdin.read().split()
    ptr = 0
    N = int(data[ptr]); ptr += 1   # 地圖行數
    M = int(data[ptr]); ptr += 1   # 地圖列數

    # 讀地形 → 轉成「禁止 bit」：bit j=1 表示第 j 格是山地 H
    forb = []
    for _ in range(N):
        row = data[ptr]; ptr += 1
        f = 0
        for j, ch in enumerate(row):
            if ch == 'H':
                f |= 1 << j
        forb.append(f)

    # ── 步驟 1：列出行內所有合法放法 ─────────────────────────
    # 合法 = 任意兩個 1-bit 距離 > 2
    # 用位元運算快速判斷：
    #   mask & (mask << 1) → 有相鄰兩炮？
    #   mask & (mask << 2) → 有距離 2 的两炮？
    valid = []
    for m in range(1 << M):
        if not (m & (m << 1)) and not (m & (m << 2)):
            valid.append(m)

    V = len(valid)  # 合法放法的總數

    # 炮兵數 = mask 中 1-bit 的個數
    cnt = [bin(m).count('1') for m in valid]

    # valid 的索引：把遮罩值對應到在 valid[] 中的位置
    idx = {m: i for i, m in enumerate(valid)}

    # ── 步驟 2：初始化 DP 表 ──────────────────────────────────
    # dp[a][b] = 前一行用 valid[a]、前兩行用 valid[b] 時，已放的最多炮兵數
    # -1 代表「這個狀態不可達」
    NEG = -1
    dp = [[NEG] * V for _ in range(V)]

    # 處理第 0 行（虛擬前兩行 = 空，用索引 0 即 valid[0]=0 代表）
    # 注意：valid[0] 一定是 0（空放置），即「前兩行什麼都沒放」
    zero_idx = idx[0]  # 0 在 valid 中的索引（一定是 0）
    for i, m in enumerate(valid):
        if not (m & forb[0]):          # 沒踩山地
            dp[i][zero_idx] = cnt[i]

    # ── 步驟 3：逐行轉移 ──────────────────────────────────────
    for row in range(1, N):
        f = forb[row]
        new_dp = [[NEG] * V for _ in range(V)]

        for ci, cur in enumerate(valid):      # 當前行的放法
            if cur & f:                        # 踩到山地，跳過
                continue
            for ai in range(V):               # 前一行
                a = valid[ai]
                if cur & a:                    # 同列衝突，跳過
                    continue
                for bi in range(V):           # 前兩行
                    if dp[ai][bi] == NEG:      # 前狀態不可達
                        continue
                    b = valid[bi]
                    if cur & b:                # 同列衝突，跳過
                        continue
                    val = dp[ai][bi] + cnt[ci]
                    if val > new_dp[ci][ai]:
                        new_dp[ci][ai] = val

        dp = new_dp

    # ── 步驟 4：取最大值輸出 ──────────────────────────────────
    ans = 0
    for row in dp:
        for v in row:
            if v > ans:
                ans = v
    print(ans)


if __name__ == "__main__":
    main()
