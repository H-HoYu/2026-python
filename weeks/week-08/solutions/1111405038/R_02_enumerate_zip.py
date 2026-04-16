# Remember（記憶）- enumerate() 和 zip()
#
# 這份程式用來整理兩個常見的 Python 內建工具：
# 1) enumerate()：在走訪序列時，同時取得「索引」與「元素值」。
# 2) zip()：把多個序列「對齊打包」後一起走訪。
#
# 學習重點：
# - 了解 enumerate 的 start 參數如何改變索引起始值。
# - 了解 zip 在長度不一致時只會配對到最短序列。
# - 了解 zip_longest 可在長度不一致時保留所有資料並補上預設值。

# 範例資料：顏色清單
colors = ["red", "green", "blue"]

print("--- enumerate() 基本用法 ---")
# enumerate(colors) 會產生 (索引, 元素) 的配對。
# 預設索引從 0 開始，所以輸出會是 0, 1, 2。
for i, color in enumerate(colors):
    print(f"{i}: {color}")

print("\n--- enumerate(start=1) ---")
# 將 start 設為 1，可把索引改成「人類較直覺」的編號方式。
# 這在顯示「第幾筆資料」時很常用。
for i, color in enumerate(colors, 1):
    print(f"第{i}個: {color}")

print("\n--- enumerate with 檔案 ---")
# 模擬讀檔後的行內容。
# 真實情境中常寫成：for lineno, line in enumerate(file, 1)
# 方便在錯誤訊息中標示「第幾行」。
lines = ["line1", "line2", "line3"]
for lineno, line in enumerate(lines, 1):
    print(f"行 {lineno}: {line}")

print("\n--- zip() 基本用法 ---")
# zip(names, scores) 會把同位置的元素配對：
# 第 1 個名字配第 1 個分數，第 2 個名字配第 2 個分數，以此類推。
names = ["Alice", "Bob", "Carol"]
scores = [90, 85, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

print("\n--- zip() 多個序列 ---")
# zip 可以同時處理 3 個以上序列。
# 每次迴圈會取出一組 (x, y, z) 進行運算。
a = [1, 2, 3]
b = [10, 20, 30]
c = [100, 200, 300]
for x, y, z in zip(a, b, c):
    print(f"{x} + {y} + {z} = {x + y + z}")

print("\n--- zip() 長度不同 ---")
# 注意：zip 遇到長度不同的序列時，會以「最短序列」為準停止。
# 也就是多出來的元素會被忽略。
x = [1, 2]
y = ["a", "b", "c"]
print(f"list(zip(x, y)): {list(zip(x, y))}")

from itertools import zip_longest

# 若不希望資料被截斷，可使用 itertools.zip_longest。
# fillvalue=0 表示缺少配對值時，用 0 補齊。
print(f"zip_longest: {list(zip_longest(x, y, fillvalue=0))}")

print("\n--- 建立字典 ---")
# 常見技巧：把 keys 和 values 用 zip 配成鍵值對，再交給 dict 建立字典。
# 前提是 keys 與 values 的順序要一一對應。
keys = ["name", "age", "city"]
values = ["John", "30", "NYC"]
d = dict(zip(keys, values))
print(f"dict: {d}")
