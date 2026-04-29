import sys

# 預先計算最多 26 個人名，避免每筆測資重建
_PEOPLE = [chr(ord('A') + k) for k in range(26)]


def parse_and_solve(text):
    # 一次 split 取出所有 token，避免逐行 strip/filter 的額外負擔
    lines = [ln for ln in text.splitlines() if ln.strip()]
    i = 0
    out = []

    while i < len(lines):
        n = int(lines[i])
        i += 1

        # ── 優化①：把禁止集合展開成二維布林表 ──────────────────────────
        # 原作用 set 做 `place in forbid[idx]`，每次查詢有雜湊計算。
        # 改成 allowed[idx][place] 直接索引，常數因子更小。
        allowed = [[True] * (n + 1) for _ in range(n)]
        for idx in range(n):
            parts = lines[i].split()
            i += 1
            for token in parts:
                x = int(token)
                if x == 0:
                    break
                if 1 <= x <= n:
                    allowed[idx][x] = False

        people = _PEOPLE[:n]          # 切片代替每次 list comprehension
        used   = bytearray(n)         # ── 優化②：bytearray 比 list[bool] 更緊湊且快速
        cur    = [''] * n

        # ── 優化③：O(1) 差異輸出 ─────────────────────────────────────────
        # 原作法：每次 emit 都用 while 迴圈找最長共同前綴 ⇒ O(n)。
        # 新作法：DFS 在「同一個 pos 嘗試第二個以上選項」時主動記錄最淺變動層，
        #         emit 時直接用 state[0] 做切片 ⇒ O(1)。
        # state = [change_depth, first_emit]
        state = [n, True]

        # 設定遞迴深度上限，避免深度稍大時 Python 拋出 RecursionError
        sys.setrecursionlimit(max(sys.getrecursionlimit(), n + 200))

        def dfs(pos):
            if pos == n:
                s = ''.join(cur)
                if state[1]:          # 第一筆輸出完整字串
                    out.append(s)
                    state[1] = False
                else:
                    out.append(s[state[0]:])   # 只輸出自 change_depth 起的尾巴
                state[0] = n          # 重置
                return

            place = pos + 1
            a_pos  = allowed          # 局部名稱參照，減少 LOAD_GLOBAL 次數
            first_try = True
            for idx in range(n):
                if not used[idx] and a_pos[idx][place]:
                    # 在同層第二次（含）嘗試 ⇒ 記錄最淺變動深度
                    if not first_try and pos < state[0]:
                        state[0] = pos
                    used[idx] = 1
                    cur[pos]  = people[idx]
                    dfs(pos + 1)
                    used[idx] = 0
                    first_try = False

        dfs(0)

    return '\n'.join(out)


def main():
    result = parse_and_solve(sys.stdin.read())
    if result:
        sys.stdout.write(result)


if __name__ == '__main__':
    main()
