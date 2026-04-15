import sys

ROWS = ["`1234567890-=", "qwertyuiop[]\\", "asdfghjkl;'", "zxcvbnm,./"]

TABLE = {row[i].upper(): row[i - 1].upper() for row in ROWS for i in range(1, len(row))}


def decode(text):
    return "".join(TABLE.get(ch.upper(), ch) for ch in text)


def main():
    for line in sys.stdin:
        print(decode(line.rstrip("\n")))


if __name__ == "__main__":
    main()
