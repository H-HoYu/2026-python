# A01. functools.partial：固定參數，減少重複
#
# 學習目標：
# 1) 了解 partial 的核心概念：先「綁定部分參數」，得到新函式
# 2) 能把 partial 套用在常見情境：sorted、重複計算、輸出格式
# 3) 比較 partial 與 lambda：兩者都能達成，但 partial 常更語意化
#
# 對應 Bloom's Taxonomy：應用（Apply）
# 代表你不只會背語法，而是能在新問題裡選擇合適工具。

from functools import partial

# ── 基本概念：固定部分參數，產生新函數 ───────────────────

def power(base, exp):
    # 回傳 base 的 exp 次方
    # 例如 power(2, 3) -> 8
    return base ** exp

# partial(power, exp=2) 的意思是：
# - 原本要傳 (base, exp)
# - 現在先把 exp 固定住
# - 之後呼叫新函式時，只要提供 base
square = partial(power, exp=2)   # 固定 exp=2，只剩 base 要填
cube   = partial(power, exp=3)   # 固定 exp=3，只剩 base 要填

print("=== partial 基本用法 ===")
print(square(5))    # 5^2 = 25
print(cube(3))      # 3^3 = 27
print([square(n) for n in range(1, 6)])  # 對 1~5 全部做平方

# ── 搭配 sorted：固定排序的 key ──────────────────────────
# 排序常見寫法是 key=某個函式，且該函式需接收「單一元素」
# 這裡 get_score(student, subject) 需要兩個參數，
# 所以用 partial 把 subject 先固定，變成可直接給 sorted 的 key 函式。

students = [
    {"name": "王小明", "math": 80, "english": 70},
    {"name": "李大華", "math": 65, "english": 90},
    {"name": "張三",   "math": 95, "english": 55},
]

def get_score(student, subject):
    # 從單筆學生資料取出指定科目分數
    return student[subject]

by_math    = partial(get_score, subject="math")     # 等價於 lambda s: s["math"]
by_english = partial(get_score, subject="english")  # 等價於 lambda s: s["english"]

print("\n=== partial 搭配 sorted ===")
print("數學排名：", [s["name"] for s in sorted(students, key=by_math,    reverse=True)])
print("英文排名：", [s["name"] for s in sorted(students, key=by_english, reverse=True)])

# ── CPE 應用：UVA 11005 進位制成本 ──────────────────────
# 題目需要計算同一個數字在不同進位下的成本
# 用 partial 固定「成本表」，讓函式呼叫集中在 (n, base)
# 實務上這樣做可減少重複傳參，也讓主流程更清楚。

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def cost_in_base(n, base, costs):
    """計算 n 在指定進位 base 下的表示成本。

    參數說明：
    - n: 要計算的十進位整數（假設 n >= 0）
    - base: 目標進位（例如 2~36）
    - costs: 長度至少 36 的成本表，costs[d] 代表數字 d 的成本

    回傳：
    - n 轉成 base 後，每一位數字成本的總和
    """
    # 特例：n == 0 時，表示法只有一位「0」
    if n == 0:
        return costs[0]

    # 一般情況：反覆取餘數 (% base) 得到每一位數字
    # 再用整除 (// base) 往高位繼續處理
    total = 0
    while n > 0:
        total += costs[n % base]
        n //= base
    return total

# 假設每個字元成本都是 1（示範用）
uniform_costs = [1] * 36

# 用 partial 固定 costs，之後主流程只要填 (n, base)
# 這樣在 min / list comprehension 中可讀性會更高
calc = partial(cost_in_base, costs=uniform_costs)

print("\n=== UVA 11005：各進位下的成本 ===")
n = 255
# 找出 2~36 進位中的最低成本
best_cost = min(calc(n, b) for b in range(2, 37))
# 找出所有達到最低成本的進位（可能不只一個）
best_bases = [b for b in range(2, 37) if calc(n, b) == best_cost]
print(f"數字 {n}，最低成本 {best_cost}，最佳進位：{best_bases}")

# ── 固定 print 的格式 ─────────────────────────────────────
# 競程輸出時常用：先把 end=" " 固定，避免每次都重複寫

print_same_line = partial(print, end=" ")
print("\n=== 同行輸出 ===")
for i in range(1, 6):
    print_same_line(i)
print()   # 換行

# ── partial vs lambda 比較 ────────────────────────────────
# 兩種寫法效果相近：
# - lambda：彈性高、可寫任意邏輯
# - partial：當需求是「固定參數」時，語意更直接

double_lambda  = lambda x: power(x, 2)        # lambda 寫法
double_partial = partial(power, exp=2)         # partial 寫法（固定 exp）

print("\n=== lambda vs partial ===")
print([double_lambda(n)  for n in range(1, 6)])   # [1, 4, 9, 16, 25]
print([double_partial(n) for n in range(1, 6)])   # [1, 4, 9, 16, 25]

# 記憶重點 ──────────────────────────────────────────────────
# partial(函數, 固定的參數) → 回傳新函數，只剩剩餘的參數要填
# 常用場景：sorted key、min/max key、print 格式、重複呼叫某個函數
# 和 lambda 效果類似，但 partial 更清楚表達「固定哪個參數」
# 小提醒：partial 不會立即執行原函式，而是建立一個可稍後呼叫的新函式
