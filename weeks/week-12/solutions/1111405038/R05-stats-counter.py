# R05. 資料統計與累加（6.13）
# Counter / defaultdict / namedtuple 整合應用

from collections import Counter, defaultdict, namedtuple

# Counter: 快速統計元素出現次數
# defaultdict: 鍵不存在時自動建立預設值
# namedtuple: 以欄位名稱存取資料，提高可讀性

# ── Counter：計數器 ──────────────────────────────────────
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
cnt = Counter(words)
print("Counter：", cnt)
# most_common(n) 會回傳出現次數最高的前 n 筆
print("最多出現：", cnt.most_common(2))      # [('apple', 3), ('banana', 2)]

# 可直接相加合併
extra = Counter(["banana", "cherry"])
# 相同 key 的計數會自動相加
print("合併：", cnt + extra)

# ── defaultdict：有預設值的 dict ─────────────────────────
# 按類別分組
records = [
    ("系資", "Alice"),
    ("電子", "Bob"),
    ("系資", "Carol"),
    ("電子", "David"),
    ("系資", "Eve"),
]

by_dept = defaultdict(list)
for dept, name in records:
    # 若 dept 尚未出現，defaultdict(list) 會先建立空 list
    by_dept[dept].append(name)

print("\ndefaultdict：")
for dept, members in by_dept.items():
    print(f"  {dept}: {members}")

# defaultdict(int) 做計數
score_sum = defaultdict(int)
scores = [("Alice", 90), ("Bob", 80), ("Alice", 85), ("Bob", 70)]
for name, score in scores:
    # int 預設值為 0，可直接累加
    score_sum[name] += score
print("\n各人總分：", dict(score_sum))

# ── namedtuple：具名結構，更可讀 ─────────────────────────
Stock = namedtuple("Stock", ["symbol", "price", "change"])
# 可用 s.symbol 取值，比 tuple 索引更直觀
s = Stock("AA", 39.48, -0.18)
print(f"\n{s.symbol}: ${s.price}  漲跌 {s.change}")

# ── 綜合：從 list of dict 做統計 ─────────────────────────
data = [
    {"dept": "系資", "score": 85},
    {"dept": "電子", "score": 78},
    {"dept": "系資", "score": 92},
    {"dept": "電子", "score": 88},
]

dept_scores = defaultdict(list)
for row in data:
    # 依部門蒐集分數，後續可再做統計
    dept_scores[row["dept"]].append(row["score"])

print("\n各系平均：")
for dept, scores in dept_scores.items():
    # 平均 = 總和 / 筆數
    avg = sum(scores) / len(scores)
    print(f"  {dept}: {avg:.1f}")
