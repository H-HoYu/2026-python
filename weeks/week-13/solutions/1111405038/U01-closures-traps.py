# U01. 陷阱！閉包與可變預設值
#
# 這份檔案整理兩個 Python 初學者很常踩到的坑：
# 1) 可變預設值會被重複共用
# 2) 閉包在迴圈中會出現延遲綁定（late binding）
#
# 這兩種情況都不是語法錯誤，程式能跑，
# 但結果常常和直覺不同，所以特別需要理解背後機制。
#
# 對應 Bloom's Taxonomy：理解（Understand）
# 重點不是死背修法，而是能解釋「為什麼會這樣」。

# ── 陷阱 1：可變的預設值 ─────────────────────────────────
# 關鍵：函數的預設值只在「定義時」建立一次，之後每次呼叫都共用同一個物件
#
# 也就是說，下面這個 cart=[] 並不是每次呼叫函式時都重建，
# 而是在 def 執行的那一刻就先建立好，之後一直沿用。

def add_to_cart(item, cart=[]):   # ← 這個 [] 只建立一次！
    # 因為 cart 其實是同一個 list，所以 append 會持續累積舊資料
    cart.append(item)
    return cart

print("=== 陷阱 1：可變預設值 ===")
print(add_to_cart("蘋果"))   # ['蘋果']
print(add_to_cart("香蕉"))   # ['蘋果', '香蕉']  ← 驚！不是 ['香蕉']
print(add_to_cart("葡萄"))   # ['蘋果', '香蕉', '葡萄']
# 原因：cart=[] 這個 list 在 def 時就建好了，三次呼叫都用同一個

print("\n--- 正確寫法：用 None 當預設值 ---")
def add_to_cart_safe(item, cart=None):
    # 用 None 當作「沒有提供 cart」的訊號值
    if cart is None:
        cart = []   # ← 每次呼叫才建立新的 list，因此彼此不會共享
    cart.append(item)
    return cart

print(add_to_cart_safe("蘋果"))  # ['蘋果']
print(add_to_cart_safe("香蕉"))  # ['香蕉'] ← 各自獨立，正確！

# ── 陷阱 2：閉包的延遲綁定 ───────────────────────────────
# 關鍵：閉包記住的是「變數名稱」，不是「當下的值」
# 等迴圈跑完，i 已經是最後的值了
#
# 這裡要分清楚：
# - 如果閉包記住的是值，那應該得到 0,1,2,3,4
# - 但 Python 閉包預設記住的是外層變數 i 本身
# - 等真正呼叫 lambda 時，才去找 i 現在是多少

print("\n=== 陷阱 2：閉包延遲綁定 ===")
funcs = []
for i in range(5):
    funcs.append(lambda: i)   # ← lambda 記住「i」這個名字，不是值

print("你以為：", [0, 1, 2, 3, 4])
print("實際上：", [f() for f in funcs])  # [4, 4, 4, 4, 4]，全部都是 4！
# 原因：迴圈結束後 i=4，所有 lambda 去查 i，都查到 4

print("\n--- 正確寫法：用預設參數把值「複製」進來 ---")
funcs_ok = []
for i in range(5):
    # i=i 的意思是：把「目前這一輪的 i 值」存成 lambda 的預設值
    # 因為預設值會在函式定義當下決定，所以每個 lambda 都有自己的 i
    funcs_ok.append(lambda i=i: i)

print("修正後：", [f() for f in funcs_ok])  # [0, 1, 2, 3, 4] ✓

# ── nonlocal：在閉包裡修改外層的變數 ─────────────────────
# 閉包預設只能「讀取」外層變數
# 要修改外層變數，必須用 nonlocal 宣告
#
# 如果沒有 nonlocal，Python 會把 count 當成內層的新區域變數，
# 導致 count += 1 時出現 UnboundLocalError。

print("\n=== nonlocal：修改外層變數 ===")

def make_counter(start=0):
    """建立並回傳一個計數器函式。

    每次呼叫回傳的 counter，都會記住自己的 count 狀態。
    這就是 closure 最常見的用途之一：封裝狀態。
    """
    count = start

    def counter():
        nonlocal count   # ← 宣告「我要修改外層的 count，不是建新的」
        count += 1
        return count

    return counter

c1 = make_counter()
c2 = make_counter(10)
print(c1(), c1(), c1())   # 1 2 3
print(c2(), c2())         # 11 12
print(c1())               # 4（c1 和 c2 是各自獨立的計數器）

# ── 實際應用：用閉包做「一次性」工具函數 ────────────────
# CPE 中偶爾需要「記住狀態」但又不想寫整個 class
# 閉包很適合做小型狀態機，
# 例如：記錄訪問過的節點、累積次數、建立特定條件的檢查器。

print("\n=== 閉包應用：記住已走過的節點 ===")
def make_visit_tracker():
    # visited 會被內部函式捕捉住，因此每次呼叫 visit 都能沿用狀態
    visited = set()

    def visit(node):
        nonlocal visited
        if node in visited:
            return False    # 已走過
        visited.add(node)
        return True         # 第一次走到

    return visit

visit = make_visit_tracker()
results = [visit(n) for n in [1, 2, 1, 3, 2, 4]]
print(results)  # [True, True, False, True, False, True]

# 記憶重點 ──────────────────────────────────────────────────
# 可變預設值陷阱 → 預設值用 None，函數內再建 [] 或 {}
# 閉包延遲綁定  → 用 lambda x=x: x 把值固定下來
# nonlocal      → 要「修改」外層變數時才需要，只「讀取」不用
# closure（閉包） → 內部函式可以記住外層作用域中的變數狀態
