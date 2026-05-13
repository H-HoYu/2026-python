import sys


def solve() -> None:
    for line in sys.stdin:
        x = line.strip()
        if x == "0":   # 以 0 作為輸入結束訊號
            break

        # Python 原生大整數可直接處理 1000 位以上的數字
        # 只需將字串轉為 int 再取餘數，無需手動實作交替加總
        if int(x) % 11 == 0:
            print(f"{x} is a multiple of 11.")
        else:
            print(f"{x} is not a multiple of 11.")


if __name__ == "__main__":
    solve()
