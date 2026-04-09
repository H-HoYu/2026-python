# U03. 字串格式化效能與陷阱（2.14–2.20）
# ============================================================
# 本檔案涵蓋三個常見陷阱：
#   1. 字串串接：+ 運算子 vs join() 的效能差異
#   2. format_map：遇到缺失鍵時如何避免 KeyError
#   3. bytes 索引：回傳整數而非字元，與 str 行為不同
# ============================================================

import timeit

# ============================================================
# 陷阱 1：字串串接用 + 效能差（2.14）
# ============================================================
# 原因：Python 的 str 是不可變物件（immutable）。
# 每次執行 s += p，Python 必須：
#   1. 建立一個「長度 = len(s) + len(p)」的全新字串物件
#   2. 把 s 和 p 都複製進去
#   3. 丟棄舊的 s
# 因此 n 次串接需複製 1+2+3+...+n 個字元 → O(n²) 時間複雜度
#
# ".join(iterable) 的做法：
#   Python 先掃描整個 iterable 計算總長度，
#   一次性分配足夠記憶體，再逐一複製 → O(n) 時間
#
# 規則：需要把多個字串合而為一時，永遠優先用 join()。
# ============================================================
parts = [f"item{i}" for i in range(1000)]  # 1000 個字串片段


def bad_concat():
    s = ""
    for p in parts:
        s += p  # 每次都建立新字串物件，累積 O(n²) 複製成本
    return s


def good_join():
    return "".join(parts)  # 以空字串為分隔符，一次性合併，O(n)


t1 = timeit.timeit(bad_concat, number=500)
t2 = timeit.timeit(good_join, number=500)
print(f"+串接: {t1:.3f}s  join: {t2:.3f}s")  # join 通常快數倍甚至數十倍


# ============================================================
# 陷阱 2：format_map 遇到缺失鍵會拋出 KeyError（2.15）
# ============================================================
# str.format_map(mapping) 與 str.format(**kwargs) 類似，
# 但直接接受 dict-like 物件，適合動態命名空間（如 vars()）。
#
# 問題：若佔位符 {key} 在 mapping 中不存在，會拋出 KeyError。
# 解法：繼承 dict 並覆寫 __missing__ 方法。
#   __missing__(key) 在 key 不存在時被自動呼叫（非 KeyError），
#   讓我們攔截缺失鍵，回傳保留原佔位符的字串。
#
# 應用場景：模板部分填充（partial template rendering），
# 只填寫已知變數，未知變數留待下一步再填。
# ============================================================
class SafeSub(dict):
    def __missing__(self, key: str) -> str:
        # 當 format_map 查詢 key 但 dict 中找不到時，
        # 回傳 "{key}" 字串，讓佔位符原樣保留而不報錯。
        return "{" + key + "}"


name = "Guido"  # 定義在區域命名空間，vars() 可以取到
s = "{name} has {n} messages."
# vars() 回傳目前區域命名空間的 dict，包含 name="Guido"，但沒有 n。
# SafeSub 攔截 {n} 的缺失，保留為 "{n}" 字串。
print(s.format_map(SafeSub(vars())))  # 'Guido has {n} messages.'

# ============================================================
# 陷阱 3：bytes 索引回傳整數，而非字元（2.20）
# ============================================================
# str[i]   → 回傳長度為 1 的字串（字元）
# bytes[i] → 回傳 0–255 的整數（該位元組的值）
#
# 這個行為差異容易在把 str 程式碼改寫成 bytes 版本時踩到。
# 若需要取得單一位元組的「字元表示」，用 chr(b[i]) 轉換。
#
# 另一個常見陷阱：bytes 物件不支援 % 格式化或 .format()，
# 必須先對 str 格式化完畢，再呼叫 .encode() 轉成 bytes。
# ============================================================
a = "Hello"   # str 物件
b = b"Hello"  # bytes 物件（ASCII 位元組序列）
print(a[0])   # 'H'（str，長度 1 的字串）
print(b[0])   # 72（int，'H' 的 ASCII 碼 = ord('H')）
# 若需要字元：chr(b[0]) == 'H'

# bytes 不能直接 format，需先格式化再 encode
# 正確流程：str.format() → 產生格式化字串 → .encode('ascii') → bytes
print("{:10s} {:5d}".format("ACME", 100).encode("ascii"))
# b'ACME            100'
# {:10s} = 左對齊、寬度 10 的字串；{:5d} = 寬度 5 的整數
