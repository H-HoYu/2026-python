# R7. OrderedDict（1.7）

from collections import OrderedDict
import json

# OrderedDict 會依照鍵值加入的先後順序來保存資料
d = OrderedDict()

# 先加入 foo，再加入 bar
d['foo'] = 1; d['bar'] = 2

# 轉成 JSON 字串時，欄位順序也會依照插入順序輸出
json.dumps(d)
