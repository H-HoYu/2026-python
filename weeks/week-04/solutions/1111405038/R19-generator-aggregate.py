# R19. 轉換+聚合：生成器表達式（1.19）

# 生成器表達式常用在「一邊轉換資料，一邊交給聚合函式處理」的情境。
# 好處是不需要先建立中間 list，寫法精簡，也較節省記憶體。

nums = [1, 2, 3]

# 這裡把 nums 中每個元素平方後，再交給 sum() 加總。
# x * x for x in nums 就是一個生成器表達式，
# 會逐個產生 1、4、9，最後 sum() 算出總和 14。
sum(x * x for x in nums)

# join() 只能串接字串，因此若 tuple 中混有整數、浮點數，
# 就需要先把每個元素轉成 str。
s = ('ACME', 50, 123.45)

# 這裡利用生成器表達式逐個轉成字串，
# 再用逗號把它們連接起來。
','.join(str(x) for x in s)

# 這裡的資料是股票清單，每一筆都是字典。
portfolio = [{'name': 'AOL', 'shares': 20}, {'name': 'YHOO', 'shares': 75}]

# 這個寫法只取出每筆資料中的 shares 值，
# 再從這些數字中找出最小值。
# 因此結果只會是最小的持股數量 20，不會知道是哪一筆資料。
min(s['shares'] for s in portfolio)

# 如果想保留整筆資料，而不是只有最小值本身，
# 可以把原始資料直接交給 min()，並用 key 指定比較依據。
# 這樣回傳的是 shares 最小的那一整個字典。
min(portfolio, key=lambda s: s['shares'])
