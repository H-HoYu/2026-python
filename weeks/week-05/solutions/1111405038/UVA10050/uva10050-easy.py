import sys


# 一次讀入全部輸入資料，並把每個數字都轉成整數。
# UVA 題目通常都是純文字輸入，這樣寫可以讓程式更精簡。
data = list(map(int, sys.stdin.read().split()))

if data:
    # 第一個數字代表總共有幾組測試資料。
    test_count = data[0]

    # index 用來追蹤目前讀到輸入串列的哪一個位置。
    index = 1

    # answers 用來收集每組測資的答案，最後再一次輸出。
    answers = []

    for _ in range(test_count):
        # 先讀出這組測資總共有幾天要模擬。
        total_days = data[index]
        index += 1

        # 再讀出這組測資有幾個政黨。
        party_count = data[index]
        index += 1

        # 取出這些政黨各自的 hartal 參數。
        # 例如某個政黨的參數是 3，就代表每隔 3 天會發生一次罷工。
        hartals = data[index:index + party_count]
        index += party_count

        # 用布林陣列記錄每一天是否已經被算成罷工日。
        # 這樣做有兩個好處：
        # 1. 同一天如果被多個政黨同時罷工，只會記一次。
        # 2. 最後可以直接用 sum(lost_days) 算出罷工天數。
        # 這裡多開一格，讓 day 可以直接對應到 lost_days[day]。
        lost_days = [False] * (total_days + 1)

        for hartal in hartals:
            # 從該政黨第一次罷工的那一天開始，
            # 之後每隔 hartal 天就再罷工一次。
            day = hartal
            while day <= total_days:
                # 依題意，模擬的第一天是星期天。
                # 因此：
                # day % 7 == 6 代表星期五
                # day % 7 == 0 代表星期六
                # 這兩天是假日，不算損失工作天。
                if day % 7 != 6 and day % 7 != 0:
                    lost_days[day] = True

                # 繼續找這個政黨下一次罷工的日期。
                day += hartal

        # 布林值在 Python 中 True 會當作 1，False 會當作 0，
        # 所以直接加總就能得到這組測資損失的工作天數。
        answers.append(str(sum(lost_days)))

    # 題目要求每組答案輸出一行，因此用換行字元串接後輸出。
    sys.stdout.write("\n".join(answers))