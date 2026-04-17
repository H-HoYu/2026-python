# R4. heapq 取 Top-N（1.4）

import heapq

# 一組數字資料，示範如何取出最大與最小的前幾筆
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]

# 取出最大的 3 個值
heapq.nlargest(3, nums)

# 取出最小的 3 個值
heapq.nsmallest(3, nums)

# 投資組合資料，每筆資料都是一個字典
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
]

# 用 key 指定以 price 欄位作為比較依據，找出價格最低的 1 筆
heapq.nsmallest(1, portfolio, key=lambda s: s['price'])

# 先把串列轉成 heap 結構，之後就能快速取得最小值
heap = list(nums)
heapq.heapify(heap)

# heappop 會取出目前 heap 中最小的元素
heapq.heappop(heap)
