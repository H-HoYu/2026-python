# R02. 物件特殊方法
#
# 所謂「特殊方法」就是名稱前後有雙底線的方法，
# 例如 __str__、__eq__、__lt__。
#
# 這些方法通常不是你手動直接呼叫，
# 而是當 Python 遇到特定語法或內建函式時，自動幫你觸發。
# 例如：
# - print(obj) 會找 __str__
# - obj1 == obj2 會找 __eq__
# - sorted(list_of_obj) 可能會找 __lt__
#
# 對應 Bloom's Taxonomy：記憶（Remember）
# 這一份重點是先建立「哪個情境會呼叫哪個特殊方法」的基礎印象。

# ── __repr__ 和 __str__：物件的自我介紹 ──────────────────
# __repr__：給「開發者」看的（在 REPL、debug 時出現）
# __str__ ：給「使用者」看的（print() 優先用這個）
#
# 一般建議：
# - __repr__ 要偏精確，最好能清楚看出物件內容
# - __str__ 要偏友善，適合直接展示給人看

class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __repr__(self):
        # !r 代表用 repr() 格式化，字串會帶引號，更適合除錯
        return f"Student(name={self.name!r}, grade={self.grade})"

    def __str__(self):
        # 給一般輸出用，格式可讀即可
        return f"{self.name}：{self.grade} 分"

print("=== __repr__ vs __str__ ===")
s = Student("王小明", 85)
print(repr(s))   # Student(name='王小明', grade=85)
print(str(s))    # 王小明：85 分
print(s)         # 王小明：85 分（print 優先用 __str__）

# ── __eq__：自訂「相等」的意義 ────────────────────────────
# 沒有 __eq__ 的話，兩個物件只有「同一個記憶體位置」才算相等
# 也就是說，就算兩個物件內容完全相同，預設也未必會被視為相等。

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        # 先確認比較對象是不是同類型
        # 若不是，回傳 NotImplemented，讓 Python 決定下一步如何處理
        if not isinstance(other, Point):
            return NotImplemented
        # 這裡定義「相等」的標準：x 和 y 都相同
        return self.x == other.x and self.y == other.y

print("\n=== __eq__：自訂相等條件 ===")
p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)
print(p1 == p2)  # True（座標相同）
print(p1 == p3)  # False
print(p1 is p2)  # False（是不同的物件，記憶體位置不同）

# ── @total_ordering：自動補齊所有比較運算子 ─────────────
# 只要定義 __eq__ 和一個比較（__lt__），
# @total_ordering 會自動補出 <=, >, >= 四個
#
# 這能減少重複程式碼，但前提是你定義的核心比較邏輯要一致。

from functools import total_ordering

@total_ordering
class Score:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Score({self.value})"

    def __eq__(self, other):
        # 在教學範例中直接比較 value
        # 實務上若型別更複雜，通常也會先做 isinstance 檢查
        return self.value == other.value

    def __lt__(self, other):
        # __lt__ 代表 less than，也就是 <
        return self.value < other.value

print("\n=== @total_ordering：只寫兩個，自動補齊全部 ===")
a = Score(80)
b = Score(90)
print(a < b)   # True
print(a > b)   # False（自動生成）
print(a <= b)  # True（自動生成）

scores = [Score(70), Score(95), Score(60)]
print(sorted(scores))  # [Score(60), Score(70), Score(95)]

# ── __slots__：大量物件時節省記憶體 ──────────────────────
# 一般 class 每個物件都有一個 __dict__，很耗記憶體
# CPE 題目有時會建立幾十萬個小物件，__slots__ 可以大幅節省
#
# __slots__ 的效果是：
# - 限定物件可擁有的屬性名稱
# - 避免每個實例都建立 __dict__
# - 在大量小物件情境中常有幫助
#
# 代價是彈性下降，不能隨意加新屬性。

class PointLite:
    __slots__ = ('x', 'y')   # 固定只有這兩個屬性

    def __init__(self, x, y):
        self.x = x
        self.y = y

print("\n=== __slots__：固定屬性，節省記憶體 ===")
p = PointLite(3, 4)
print(p.x, p.y)   # 3 4
# p.z = 5  # 這行會 AttributeError，因為 z 不在 __slots__ 裡

# 記憶重點 ──────────────────────────────────────────────────
# __repr__  → 開發者用，要能「重現」物件
# __str__   → 使用者用，print() 呼叫
# __eq__    → 自訂 == 的意義
# @total_ordering + __lt__ → 自動補齊 <, <=, >, >=
# __slots__ → 固定屬性，大量物件時省記憶體
# 特殊方法的價值，在於讓你的物件更自然地融入 Python 語法與內建工具
