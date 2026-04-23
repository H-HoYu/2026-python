# A06. 壓縮檔、臨時資料夾、物件序列化（5.7 / 5.19 / 5.21）
# Bloom: Apply — 能把標準庫工具組合起來解一個小任務

# gzip：讀寫 .gz 壓縮檔（介面與 open 類似）
import gzip
# pickle：將 Python 物件序列化成 bytes（僅建議在 Python 生態內使用）
import pickle
# tempfile：建立會自動清理的暫存檔案/資料夾
import tempfile
# Path：路徑與檔案操作的物件化 API
from pathlib import Path

# ── 5.7 讀寫壓縮檔：gzip.open 幾乎和 open 一樣 ─────────
# 寫 .gz（文字模式要記得 encoding）
# 文字模式 wt：寫入 str，gzip 會先編碼再壓縮
with gzip.open("notes.txt.gz", "wt", encoding="utf-8") as f:
    f.write("第一行筆記\n")
    f.write("第二行筆記\n")

# 讀回：直接逐行迭代
# 文字模式 rt：讀出時會先解壓縮，再依 encoding 解碼成 str
with gzip.open("notes.txt.gz", "rt", encoding="utf-8") as f:
    for line in f:
        # line 通常含尾端換行，顯示前用 rstrip() 去掉
        print("gz:", line.rstrip())

# 也能用 'wb'/'rb' 處理二進位資料
# 二進位模式 wb：直接寫 bytes，不處理文字編碼
with gzip.open("blob.bin.gz", "wb") as f:
    f.write(b"\x00\x01\x02\x03")

# stat().st_size 是「壓縮後檔案」實際大小（單位 bytes）
print("blob size:", Path("blob.bin.gz").stat().st_size, "bytes")

# ── 5.19 臨時檔案與資料夾：離開 with 自動清理 ──────────
# 場景：想跑個小實驗但不想在專案亂留檔
# TemporaryDirectory() 會建立一個暫存目錄，離開 with 後自動刪除
with tempfile.TemporaryDirectory() as tmp:
    # tmp 原本是字串路徑，轉成 Path 方便後續操作
    tmp = Path(tmp)
    print("暫存資料夾:", tmp)

    # 在裡面寫幾個檔
    (tmp / "a.txt").write_text("hello\n", encoding="utf-8")
    (tmp / "b.txt").write_text("world\n", encoding="utf-8")

    # 列出內容
    # iterdir() 只列當層，不遞迴
    for p in tmp.iterdir():
        print("  ", p.name, "→", p.read_text(encoding="utf-8").rstrip())

# 離開 with 後，tmp 已自動刪除
print("離開後還存在嗎？", tmp.exists())  # False

# 單一臨時檔：NamedTemporaryFile
# delete=False：關閉檔案後不立刻刪除，方便跨流程/外部程式再使用
with tempfile.NamedTemporaryFile("wt", delete=False, suffix=".log",
                                 encoding="utf-8") as f:
    f.write("暫存 log\n")
    # f.name 是暫存檔實際路徑
    log_path = f.name
print("暫存檔位置:", log_path)

# 用完後手動刪除，避免留下垃圾檔
Path(log_path).unlink()  # 用完自己刪

# ── 5.21 pickle：把 Python 物件「原樣」存檔 ────────────
# 適用：dict/list/自訂類別；不適用：跨語言、長期存檔（用 json 更穩）
scores = {
    "alice": [90, 85, 92],
    "bob":   [70, 75, 80],
    "carol": [88, 91, 95],
}

# 注意：pickle 是 bytes → 一定要 'wb'/'rb'
# dump：把 Python 物件序列化並寫入檔案
with open("scores.pkl", "wb") as f:
    pickle.dump(scores, f)

# load：從檔案讀回 bytes 並反序列化為 Python 物件
with open("scores.pkl", "rb") as f:
    loaded = pickle.load(f)

print("讀回的物件:", loaded)
print("型別一致?", type(loaded) is dict)         # True
print("內容相等?", loaded == scores)              # True

# 讀回資料後可直接做一般運算
print("alice 平均:", sum(loaded["alice"]) / 3)   # 89.0

# ⚠️ 安全提醒：pickle.load 會執行內嵌指令，
# 絕對不要對「來路不明」的 .pkl 檔做 load。

# ── 課堂延伸挑戰 ───────────────────────────────────────
# 1) 把 scores 存成 gzip 壓縮後的 pickle：gzip.open('scores.pkl.gz','wb')
# 2) 用 TemporaryDirectory 跑完整流程（寫→讀→比對），不在專案留任何檔
# 3) 試著 pickle 一個 lambda，觀察錯誤訊息（pickle 不能存 lambda）
