# A05. 綜合應用：僅寫新檔 + 目錄統計（5.5 / 5.13 / 5.1）
# Bloom: Apply — 把前面學到的 API 組起來解小任務

# Path：跨平台路徑操作（組路徑、檢查存在、遞迴找檔）
from pathlib import Path
# date：取得今天日期，用來生成「每日唯一」的日記檔名
from datetime import date

# ── 任務一：日記小工具（5.5 的 'x' 模式） ──────────────
# 規則：每天只能建一次；同一天重複執行要提示「已存在」。
# isoformat() 會得到 YYYY-MM-DD 格式，適合放進檔名
today = date.today().isoformat()          # 例如 2026-04-23

# 每天一個檔案，例如 diary-2026-04-23.txt
diary = Path(f"diary-{today}.txt")

try:
    # 'x' = exclusive create：檔案不存在才建立，已存在就丟 FileExistsError
    # 這個模式很適合「避免覆蓋」的情境（像每日日記、初始化設定檔）
    with open(diary, "x", encoding="utf-8") as f:   # 'x' = exclusive create
        f.write(f"# {today} 日記\n")
        f.write("今天學了檔案 I/O。\n")

    # 只有成功建立新檔時才會走到這裡
    print(f"已建立 {diary}")
except FileExistsError:
    # 若同日已建立過，就提示並保留既有內容
    print(f"{diary} 今天已寫過，保留原內容不覆蓋")

# ── 任務二：統計某資料夾裡 .py 檔的行數 ────────────────
# 走訪目錄 → 逐檔逐行讀 → 累計三個數字
def count_py(folder: Path):
    # total：總行數（含空行）
    # nonblank：非空白行數
    # defs：去掉前後空白後，以 "def " 開頭的行數
    total, nonblank, defs = 0, 0, 0

    # rglob("*.py")：遞迴掃描 folder 及所有子資料夾中的 .py 檔
    for p in folder.rglob("*.py"):
        # errors="replace"：遇到少數無法解碼字元時用替代字元，不讓程式中斷
        with open(p, "rt", encoding="utf-8", errors="replace") as f:
            for line in f:
                # 每讀到一行就累計總行數
                total += 1

                # strip() 後便於判斷空行與比對開頭關鍵字
                s = line.strip()

                # 不是空字串就算非空白行
                if s:
                    nonblank += 1

                # 函式定義通常以 def 開頭（此處是簡化統計，非語法解析）
                if s.startswith("def "):
                    defs += 1

    # 回傳三個統計值，供呼叫端顯示或後續處理
    return total, nonblank, defs

# 示範目標資料夾：從目前目錄往上兩層，再進入 week-04/in-class
target = Path("..") / ".." / "week-04" / "in-class"

# 先檢查目錄是否存在，避免直接掃描不存在路徑造成問題
if target.exists():
    total, nonblank, defs = count_py(target)
    print(f"{target}")
    print(f"  總行數       : {total}")
    print(f"  非空白行     : {nonblank}")
    print(f"  def 起頭行數 : {defs}")
else:
    print(f"示範目錄不存在：{target}")

# ── 課堂延伸挑戰（自行嘗試） ───────────────────────────
# 1) 把日記工具改成「附加」模式 'a'：同一天可多次追寫一行時間戳。
# 2) count_py 再多算一個「註解行（以 # 開頭）」的數字。
# 3) 把統計結果用 print(..., sep='\t', file=f) 寫到 stats.tsv。
