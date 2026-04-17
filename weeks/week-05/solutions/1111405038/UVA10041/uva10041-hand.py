import sys


data = list(map(int, sys.stdin.read().split()))

if data:
    test_count = data[0]
    index = 1
    answers = []

    for _ in range(test_count):
        relative_count = data[index]
        index += 1

        relatives = sorted(data[index:index + relative_count])
        index += relative_count

        home = relatives[relative_count // 2]
        total_distance = 0

        for address in relatives:
            total_distance += abs(address - home)

        answers.append(str(total_distance))

    sys.stdout.write("\n".join(answers))