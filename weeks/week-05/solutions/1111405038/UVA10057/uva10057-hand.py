import sys


data = sys.stdin.read().split()
index = 0
answers = []

while index < len(data):
    count = int(data[index])
    index += 1

    numbers = sorted(int(value) for value in data[index:index + count])
    index += count

    low = numbers[(count - 1) // 2]
    high = numbers[count // 2]
    count_in_range = 0

    for value in numbers:
        if low <= value <= high:
            count_in_range += 1

    answers.append(f"{low} {count_in_range} {high - low + 1}")

if answers:
    sys.stdout.write("\n".join(answers))