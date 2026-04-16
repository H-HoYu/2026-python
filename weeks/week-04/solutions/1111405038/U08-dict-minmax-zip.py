# U8. 字典最值為何常用 zip(values, keys)（1.8）

# 這個字典的 key 是代號，value 是價格。
prices = {'A': 2.0, 'B': 1.0}

# 直接對 dict 使用 min(prices)，
# Python 會把它視為「對所有 key 做 min」，
# 因此比較的是 key 本身，而不是 value。
# 這裡回傳的是字母序較小的 key，也就是 'A'。
min(prices)            # 回傳 key 的最小值（字母序）

# 如果改成 min(prices.values())，
# 的確可以取得最小 value，也就是 1.0，
# 但這時只拿到數值本身，已經不知道它原本對應哪個 key。
min(prices.values())   # 回傳最小 value，但你不知道是哪個 key

# zip(prices.values(), prices.keys()) 會把 value 和 key 配成 tuple：
# (2.0, 'A'), (1.0, 'B')
#
# 接著 min() 會先比較 tuple 的第一個元素，也就是 value，
# 因此能找出最小價格對應的那一組資料。
# 最後得到的結果會是 (1.0, 'B')，也就是：
# 最小 value 與它對應的 key 一次拿到。
min(zip(prices.values(), prices.keys()))
# 回傳 (最小value, 對應key)，一次拿到兩者
