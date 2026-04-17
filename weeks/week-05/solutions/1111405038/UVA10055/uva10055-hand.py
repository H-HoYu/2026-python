import sys


data = list(map(int, sys.stdin.read().split()))

if data:
    n = data[0]
    q = data[1]
    index = 2

    tree = [0] * (n + 1)
    answers = []

    def toggle(position: int) -> None:
        while position <= n:
            tree[position] ^= 1
            position += position & -position

    def prefix_xor(position: int) -> int:
        result = 0
        while position > 0:
            result ^= tree[position]
            position -= position & -position
        return result

    for _ in range(q):
        command = data[index]
        index += 1

        if command == 1:
            position = data[index]
            index += 1
            toggle(position)
        else:
            left = data[index]
            right = data[index + 1]
            index += 2
            answers.append(str(prefix_xor(right) ^ prefix_xor(left - 1)))

    sys.stdout.write("\n".join(answers))