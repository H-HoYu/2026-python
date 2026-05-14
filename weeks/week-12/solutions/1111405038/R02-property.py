# R02. 屬性封裝（8.6）
# @property / getter / setter / 唯讀屬性

# ── 基本 @property ────────────────────────────────────────
class Circle:
    def __init__(self, radius):
        self._radius = radius   # _radius：慣例上表示「受保護」，不直接存取

    @property
    def radius(self):
        # getter：外部讀取 c.radius 時會呼叫這裡
        return self._radius

    @radius.setter
    def radius(self, value):
        # setter：集中放入檢查邏輯，避免不合法資料
        if value < 0:
            raise ValueError("半徑不能為負數")
        self._radius = value

    @property
    def area(self):             # 唯讀屬性（沒有 setter）
        # 每次讀取時即時計算，不額外儲存
        import math
        return math.pi * self._radius ** 2

    @property
    def diameter(self):
        return self._radius * 2


c = Circle(5)
print(c.radius)     # 5
print(c.area)       # 78.539...
print(c.diameter)   # 10

c.radius = 10       # 呼叫 setter
print(c.area)       # 314.159...

try:
    c.radius = -1   # 觸發 ValueError
except ValueError as e:
    print(e)        # 半徑不能為負數

try:
    c.area = 100    # 唯讀屬性不能設定
except AttributeError as e:
    print(e)

# ── 用 property 做延遲計算 ────────────────────────────────
class Rectangle:
    def __init__(self, width, height):
        # 直接存原始資料，衍生值交由 property 計算
        self.width = width
        self.height = height

    @property
    def area(self):
        # 屬性值會隨寬高變化，自動反映最新結果
        return self.width * self.height

    @property
    def perimeter(self):
        return 2 * (self.width + self.height)


r = Rectangle(4, 6)
print(r.area)       # 24
print(r.perimeter)  # 20
r.width = 8         # 修改後 area 自動更新
print(r.area)       # 48
