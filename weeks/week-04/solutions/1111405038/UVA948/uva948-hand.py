import sys


def main():
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

        for coin in range(1, n + 1):
            ok = False

            for kind in ("heavy", "light"):
                valid = True

                for left, right, result in weighings:
                    in_left = coin in left
                    in_right = coin in right

                    if result == "=":
                        if in_left or in_right:
                            valid = False
                            break
                    elif result == "<":
                        if kind == "heavy":
                            if not in_right:
                                valid = False
                                break
                        else:
                            if not in_left:
                                valid = False
                                break
                    else:
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

        if len(possible) == 1:
            answers.append(str(possible[0]))
        else:
            answers.append("0")

    print("\n\n".join(answers))


if __name__ == "__main__":
    main()