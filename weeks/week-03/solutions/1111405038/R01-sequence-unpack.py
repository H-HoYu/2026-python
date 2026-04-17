# R1. 序列解包（1.1）

# 將 tuple 中的兩個值依序拆開，分別指定給 x 與 y
p = (4, 5)
x, y = p

# data 內包含字串、整數、浮點數，以及一個日期 tuple
data = ['ACME', 50, 91.1, (2012, 12, 21)]

# 直接把串列中的 4 個元素依序解包到對應變數
name, shares, price, date = data

# 也可以在解包時，繼續把內層的日期 tuple 拆成年、月、日
name, shares, price, (year, mon, day) = data

# 丟棄不需要的值（占位）
# 用 _ 當作占位符號，表示這些值有接到但後續不會使用
_, shares, price, _ = data
