# R01. 文本 I/O 基本式（5.1 / 5.2 / 5.3 / 5.17）
# Bloom: Remember — 會叫出 open/print 的基本參數

# Path 提供方便的檔案路徑操作與快速讀寫方法（read_text / write_text）
from pathlib import Path

# ── 5.1 讀寫文本檔 ─────────────────────────────────────
# 寫入：mode='wt'（write text）
# 重點：文字檔應明確指定 encoding='utf-8'，避免不同系統預設編碼造成亂碼
path = Path("hello.txt")
with open(path, "wt", encoding="utf-8") as f:
    # write() 會回傳寫入字元數；這裡不需使用回傳值
    f.write("你好，Python\n")
    f.write("第二行\n")

# 讀回：一次讀完 vs 逐行讀
with open(path, "rt", encoding="utf-8") as f:
    # f.read() 會一次把整個檔案載入記憶體
    # 適合小檔；大檔可能吃掉大量 RAM
    print(f.read())  # 一次讀完（小檔才適合）

with open(path, "rt", encoding="utf-8") as f:
    # 逐行迭代：一次只讀一行，對大檔更安全、穩定
    for line in f:  # 大檔必備：逐行迭代
        # line 本身通常含有尾端換行，因此用 rstrip() 去除右側空白/換行
        print(line.rstrip())

# ── 5.2 print 導向檔案 ─────────────────────────────────
# print(..., file=f) 可把輸出改寫到檔案，而不是終端機
with open("log.txt", "wt", encoding="utf-8") as f:
    print("登入成功", file=f)
    print("使用者:", "alice", file=f)

# ── 5.3 調整分隔符與行終止符 ───────────────────────────
fruits = ["apple", "banana", "cherry"]
with open("fruits.csv", "wt", encoding="utf-8") as f:
    # *fruits 展開清單，sep="," 指定欄位分隔
    # end="\n" 保留每次 print 結尾換行（預設本來就是 \n）
    print(*fruits, sep=",", end="\n", file=f)

# end='' 可避免多一個換行
with open("fruits.csv", "at", encoding="utf-8") as f:
    # 'at' = append text：在原檔尾端追加，不覆蓋既有內容
    print("date", end=",", file=f)
    print("2026-04-23", file=f)

# 用 Path.read_text 快速讀回整個文字檔並印出
print(Path("fruits.csv").read_text(encoding="utf-8"))
# apple,banana,cherry
# date,2026-04-23

# ── 5.17 文字模式 vs 位元組模式提醒 ────────────────────
# 'wt' 寫 str、'wb' 寫 bytes；寫錯型別會 TypeError
try:
    with open("bad.txt", "wt", encoding="utf-8") as f:
        # 文字模式要求 str；這裡故意傳 bytes 來示範錯誤
        f.write(b"bytes in text mode")  # ← 會錯
except TypeError as e:
    # 捕捉後印出錯誤，讓教學流程能繼續執行
    print("錯誤示範:", e)
