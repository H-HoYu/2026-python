# R3. deque 保留最後 N 筆（1.3）

from collections import deque

# 建立一個最多只能存 3 筆資料的 deque
q = deque(maxlen=3)
q.append(1); q.append(2); q.append(3)

# 再加入新資料時，因為超過上限，最左邊最舊的資料會被自動移除
q.append(4)  # 自動丟掉最舊的 1

# 不設定 maxlen 時，deque 可以自由從左右兩端加入或移除資料
q = deque()

# append 從右邊加入，appendleft 從左邊加入
q.append(1); q.appendleft(2)

# pop 移除右邊資料，popleft 移除左邊資料
q.pop(); q.popleft()
