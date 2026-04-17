# R11. 命名切片 slice（1.11）

# 一筆固定欄位格式的字串資料
record = '....................100 .......513.25 ..........'

# 用 slice 先定義好股票數量欄位的位置
SHARES = slice(20, 23)

# 用 slice 定義價格欄位的位置
PRICE = slice(31, 37)

# 依照切片位置取出字串，再轉成數字計算總成本
cost = int(record[SHARES]) * float(record[PRICE])
