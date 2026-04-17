import sys


data = list(map(int, sys.stdin.read().split()))

if data:
    test_count = data[0]
    index = 1
    answers = []

    for _ in range(test_count):
        total_days = data[index]
        index += 1

        party_count = data[index]
        index += 1

        hartals = data[index:index + party_count]
        index += party_count

        lost_days = [False] * (total_days + 1)

        for hartal in hartals:
            day = hartal
            while day <= total_days:
                if day % 7 != 6 and day % 7 != 0:
                    lost_days[day] = True
                day += hartal

        answers.append(str(sum(lost_days)))

    sys.stdout.write("\n".join(answers))