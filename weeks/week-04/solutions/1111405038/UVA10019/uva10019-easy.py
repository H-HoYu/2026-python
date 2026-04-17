import sys


def main():
    # 一行一行讀到檔案結束為止。
    for line in sys.stdin:
        parts = line.split()

        # 如果這行不是剛好兩個數字，就跳過。
        if len(parts) != 2:
            continue

        a = int(parts[0])
        b = int(parts[1])

        # 題目要輸出正差值，所以直接取絕對值。
        print(abs(a - b))


if __name__ == "__main__":
    main()