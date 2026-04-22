import sys

MOD = 1_000_000_007


def parse_row(line):
    # 支援 "0101" 與 "0 1 0 1" 兩種輸入型式。
    s = line.strip()
    parts = s.split()
    return "".join(parts) if len(parts) > 1 else s


def count_ways(grid):
    n = len(grid)
    m = len(grid[0]) if n else 0

    # 狀態：(mask, left)
    # mask 第 c 位是此格的上方邊是否已存在；left 是左邊是否已有邊連進來。
    dp = {(0, 0): 1}

    for r in range(n):
        for c in range(m):
            nxt = {}
            open_cell = grid[r][c] == "1"

            for (mask, left), ways in dp.items():
                up = (mask >> c) & 1

                rights = (0, 1) if c + 1 < m else (0,)
                downs = (0, 1) if r + 1 < n else (0,)

                if not open_cell:
                    # 0 格（有插座）不可被蛇覆蓋，因此上下左右都不能有邊。
                    if up or left:
                        continue
                    nm = mask & ~(1 << c)
                    key = (nm, 0)
                    nxt[key] = (nxt.get(key, 0) + ways) % MOD
                    continue

                for right in rights:
                    for down in downs:
                        # 開放格必須剛好接兩條邊。
                        if left + up + right + down != 2:
                            continue
                        nm = (mask & ~(1 << c)) | (down << c)
                        key = (nm, right)
                        nxt[key] = (nxt.get(key, 0) + ways) % MOD

            dp = nxt

    return dp.get((0, 0), 0)


def solve(text):
    # 每筆輸出格式：Case i: ans
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    t = int(lines[0])
    i = 1
    out = []

    for case_id in range(1, t + 1):
        n, m = map(int, lines[i].split())
        i += 1

        grid = []
        for _ in range(n):
            grid.append(parse_row(lines[i]))
            i += 1

        out.append(f"Case {case_id}: {count_ways(grid)}")

    return "\n".join(out)


def main():
    data = sys.stdin.read()
    ans = solve(data)
    if ans:
        sys.stdout.write(ans)


if __name__ == "__main__":
    main()
