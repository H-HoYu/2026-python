# U6. defaultdict 為何比手動初始化乾淨（1.6）

from collections import defaultdict

# 這份資料的形式是 (key, value) 配對。
# 目標通常是把相同 key 的值收集到同一個 list 中。
pairs = [('a', 1), ('a', 2), ('b', 3)]

# 手動版：一直判斷 key 是否存在
# 一般 dict 在存取不存在的 key 時會出錯，
# 所以若想把值累加到 list 裡，必須先檢查 key 是否已建立。
d = {}
for k, v in pairs:
    # 第一次遇到某個 key 時，先手動放一個空 list。
    if k not in d:
        d[k] = []
    # 接著再把目前的值加進去。
    d[k].append(v)

# defaultdict：省掉初始化分支
# defaultdict(list) 的意思是：
# 當存取不存在的 key 時，自動呼叫 list() 建立預設值。
# 由於 list() 會產生 []，所以第一次遇到新 key 時，
# d2[k] 會自動變成空串列，之後就能直接 append。
d2 = defaultdict(list)
for k, v in pairs:
    # 不需要再寫 if k not in d2 這種初始化判斷，
# 程式會更短、更乾淨，也更不容易漏掉初始化邏輯。
    d2[k].append(v)
