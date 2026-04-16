# R18. namedtuple（1.18）

from collections import namedtuple

# namedtuple 可以建立「帶有欄位名稱的 tuple 類型」。
# 它仍然保有 tuple 輕量、不可變的特性，
# 但使用時可以用欄位名稱存取資料，可讀性比純索引更好。
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])

# 建立一筆 Subscriber 資料。
# 第一個欄位是 addr，第二個欄位是 joined。
sub = Subscriber('jonesy@example.com', '2012-10-19')

# 與一般 tuple 用 sub[0] 相比，sub.addr 更容易理解欄位意義。
sub.addr

# 再建立另一個 namedtuple 類型 Stock，
# 用來表示股票名稱、持股數量與價格。
Stock = namedtuple('Stock', ['name', 'shares', 'price'])
s = Stock('ACME', 100, 123.45)

# namedtuple 是不可變物件，不能像一般物件那樣直接修改欄位值。
# _replace() 會依指定欄位建立一個「更新後的新物件」，
# 原本的 s 不會在原地被改動，因此通常要重新指定回變數。
s = s._replace(shares=75)
