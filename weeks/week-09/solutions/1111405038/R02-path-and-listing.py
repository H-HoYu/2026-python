# R02. 路徑操作與目錄列舉（5.11 / 5.12 / 5.13）
# Bloom: Remember — 會用 pathlib 組路徑、檢查存在、列出檔案

# os：傳統路徑/檔案系統 API，像 os.path.join、os.listdir
import os
# Path：pathlib 的核心類別，物件化路徑操作更直覺、可讀性更高
from pathlib import Path

# ── 5.11 組路徑：pathlib 是現代寫法 ────────────────────
# 用 / 來串接路徑（不是做除法），會自動處理不同平台分隔符
base = Path("weeks") / "week-09"

# Path 物件常用屬性：
# - name：最後一段名稱
# - parent：上一層路徑
# - suffix：副檔名（含點），資料夾通常為空字串
print(base)              # weeks/week-09（Windows 會自動變成反斜線）
print(base.name)         # week-09
print(base.parent)       # weeks
print(base.suffix)       # ''（無副檔名）

# 檔名相關拆解：
# - stem：去掉副檔名後的主檔名
# - suffix：副檔名
f = Path("hello.txt")
print(f.stem, f.suffix)  # hello .txt

# 相容舊寫法：os.path.join
# 舊專案常見，了解有助於閱讀既有程式碼
print(os.path.join("weeks", "week-09", "README.md"))

# ── 5.12 存在判斷 ──────────────────────────────────────
p = Path("hello.txt")

# 三個常用檢查：
# - exists()：路徑是否存在（檔案或資料夾都算）
# - is_file()：是否是檔案
# - is_dir()：是否是資料夾
print(p.exists())    # 是否存在
print(p.is_file())   # 是否是檔案
print(p.is_dir())    # 是否是資料夾

# 常見防呆：先檢查存在，再決定是否讀取/處理
missing = Path("no_such_file.txt")
if not missing.exists():
    print(f"{missing} 不存在，略過讀取")

# ── 5.13 列出資料夾內容 ────────────────────────────────
# 目前工作目錄（current working directory）
here = Path(".")

# 只列當層
# os.listdir 回傳字串名稱，不含完整路徑
for name in os.listdir(here):
    print("listdir:", name)

# 只抓 .py（當層）
# Path.glob 回傳 Path 物件，可直接做後續檔案操作
for p in here.glob("*.py"):
    print("glob:", p)

# 遞迴抓所有 .py（含子資料夾）
# rglob 會深入子目錄；在大型專案中結果可能很多
for p in Path("..").rglob("*.py"):
    print("rglob:", p)
    break  # 示範用，只印第一個
