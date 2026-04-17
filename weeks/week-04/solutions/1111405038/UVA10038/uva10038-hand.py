import sys


def main():
    for line in sys.stdin:
        nums = list(map(int, line.split()))
        if not nums:
            continue

        n = nums[0]
        arr = nums[1:]

        diffs = set()
        for i in range(1, n):
            diffs.add(abs(arr[i] - arr[i - 1]))

        if diffs == set(range(1, n)):
            print("Jolly")
        else:
            print("Not jolly")


if __name__ == "__main__":
    main()