import sys


def main():
    # 先把所有非空白行讀進來，這樣就不用一直處理題目中的空白列。
    lines = [line.strip() for line in sys.stdin if line.strip()]
    if not lines:
        return

    case_count = int(lines[0])
    index = 1
    answers = []

    for _ in range(case_count):
        n, k = map(int, lines[index].split())
        index += 1

        weighings = []
        for _ in range(k):
            parts = list(map(int, lines[index].split()))
            index += 1

            p = parts[0]
            left = parts[1:1 + p]
            right = parts[1 + p:1 + 2 * p]
            result = lines[index]
            index += 1

            weighings.append((left, right, result))

        possible = []

        # 依序假設每一枚硬幣是假幣。
        for coin in range(1, n + 1):
            ok = False

            # 再假設它可能是重的，也可能是輕的，只要其中一種說得通就先保留。
            for kind in ("heavy", "light"):
                valid = True

                for left, right, result in weighings:
                    in_left = coin in left
                    in_right = coin in right

                    if result == "=":
                        # 平衡代表這次上秤的都是真幣。
                        if in_left or in_right:
                            valid = False
                            break
                    elif result == "<":
                        # 左邊較輕：假幣只能是左邊的輕幣，或右邊的重幣。
                        if kind == "heavy":
                            if not in_right:
                                valid = False
                                break
                        else:
                            if not in_left:
                                valid = False
                                break
                    else:
                        # 左邊較重：假幣只能是左邊的重幣，或右邊的輕幣。
                        if kind == "heavy":
                            if not in_left:
                                valid = False
                                break
                        else:
                            if not in_right:
                                valid = False
                                break

                if valid:
                    ok = True
                    break

            if ok:
                possible.append(coin)

        # 只有唯一答案時才輸出該硬幣，否則輸出 0。
        if len(possible) == 1:
            answers.append(str(possible[0]))
        else:
            answers.append("0")

    print("\n\n".join(answers))


if __name__ == "__main__":
    main()