# R20. ChainMap 合併映射（1.20）

from collections import ChainMap

# 這裡準備兩個字典，等等會把它們視為一個「串接起來的映射」來查找。
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}

# ChainMap(a, b) 不會真的把 a、b 複製合併成一個新字典，
# 而是建立一個可視為「先查 a，再查 b」的查找視圖。
# 因此它很適合用在多層設定值、區域變數/全域變數之類的情境。
c = ChainMap(a, b)

# 查找鍵 x 時，會先看 a，a 裡有 x，所以直接回傳 1。
c['x']

# 查找鍵 z 時，a 和 b 都有 z。
# ChainMap 的規則是：前面的 mapping 優先，
# 因此這裡會取到 a['z']，也就是 3，而不是 b['z'] 的 4。
c['z']  # 取到 a 的 z
