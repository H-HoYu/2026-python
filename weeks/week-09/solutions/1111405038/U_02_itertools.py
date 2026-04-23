# Understand（理解）- itertools 工具函數

# 從 itertools 匯入常見工具：
# - islice：對「可迭代物件」做切片，不必先轉 list
# - dropwhile：條件成立時持續丟棄，直到第一次不成立後全部保留
# - takewhile：條件成立時持續取用，遇到第一次不成立就停止
# - chain：把多個可迭代物件串成一個連續序列
# - permutations：排列（順序不同算不同）
# - combinations：組合（順序不同視為相同）
from itertools import islice, dropwhile, takewhile, chain, permutations, combinations

print("--- islice() 切片 ---")


# 產生一個無限遞增的產生器（generator）
# 與 range 不同：它不會一次建立整個序列，適合示範惰性計算
def count(n):
    i = n
    while True:
        yield i
        i += 1


# 從 0 開始的無限序列：0,1,2,3,4,...
c = count(0)

# islice(c, 5, 10) 類似序列切片 [5:10]
# 會取到第 5~9 個元素（不含 10）=> [5,6,7,8,9]
result = list(islice(c, 5, 10))
print(f"islice(c, 5, 10): {result}")

print("\n--- dropwhile() 條件跳過 ---")
nums = [1, 3, 5, 2, 4, 6]

# dropwhile(lambda x: x < 5, nums)
# 流程：
# 1) 一開始只要 x < 5 就丟掉（1、3 被丟掉）
# 2) 遇到 5 時條件不成立，從這一刻起「後面全部保留」
# 3) 所以結果是 [5,2,4,6]（後面的 2、4 不會再被判斷丟棄）
result = list(dropwhile(lambda x: x < 5, nums))
print(f"dropwhile(x<5, {nums}): {result}")

print("\n--- takewhile() 條件取用 ---")

# takewhile(lambda x: x < 5, nums)
# 從頭開始「只要條件成立就取」，第一個不成立就立即停止
# 因為遇到 5 就停止，所以只會得到 [1,3]
result = list(takewhile(lambda x: x < 5, nums))
print(f"takewhile(x<5, {nums}): {result}")

print("\n--- chain() 串聯 ---")
a = [1, 2]
b = [3, 4]
c = [5]

# chain(a, b, c) 不會建立中間大陣列，而是逐段迭代輸出
# 最後轉成 list 才真正得到 [1,2,3,4,5]
print(f"chain(a, b, c): {list(chain(a, b, c))}")

print("\n--- permutations() 排列 ---")
items = ["a", "b", "c"]
print(f"permutations(items):")

# permutations(items) 預設 r=len(items)
# 會列出 3 個元素的所有排列，共 3! = 6 種
for p in permutations(items):
    print(f"  {p}")

print(f"permutations(items, 2):")

# permutations(items, 2)：從 3 個元素中挑 2 個並考慮順序
# 數量為 P(3,2)=3*2=6
for p in permutations(items, 2):
    print(f"  {p}")

print("\n--- combinations() 組合 ---")
print(f"combinations(items, 2):")

# combinations(items, 2)：從 3 個元素中挑 2 個，不考慮順序
# ('a','b') 與 ('b','a') 視為同一組，所以只有 C(3,2)=3 種
for c in combinations(items, 2):
    print(f"  {c}")

print("\n--- 組合應用：密碼窮舉 ---")
chars = ["A", "B", "1"]
print("2位數密碼:")

# 用 permutations(chars, 2) 產生「不重複字元」的 2 位密碼
for p in permutations(chars, 2):
    print(f"  {''.join(p)}")

print("2位數密碼（可重複）:")

# combinations_with_replacement：允許重複取元素，但不考慮順序
# 例如會有 AA、AB、A1、BB、B1、11，但不會另外出現 BA、1A...
from itertools import combinations_with_replacement

for p in combinations_with_replacement(chars, 2):
    print(f"  {''.join(p)}")
