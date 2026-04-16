# U9. groupby 為何一定要先 sort（1.15）

from itertools import groupby
from operator import itemgetter

# 這裡故意準備一組「相同 date 沒有排在一起」的資料。
# 第一筆和第三筆都是 07/02/2012，但中間夾了一筆 07/01/2012。
rows = [
    {'date': '07/02/2012', 'x': 1},
    {'date': '07/01/2012', 'x': 2},
    {'date': '07/02/2012', 'x': 3},
]

# groupby() 的重要特性是：
# 它不是掃完整份資料後再把相同 key 全部收攏，
# 而是只要發現「目前元素的 key 改變了」，就開始下一組。
#
# 也就是說，groupby 其實是在做「連續區塊分組」，
# 因此如果同一個 date 分散在不同位置，就會被拆成多組。
# 下面這段中，07/02 會先成為一組，後面第三筆的 07/02 又會變成另一組。
for k, g in groupby(rows, key=itemgetter('date')):
    # g 是目前這一組的迭代器；轉成 list 只是為了把這一組的內容取出來。
    list(g)

# 先用同一個 key 做排序後，
# 所有相同 date 的資料就會排成連續的一段。
# 這時再交給 groupby，才會得到符合直覺的分組結果。
rows.sort(key=itemgetter('date'))
for k, g in groupby(rows, key=itemgetter('date')):
    list(g)
