import sys
from collections import Counter


def main() -> None:


    data = sys.stdin.read().strip().split()
    if not data:
        return

    it = iter(data)

    n = int(next(it))


    nums = [int(next(it)) for _ in range(n)]


    left_count: Counter[int] = Counter()

    for i in range(n):
        a = nums[i]
        for j in range(n):
            b = nums[j]
            for k in range(n):
                c = nums[k]
                s = a + b + c
                left_count[s] += 1


    total = 0

    for i in range(n):
        d = nums[i]
        for j in range(n):
            e = nums[j]
            for k in range(n):
                f_val = nums[k]
                r = f_val - d - e
                total += left_count.get(r, 0)

    sys.stdout.write(str(total) + "\n")


if __name__ == "__main__":
    main()
