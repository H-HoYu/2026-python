# R16. 過濾：推導式 / generator / filter / compress（1.16）

# 這份範例示範幾種常見的「篩選資料」方式。
# 有些方式會立刻產生結果，有些則是延後計算。

mylist = [1, 4, -5, 10]

# 串列推導式：從 mylist 中挑出大於 0 的元素。
# 這種寫法會立刻建立新的 list，結果是 [1, 4, 10]。
[n for n in mylist if n > 0]

# generator expression（生成器表達式）和串列推導式很像，
# 但它不會立刻把所有結果都算出來，而是需要時才逐個產生。
# 因此比較省記憶體，適合處理大量資料。
pos = (n for n in mylist if n > 0)

# 這組資料混有可轉成整數的字串，以及無法轉換的內容。
values = ['1', '2', '-3', '-', 'N/A']

# 自訂判斷函式：如果 val 可以成功轉成 int，就回傳 True；
# 否則表示它不是有效整數字串，回傳 False。
def is_int(val):
    try:
        # int(val) 只用來測試是否能轉型，成功就代表合法。
        int(val); return True
    except ValueError:
        return False

# filter(is_int, values) 會把 values 中每個元素交給 is_int 檢查，
# 只保留回傳 True 的項目。
# 在 Python 3 中，filter() 回傳的是迭代器，因此常用 list() 包起來查看結果。
list(filter(is_int, values))

from itertools import compress

# compress(data, selectors) 會根據 selectors 中對應位置的布林值，
# 決定是否保留 data 裡的元素。
addresses = ['a1', 'a2', 'a3']
counts = [0, 3, 10]

# 先建立條件列表：只有大於 5 的位置會是 True。
# 結果為 [False, False, True]。
more5 = [n > 5 for n in counts]

# 因此只有 addresses 中對應到 True 的元素會被留下，也就是 ['a3']。
list(compress(addresses, more5))
