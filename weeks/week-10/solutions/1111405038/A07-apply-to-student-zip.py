# A07. 綜合應用：把 I/O 技巧套到真實學生資料
# Bloom: Apply — 複習並組合 R01~A06 的 API
#
# 資料來源：assets/npu-stu-109-114-anon.zip（6 屆新生資料庫，學號已匿名）
# 用到的小節對照：
#   5.11 pathlib 組路徑
#   5.12 exists 檢查
#   5.7  zipfile 讀壓縮檔（不解壓）
#   5.1  encoding='utf-8-sig' 處理 Excel 存的 BOM
#   5.6  io.StringIO 把 bytes 轉成 csv 可讀的 file-like
#   5.19 TemporaryDirectory 沙箱輸出
#   5.5  open(..., 'x') 只寫一次的報告檔
#   5.21 pickle 保存跨屆統計快照
#   5.2  print(file=) 寫 Markdown 週報

# ── 標準函式庫匯入 ─────────────────────────────────────
import csv          # 讀寫 CSV 格式檔案
import io           # 提供 StringIO，用於將字串當作檔案物件操作
import pickle       # 將 Python 物件序列化（二進位存檔）與反序列化（讀回）
import tempfile     # 建立系統暫存目錄，程式結束後自動清除
import zipfile      # 讀寫 .zip 壓縮檔，支援不解壓直接讀取內容
from collections import Counter  # 計數器，自動統計各元素出現次數
from pathlib import Path          # 跨平台路徑物件，比字串更安全方便

# ── 5.11 / 5.12 找到資料檔 ─────────────────────────────
# __file__ 是本程式檔的路徑，resolve() 轉為絕對路徑，parent 取上一層目錄
HERE = Path(__file__).resolve().parent

# 從本檔位置往上三層（solutions → week-10 → weeks → 專案根），再進 assets/
ZIP_PATH = HERE.parent.parent.parent / "assets" / "npu-stu-109-114-anon.zip"

# 5.12 確認壓縮檔存在，若不存在立即中止並印出完整路徑供除錯
assert ZIP_PATH.exists(), f"找不到資料：{ZIP_PATH}"
print("資料來源:", ZIP_PATH.name)


# ── 5.7 + 5.6 + 5.1 不解壓讀 zip 裡的 CSV ──────────────
def iter_year_csv(zip_path: Path):
    """
    逐年讀取壓縮檔內的 CSV，以生成器（generator）方式 yield 每一屆資料。

    參數：
        zip_path: zip 壓縮檔的 Path 物件

    每次 yield 回傳三個值：
        year  (str)       -- 學年度字串，例如 '109'、'114'
        header (list)     -- CSV 第一列的欄位名稱清單
        rows  (list[list])-- 扣掉表頭後的資料列，每列為字串清單
    """
    # 5.7 以唯讀方式開啟 zip，with 結束後自動關閉，不留開啟的控制代碼
    with zipfile.ZipFile(zip_path) as z:
        # infolist() 取得壓縮檔內所有條目（ZipInfo 物件）的清單
        for info in z.infolist():
            # 舊 zip 的中文檔名常見 cp437 錯碼；此資料集已是乾淨 utf-8，可直接使用
            name = info.filename

            # 只處理副檔名為 .csv 的檔案，略過目錄或其他格式
            if not name.endswith(".csv"):
                continue

            # 取檔名前三字元作為學年度（例如 '109新生.csv' → '109'）
            year = name[:3]  # '109'~'114'

            # 5.7 z.read() 以 bytes 讀取 zip 內檔案內容（完全在記憶體中，不寫磁碟）
            raw = z.read(info)

            # 5.1 decode('utf-8-sig')：utf-8-sig 會自動去除 UTF-8 BOM（\xef\xbb\xbf）
            #     Excel 另存 CSV 時常加上 BOM，若不處理會導致第一欄欄名前出現奇特字元
            text = raw.decode("utf-8-sig")

            # 5.6 io.StringIO 將字串包裝成「類檔案物件」（file-like object）
            #     讓 csv.reader 以為在讀一個真實開啟的文字檔，完全不需要暫存到磁碟
            reader = csv.reader(io.StringIO(text))

            # 一次讀完所有列，rows[0] 是表頭，rows[1:] 是資料列
            rows = list(reader)
            yield year, rows[0], rows[1:]


# ── 跨屆統計 ───────────────────────────────────────────
# summary 以學年度為鍵，存放每屆的彙總資訊：
#   'total'    (int)     -- 該屆新生總人數
#   'by_dept'  (Counter) -- 各系所人數計數
#   'by_entry' (Counter) -- 各入學方式人數計數
summary = {}

# all_depts 累計六屆所有系所的總人數，用於找出最熱門科系
all_depts = Counter()

for year, header, rows in iter_year_csv(ZIP_PATH):
    # header.index() 依欄位名稱找出對應的欄位索引，避免硬編碼欄號
    dept_idx  = header.index("系所名稱")   # 「系所名稱」欄的位置
    entry_idx = header.index("入學方式")   # 「入學方式」欄的位置

    # Counter 生成式：遍歷每一列，取出系所欄值並計數
    # 加上 len(r) > dept_idx 防止資料列欄數不足時發生 IndexError
    by_dept  = Counter(r[dept_idx]  for r in rows if len(r) > dept_idx)
    by_entry = Counter(r[entry_idx] for r in rows if len(r) > entry_idx)

    # 將本屆彙總結果存入 summary 字典
    summary[year] = {
        "total":    len(rows),    # 資料列數即為新生人數（已扣除表頭）
        "by_dept":  by_dept,
        "by_entry": by_entry,
    }

    # 將本屆各系所人數累加到全體統計中（Counter 支援 update 合併）
    all_depts.update(by_dept)

# ── 終端輸出：總覽 ─────────────────────────────────────
print("\n=== 6 屆新生人數 ===")
for year in sorted(summary):   # sorted() 確保按學年度由小到大排列
    # :>4 右對齊、寬度 4，讓人數欄位整齊對齊
    print(f"  {year} 學年：{summary[year]['total']:>4} 人")

print("\n=== 全體最熱門 5 個系所（累計 6 屆） ===")
# most_common(5) 回傳計數最高的前 5 個 (元素, 次數) 元組
for dept, n in all_depts.most_common(5):
    print(f"  {n:>4} 人  {dept}")

print("\n=== 114 學年入學方式分布 ===")
# most_common() 不傳參數則依計數由高到低全部列出
for kind, n in summary["114"]["by_entry"].most_common():
    print(f"  {n:>4} 人  {kind}")


# ── 5.19 + 5.5 + 5.2 沙箱產生報告、5.21 存快照 ─────────
# 5.19 TemporaryDirectory：建立系統暫存目錄作為「沙箱」
#      with 區塊結束（正常或例外）後，目錄及其所有內容會自動刪除
#      優點：不污染專案目錄，安全測試檔案 I/O
with tempfile.TemporaryDirectory() as tmp:
    # 將字串路徑轉為 Path 物件，以便使用 / 運算子組合子路徑
    tmp = Path(tmp)

    # 5.21 pickle 序列化：將整個 summary 字典以二進位格式存檔
    #      'wb' = write binary（必須用二進位模式）
    #      日後只需 pickle.load() 即可還原完整的 Python 字典，不必重新計算
    snap = tmp / "summary.pkl"
    with open(snap, "wb") as f:
        pickle.dump(summary, f)   # dump：物件 → 檔案
    # stat().st_size 取得檔案大小（bytes），確認序列化成功
    print(f"\n快照寫入 {snap.name}：{snap.stat().st_size} bytes")

    # 5.5 open(..., 'x') 以「獨佔建立」模式開啟檔案：
    #     若檔案已存在則拋出 FileExistsError，確保不會意外覆蓋舊報告
    #     適合「只應產生一次」的正式輸出檔（例如最終報告）
    report = tmp / "report.md"
    with open(report, "x", encoding="utf-8") as f:      # 5.5
        # 5.2 print(file=f)：將輸出重導向到檔案，而非標準輸出（螢幕）
        print("# 6 屆新生概況報告\n", file=f)           # 5.2 寫 Markdown 標題
        print("| 學年 | 人數 | 第一大系所 |", file=f)   # Markdown 表格標頭
        print("|------|------|------------|", file=f)   # Markdown 表格分隔線
        for year in sorted(summary):
            # most_common(1) 取計數最高的 1 個，回傳長度為 1 的清單，[0] 取第一個元組
            top_dept, top_n = summary[year]["by_dept"].most_common(1)[0]
            # 將每屆資料格式化為 Markdown 表格的一列
            print(f"| {year} | {summary[year]['total']} | "
                  f"{top_dept} ({top_n}) |", file=f)

    # 將剛寫好的 Markdown 報告讀回並印至終端，驗證寫入內容正確
    # read_text() 等同於 open().read()，但更簡潔
    print("\n=== Markdown 報告預覽 ===")
    print(report.read_text(encoding="utf-8"))

    # 驗證 pickle 能正確讀回：反序列化後型別與內容應與原 summary 一致
    # 'rb' = read binary（pickle 必須用二進位模式讀取）
    with open(snap, "rb") as f:
        loaded = pickle.load(f)   # load：檔案 → 物件
    print("pickle 讀回 key:", sorted(loaded.keys()))

# 離開 with 區塊 → TemporaryDirectory 的 __exit__ 觸發，tmp 目錄連同內容全部清除
# 專案目錄保持乾淨，不殘留任何暫存檔
print("\n(沙箱已自動清理)")


# ── 課堂延伸挑戰 ───────────────────────────────────────
# 1) 把報告改寫到 HERE / 'report.md'（改用 'w' 模式會覆蓋，'x' 會在檔案已存在時報錯）。
# 2) 加一欄「女性比例」：找出性別欄位後用 Counter 統計，計算女性人數／總人數。
# 3) 把 summary 壓縮存成 summary.pkl.gz（gzip.open('wb') + pickle.dump，節省磁碟空間）。
# 4) 跨屆找出「人數逐年下降最明顯」的系所（需要把 by_dept 按年排成折線，計算斜率）。
