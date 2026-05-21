# R03. @property：屬性的守門員
#
# 核心想法：
# 有些資料不能隨便被改，例如成績不能是負數、半徑不能亂設成無效值。
# 這時就可以用 @property 把「像屬性一樣的操作」包進方法裡，
# 在不改使用方式的前提下，加入檢查、計算或保護機制。
#
# 對應 Bloom's Taxonomy：記憶（Remember）
# 先把語法、角色與適用時機記清楚，之後才能正確運用。

# ── 沒有保護的屬性會怎樣？ ───────────────────────────────
# 如果直接把資料公開暴露，外部程式碼就能任意塞入不合理的值。

class BadStudent:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade   # 沒有檢查機制，任何值都能塞進去

s = BadStudent("王小明", 85)
s.grade = -100   # 竟然可以！成績不能是負數
print(f"糟糕：{s.name} 的成績是 {s.grade}")  # -100

# ── @property：在存取屬性時加上檢查 ─────────────────────
# @property 讓「方法」看起來像「屬性」：
# - 讀取 s.grade 時，實際上會呼叫 getter
# - 設定 s.grade = 90 時，實際上會呼叫 setter
#
# 這樣的好處是：
# - 外部用法維持簡潔
# - 內部可以集中處理驗證邏輯

class Student:
    def __init__(self, name, grade):
        self.name = name
        # 注意：這裡看似普通指定，實際上會觸發下面的 setter
        # 因此建立物件時就能先做合法性檢查
        self.grade = grade

    @property
    def grade(self):
        """getter：讀取成績時呼叫。

        對外暴露的名字是 grade，
        但實際資料存在 _grade，避免 getter 自己呼叫自己造成無限遞迴。
        """
        return self._grade   # 底線開頭通常表示內部實作細節

    @grade.setter
    def grade(self, value):
        """setter：設定成績時呼叫，負責驗證輸入值。"""
        if not (0 <= value <= 100):
            raise ValueError(f"成績必須在 0～100，你給了 {value}")
        self._grade = value

print("\n=== @property 守門員 ===")
s = Student("李大華", 90)
print(s.grade)    # 90

s.grade = 75      # 合法，通過檢查
print(s.grade)    # 75

try:
    s.grade = -10  # 觸發 ValueError
except ValueError as e:
    print(f"錯誤：{e}")

# ── 唯讀屬性：計算出來的值不需要存 ──────────────────────
# 有些資料不需要真的存進物件，而是每次根據其他欄位動態計算。
# 像圓面積就是由半徑推導出來的，不應讓外部直接指定 area。

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        """唯讀屬性：依 radius 即時計算面積。"""
        import math
        return math.pi * self.radius ** 2

    @property
    def diameter(self):
        # 直徑也是由半徑推導而來，因此也適合做成唯讀屬性
        return self.radius * 2

print("\n=== 唯讀屬性（計算值）===")
c = Circle(5)
print(f"半徑 {c.radius}，直徑 {c.diameter:.1f}，面積 {c.area:.2f}")

c.radius = 10
print(f"半徑 {c.radius}，直徑 {c.diameter:.1f}，面積 {c.area:.2f}")

# try:
#     c.area = 100   # AttributeError：唯讀屬性不能設定

# ── 子類覆寫 setter ───────────────────────────────────────
# 研究生有加分機制，成績可以超過 100
# 子類別可以沿用父類別的 getter，
# 只針對 setter 改寫驗證規則，這就是多型的一種實際應用。

class GradStudent(Student):

    @Student.grade.setter
    def grade(self, value):
        # 研究生成績允許到 150，因此規則與一般學生不同
        if not (0 <= value <= 150):
            raise ValueError(f"研究生成績必須在 0～150，你給了 {value}")
        self._grade = value

print("\n=== 子類覆寫 setter ===")
g = GradStudent("張教授", 120)
print(g.grade)   # 120（研究生可以超過 100）

# 記憶重點 ──────────────────────────────────────────────────
# @property           → getter，讀取時觸發
# @屬性名.setter      → setter，設定時觸發（可加驗證）
# 沒有 setter 的就是「唯讀屬性」
# 實際資料習慣存在 _屬性名（底線開頭）
# 用 property 的目的不是把程式寫複雜，而是讓資料存取更安全、語意更清楚
