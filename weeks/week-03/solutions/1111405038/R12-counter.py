# R12. Counter 統計 + most_common（1.12）

from collections import Counter

# 一串單字資料，裡面可能有重複出現的詞
words = ['look', 'into', 'my', 'eyes', 'look']

# Counter 會自動統計每個元素出現的次數
word_counts = Counter(words)

# most_common(3) 會回傳出現次數最多的前 3 個元素
word_counts.most_common(3)

# update 可以把新資料加入原本的統計結果中
word_counts.update(['eyes', 'eyes'])
