# U5. 優先佇列為何要加 index（1.5）

import heapq

class Item:
    def __init__(self, name):
        self.name = name

# pq 會被當作 heap 使用。
# heapq 本身沒有專屬的 PriorityQueue 類別結構，
# 常見做法是把 tuple 放進 heap，利用 tuple 的比較規則決定優先順序。
pq = []

# 如果只放 (priority, item)，當 priority 不同時沒有問題，
# heapq 只需要比較第一個欄位就能決定順序。
#
# 但如果兩筆資料的 priority 一樣，Python 會繼續比較 tuple 的第二個欄位，
# 也就是兩個 Item 物件本身。
# Item 類別沒有定義 < 的比較方式，因此會觸發 TypeError。
# heapq.heappush(pq, (-1, Item('a')))
# heapq.heappush(pq, (-1, Item('b')))  # TypeError

# 正確做法是在中間多放一個遞增的 index。
# 這樣 tuple 會變成 (priority, index, item)：
# 1. 先比 priority
# 2. 若 priority 相同，再比 index
# 3. 不需要真的去比較 item 本身
#
# 另外，index 也能保證相同 priority 的元素維持插入順序，
# 也就是常說的 stable ordering。
idx = 0
heapq.heappush(pq, (-1, idx, Item('a'))); idx += 1
heapq.heappush(pq, (-1, idx, Item('b'))); idx += 1
