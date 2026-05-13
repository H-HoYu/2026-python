import sys


def solve() -> None:
    data = sys.stdin.read().split()
    idx = 0
    T = int(data[idx]); idx += 1
    out = []

    for _ in range(T):
        M, N, Q = int(data[idx]), int(data[idx+1]), int(data[idx+2])
        idx += 3
        grid = []
        for _ in range(M):
            grid.append(data[idx]); idx += 1

        out.append(f"{M} {N} {Q}")

        for _ in range(Q):
            r, c = int(data[idx]), int(data[idx+1])
            idx += 2
            ch = grid[r][c]
            best = 1
            half = 1
            while True:
                r0, r1 = r - half, r + half
                c0, c1 = c - half, c + half
                if r0 < 0 or r1 >= M or c0 < 0 or c1 >= N:
                    break
                if all(grid[i][j] == ch for i in range(r0, r1+1) for j in range(c0, c1+1)):
                    best = 2 * half + 1
                    half += 1
                else:
                    break
            out.append(str(best))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
