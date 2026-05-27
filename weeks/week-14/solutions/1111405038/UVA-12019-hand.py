import sys

days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
name = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

arr = sys.stdin.read().split()
if arr:
    t = int(arr[0])
    p = 1
    ans = []

    for _ in range(t):
        m = int(arr[p])
        d = int(arr[p + 1])
        p += 2
        x = sum(days[: m - 1]) + (d - 1)
        ans.append(name[x % 7])

    print("\n".join(ans))
