# U03. 文字 vs 位元組、編碼觀念（5.1 encoding / 5.4）
# Bloom: Understand — 能解釋什麼時候用 'rb'、為什麼要指定 encoding

# Path 提供直觀的路徑與檔案操作 API（write_text / write_bytes / read_text）
from pathlib import Path

# ── 5.4 二進位讀寫：圖片、zip、任何非文字 ───────────────
# 先造一個「假 PNG」：只寫前 8 bytes 的 magic number（檔案簽章）
# PNG 固定檔頭為：89 50 4E 47 0D 0A 1A 0A（16 進位）
# bytes([...]) 會把 0~255 的整數序列轉成位元組物件
magic = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])

# write_bytes：以二進位方式寫入，不涉及文字編碼
Path("fake.png").write_bytes(magic)

# 讀回前 8 bytes，對照 PNG 檔頭
# 注意這裡用 'rb'（read binary）：讀到的是 bytes，不是 str
with open("fake.png", "rb") as f:
    head = f.read(8)

# bytes 的印出格式會帶 b'' 前綴
print(head)           # b'\x89PNG\r\n\x1a\n'

# 直接比較兩個 bytes 內容是否完全一致
print(head == magic)  # True

# bytes 可逐位元組迭代（拿到 int，不是 str）
# head[:4] 只取前四個位元組，示範每個位元組可轉成十六進位顯示
for b in head[:4]:
    print(b, hex(b))

# ── 文字 vs 位元組的型別差 ─────────────────────────────
s = "你好"

# encode：把 Python 字串（Unicode）依指定編碼轉成 bytes
b = s.encode("utf-8")   # str → bytes

# 型別對照：文字是 str、編碼後是 bytes
print(s, type(s))       # <class 'str'>
print(b, type(b))       # <class 'bytes'>

# decode：把 bytes 按相同編碼還原回字串
print(b.decode("utf-8"))  # bytes → str

# ── 5.1 encoding 參數：寫錯會爛掉 ──────────────────────
# 用 UTF-8 寫入中文文字檔
Path("zh.txt").write_text("中文測試\n", encoding="utf-8")

# 正常：用 utf-8 讀 utf-8 寫的檔
print(Path("zh.txt").read_text(encoding="utf-8"))

# 故意弄錯：用 big5 解 utf-8 → UnicodeDecodeError
# 不同編碼規則彼此不一定相容，讀取時編碼要和寫入時一致
try:
    print(Path("zh.txt").read_text(encoding="big5"))
except UnicodeDecodeError as e:
    # 捕捉解碼失敗，避免程式直接中止
    print("解碼錯誤:", e)

# 小結：
# - 文字檔 → 'rt'/'wt'，一律明示 encoding='utf-8'
# - 非文字（png/zip/pickle）→ 'rb'/'wb'，不談 encoding
