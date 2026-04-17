# R8. 字典運算：min/max/sorted + zip（1.8）

# 股票名稱對應價格的字典
prices = {'ACME': 45.23, 'AAPL': 612.78, 'FB': 10.75}

# 把 value 和 key 配成 (價格, 名稱) 的 tuple，再找出最小的一組
min(zip(prices.values(), prices.keys()))

# 找出價格最大的一組資料
max(zip(prices.values(), prices.keys()))

# 依照價格由小到大排序，結果會是一串 (價格, 名稱) 的 tuple
sorted(zip(prices.values(), prices.keys()))

# 也可以直接對字典做 min，並用 key 指定比較依據是價格
# 這種寫法最後回傳的是 key，也就是股票名稱
min(prices, key=lambda k: prices[k])  # 回傳 key
