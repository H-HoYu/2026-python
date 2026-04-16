# R17. 字典子集（1.17）

# 原始字典：key 是股票代號，value 是對應價格。
prices = {'ACME': 45.23, 'AAPL': 612.78, 'IBM': 205.55}

# 字典推導式的寫法和串列推導式相似，
# 差別在於產生的是 {key: value} 形式的新字典。
# prices.items() 會逐一取出 (key, value) 配對。
# 這裡的條件是 v > 200，因此只保留價格大於 200 的項目。
p1 = {k: v for k, v in prices.items() if v > 200}

# 也可以不是依 value 篩選，而是依 key 是否屬於某個集合來挑選。
# set 很適合做 membership test，也就是「某元素是否存在」的判斷。
tech_names = {'AAPL', 'IBM'}

# 這裡表示：如果股票代號 k 出現在 tech_names 中，
# 就把該項目保留到新的字典 p2。
p2 = {k: v for k, v in prices.items() if k in tech_names}
