# U2. 星號解包為何能處理「不定長」且結果固定是 list（1.2）

# record 只有兩個元素：姓名與 email。
record = ('Dave', 'dave@example.com')

# 前兩個變數 name、email 會依序接收前兩個元素。
# *phones 是 starred expression，意思是：
# 把「剩下所有尚未分配的元素」通通收集起來。
#
# 這種寫法的好處是可以處理不定長資料：
# 就算 record 後面還多很多電話號碼，也都能被 phones 一次接住。
name, email, *phones = record

# 這個例子裡，前兩個元素分給 name 和 email 後，
# 已經沒有剩餘元素可放進 phones。
# 但 Python 不會讓 phones 變成 None，也不會報錯，
# 而是固定給它一個空的 list。
#
# 也就是說，星號解包得到的結果型別一律是 list，
# 不管原本右邊是 tuple、list，或最後是否真的有剩餘元素。
# phones == []  仍是 list
