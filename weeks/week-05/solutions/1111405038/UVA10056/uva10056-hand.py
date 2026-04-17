import sys


data = sys.stdin.read().split()

if data:
    case_count = int(data[0])
    index = 1
    answers = []

    for _ in range(case_count):
        player_count = int(data[index])
        success_probability = float(data[index + 1])
        player_index = int(data[index + 2])
        index += 3

        if success_probability == 0:
            answers.append("0.0000")
            continue

        first_win_probability = ((1 - success_probability) ** (player_index - 1)) * success_probability
        full_round_failure = (1 - success_probability) ** player_count
        total_probability = first_win_probability / (1 - full_round_failure)
        answers.append(f"{total_probability:.4f}")

    sys.stdout.write("\n".join(answers))