# U04. 類檔案物件 StringIO 與逐行處理（5.6 / 5.1 逐行）
# Bloom: Understand — 知道 file-like 是鴨子型別，能把記憶體當檔案用

# io：提供 StringIO/BytesIO，讓「記憶體中的資料」看起來像檔案物件
import io
# Path：以物件方式操作路徑，跨平台且比字串拼接更安全
from pathlib import Path

# ── 5.6 StringIO：記憶體裡的「假檔案」 ─────────────────
# 建立一個空的文字緩衝區（in-memory text stream）
# 它支援 .write()、.read()、迭代等檔案常見操作
buf = io.StringIO()

# print(..., file=buf) 代表把輸出導向 buf，而不是終端機
# 這和 print(..., file=open(...)) 的概念完全一致
print("第一行", file=buf)
print("第二行", file=buf)
print("第三行", file=buf)

# getvalue() 會一次取出目前緩衝區中的完整文字內容
# 常用於測試：先把函式輸出寫到 StringIO，再比對字串是否正確
text = buf.getvalue()
print("---StringIO 內容---")
print(text)

# 寫入後，游標會停在尾端；若要「從頭讀」，要先 seek(0)
# 這和實體檔案的讀寫游標行為相同
buf.seek(0)

# enumerate(buf, 1)：逐行迭代並從 1 開始編號
# line 會保留行尾 '\n'，所以輸出前常用 rstrip() 去掉尾端換行
for i, line in enumerate(buf, 1):
    print(i, line.rstrip())

# 為什麼有用？任何收 file-like 的 API（csv、json、logging）
# 都能塞 StringIO，不必真的寫到磁碟、方便測試。
import csv

# 第二個記憶體檔案：示範 csv.writer 也能直接寫入 StringIO
mem = io.StringIO()
writer = csv.writer(mem)

# writerow 會自動依 CSV 規則處理欄位分隔與必要的跳脫
writer.writerow(["name", "score"])
writer.writerow(["alice", 90])

# 取出記憶體中的 CSV 文字，可直接拿去顯示、傳輸或測試比對
print("---CSV in memory---")
print(mem.getvalue())

# ── 5.1 延伸：逐行處理檔案（大檔友善） ─────────────────
# 先造一個多行檔：中間刻意放空行，方便示範「過濾空白行」
src = Path("poem.txt")

# write_text 是 Path 的便捷 API，等價於 open(...).write(...)
# 明確指定 encoding='utf-8' 可避免跨系統編碼差異
src.write_text("床前明月光\n\n疑是地上霜\n\n舉頭望明月\n低頭思故鄉\n", encoding="utf-8")

# 任務：過濾空行、加上行號、寫到新檔
dst = Path("poem_numbered.txt")

# 同時開啟來源與目的檔案：
# - src 用 'rt' 文字讀取
# - dst 用 'wt' 文字寫入（若已存在會覆蓋）
# 反斜線（\）是換行續寫語法，讓 with 區塊更易讀
with open(src, "rt", encoding="utf-8") as fin, \
     open(dst, "wt", encoding="utf-8") as fout:
    # n：輸出的「有效行」計數器（不含空白行）
    n = 0

    # 逐行處理是大檔實務中的基本技巧：
    # 一次只保留當前行，記憶體使用量穩定
    for line in fin:
        # rstrip() 去除右側空白與換行，便於判斷是否為空行
        line = line.rstrip()

        # 空字串代表空行（或只有空白），直接跳過不輸出
        if not line:
            continue

        # 只有非空行才編號，讓結果連續
        n += 1

        # {n:02d}：數字補 0 至兩位，例如 01、02、03
        # file=fout：把格式化後字串寫到目的檔
        print(f"{n:02d}. {line}", file=fout)

# 最後讀回輸出檔，確認結果是否符合預期
print("---加行號後---")
print(dst.read_text(encoding="utf-8"))
