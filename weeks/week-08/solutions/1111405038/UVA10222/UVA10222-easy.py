import sys

# QWERTY 鍵盤各行（由左到右）
# 瘋狂的人打字時手向右偏 1 格，所以解碼要往左移 1 格
ROWS = ["`1234567890-=", "qwertyuiop[]\\", "asdfghjkl;'", "zxcvbnm,./"]

# 預先建立解碼對照表：加密字元（大寫）→ 原字元（大寫）
# row[i] 是加密字元，row[i-1] 是原字元
TABLE = {row[i].upper(): row[i - 1].upper() for row in ROWS for i in range(1, len(row))}


def decode(text):
    # 逐字元查表解碼；查不到（空白、換行等）直接保留
    return "".join(TABLE.get(ch.upper(), ch) for ch in text)


def main():
    # 逐行讀到 EOF，每行解碼後輸出
    for line in sys.stdin:
        print(decode(line.rstrip("\n")))


if __name__ == "__main__":
    main()
