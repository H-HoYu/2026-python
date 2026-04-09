# Remember（記憶）- 迭代器基礎概念
# ============================================================
# 本檔案涵蓋 Python 迭代器協議（Iterator Protocol）的核心知識。
# 迭代器是 for 迴圈、生成器、解析式的底層機制，
# 理解它有助於寫出更高效、更 Pythonic 的程式碼。
# ============================================================

# ============================================================
# 1. 迭代器協議的核心方法
# ============================================================
# Python 的迭代器協議由兩個魔法方法組成：
#   __iter__(self)  → 回傳迭代器本身（讓物件可被 for 迴圈使用）
#   __next__(self)  → 回傳序列的下一個元素；無元素時擲出 StopIteration
#
# 內建的 iter() / next() 是呼叫這兩個魔法方法的橋接器，
# 讓使用者不必直接呼叫雙底線方法。
# ============================================================
items = [1, 2, 3]

# iter() 內部呼叫 items.__iter__()，回傳 list_iterator 物件。
# list_iterator 內部維護一個索引，每次 next() 就往前一格。
it = iter(items)
print(f"迭代器: {it}")  # <list_iterator object at 0x...>

# next() 內部呼叫 it.__next__()，逐一取出元素。
print(f"第一個: {next(it)}")  # 1 — 讀取索引 0
print(f"第二個: {next(it)}")  # 2 — 讀取索引 1
print(f"第三個: {next(it)}")  # 3 — 讀取索引 2

# 索引超出範圍後，__next__() 自動擲出 StopIteration。
# for 迴圈會靜默地捕捉此例外並停止；
# 手動呼叫 next() 時，例外會往上傳播，需自行處理。
try:
    next(it)  # 已無元素，必然擲出 StopIteration
except StopIteration:
    print("迭代結束!")

# ============================================================
# 2. 常見可迭代物件
# ============================================================
# 「可迭代物件」（Iterable）：實作了 __iter__() 的物件，可被 for 迴圈使用。
# 「迭代器」（Iterator）：同時實作 __iter__() 與 __next__() 的物件，
#   是「有狀態的讀取指標」，只能往前走，不能倒退。
# ============================================================
print("\n--- 常見可迭代物件 ---")

# 列表（list）：可迭代物件，iter() 每次產生全新的 list_iterator，
# 因此列表可以被重複迭代（每次 for 迴圈都從頭開始）。
print(f"列表 iter: {iter([1, 2, 3])}")  # <list_iterator object>

# 字串（str）：iter() 回傳 str_ascii_iterator，逐字元讀取。
print(f"字串 iter: {iter('abc')}")  # <str_ascii_iterator object>

# 字典（dict）：iter() 回傳 dict_keyiterator，預設遍歷「鍵」。
# 若要遍歷值或鍵值對，需改用 .values() / .items()。
print(f"字典 iter: {iter({'a': 1, 'b': 2})}")  # <dict_keyiterator object>

# 檔案物件（file / StringIO）本身就是迭代器——它實作了 __next__ 逐行讀取，
# 因此 iter(f) 回傳的就是 f 本身（不會建立新物件）。
import io

f = io.StringIO("line1\nline2\nline3")
print(f"檔案 iter: {iter(f)}")  # iter(f) is f → True


# ============================================================
# 3. 自訂可迭代物件
# ============================================================
# 設計模式：將「資料容器」與「迭代狀態」分成兩個類別。
#   CountDown          → 只儲存起始值，無迭代狀態，可被多次迭代。
#   CountDownIterator  → 儲存目前倒數值（current），一次性；用完即廢。
#
# 好處：同一個 CountDown 可同時有多個獨立的迭代器互不干擾，
# 就像列表可以被 for 迴圈跑無數次一樣。
# ============================================================
class CountDown:
    def __init__(self, start):
        self.start = start  # 只存資料，不存迭代狀態

    def __iter__(self):
        # 每次被 for 迴圈使用時，都建立全新的迭代器實例，
        # 確保多次迭代之間狀態完全獨立。
        return CountDownIterator(self.start)


class CountDownIterator:
    def __init__(self, start):
        self.current = start  # 可變的迭代狀態：目前倒數到哪

    def __next__(self):
        if self.current <= 0:
            # 倒數至 0，通知 for 迴圈（或 next()）停止
            raise StopIteration
        self.current -= 1       # 先遞減（例：3 → 2）
        return self.current + 1  # 再回傳遞減前的值（2 + 1 = 3）


print("\n--- 自訂迭代器 ---")
for i in CountDown(3):
    print(i, end=" ")  # 依序印出 3 2 1，for 自動捕捉 StopIteration

# ============================================================
# 4. 迭代器 vs 可迭代物件
# ============================================================
# 核心差異整理：
#   可迭代物件（Iterable）  → 有 __iter__()，可多次迭代
#   迭代器（Iterator）      → 有 __iter__() + __next__()，一次性
#   規則：所有迭代器都是可迭代物件（__iter__ 回傳 self），反之不成立
# ============================================================
print("\n\n--- 迭代器 vs 可迭代物件 ---")

# 列表沒有 __next__()，直接 next(my_list) 會拋出 TypeError。
# 但有 __iter__()，for 迴圈會先呼叫 iter() 再開始迭代。
my_list = [1, 2, 3]
print(f"列表: 可迭代物件 ✓, 迭代器 ✗")

# iter(list) 回傳 list_iterator，它有 __next__()，所以是迭代器。
# 迭代器是「一次性」的，耗盡後不能重頭；若要再迭代，需再呼叫 iter()。
my_iter = iter(my_list)
print(f"iter(列表): 可迭代物件 ✓（__iter__ 回傳 self）, 迭代器 ✓（有 __next__）")

# 迭代器的 __iter__ 慣例上回傳 self，讓它也能直接用 for 迴圈迭代。
print(f"迭代器: 可迭代物件 ✓ (有__iter__), 迭代器 ✓ (有__next__)")

# ============================================================
# 5. StopIteration 例外
# ============================================================
# Python 的 for 迴圈本質上是下方 while + try/except 的語法糖。
# 理解這個展開過程，有助於除錯迭代相關的問題。
# ============================================================
print("\n--- StopIteration 用法 ---")


# 手動展開 for 迴圈：模擬 `for item in items` 的底層行為
def manual_iter(items):
    it = iter(items)       # 步驟 1：呼叫 __iter__() 取得迭代器
    while True:
        try:
            item = next(it)              # 步驟 2：呼叫 __next__() 取值
            print(f"取得: {item}")
        except StopIteration:
            break                        # 步驟 3：StopIteration → 迴圈結束


manual_iter(["a", "b", "c"])


# 使用預設值的版本：next(iterator, default) 在耗盡時回傳預設值，
# 而非擲出 StopIteration，語法更簡潔、不需 try/except。
# ⚠ 注意：若資料本身包含 None，此方式會誤判提早停止，
#         建議改用 sentinel = object() 作為唯一哨兵值。
def manual_iter_default(items):
    it = iter(items)
    while True:
        item = next(it, None)   # None 作為「結束信號」（哨兵值）
        if item is None:        # 收到 None 代表序列已耗盡
            break
        print(f"取得: {item}")


print("\n使用預設值:")
manual_iter_default(["a", "b", "c"])
