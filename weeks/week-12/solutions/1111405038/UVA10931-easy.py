import sys


def solve() -> None:
    for line in sys.stdin:
        value = int(line.strip())
        if value == 0:  # 0 代表輸入結束，不需處理
            break

        # 轉成不含前導零的二進位字串，並計算其中 1 的個數
        binary = bin(value)[2:]
        ones = binary.count("1")
        print(f"The parity of {binary} is {ones} (mod 2).")


if __name__ == "__main__":
    solve()
