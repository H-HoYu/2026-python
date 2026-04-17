import sys


# 一次把整份輸入資料讀進來並切開。
# 這題是讀到 EOF 為止，所以不一定只有一組測資，
# 用這種方式可以方便地一路往後解析。
data = sys.stdin.read().split()

# index 用來記錄目前讀到第幾個輸入值。
index = 0

# answers 用來收集每組測資的輸出結果。
answers = []

while index < len(data):
    # 先讀出這組測資的數字個數。
    count = int(data[index])
    index += 1

    # 取出這一組的所有數字並排序。
    # 這題的關鍵在於：
    # 讓 |X1-A| + |X2-A| + ... + |Xn-A| 最小的 A，
    # 一定會落在排序後的中位數區間內。
    numbers = sorted(int(value) for value in data[index:index + count])
    index += count

    # 若資料筆數是奇數，low 和 high 會是同一個中位數。
    # 若資料筆數是偶數，所有介於 low 到 high 之間的整數，
    # 都能讓總距離達到最小值。
    low = numbers[(count - 1) // 2]
    high = numbers[count // 2]

    # count_in_range 代表有多少原始數字落在最佳區間 [low, high] 內。
    # 這正是題目第二個要輸出的數值。
    count_in_range = 0

    for value in numbers:
        if low <= value <= high:
            count_in_range += 1

    # 題目要求輸出三個整數：
    # 1. 最小的最佳 A，也就是 low
    # 2. 能得到最小總距離的資料個數，也就是落在 [low, high] 內的數量
    # 3. 可能的最佳 A 有幾種，也就是 high - low + 1
    answers.append(f"{low} {count_in_range} {high - low + 1}")

# 題目要求每組測資輸出一行，因此最後用換行字元串接。
if answers:
    sys.stdout.write("\n".join(answers))