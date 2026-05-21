# A02. with 語句與 Context Manager
#
# 核心觀念：
# 「借東西要還」：凡是需要手動釋放的資源（檔案、網路連線、鎖、暫存設定）
# 都應該包進 with，讓 Python 幫你保證收尾。
#
# 對應 Bloom's Taxonomy：應用（Apply）
# 你不只知道 with 能開檔，而是能自行設計與封裝 context manager。

# ── 為什麼需要 with？ ─────────────────────────────────────
# 沒有 with 的開檔方式：如果中途發生例外，close() 可能永遠不會被呼叫

# 不好的寫法
# f = open("demo.txt", "w")
# f.write("hello")
# f.close()   # 如果 write 出錯，這行就不會執行了

# 正確的寫法：with 會自動呼叫 close()，即使出錯也一樣
# 語法重點：
# with 資源建立式 as 變數:
#     使用資源
#
# 離開區塊時會自動做清理，開發者不必手動呼叫 close()
print("=== with 開檔：自動關閉 ===")
with open("/tmp/week13_demo.txt", "w") as f:
    f.write("Hello from Week 13\n")

with open("/tmp/week13_demo.txt", "r") as f:
    print(f.read().strip())

# ── 自己寫 Context Manager（用 class）────────────────────
# 需要實作兩個方法：
#   __enter__：進入 with 區塊時執行，回傳值會被 as 接收
#   __exit__ ：離開 with 區塊時執行（不管有沒有出錯）
#
# __exit__(exc_type, exc_val, exc_tb) 參數說明：
# - exc_type: 例外類型，例如 ValueError
# - exc_val : 例外物件本身
# - exc_tb  : traceback 物件
# 若 with 區塊沒有錯誤，三者都會是 None

import time

class Timer:
    """計時器範例：示範 class 版 context manager。

    用法：
    with Timer() as t:
        ... 需要計時的程式 ...
    """

    def __enter__(self):
        # 記錄進入區塊的時間戳
        self.start = time.time()
        print("⏱  開始計時")
        return self   # 這個值會被 as 接收，例如 as t

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 不論正常離開或拋出例外，都會執行到這裡
        elapsed = time.time() - self.start
        print(f"⏱  結束：{elapsed:.4f} 秒")
        return False  # False = 不吃掉例外（讓錯誤繼續往外傳）

print("\n=== 自訂計時器 ===")
with Timer() as t:
    total = sum(range(1_000_000))
print(f"計算結果：{total}")

# ── 更簡單的寫法：@contextmanager ─────────────────────────
# 不用寫 class，用 yield 分隔「進入前」和「離開後」
#
# 結構可記成：
# @contextmanager
# def cm():
#     # 進入 with 前
#     yield 可給 as 的值
#     # 離開 with 後

from contextlib import contextmanager

@contextmanager
def section(title):
    """建立有框線的輸出區段。

    這類小型 context manager 很適合整理 CLI 輸出，
    讓測試紀錄或示範畫面更有結構。
    """
    print(f"\n{'='*40}")
    print(f"  {title}")
    print(f"{'='*40}")
    yield           # with 區塊的主體會在此執行
    print(f"{'─'*40}")

print()
with section("Week 13 CPE 模擬考"):
    print("  題目：UVA 11005 Cheapest Base")
    print("  時間限制：20 分鐘")

# ── CPE 應用：截取 stdout，方便測試輸出 ─────────────────
# 有些 CPE 題目會直接 print 答案
# 測試時可以截取 print 的輸出來比對
#
# 這個技巧常用在：
# 1) 你的解法只會 print，沒有 return
# 2) 需要比對完整輸出格式（空白、換行、字串）

import io, sys

@contextmanager
def capture_output():
    """暫時攔截標準輸出（stdout），將 print 內容寫入記憶體。

    回傳 StringIO 緩衝區，可在 with 區塊外用 getvalue() 取得輸出字串。
    """
    # 保存原本 stdout，避免影響程式其他部分
    old_stdout = sys.stdout
    # 讓後續 print 先寫到字串緩衝區
    sys.stdout = buffer = io.StringIO()
    try:
        yield buffer     # with ... as out 的 out 就是這個 buffer
    finally:
        # 不論中間是否例外，都必須還原 stdout
        # finally 會保證執行，這是資源管理的關鍵
        sys.stdout = old_stdout

def solve_parity(n):
    """UVA 10931 Parity：計算 n 的二進位中 1 的個數。"""
    bits = bin(n)[2:]
    ones = bits.count('1')
    print(f"The parity of {bits} is {ones} (mod 2 is {ones % 2}).")

print("\n=== 截取輸出（測試用）===")
with capture_output() as out:
    solve_parity(10)
    solve_parity(7)

captured = out.getvalue()
print("截取到的輸出：")
print(captured)

# 可以直接拿來做 assertEqual / 字串比對
# 例如在單元測試中：assert expected in captured
lines = captured.strip().split('\n')
print(f"共 {len(lines)} 行輸出")

# 記憶重點 ──────────────────────────────────────────────────
# __enter__ → 進入 with 時執行，回傳值被 as 接收
# __exit__  → 離開 with 時執行（出錯也會執行）
# @contextmanager + yield → 更簡單的寫法，yield 前是 enter，yield 後是 exit
# 常用場景：開檔、計時、測試輸出截取、任何「借了要還」的資源
# __exit__ 回傳 True 表示「吞掉例外」；回傳 False 表示讓例外繼續拋出
