import sys

MOD = 1_000_000_007


def parse_row(line: str) -> str:
    s = line.strip()
    parts = s.split()
    return "".join(parts) if len(parts) > 1 else s


def count_ways(grid: list) -> int:
    n = len(grid)
    if n == 0:
        return 0
    m = len(grid[0])
    if m == 0:
        return 0

    size     = 1 << m
    full_mask = size - 1

    # ── 優化①：用兩個陣列取代單一 dict ──────────────────────────────────
    # 原版用 dict[(mask, left)] 儲存方案數，每次存取都需要：
    #   (1) 建立 tuple 物件  (2) 計算 tuple 的 hash  (3) dict 桶查找
    # 改為 dp0[mask]（left=0）/ dp1[mask]（left=1）兩個 list，
    # 全部操作變成純整數索引，常數因子降低 5~10 倍。
    dp0 = [0] * size   # left = 0
    dp1 = [0] * size   # left = 1
    dp0[0] = 1

    # ── 優化②：預計算每列的位元遮罩 ──────────────────────────────────────
    # 原版在最內層迴圈每格重複計算 `1 << c` 與 `~(1 << c) & mask`。
    # 改為在迴圈外預先算好，避免重複運算。
    set_bit = [1 << c for c in range(m)]
    clr_bit = [(~(1 << c)) & full_mask for c in range(m)]

    for r in range(n):
        row      = grid[r]
        last_row = (r == n - 1)

        for c in range(m):
            sc        = set_bit[c]
            cc        = clr_bit[c]
            open_cell = row[c] == '1'
            can_right = c < m - 1
            can_down  = not last_row

            ndp0 = [0] * size
            ndp1 = [0] * size

            # ── 優化③：在遮罩迴圈外做 open_cell 分支 ───────────────────
            # 原版在最內層 `for (mask, left)` 裡用 `if not open_cell: ... continue`，
            # 每個 mask 都要重新判斷。改在外層先分支，迴圈本體不再含 if。
            if not open_cell:
                # 0 格（有插座）：要求 up=0, left=0，輸出 down=0, right=0。
                for mask in range(size):
                    if not (mask & sc):       # up=0（bit c 為 0）
                        w = dp0[mask]         # 只接受 left=0
                        if w:
                            # mask 的 bit c 已為 0，故 mask & cc == mask
                            ndp0[mask] = (ndp0[mask] + w) % MOD
            else:
                # 1 格（開放）：left + up + right + down == 2
                for mask in range(size):
                    # ── 優化④：每個 mask 只算一次 nm0/nm1 ─────────────
                    # 原版在 right/down 的四個組合裡各自計算 nm，
                    # 同一 mask 重複執行位元運算最多 4 次。
                    # 改為每個 mask 預算 nm0（down=0）和 nm1（down=1），在分支中直接引用。
                    nm0 = mask & cc          # down=0 → 清除 bit c
                    nm1 = nm0 | sc           # down=1 → 設定 bit c

                    up  = 1 if (mask & sc) else 0

                    # ── left = 0 ──────────────────────────────────────
                    w = dp0[mask]
                    if w:
                        if up == 0:          # need right+down = 2
                            if can_right and can_down:
                                ndp1[nm1] = (ndp1[nm1] + w) % MOD
                        else:                # need right+down = 1
                            if can_right:
                                ndp1[nm0] = (ndp1[nm0] + w) % MOD
                            if can_down:
                                ndp0[nm1] = (ndp0[nm1] + w) % MOD

                    # ── left = 1 ──────────────────────────────────────
                    w = dp1[mask]
                    if w:
                        if up == 0:          # need right+down = 1
                            if can_right:
                                ndp1[nm0] = (ndp1[nm0] + w) % MOD
                            if can_down:
                                ndp0[nm1] = (ndp0[nm1] + w) % MOD
                        else:                # need right+down = 0
                            ndp0[nm0] = (ndp0[nm0] + w) % MOD

            dp0 = ndp0
            dp1 = ndp1

    return dp0[0]


def solve(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    t = int(lines[0])
    i = 1
    out = []

    for case_id in range(1, t + 1):
        n, m = map(int, lines[i].split())
        i += 1

        grid = []
        for _ in range(n):
            grid.append(parse_row(lines[i]))
            i += 1

        out.append(f"Case {case_id}: {count_ways(grid)}")

    return "\n".join(out)


def main():
    data = sys.stdin.read()
    ans = solve(data)
    if ans:
        sys.stdout.write(ans)


if __name__ == "__main__":
    main()
