# R03. 字串清理、對齊、拼接與格式化（2.11–2.16）
# strip / ljust / join / format / format_map / textwrap

import textwrap

# ── 2.11 清理字元 ─────────────────────────────────────
# 原字串前面有空白，後面有空白與換行字元 \n。
# repr() 用來把不可見字元也顯示出來，方便觀察 strip 的效果。
s = "  hello world \n"

# strip() 預設會移除字串左右兩端的空白字元，
# 包含空白、tab、換行等，但不會影響中間的內容。
print(repr(s.strip()))  # 'hello world'

# lstrip() 只移除左側的空白字元，右邊保留不動。
print(repr(s.lstrip()))  # 'hello world \n'

# strip("-=") 不是把整段 "-=" 當成固定前後綴，
# 而是表示「左右兩端只要是 - 或 = 就持續移除」。
print("-----hello=====".strip("-="))  # 'hello'

# ── 2.13 字串對齊 ─────────────────────────────────────
# 以下示範如何把文字排到固定寬度，常用於表格輸出或主控台排版。
text = "Hello World"

# ljust(20) 表示靠左對齊，總寬度補到 20 個字元。
print(text.ljust(20))  # 'Hello World         '

# rjust(20) 表示靠右對齊。
print(text.rjust(20))  # '         Hello World'

# center(20, "*") 表示置中，空白不足的部分用 * 補滿。
print(text.center(20, "*"))  # '****Hello World*****'

# format() 提供更通用的格式控制。
# ^20 表示在寬度 20 內置中對齊。
print(format(text, "^20"))  # '    Hello World     '

# >10.2f 表示數字靠右、總寬 10、顯示 2 位小數。
print(format(1.2345, ">10.2f"))  # '      1.23'

# ── 2.14 合併拼接 ─────────────────────────────────────
# join() 是字串串接的標準方法。
# 呼叫者本身是「分隔符」，括號內則是要被串起來的字串序列。
parts = ["Is", "Chicago", "Not", "Chicago?"]

# 以單一空白作為分隔符。
print(" ".join(parts))  # 'Is Chicago Not Chicago?'

# 以逗號作為分隔符。
print(",".join(parts))  # 'Is,Chicago,Not,Chicago?'

# join() 要求序列中的元素必須都是字串。
# 因此若資料中有整數、浮點數，要先轉成 str。
data = ["ACME", 50, 91.1]
print(",".join(str(d) for d in data))  # 'ACME,50,91.1'

# ── 2.15 插入變量 ─────────────────────────────────────
# 這一段示範三種常見的字串插值方式。
name, n = "Guido", 37
s = "{name} has {n} messages."

# format() 以關鍵字參數把值帶入欄位名稱。
print(s.format(name=name, n=n))  # 'Guido has 37 messages.'

# format_map() 接收一個 mapping，例如 dict。
# vars() 會回傳目前區域變數的字典，因此可直接帶入 name、n。
print(s.format_map(vars()))  # 'Guido has 37 messages.'

# f-string 可直接在字串中嵌入變數或表達式，通常最直觀、最常用。
print(f"{name} has {n} messages.")  # f-string（最簡潔）

# ── 2.16 指定列寬 ─────────────────────────────────────
# textwrap.fill() 會把長字串自動折成指定寬度，
# 很適合輸出說明文字、文件或終端機訊息。
long_s = (
    "Look into my eyes, look into my eyes, the eyes, "
    "not around the eyes, look into my eyes, you're under."
)

# 每行最大寬度設為 40。
print(textwrap.fill(long_s, 40))

# initial_indent 只會影響第一行的縮排。
print(textwrap.fill(long_s, 40, initial_indent="    "))
