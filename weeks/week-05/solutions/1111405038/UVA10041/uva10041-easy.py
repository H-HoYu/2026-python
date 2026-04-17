import sys


# 一次把整份輸入讀進來，依空白切開後全部轉成整數。
# 這種寫法很適合 UVA 這類純標準輸入題，程式會比較短。
data = list(map(int, sys.stdin.read().split()))

if data:
    # 第一個數字是測試資料組數。
    test_count = data[0]

    # index 用來記錄目前讀到輸入串列的哪個位置。
    index = 1

    # answers 用來收集每組測資的答案，最後再一起輸出。
    answers = []

    for _ in range(test_count):
        # 每組測資的第一個數字是親戚數量。
        relative_count = data[index]
        index += 1

        # 取出這一組所有親戚的門牌號碼，並排序。
        # 排序之後，中位數的位置就能直接找出來。
        relatives = sorted(data[index:index + relative_count])
        index += relative_count

        # 這題的關鍵是：
        # 如果想讓「到所有親戚的距離總和」最小，最佳位置會落在中位數。
        # 因此只要選排序後中間那個門牌即可。
        # 若親戚數量是偶數，取中間偏右或偏左都可以得到最小值，
        # 這裡直接取 relative_count // 2 的位置。
        home = relatives[relative_count // 2]

        # 計算把新家設在 home 時，到所有親戚家的總距離。
        total_distance = 0

        for address in relatives:
            # abs(address - home) 就是兩個門牌之間的距離。
            total_distance += abs(address - home)

        # 這一組測資的最小總距離先轉成字串存起來，
        # 方便最後用換行字元一次輸出。
        answers.append(str(total_distance))

    # UVA 題目通常要求每組答案各佔一行，因此用 \n 串接後輸出。
    sys.stdout.write("\n".join(answers))