# R5. 優先佇列 PriorityQueue（1.5）

import heapq

# 自訂一個簡單的優先佇列類別
class PriorityQueue:
    def __init__(self):
        # _queue 用來存放堆積資料
        self._queue = []
        # _index 用來記錄插入順序，避免優先權相同時無法比較 item
        self._index = 0

    # push 時將資料依照優先權放入 heap
    def push(self, item, priority):
        # heapq 是最小堆，所以用負的 priority 來模擬「數字越大，優先權越高」
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    # pop 時會取出目前優先權最高的項目
    def pop(self):
        return heapq.heappop(self._queue)[-1]
