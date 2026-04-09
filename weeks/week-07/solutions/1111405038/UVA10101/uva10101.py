import sys

# ============================================================
# UVA 10101 — 移動一根木棒使等式成立（Matchstick）
#
# 七段顯示器各數字的木棒數（索引 0~9）：
#   0→6, 1→2, 2→5, 3→5, 4→4, 5→5, 6→6, 7→3, 8→7, 9→6
#
# 解題策略：暴力枚舉所有「移動方式」
#   移動方式分兩類：
#   1. 同位置重排：把某個數字換成「木棒總數相同但形狀不同」的另一個數字
#      （物理上就是把同一個數字內某段移到另一段）
#   2. 跨位置移一根：從數字 i 取走一根（i 變成少一根的數字）
#      再加到數字 j（j 變成多一根的數字），i ≠ j
#
# 限制：+、-、= 不能動，只能動數字。
# ============================================================

# 七段顯示器各數字使用的木棒數（索引即數字）
STICKS = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]


def eval_side(s: str) -> int:
    """計算只含數字與加減號的算式，支援前導零。

    例如："-3+05" → (-3) + 5 = 2
    不使用 eval() 是因為 Python 3 不允許以 0 開頭的整數字面值。
    """
    result = 0
    sign = 1    # 目前的符號，+1 或 -1
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == '+':
            sign = 1
            i += 1
        elif c == '-':
            sign = -1
            i += 1
        else:
            # 讀取一段連續的數字字元
            j = i
            while j < n and s[j].isdigit():
                j += 1
            result += sign * int(s[i:j])
            i = j
            sign = 1  # 每讀完一個數後重置符號
    return result


def is_valid(expr: str) -> bool:
    """確認等式兩邊計算結果是否相等。"""
    eq = expr.index('=')
    return eval_side(expr[:eq]) == eval_side(expr[eq + 1:])


def solve(expr: str) -> str | None:
    """嘗試移動一根木棒使等式成立，返回新等式或 None。"""

    # 找出所有「數字字元」的位置（只有這些位置可以被修改）
    dpos = [i for i, c in enumerate(expr) if c.isdigit()]
    chars = list(expr)  # 轉成 list 以便修改

    for i in range(len(dpos)):
        pi = dpos[i]
        di = int(chars[pi])   # 位置 i 原本的數字
        si = STICKS[di]       # 位置 i 原本的木棒數

        # ── 移法 1：同位置重排 ────────────────────────────────
        # 換成木棒數相同（si）但數值不同的數字
        for nd in range(10):
            if STICKS[nd] == si and nd != di:
                chars[pi] = str(nd)
                if is_valid(''.join(chars)):
                    return ''.join(chars)
                chars[pi] = str(di)   # 還原

        # ── 移法 2：從位置 i 移走一根，加到位置 j ─────────────
        # 先找出 i 少一根後可變成哪些數字
        for nd_i in range(10):
            if STICKS[nd_i] != si - 1:
                continue
            chars[pi] = str(nd_i)    # i 位置少一根

            for j in range(len(dpos)):
                if j == i:
                    continue
                pj = dpos[j]
                dj = int(expr[pj])   # j 位置的原始數字（從 expr 取，因為 chars[pj] 未動）
                sj = STICKS[dj]

                # 找出 j 多一根後可變成哪些數字
                for nd_j in range(10):
                    if STICKS[nd_j] != sj + 1:
                        continue
                    chars[pj] = str(nd_j)    # j 位置多一根
                    if is_valid(''.join(chars)):
                        return ''.join(chars)
                    chars[pj] = str(dj)      # 還原 j

            chars[pi] = str(di)              # 還原 i

    return None  # 無解


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        # 取 '#' 之前的式子（'#' 之後可能有無關字元）
        hash_idx = line.index('#')
        expr = line[:hash_idx]

        result = solve(expr)
        if result:
            print(result + '#')
        else:
            print('No')


if __name__ == '__main__':
    main()
