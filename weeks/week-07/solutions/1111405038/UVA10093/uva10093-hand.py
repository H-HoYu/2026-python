import sys


def main() -> None:
    data = sys.stdin.read().split()
    ptr = 0
    N = int(data[ptr]); ptr += 1
    M = int(data[ptr]); ptr += 1

    forb = []
    for _ in range(N):
        row = data[ptr]; ptr += 1
        f = 0
        for j, ch in enumerate(row):
            if ch == 'H':
                f |= 1 << j
        forb.append(f)


    valid = []
    for m in range(1 << M):
        if not (m & (m << 1)) and not (m & (m << 2)):
            valid.append(m)

    V = len(valid)

    cnt = [bin(m).count('1') for m in valid]

    idx = {m: i for i, m in enumerate(valid)}


    NEG = -1
    dp = [[NEG] * V for _ in range(V)]


    zero_idx = idx[0]  
    for i, m in enumerate(valid):
        if not (m & forb[0]):
            dp[i][zero_idx] = cnt[i]

    for row in range(1, N):
        f = forb[row]
        new_dp = [[NEG] * V for _ in range(V)]

        for ci, cur in enumerate(valid):
            if cur & f:
                continue
            for ai in range(V):
                a = valid[ai]
                if cur & a:
                    continue
                for bi in range(V):  
                    if dp[ai][bi] == NEG:
                        continue
                    b = valid[bi]
                    if cur & b:                
                        continue
                    val = dp[ai][bi] + cnt[ci]
                    if val > new_dp[ci][ai]:
                        new_dp[ci][ai] = val

        dp = new_dp

    ans = 0
    for row in dp:
        for v in row:
            if v > ans:
                ans = v
    print(ans)


if __name__ == "__main__":
    main()
