import sys


def main():
    # 題目是一行一組測資，因此直接一路讀到輸入結束。
    for line in sys.stdin:
        # 每行會有兩個整數，代表要做加法的兩個數字。
        a, b = map(int, line.split())

        # 讀到 0 0 代表所有測資結束，不再處理後面的資料。
        if a == 0 and b == 0:
            break

        # carry 代表「上一位」是否有進位到目前這一位。
        # count 則是累計總共發生了幾次進位。
        carry = 0
        count = 0

        # 從個位數開始，逐位相加。
        # 只要兩個數其中之一還沒處理完，就要繼續算下去。
        while a > 0 or b > 0:
            # a % 10 取出個位數，b % 10 也取出個位數，
            # 再加上前一位可能留下來的進位 carry。
            total = a % 10 + b % 10 + carry

            # 如果這一位相加結果大於等於 10，就會產生新的進位。
            if total >= 10:
                carry = 1
                count += 1
            else:
                # 沒有進位的話，下一位就不需要多加 1。
                carry = 0

            # 去掉目前已經處理完的個位數，往更高位繼續算。
            a //= 10
            b //= 10

        # 依照題目要求輸出固定格式。
        # 0 次進位、1 次進位、2 次以上進位的句子都不一樣。
        if count == 0:
            print("No carry operation.")
        elif count == 1:
            print("1 carry operation.")
        else:
            print(f"{count} carry operations.")


if __name__ == "__main__":
    main()