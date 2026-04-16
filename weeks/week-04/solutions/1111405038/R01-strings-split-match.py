# R01. 字串分割與匹配（2.1–2.3）
# re.split() 多分隔符 / startswith / endswith / fnmatch

import re
from fnmatch import fnmatch, fnmatchcase

# ── 2.1 多界定符分割 ──────────────────────────────────
# 這個字串同時包含空白、分號、逗號等不同分隔符，
# 單靠 str.split() 很難一次處理，所以改用 re.split()。
line = "asdf fjdk; afed, fjek,asdf, foo"

# [;,\s] 表示「符合分號、逗號或任一空白字元」其中之一。
# 後面的 \s* 表示：分隔符後面如果還有 0 個以上空白，也一併吃掉。
# 因此可以把不同格式的分隔方式統一切開。
print(re.split(r"[;,\s]\s*", line))
# ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

# 這裡改用另一種寫法：(?:...) 是「非捕獲分組」，
# 用來把多個選項放在一起比對，但不會把分組內容保留下來。
# 也就是說，這些分隔符只負責切割，不會出現在結果串列中。
print(re.split(r"(?:,|;|\s)\s*", line))
# ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

# ── 2.2 開頭/結尾匹配 ────────────────────────────────
# startswith() 與 endswith() 適合做簡單、快速、可讀性高的前後綴判斷。
# 這類需求若不用正規表示式，通常會更直觀也更容易維護。
filename = "spam.txt"
# 判斷檔名是否以 .txt 結尾。
print(filename.endswith(".txt"))  # True
# 判斷字串是否以 file: 開頭。
print(filename.startswith("file:"))  # False

# 同時檢查多種後綴 → 傳入 tuple（不能傳 list）
# endswith() 可以一次接收多個候選結尾，常用在篩選副檔名。
# 下面會挑出所有以 .c 或 .h 結尾的檔案名稱。
filenames = ["Makefile", "foo.c", "bar.py", "spam.c", "spam.h"]
print([name for name in filenames if name.endswith((".c", ".h"))])
# ['foo.c', 'spam.c', 'spam.h']

# ── 2.3 Shell 通配符匹配 ─────────────────────────────
# fnmatch() 使用的是 shell 風格的萬用字元，不是正規表示式。
# * 代表任意長度字元，適合做簡單樣式比對。
print(fnmatch("foo.txt", "*.txt"))  # True

# [0-9] 代表任一數字，所以 Dat[0-9]* 表示：
# 開頭是 Dat，後面接一個數字，再接任意長度字元。
print(fnmatch("Dat45.csv", "Dat[0-9]*"))  # True

# fnmatch() 在不同作業系統上可能會受到檔名大小寫規則影響；
# 若想明確要求大小寫必須完全一致，可使用 fnmatchcase()。
print(fnmatchcase("foo.txt", "*.TXT"))  # False

# 篩選所有以 ST 結尾的地址。
# 這裡使用 fnmatchcase(a, "* ST")，表示前面可有任意字元，最後必須是空白加上 ST。
addresses = ["5412 N CLARK ST", "1060 W ADDISON ST", "1039 W GRANVILLE AVE"]
print([a for a in addresses if fnmatchcase(a, "* ST")])
# ['5412 N CLARK ST', '1060 W ADDISON ST']
