# U4. heap 為何能高效拿 Top-N（1.4）

import heapq

# 原始資料是一個普通 list，裡面的順序還不是 heap 結構。
nums = [5, 1, 9, 2]

# 先複製一份，避免直接改到原本的 nums。
h = nums[:]

# heapify() 會把 list 原地重排成「最小堆（min-heap）」。
# 注意：heap 排列後看起來不一定是完整排序結果，
# 它只保證一件核心事情：父節點會小於等於子節點。
# 因此最小元素一定會放在索引 0 的位置。
heapq.heapify(h)
# h[0] 永遠是最小值（這是 heap 的核心性質）

# heappop() 會移除並回傳目前 heap 中最小的元素。
# 取出後，heap 會自動重新調整，讓新的最小值再次回到 h[0]。
# 也因為這種結構維護成本低，heap 很適合用來反覆取得最小值，
# 或延伸用在取 Top-N / priority queue 等場景。
m = heapq.heappop(h)  # 每次 pop 都拿到目前最小
