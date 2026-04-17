# R13. 字典列表排序 itemgetter（1.13）

from operator import itemgetter

# rows 是由多個字典組成的串列，每個字典代表一筆資料
rows = [{'fname': 'Brian', 'uid': 1003}, {'fname': 'John', 'uid': 1001}]

# 依照 fname 欄位排序
sorted(rows, key=itemgetter('fname'))

# 依照 uid 欄位排序
sorted(rows, key=itemgetter('uid'))

# 先依 uid 排序，若 uid 相同再依 fname 排序
sorted(rows, key=itemgetter('uid', 'fname'))
