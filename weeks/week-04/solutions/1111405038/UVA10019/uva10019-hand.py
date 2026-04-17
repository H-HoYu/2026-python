import sys


def main():
    for line in sys.stdin:
        parts = line.split()

        if len(parts) != 2:
            continue

        a = int(parts[0])
        b = int(parts[1])

        print(abs(a - b))


if __name__ == "__main__":
    main()