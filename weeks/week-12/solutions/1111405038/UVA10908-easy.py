import sys


def solve() -> None:
    # 一次讀入全部資料，以空白分割（每行字元串不含空白，可安全 split）
    data = sys.stdin.read().split()
    idx = 0
    T = int(data[idx]); idx += 1   # 測試組數
    out = []

    for _ in range(T):
        M, N, Q = int(data[idx]), int(data[idx+1]), int(data[idx+2])
        idx += 3
        grid = []
        for _ in range(M):
            grid.append(data[idx]); idx += 1   # 讀入 M 行字元網格

        # 每組測試先輸出 "M N Q"
        out.append(f"{M} {N} {Q}")

        for _ in range(Q):
            r, c = int(data[idx]), int(data[idx+1])
            idx += 2
            ch = grid[r][c]   # 中心點字元，所有擴展格必須與其相同
            best = 1          # 最小邊長為 1（中心點本身）
            half = 1          # half 表示從中心往外延伸的格數，邊長 = 2*half+1

            while True:
                r0, r1 = r - half, r + half   # 正方形的上下邊界列
                c0, c1 = c - half, c + half   # 正方形的左右邊界欄

                # 超出網格邊界則停止擴展
                if r0 < 0 or r1 >= M or c0 < 0 or c1 >= N:
                    break

                # 檢查正方形內所有格是否與中心字元相同
                if all(grid[i][j] == ch for i in range(r0, r1+1) for j in range(c0, c1+1)):
                    best = 2 * half + 1   # 更新最大邊長
                    half += 1             # 繼續嘗試更大的正方形
                else:
                    break   # 出現不同字元，停止擴展

            out.append(str(best))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
