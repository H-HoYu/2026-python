import sys


def main():
    n = int(sys.stdin.readline())

    counts = {}

    for _ in range(n):
        line = sys.stdin.readline()
        for ch in line:
            if "a" <= ch <= "z":
                ch = chr(ord(ch) - 32)
            if "A" <= ch <= "Z":
                counts[ch] = counts.get(ch, 0) + 1

    items = list(counts.items())

    items.sort()

    items.sort(key=lambda item: item[1], reverse=True)

    for ch, count in items:
        print(ch, count)


if __name__ == "__main__":
    main()