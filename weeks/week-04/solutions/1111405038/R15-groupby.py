# R15. 分組 groupby（1.15）

from itertools import groupby
from operator import itemgetter

# 這是一組字典資料，每筆資料都包含 date 與 address 欄位。
# groupby() 常用來依某個欄位把連續資料分成多組。
rows = [{'date': '07/01/2012', 'address': '...'}, {'date': '07/02/2012', 'address': '...'}]

# itemgetter('date') 會建立一個函式，取出每筆資料中的 date 欄位。
# groupby() 只會把「相鄰且 key 相同」的元素分在一起，
# 所以在使用前通常要先依同一個 key 排序。
rows.sort(key=itemgetter('date'))

# groupby(rows, key=itemgetter('date')) 會依 date 欄位逐組產生資料。
# 每次迴圈會得到：
# 1. date: 目前這一組的分組鍵
# 2. items: 一個迭代器，內容是所有屬於該日期的資料列
for date, items in groupby(rows, key=itemgetter('date')):
    # items 不是 list，而是只能逐一往下走的群組迭代器。
    # 若要實際處理每筆資料，通常會在這裡再做一次內層迴圈。
    for i in items:
        # i 是該日期分組中的其中一筆資料，例如：
        # {'date': '07/01/2012', 'address': '...'}
        # 這個範例只示意分組流程，因此暫時不做其他處理。
        pass
