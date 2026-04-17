# R6. 多值字典 defaultdict / setdefault（1.6）

from collections import defaultdict

# defaultdict(list) 會在鍵不存在時，自動建立空串列
d = defaultdict(list)
# 因此可以直接 append，而不用先判斷鍵是否存在
d['a'].append(1); d['a'].append(2)

# defaultdict(set) 會在鍵不存在時，自動建立空集合
d = defaultdict(set)
# set 適合用來存不重複的值
d['a'].add(1); d['a'].add(2)

# 一般 dict 也能搭配 setdefault 達到類似效果
d = {}
# 如果鍵 'a' 不存在，就先放入空串列，再對這個串列 append
d.setdefault('a', []).append(1)
