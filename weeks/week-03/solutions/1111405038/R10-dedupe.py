# R10. 去重且保序（1.10）

# 這個函式會去除重複元素，同時保留原本出現的順序
def dedupe(items):
    # 用 seen 記錄已經看過的值
    seen = set()
    for item in items:
        # 只有第一次出現的值才輸出
        if item not in seen:
            yield item
            seen.add(item)

# 這個版本可搭配 key，自訂「如何判斷重複」
def dedupe2(items, key=None):
    seen = set()
    for item in items:
        # 如果有提供 key，就用 key(item) 的結果作為去重依據
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)
