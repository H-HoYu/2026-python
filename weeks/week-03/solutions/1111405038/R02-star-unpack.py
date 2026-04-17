# R2. 解包數量不固定：星號解包（1.2）

# 取出第一個與最後一個成績，中間其餘成績用 *middle 接住
def drop_first_last(grades):
    first, *middle, last = grades
    # 計算中間成績的平均，常見於去頭去尾後再評分的情境
    return sum(middle) / len(middle)

# 一筆資料中前兩個欄位固定，後面其餘電話號碼用串列收集
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = record

# 把最後一個值指定給 current，前面所有值交給 trailing
*trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]
