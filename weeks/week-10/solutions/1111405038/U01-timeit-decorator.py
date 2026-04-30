# U01. 計時裝飾器實作與資料格式速度比較（6.1 / 6.2 / 6.3）
# 從「重複的計時程式碼」出發，引入裝飾器，再做格式實驗

# ── 標準函式庫匯入 ─────────────────────────────────────
import csv          # 讀取 CSV 格式資料
import json         # 讀取 JSON 格式資料
import time         # 提供 perf_counter() 進行高精度計時
import io           # StringIO：把字串包裝成 file-like 物件
import xml.etree.ElementTree as ET  # 解析 XML 格式資料
import functools    # 提供 wraps 裝飾器，保留被裝飾函式的 metadata

# ═══════════════════════════════════════════════════════════
# Part 1｜問題：每個函式都要手動計時 → 大量重複
# ═══════════════════════════════════════════════════════════
# 場景：需要計測不同資料格式（CSV、JSON、XML）的讀取速度。
# 若沒有裝飾器，每個函式前後都要複製貼上計時程式碼：
#   - 計時開始（start = time.perf_counter()）
#   - 執行函式
#   - 計時結束並印出耗時
# 問題：程式碼重複、容易出錯、不易維護。

# 各資料格式的讀取函式（內部邏輯不同，但外層計時邏輯完全相同）

def read_csv_raw(data: str) -> list:
    """讀 CSV 資料，回傳字典清單"""
    return list(csv.DictReader(io.StringIO(data)))

def read_json_raw(data: str) -> list:
    """解析 JSON 資料，回傳列表"""
    return json.loads(data)

def read_xml_raw(data: str) -> list:
    """解析 XML 資料，回傳屬性字典清單"""
    root = ET.fromstring(data)
    return [r.attrib for r in root.findall("row")]

# ── 傳統做法（無裝飾器） ────────────────────────────────────
# 每個函式都要用這三行計時程式碼包住：
# start = time.perf_counter()       # 開始計時
# result = read_csv_raw(data)       # 執行函式
# print(f"read_csv_raw 耗時 {time.perf_counter() - start:.6f}s")  # 顯示結果
#
# 問題：
#   1. 計時邏輯重複 N 次（每個函式一次）
#   2. 要改計時方式就要改 N 個地方
#   3. 忘記包裝會遺漏某些函式

# ═══════════════════════════════════════════════════════════
# Part 2｜解法：裝飾器把計時邏輯包起來，一次定義，到處復用
# ═══════════════════════════════════════════════════════════
# 裝飾器（decorator）是一個「函式工廠」：接收一個函式，回傳一個被包裝的新函式。
# 優點：
#   - 計時邏輯只寫一次，不同函式聲明 @timeit 即可復用
#   - 原函式保持簡潔，不被計時程式碼汙染
#   - 要停用計時只需移除 @timeit，無須修改函式本身

def timeit(func):
    """
    基礎版計時裝飾器：測量函式執行耗時。
    
    參數：
        func -- 要被裝飾（包裝）的函式物件
        
    回傳：
        wrapper -- 執行計時、然後呼叫原函式的新函式
        
    執行流程：
        1. 呼叫 @timeit 修飾的函式時，實際執行 wrapper
        2. wrapper 記錄開始時間
        3. wrapper 呼叫原函式 func()，得到結果
        4. wrapper 記錄結束時間，計算耗時
        5. wrapper 印出函式名稱與耗時
        6. wrapper 回傳原函式的結果（保持函式行為不變）
    """
    def wrapper(*args, **kwargs):
        # *args 捕捉所有位置參數，**kwargs 捕捉所有關鍵字參數
        # 這樣 wrapper 可以相容任何簽名的函式
        start = time.perf_counter()     # 開始計時（高精度，以浮點數秒為單位）
        result = func(*args, **kwargs)   # 呼叫原函式
        elapsed = time.perf_counter() - start  # 計算耗時
        print(f"  {func.__name__:<20s} {elapsed:.6f}s")  # 秒數精確到小數點後 6 位
        return result  # 回傳原函式的結果
    return wrapper


# ── 陷阱 1：wrapper 覆蓋原函式的 metadata ────────────────
def demo():
    """這是 demo 的說明文字"""
    pass

wrapped = timeit(demo)
print("未加 wraps 前：", wrapped.__name__)   # 打印 wrapper（錯誤！應為 demo）
# 問題：被裝飾後，函式名稱、docstring、module 等都被 wrapper 蓋掉，
# 導致 help() / debug / IDE 自動完成時看不到原函式資訊

# ── Part 3｜functools.wraps：保留原函式的 metadata ──────────
# 解法：在 wrapper 定義上加 @functools.wraps(func)
# 效果：自動複製原函式的 __name__、__doc__、__module__、__qualname__、__annotations__ 等

def timeit(func):
    """改良版：使用 functools.wraps 保留原函式的所有 metadata"""
    @functools.wraps(func)  # 關鍵一行！
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__:<20s} {elapsed:.6f}s")
        return result
    return wrapper

wrapped = timeit(demo)
print("加 wraps 後：  ", wrapped.__name__)   # 現在打印 demo（正確！）
# functools.wraps 背後的原理：
#   它呼叫 functools.update_wrapper()，將 func 的幾個特殊屬性複製到 wrapper：
#   - __name__：函式名稱
#   - __doc__：文檔字符串
#   - __module__：定義時所在的模組
#   - __qualname__：合格名稱（for nested functions）
#   - __annotations__：型別提示
#   - __dict__：自訂屬性
print()

# ═══════════════════════════════════════════════════════════
# Part 4｜實驗：相同資料，CSV vs JSON vs XML 速度比較
# ═══════════════════════════════════════════════════════════
# 目的：用同一組資料（1000 筆學生記錄），用三種不同格式儲存，
#      再用各自的解析器讀回，計測哪個格式讀取最快。
# 這能展示：
#   - 資料格式的設計對效能的重大影響
#   - 同一個裝飾器可應用於不同場景

# ── 產生測試資料（1000 筆學生記錄）────────────────────────
N = 1000  # 筆數

# ①★CSV 格式★：以逗號分隔的文字，第一列為表頭
# 格式範例：
#   id,name,score
#   0,Student0000,60
#   1,Student0001,61
#   ...
csv_buf = io.StringIO()  # 先用 StringIO 在記憶體「寫」CSV
writer = csv.DictWriter(csv_buf, fieldnames=["id", "name", "score"])
writer.writeheader()  # 寫表頭列
for i in range(N):
    writer.writerow({"id": i, "name": f"Student{i:04d}", "score": 60 + i % 40})
    # 注：score 利用模運算讓範圍固定在 60~99
CSV_DATA = csv_buf.getvalue()  # 把 StringIO 內容轉為字串

# ②★JSON 格式★：JavaScript 物件標記法，結構化且緊湊
# 格式範例：
#   [{"id": 0, "name": "Student0000", "score": 60}, ...}]
JSON_DATA = json.dumps([
    {"id": i, "name": f"Student{i:04d}", "score": 60 + i % 40}
    for i in range(N)
])  # json.dumps() 將 Python list 序列化為 JSON 字串

# ③★XML 格式★：標籤型格式，結構清晰但內容多
# 格式範例：
#   <data>
#     <row id="0" name="Student0000" score="60"/>
#     ...
#   </data>
xml_rows = "".join(
    f'<row id="{i}" name="Student{i:04d}" score="{60 + i % 40}"/>'
    for i in range(N)
)  # 逐列組合 XML 標籤
XML_DATA = f"<data>{xml_rows}</data>"  # 包在根標籤內

# ── 帶回傳耗時的計時包裝（第二種用法）────────────────────
# Part 2 的 timeit 直接印出耗時，但實驗時需要「收集耗時數據」再統計。
# 所以定義另一版本，回傳 (結果, 耗時) 元組

def timeit_silent(func):
    """
    計時裝飾器（無列印版本）：測量並回傳耗時，但不直接列印。
    
    回傳值變更：不再回傳原函式結果，而是回傳 (結果, 耗時) 元組。
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        # 注：不印出結果，而是連同結果一起回傳
        return result, time.perf_counter() - start
    return wrapper

# 套用裝飾器到三個讀取函式
_csv  = timeit_silent(read_csv_raw)   # 被裝飾後的 CSV 讀取函式
_json = timeit_silent(read_json_raw)  # 被裝飾後的 JSON 讀取函式
_xml  = timeit_silent(read_xml_raw)   # 被裝飾後的 XML 讀取函式

# ── 執行比較（重複多次取平均）─────────────────────────────
# 為何要重複？
#   - 電腦首次執行會有「冷啟動」延遲（記憶體、CPU 快取還沒熱身）
#   - 取多次平均能消除單次異常值
#   - RUNS 次重複後的平均更能代表「實際效能」

RUNS = 5  # 重複執行的次數
times = {"CSV": 0.0, "JSON": 0.0, "XML": 0.0}  # 累計耗時（秒）

for _ in range(RUNS):
    _, t = _csv(CSV_DATA);   times["CSV"]  += t    # 執行讀 CSV，累加耗時
    _, t = _json(JSON_DATA); times["JSON"] += t    # 執行讀 JSON，累加耗時
    _, t = _xml(XML_DATA);   times["XML"]  += t    # 執行讀 XML，累加耗時

# ── 結果統計與顯示 ────────────────────────────────────────
print(f"=== 讀取 {N} 筆資料，重複 {RUNS} 次平均 ===\n")
print(f"{'格式':<6} {'平均耗時':>12}  {'相對 JSON':>10}")
base = times["JSON"] / RUNS  # 以 JSON 耗時作為基準（1.0x）
for fmt, total in times.items():
    avg = total / RUNS  # 計算此格式的平均耗時
    print(f"  {fmt:<6} {avg:.6f}s   {avg/base:>8.2f}x")
    # 輸出格式範例：
    #   CSV     0.003456s       0.95x   （CSV 比 JSON 快 5%）
    #   JSON    0.003641s       1.00x   （JSON 作為基準 1.0x）
    #   XML     0.005123s       1.41x   （XML 比 JSON 慢 41%）

# ═══════════════════════════════════════════════════════════
# 結論與觀察重點
# ═══════════════════════════════════════════════════════════
# 
# 【典型的效能排序】
#   1️⃣ JSON  — 通常最快
#      原因：JSON 的解析器名採用原生 C 實作（在如 CPython 的直譯器中），
#           且 JSON 結構簡潔（無多餘標籤），解析開銷最小。
#
#   2️⃣ CSV   — 介於中間
#      原因：CSV 是簡單的文字格式，但每個欄位都是字串，
#           若需要型別轉換（int、float），要額外成本。
#           Python csv 模組是 C 實作，效率尚佳。
#
#   3️⃣ XML   — 通常最慢
#      原因：XML 標籤冗冗（<row>…</row> 對每筆記錄），
#           且每個屬性值都是字串需轉換，
#           ElementTree 要構造樹狀結構（佔記憶體）。
#           整體解析開銷最大。
#
# 隱含啟示：
#   - 若對效能敏感（大資料、實時應用），應優先考慮 JSON
#   - XML 適合「人類可讀」為主、效能其次的場景（如設定檔）
#   - CSV 是折衷方案（簡潔、相容性好）
#
# ═════════════════════════════════════════════════════════════
#
# 【裝飾器帶來的軟體工程好處】
#
#   ✓ 關注點分離（Separation of Concerns，SoC）：
#     計時邏輯與業務邏輯分開，讀取函式不被計時程式碼污染。
#
#   ✓ DRY 原則（Don't Repeat Yourself）：
#     計時邏輯只寫一次，不同函式都能複用 @timeit。
#
#   ✓ 易於擴展：
#     若要新增「記錄到 log 檔」功能，只需改一個地方（timeit 函式），
#     所有被 @timeit 修飾的函式自動獲得新功能。
#
#   ✓ 易於禁用：
#     移除 @timeit 裝飾器一行，就停用所有計時，
#     原函式本體完全不動。
#
#   ✓ functools.wraps 的重要性：
#     確保 IDE 自動完成、help()、debugger 都看到正確的函式名稱與說明文字，
#     提升開發體驗與程式碼可讀性。
