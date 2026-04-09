import sys

# ============================================================
# UVA 10101 — 移動一根木棒（簡單易記版）
#
# 記憶口訣：
#   「建表 FROM，枚舉每對(i,j)數字位置，
#     先試同位置換，再試 i 給 j 一根」
#
# 三個步驟：
#   Step 1. 建 FROM 表：FROM[n] = 可由 n 根木棒組成的數字列表
#   Step 2. 找算式中所有數字字元的位置（dpos）
#   Step 3. 對每個位置 i：
#             a. 換成 FROM[同根數] 的其他數字 → 看等式是否成立
#             b. 對每個位置 j：試 i→FROM[根數-1]、j→FROM[根數+1]
# ============================================================

# 七段顯示器各數字的根數
STICKS = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]

# Step 1：建 FROM 表（根數 → 數字列表）
# FROM[n] = 所有恰好用 n 根木棒能組成的數字
FROM: dict[int, list[int]] = {}
for _d in range(10):
    FROM.setdefault(STICKS[_d], []).append(_d)


def calc(s: str) -> int:
    """計算加減法字串（支援前導零，不用 eval 避免語法錯誤）。"""
    res, sign, i = 0, 1, 0
    while i < len(s):
        if s[i] in '+-':
            # 遇到符號，更新正負號
            sign = 1 if s[i] == '+' else -1
            i += 1
        else:
            # 讀到數字，一次讀完整段連續數字
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            res += sign * int(s[i:j])
            i = j
    return res


def ok(expr: str) -> bool:
    """確認等式兩邊相等。"""
    eq = expr.index('=')
    return calc(expr[:eq]) == calc(expr[eq + 1:])


def solve(expr: str) -> str | None:
    """核心：枚舉所有移動方式，找到第一個讓等式成立的結果。"""

    # Step 2：收集所有數字字元的位置
    dpos = [i for i, c in enumerate(expr) if c.isdigit()]
    ch = list(expr)  # 可修改的字元列表

    for i in range(len(dpos)):
        pi = dpos[i]
        di = int(ch[pi])               # 原來的數字
        si = STICKS[di]                # 原來的根數

        # Step 3a：同位置換（換成同根數的其他數字）
        for nd in FROM.get(si, []):
            if nd == di:
                continue               # 跳過自己
            ch[pi] = str(nd)
            if ok(''.join(ch)):
                return ''.join(ch)
            ch[pi] = str(di)           # 還原

        # Step 3b：i 給 j 一根（i 少一根，j 多一根）
        for nd_i in FROM.get(si - 1, []):      # i 少一根後的數字
            ch[pi] = str(nd_i)
            for j in range(len(dpos)):
                if j == i:
                    continue
                pj = dpos[j]
                dj = int(expr[pj])             # j 的原始數字
                for nd_j in FROM.get(STICKS[dj] + 1, []):  # j 多一根後的數字
                    ch[pj] = str(nd_j)
                    if ok(''.join(ch)):
                        return ''.join(ch)
                    ch[pj] = str(dj)           # 還原 j
            ch[pi] = str(di)                   # 還原 i

    return None  # 全試過都不行 → 無解


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        e = line.index('#')       # 找到結尾的 #
        result = solve(line[:e])  # 只取式子部分
        print((result + '#') if result else 'No')


if __name__ == '__main__':
    main()
