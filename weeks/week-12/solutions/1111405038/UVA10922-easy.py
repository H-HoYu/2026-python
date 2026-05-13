import sys


def solve() -> None:
    for line in sys.stdin:
        x = line.strip()
        if x == "0":   # 以 0 作為輸入結束訊號
            break

        s = x          # 用字串保留原始數字（可能超過整數範圍）
        degree = 0

        # 反覆對各位數字加總，直到只剩一位數
        # 每做一次加總就累計深度 +1
        while True:
            s = str(sum(int(c) for c in s))   # 計算各位數字之和
            degree += 1
            if len(s) == 1:   # 已縮減至一位數，停止
                break

        # 最終一位數若為 9，原數為 9 的倍數，輸出深度
        if s == "9":
            print(f"9-degree of {x} is {degree}.")
        else:
            print(f"{x} is not a multiple of 9.")


if __name__ == "__main__":
    solve()
