# U01. 字串分割與匹配的陷阱（2.1–2.11）
# ============================================================
# 本檔案示範三個處理字串時容易踩到的陷阱：
#   1. re.split() 捕獲分組（capturing group）會保留分隔符在結果中
#   2. str.startswith() / endswith() 只接受 str 或 tuple，不接受 list
#   3. str.strip() 只清除頭尾空白，中間多餘空白需另外處理
# ============================================================

import re

# ============================================================
# 陷阱 1：捕獲分組保留分隔符（2.1）
# ============================================================
# re.split() 的行為差異：
#   - 無括號：re.split(r";|,|\s", s)  → 分隔符直接丟棄
#   - 有括號：re.split(r"(;|,|\s)", s) → 分隔符保留在結果清單中
#
# 有括號時，結果清單的結構為：
#   [值, 分隔符, 值, 分隔符, 值, ...]
#   索引 0, 2, 4... = 實際內容（偶數）
#   索引 1, 3, 5... = 分隔符（奇數）
#
# 本例額外加上 \s* 消耗分隔符後面的多餘空白，
# 但 \s* 不在括號內，所以不會出現在結果中。
# ============================================================
line = "asdf fjdk; afed, fjek,asdf, foo"
fields = re.split(r"(;|,|\s)\s*", line)
# fields 內容示意：['asdf', ' ', 'fjdk', ';', 'afed', ',', 'fjek', ',', 'asdf', ',', 'foo']
values = fields[::2]       # 偶數索引 = 實際值：['asdf','fjdk','afed','fjek','asdf','foo']
delimiters = fields[1::2] + [""]  # 奇數索引 = 分隔符，補一個空字串讓 zip 對齊
# 將每個值與其後的分隔符拼接，重新組合成清理過的字串
rebuilt = "".join(v + d for v, d in zip(values, delimiters))
print(rebuilt)  # 'asdf fjdk;afed,fjek,asdf,foo'（多餘空白已去除）

# ============================================================
# 陷阱 2：startswith / endswith 只接受 tuple，不接受 list（2.2）
# ============================================================
# str.startswith(prefix) 的 prefix 參數型別限制：
#   ✓ str    → startswith("http:")
#   ✓ tuple  → startswith(("http:", "ftp:"))  ← 同時檢查多個前綴
#   ✗ list   → TypeError（即使內容相同，list 也不行）
#
# 常見場景：從設定檔讀入 list，直接丟入時才發現錯誤。
# 修正方式：用 tuple() 轉型，或改用 any() + 生成器。
# ============================================================
url = "http://www.python.org"
choices = ["http:", "ftp:"]  # 從設定讀入的是 list
try:
    url.startswith(choices)  # type: ignore[arg-type]  ← 此行會拋出 TypeError
except TypeError as e:
    print(f"TypeError: {e}")  # first arg must be str or a tuple of str, not list
print(url.startswith(tuple(choices)))  # True（轉成 tuple 後正確執行）
# 替代寫法（語意更清晰，但效能略低）：
# print(any(url.startswith(c) for c in choices))

# ============================================================
# 陷阱 3：strip 只處理頭尾，中間多餘空白需另外處理（2.11）
# ============================================================
# str.strip([chars])：移除字串「開頭」與「結尾」的指定字元（預設為空白）
#   ✓ 移除頭尾空白 / \t / \n / \r
#   ✗ 不處理字串中間的多餘空白
#
# 三種常見做法的比較：
#   1. s.strip()          → 只清頭尾，中間多餘空白原封不動（常見誤解）
#   2. s.replace(" ", "") → 把所有空格全刪，連詞間的分隔也消失（過度清理）
#   3. re.sub(r"\s+"," ",s.strip()) → 先清頭尾，再把連續空白壓縮為一個（推薦）
# ============================================================
s = "  hello     world  "
print(repr(s.strip()))               # 'hello     world'  ← 中間 5 個空格仍在
print(repr(s.replace(" ", "")))      # 'helloworld'       ← 詞間空格也消失了
print(repr(re.sub(r"\s+", " ", s.strip())))  # 'hello world'  ← 正確結果

# ── 高效逐行清理：生成器表達式（2.11）───────────────
# 使用「生成器表達式」(generator expression) 取代先建立完整 list 再遍歷，
# 優點：惰性求值（lazy evaluation），一次只處理一行，不預先載入全部資料，
# 適合處理超大檔案或串流資料。
lines = ["  apple  \n", "  banana  \n"]
for line in (l.strip() for l in lines):  # 括號 () = 生成器；方括號 [] 才是 list
    print(line)  # 每次迴圈才計算一行，記憶體用量為 O(1)
