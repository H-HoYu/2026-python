# A08. 用 seaborn 畫 109~114 學年各學院生源分析圖
# Bloom: Apply — 把 A07 的統計成果交給視覺化套件
#
# 需要：pip install seaborn matplotlib pandas
#
# 用到的 I/O 技巧延續 A07：
#   5.7  zipfile 不解壓讀 CSV
#   5.1  utf-8-sig 去 BOM
#   5.6  io.StringIO → csv
#   5.11 pathlib
#   5.5  open('x') 不覆蓋輸出檔

# ── 標準函式庫匯入 ─────────────────────────────────────
import csv          # 讀取 CSV 格式；搭配 DictReader 可以用欄位名稱取值
import io           # StringIO：把字串包裝成 file-like，讓 csv 以為在讀檔
import platform     # 偵測作業系統（Darwin / Windows / Linux），用來選擇中文字型
import zipfile      # 讀 .zip 壓縮檔，不需先解壓到磁碟
from pathlib import Path  # 跨平台路徑物件

# ── 第三方套件匯入 ─────────────────────────────────────
import matplotlib.pyplot as plt  # 底層繪圖引擎；seaborn 建立在它之上
import pandas as pd              # 提供 DataFrame，做資料整理與樞紐分析
import seaborn as sns            # 高階統計視覺化；自動產生美觀的配色與版面

# ── 中文字型：依平台挑一個有的 ─────────────────────────
# 問題背景：matplotlib 預設字型不含中文字元，畫出來會變成方框（豆腐）。
# 解法：依作業系統提供「內建有 CJK 字符的字型」清單，往前插入 rcParams。
# 字典的 key 對應 platform.system() 回傳值；get() 的預設值處理不認識的平台。
_CJK_FONTS = {
    "Darwin":  ["Heiti TC", "Arial Unicode MS", "PingFang TC"],   # macOS
    "Windows": ["Microsoft JhengHei", "Microsoft YaHei"],          # Windows 繁/簡
    "Linux":   ["Noto Sans CJK TC", "WenQuanYi Zen Hei"],          # Linux 常見
}.get(platform.system(), ["sans-serif"])  # 未知平台退回通用 sans-serif


def _apply_cjk_font():
    """
    將 CJK 字型插入 matplotlib 全域設定。

    為何需要獨立成函式而非只設定一次？
    因為 sns.set_theme() 會完整重設 rcParams（含字型），
    所以必須在每次呼叫 sns.set_theme() **之後**再重新套用。
    """
    # 將 CJK 清單插到現有字型串列的最前面，確保優先被選用
    plt.rcParams["font.sans-serif"] = _CJK_FONTS + plt.rcParams["font.sans-serif"]
    plt.rcParams["font.family"] = "sans-serif"
    # axes.unicode_minus=False：讓負號顯示為 ASCII '-'，而非 Unicode 全形減號
    # 若為 True，負號也會因字型問題變成方框
    plt.rcParams["axes.unicode_minus"] = False


# 程式啟動時先套一次（sns.set_theme 呼叫前）
_apply_cjk_font()

# ── 系所 → 學院 對照表（NPU 三大學院） ─────────────────
# 原始資料只有「系所名稱」欄，沒有「學院」欄。
# 透過此字典做映射，讓我們能在 DataFrame 中新增「學院」欄位進行分組。
# 找不到對應的系所（例如通識、進修部）一律歸入「其他」。
DEPT_TO_COLLEGE = {
    # 人文暨管理學院
    "應用外語系":       "人文暨管理學院",
    "航運管理系":       "人文暨管理學院",
    "行銷與物流管理系": "人文暨管理學院",
    "觀光休閒系":       "人文暨管理學院",
    "資訊管理系":       "人文暨管理學院",
    "餐旅管理系":       "人文暨管理學院",
    # 海洋資源暨工程學院
    "水產養殖系":       "海洋資源暨工程學院",
    "海洋遊憩系":       "海洋資源暨工程學院",
    "食品科學系":       "海洋資源暨工程學院",
    # 電資工程學院
    "資訊工程系":       "電資工程學院",
    "電信工程系":       "電資工程學院",
    "電機工程系":       "電資工程學院",
}

# ── 5.11 定位資料 ─────────────────────────────────────
# __file__ 是本程式的路徑，resolve() 轉絕對路徑，parent 取所在目錄
HERE = Path(__file__).resolve().parent
# 從本檔往上四層（1111405038 → solutions → week-10 → weeks → 專案根），再進 assets/
ZIP_PATH = HERE.parent.parent.parent.parent / "assets" / "npu-stu-109-114-anon.zip"
# 若檔案不存在立即終止，顯示完整路徑協助除錯
assert ZIP_PATH.exists(), f"找不到：{ZIP_PATH}"


# ── 5.7 + 5.6 + 5.1 讀 zip 內所有 CSV 成一張 long-form 表 ─
def load_long_frame(zip_path: Path) -> pd.DataFrame:
    """
    讀取壓縮檔內所有學年的 CSV，整合成 pandas long-form（長格式）DataFrame。

    long-form 是 seaborn 最愛的資料格式：
    每一列代表一個觀測值，欄位為維度（學年、學院、系所），
    而非每個學院獨佔一欄的 wide-form（寬格式）。

    回傳欄位：
        學年 (int)   -- 例如 109, 110 … 114
        學院 (str)   -- 依 DEPT_TO_COLLEGE 對照，對應不到的為「其他」
        系所 (str)   -- 原始系所名稱
    """
    records = []  # 先收集 dict，最後一次轉 DataFrame（比逐列 append 快）

    # 5.7 開啟 zip，with 結束後自動關閉，不需手動 close()
    with zipfile.ZipFile(zip_path) as z:
        for info in z.infolist():
            # 僅處理 .csv 檔，略過 zip 內可能存在的目錄條目或其他格式
            if not info.filename.endswith(".csv"):
                continue

            # 學年度：取檔名前三字元（例如 '109新生.csv' → '109'）
            year = info.filename[:3]  # '109'..'114'

            # 5.7 + 5.1 以 bytes 讀取，再用 utf-8-sig 解碼自動去除 Excel BOM
            text = z.read(info).decode("utf-8-sig")

            # 5.6 io.StringIO 把字串變成 file-like，讓 csv.DictReader 當檔案讀
            # DictReader 與 reader 的差別：DictReader 以第一列為欄位名稱，
            # 每列回傳 dict（{'系所名稱': '資訊工程系', ...}），比位置索引更易讀
            reader = csv.DictReader(io.StringIO(text))

            for row in reader:
                # strip() 去除系所名稱前後空白，避免「 資訊工程系」≠「資訊工程系」
                dept = row.get("系所名稱", "").strip()
                # 略過系所欄為空的列（可能是資料底部的空白行）
                if not dept:
                    continue
                records.append({
                    "學年": int(year),                              # 字串轉整數，利於排序與繪圖
                    "學院": DEPT_TO_COLLEGE.get(dept, "其他"),     # 查表；查不到給「其他」
                    "系所": dept,                                   # 保留原始系所名稱供擴充使用
                })

    # from_records 接受 list[dict]，比逐列 append 的 DataFrame 效能高很多
    return pd.DataFrame.from_records(records)


# 讀入所有資料並印出基本資訊供確認
df = load_long_frame(ZIP_PATH)
print("總筆數:", len(df))   # 預期約數千筆（6 屆 × 每屆數百人）
print(df.head())            # 印出前 5 列，快速確認欄位與內容正確

# ── 樞紐：各學年 × 各學院 的人數 ──────────────────────
# groupby + size()：依（學年、學院）分組後計算每組的列數（即人數）
# reset_index(name='人數')：把分組索引還原為欄位，並把計數欄命名為「人數」
# 結果為 long-form：每列是「某學年某學院有 n 人」
pivot = (df.groupby(["學年", "學院"])
           .size()
           .reset_index(name="人數"))
print("\n各學年各學院:")
# pivot() 轉為 wide-form 方便人眼閱讀：行＝學年，列＝學院，值＝人數
print(pivot.pivot(index="學年", columns="學院", values="人數"))


# ── seaborn 繪圖 ──────────────────────────────────────
# set_theme() 設定全域主題：
#   style="whitegrid" — 白底加淺灰格線，數值容易對齊閱讀
#   context="talk"    — 字體比預設大，適合簡報或課堂展示
#   palette="Set2"    — 柔和的 8 色定性色盤，各學院顏色有足夠區別
sns.set_theme(style="whitegrid", context="talk", palette="Set2")
_apply_cjk_font()  # set_theme 重設了 rcParams，需再套一次中文字型

# 建立 1 行 2 列的子圖版面
# figsize=(15, 6)：寬 15 吋、高 6 吋，giving 足夠空間放兩張圖
# width_ratios=[1.3, 1]：左圖比右圖稍寬（折線圖需要更多橫向空間）
fig, axes = plt.subplots(1, 2, figsize=(15, 6),
                         gridspec_kw={"width_ratios": [1.3, 1]})

# ── 圖 A：折線＋散點 —— 各學院逐年趨勢 ─────────────────
# sns.lineplot：
#   hue="學院"   — 依學院分色，自動產生圖例
#   marker="o"   — 每個資料點畫圓形標記，方便看各年確切位置
#   markersize   — 標記直徑（點）
#   linewidth    — 折線粗細
#   ax=axes[0]   — 指定繪製到左側子圖
sns.lineplot(data=pivot, x="學年", y="人數", hue="學院",
             marker="o", markersize=10, linewidth=2.5, ax=axes[0])
axes[0].set_title("109–114 各學院新生人數趨勢", fontsize=16, pad=12)
# set_xticks 確保 x 軸只顯示實際存在的學年，不自動插入不存在的刻度
axes[0].set_xticks(sorted(pivot["學年"].unique()))
# 縮小圖例文字大小，避免壓到圖形
axes[0].legend(title="學院", loc="upper right", frameon=True, fontsize=8)

# 在折線每個資料點上方標註實際人數，方便讀者不需看 y 軸即可得知確切數值
for _, r in pivot.iterrows():
    axes[0].annotate(
        int(r["人數"]),                  # 標注文字：人數（轉整數去掉小數點）
        (r["學年"], r["人數"]),           # 錨點：該資料點的座標（x, y）
        textcoords="offset points",      # xytext 以「點」為單位的偏移量
        xytext=(0, 8),                   # 往上偏移 8 點，避免文字壓到標記
        ha="center",                     # 水平置中對齊錨點
        fontsize=9,
        alpha=0.8,                       # 略透明，避免文字太搶眼
    )

# ── 圖 B：堆疊長條 —— 每年學院占比 ──────────────────────
# 先把 long-form 的 pivot 轉回 wide-form：行＝學年，欄＝各學院的人數
# fillna(0)：有些學年可能某學院人數為 0，填 0 以免繪圖時出現 NaN
pivot_wide = pivot.pivot(index="學年", columns="學院", values="人數").fillna(0)

# DataFrame.plot()：pandas 內建的 matplotlib 封裝，可直接對 DataFrame 畫圖
#   kind="bar"      — 長條圖
#   stacked=True    — 堆疊模式，讓總高度代表該年度總人數，各色段代表各學院比例
#   colormap="Set2" — 與折線圖使用相同色盤，保持視覺一致性
#   width=0.75      — 長條寬度（0~1）
#   edgecolor       — 長條邊框顏色，白色可幫助視覺區隔各學院色段
pivot_wide.plot(kind="bar", stacked=True,
                ax=axes[1], colormap="Set2", width=0.75, edgecolor="white")
axes[1].set_title("各學年學院結構（堆疊）", fontsize=16, pad=12)
axes[1].set_ylabel("人數")
axes[1].tick_params(axis="x", rotation=0)   # x 軸刻度文字不旋轉，預設 90 度不易讀
axes[1].legend(title="學院", loc="upper right", fontsize=9)

# 全圖大標題（suptitle）：放在所有子圖上方
# y=1.02 讓標題稍微超出圖框，避免與子圖標題重疊
fig.suptitle("國立澎湖科技大學  109–114 學年新生生源分析",
             fontsize=18, fontweight="bold", y=1.02)

# tight_layout 自動調整子圖間距，防止標題、軸標籤互相遮蓋
fig.tight_layout()

# ── 5.5 'x' 模式輸出：檔已存在就保留舊的 ────────────────
# 'xb'：x = 獨佔建立（FileExistsError if exists），b = 二進位（圖片必須用 binary）
# 設計哲學：圖表視為「一次性產出」，不應靜默覆蓋。
#            需要重畫時，使用者必須刻意刪除舊檔，避免意外遺失手動調整的版本。
OUT = HERE / "A08-college-trend.png"
try:
    with open(OUT, "xb") as f:
        # bbox_inches="tight"：自動裁切邊框，確保 suptitle 不被切掉
        fig.savefig(f, dpi=150, bbox_inches="tight")
    print(f"\n圖檔已寫入：{OUT.name}")
except FileExistsError:
    # 檔案已存在：提示但不中止，讓 plt.show() 仍能顯示圖形
    print(f"\n{OUT.name} 已存在，保留舊檔（要重畫請先刪除）")

# 顯示互動視窗（在非互動環境（如 CI）可將此行移除）
plt.show()

# ── 延伸挑戰 ──────────────────────────────────────────
# 1) 改畫「各系所」熱力圖：sns.heatmap(pivot_by_dept, annot=True, fmt='d')
#    -- annot=True 在每格顯示數值；fmt='d' 格式化為整數
# 2) 加一張圓餅圖：114 學年學院占比
#    -- axes.pie(sizes, labels=labels, autopct='%1.1f%%')
# 3) 把年度 x 軸改成 '109學年'~'114學年' 字串
#    -- pivot_wide.index = [f"{y}學年" for y in pivot_wide.index]，再重畫
