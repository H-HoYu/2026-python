import sys


def main():
    # 第一行是接下來要分析的文字行數。
    n = int(sys.stdin.readline())

    # 用字典記錄每個大寫英文字母出現的次數。
    # 例如 counts["A"] = 3 代表 A 在所有輸入中總共出現 3 次。
    counts = {}

    # 一行一行讀入，把每一行中的每個字元逐一檢查。
    # 題目規定大小寫要視為同一個字母，所以先把小寫轉成大寫。
    # 只有 A 到 Z 需要統計，空白、數字、符號都直接忽略。
    for _ in range(n):
        line = sys.stdin.readline()
        for ch in line:
            if "a" <= ch <= "z":
                # 利用 ASCII 編碼把小寫字母改成對應的大寫字母。
                ch = chr(ord(ch) - 32)
            if "A" <= ch <= "Z":
                # 如果這個字母還沒出現過，就從 0 開始累加。
                counts[ch] = counts.get(ch, 0) + 1

    # 把字典內容轉成 [(字母, 次數), ...] 的串列，後面才方便排序。
    items = list(counts.items())

    # 先照字母排序，目的是先把同次數時的先後順序排好。
    # 例如次數一樣時，A 要排在 B 前面。
    items.sort()

    # Python 的排序是穩定排序。
    # 所以第二次只要依次數由大到小排序，若次數相同，
    # 就會保留前一次已經排好的字母順序，剛好符合題目要求。
    items.sort(key=lambda item: item[1], reverse=True)

    # 依序輸出：字母 空白 次數
    for ch, count in items:
        print(ch, count)


if __name__ == "__main__":
    main()