# R02. 正則表達式：搜尋、替換、旗標（2.4–2.8）
# re.compile / findall / sub / IGNORECASE / 非貪婪 / DOTALL

import re

# ── 2.4 匹配和搜尋 ────────────────────────────────────
# 測試字串中包含兩個日期，格式皆為 月/日/年。
text = "Today is 11/27/2012. PyCon starts 3/13/2013."

# 先把正則表達式編譯成 Pattern 物件，之後重複使用時會更方便。
# (\d+) 代表「一個以上的數字」，這裡用 3 個群組分別抓 month/day/year。
# 中間的 / 則是字面上的斜線。
datepat = re.compile(r"(\d+)/(\d+)/(\d+)")

# findall() 會找出字串中所有符合的片段。
# 因為樣式中有 3 個括號群組，所以回傳結果會是 tuple 的串列。
print(datepat.findall(text))
# [('11', '27', '2012'), ('3', '13', '2013')]

# match() 只會從字串開頭開始比對。
# 這個字串一開頭就是日期，因此能成功取得 Match 物件。
m = datepat.match("11/27/2012")
assert m is not None
# group(0) 是整段匹配到的文字；groups() 則是各個括號群組的內容。
print(m.group(0), m.groups())  # '11/27/2012' ('11', '27', '2012')

# finditer() 會逐一回傳每個匹配結果的 Match 物件。
# 若後續還要做欄位拆解、格式轉換，finditer() 通常比 findall() 更彈性。
for m in datepat.finditer(text):
    month, day, year = m.groups()
    print(f"{year}-{month}-{day}")

# ── 2.5 搜尋和替換 ───────────────────────────────────
# re.sub() 用來把符合樣式的內容替換成新字串。
# \1、\2、\3 分別代表第 1、2、3 個括號群組。
# 下面把原本的 月/日/年 改成 年-月-日。
print(re.sub(r"(\d+)/(\d+)/(\d+)", r"\3-\1-\2", text))
# 'Today is 2012-11-27. PyCon starts 2013-3-13.'

# 命名群組讓正則更容易閱讀。
# (?P<month>...) 表示把這個群組命名為 month，
# 替換時就能用 \g<month> 這種較清楚的方式引用。
print(
    re.sub(
        r"(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)",
        r"\g<year>-\g<month>-\g<day>",
        text,
    )
)

# re.subn() 和 re.sub() 類似，但會額外回傳替換次數。
# 第一個回傳值是新字串，第二個回傳值是實際替換了幾次。
newtext, n = re.subn(r"(\d+)/(\d+)/(\d+)", r"\3-\1-\2", text)
print(f"替換了 {n} 次")  # 替換了 2 次

# ── 2.6 忽略大小寫 ───────────────────────────────────
# flags=re.IGNORECASE 讓搜尋時忽略大小寫差異，
# 所以 PYTHON、python、Python 都會被視為匹配成功。
s = "UPPER PYTHON, lower python, Mixed Python"
print(re.findall("python", s, flags=re.IGNORECASE))
# ['PYTHON', 'python', 'Python']

# ── 2.7 非貪婪（最短匹配）────────────────────────────
# 這個字串裡有兩段被雙引號包住的內容。
text2 = 'Computer says "no." Phone says "yes."'

# .* 是貪婪匹配，會盡可能吃到最長。
# 因此它會從第一個引號一路吃到最後一個引號，
# 導致中間兩段文字被當成一次匹配。
print(re.compile(r'"(.*)"').findall(text2))  # 貪婪：['no." Phone says "yes.']

# .*? 是非貪婪匹配，表示「在滿足整體規則的前提下盡量短」。
# 因此每次只抓到一對引號中的最短內容。
print(re.compile(r'"(.*?)"').findall(text2))  # 非貪婪：['no.', 'yes.']

# ── 2.8 多行匹配（DOTALL）────────────────────────────
# 一般情況下，. 不會匹配換行字元。
# 開啟 re.DOTALL 後，. 就可以跨行匹配，適合抓取多行區塊。
code = "/* this is a\nmultiline comment */"
print(re.compile(r"/\*(.*?)\*/", re.DOTALL).findall(code))
# [' this is a\nmultiline comment ']
