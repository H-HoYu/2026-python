# R01. 函數彈性簽章
#
# 本檔重點：理解 Python 函數參數的幾種彈性寫法，
# 讓你在設計 API 或工具函式時，可以更精準控制「怎麼傳參數」。
#
# 對應 Bloom's Taxonomy：記憶（Remember）
# 先把語法和規則記熟，之後才容易在實作時正確使用。

# ── *args：不定個數的位置參數 ─────────────────────────────
# 問題：想加總任意幾個數字，不知道會有幾個
#
# *args 的意思是：
# - 呼叫者可以傳 0 個、1 個、很多個「位置參數」
# - 進到函式後，這些值會被打包成 tuple
# - args 只是慣例名稱，你也可以寫成 *numbers、*items

def add_all(*args):
    """把任意個數的數字全部加總。

    參數：
    - *args: 任意多個位置參數，在函式內會是一個 tuple

    回傳：
    - 所有參數的總和
    """
    return sum(args)

print("=== *args：不定個數的位置參數 ===")
print(add_all(1, 2))            # 1 + 2 = 3
print(add_all(1, 2, 3, 4, 5))  # 可接受更多參數
print(add_all())                # 0（空的也沒問題）

# ── **kwargs：不定個數的關鍵字參數 ───────────────────────
# kwargs 在函數內是一個 dict
#
# **kwargs 的意思是：
# - 呼叫者可傳任意多個 名稱=值
# - 函式內會把它們收集成字典
# - 很適合資料欄位不固定、選項很多的情境

def make_student(**kwargs):
    """建立學生資料，欄位名稱與內容都可自由擴充。"""
    return kwargs

print("\n=== **kwargs：不定個數的關鍵字參數 ===")
s = make_student(name="王小明", grade=85, seat=12)
print(s)   # {'name': '王小明', 'grade': 85, 'seat': 12}

# ── keyword-only：強制用名稱呼叫 ─────────────────────────
# * 後面的參數「一定要具名」，避免填錯順序
#
# 這在參數意義很接近時特別有用，
# 例如 subject 與 score 若都用位置傳遞，容易看錯位置。

def send_score(student_id, *, subject, score):
    """示範 keyword-only 參數。

    student_id 可以用位置傳入；
    subject 與 score 則必須寫成名稱=值。
    """
    print(f"學號 {student_id}｜{subject}：{score} 分")

print("\n=== keyword-only：強制具名，避免填錯順序 ===")
send_score("411234001", subject="數學", score=90)   # 正確
# send_score("411234001", "數學", 90)  # ← 這樣會 TypeError！

# ── 三種參數混合使用 ──────────────────────────────────────
# 下面這個例子展示：
# - title：一般參數
# - *scores：任意多個成績
# - prefix：一般預設值參數
#
# 注意：prefix 放在 *scores 後面時，呼叫時通常會以具名方式傳入，
# 這樣可讀性會比較高。
def report(title, *scores, prefix="成績"):
    """輸出一份簡單成績報告。"""
    avg = sum(scores) / len(scores) if scores else 0
    print(f"{prefix}報告－{title}：平均 {avg:.1f}")

print("\n=== 混合：普通 + *args + 預設值 ===")
report("期中考", 80, 90, 70)
report("期末考", 95, 85, 75, 100, prefix="最終")

# ── 記憶重點 ──────────────────────────────────────────────
# *args   → tuple，接受任意個「值」
# **kwargs → dict，接受任意個「名稱=值」
# *（單獨）→ 後面的參數一定要具名
# 順序：普通參數 → *args → keyword-only → **kwargs
# 補充：閱讀函式簽章時，先看每個符號控制的是「數量」還是「呼叫方式」
# - *args 控制的是「可接受很多個位置值」
# - **kwargs 控制的是「可接受很多個具名值」
# - 單獨的 * 控制的是「後面必須具名」
