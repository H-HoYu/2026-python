import sys


# 一次把整份輸入資料讀進來，並依空白切開。
# 因為題目每組資料都只有 3 個值，使用 index 依序讀取會很方便。
data = sys.stdin.read().split()

if data:
    # 第一個值代表總共有幾組測試資料。
    case_count = int(data[0])

    # index 用來記錄目前讀到輸入串列的哪個位置。
    index = 1

    # answers 用來收集每一組測資的輸出結果。
    answers = []

    for _ in range(case_count):
        # player_count = 玩家總數 N
        # success_probability = 單次出現成功事件的機率 p
        # player_index = 想查詢的第幾位玩家 i
        player_count = int(data[index])
        success_probability = float(data[index + 1])
        player_index = int(data[index + 2])
        index += 3

        # 如果 p = 0，表示永遠不可能有人成功，
        # 那麼第 i 位玩家獲勝機率自然就是 0。
        if success_probability == 0:
            answers.append("0.0000")
            continue

        # first_win_probability 表示：
        # 前面第 1 到第 i-1 位玩家都失敗，然後第 i 位玩家成功的機率。
        # 因此公式是：
        # (1 - p)^(i - 1) * p
        first_win_probability = ((1 - success_probability) ** (player_index - 1)) * success_probability

        # full_round_failure 表示一整輪 N 個玩家全部都失敗的機率。
        # 一個玩家失敗的機率是 (1 - p)，
        # N 個玩家都失敗就是 (1 - p)^N。
        full_round_failure = (1 - success_probability) ** player_count

        # 第 i 位玩家的總獲勝機率不是只有第一輪，還包含：
        # - 第一輪前面都失敗，第 i 位成功
        # - 第二輪前面整整一輪都沒人成功，再輪到第 i 位成功
        # - 第三輪前面兩整輪都沒人成功，再輪到第 i 位成功
        # ...
        #
        # 也就是：
        # first_win_probability
        # + first_win_probability * full_round_failure
        # + first_win_probability * full_round_failure^2
        # + ...
        #
        # 這是一個等比級數，總和公式為：
        # first_win_probability / (1 - full_round_failure)
        total_probability = first_win_probability / (1 - full_round_failure)

        # 題目要求輸出到小數點後四位，因此使用 :.4f 格式化。
        answers.append(f"{total_probability:.4f}")

    # 每組測資答案各輸出一行。
    sys.stdout.write("\n".join(answers))