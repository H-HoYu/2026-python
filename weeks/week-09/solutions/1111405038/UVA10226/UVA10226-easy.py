import sys


def parse_cases(text):
    # 讀到 EOF，忽略空行，整理成 (人數, 每個人不能站的位置集合)。
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    i = 0
    cases = []

    while i < len(lines):
        n = int(lines[i])
        i += 1

        forbid = []
        for _ in range(n):
            row = list(map(int, lines[i].split()))
            i += 1

            bad = set()
            for x in row:
                if x == 0:
                    break
                bad.add(x)
            forbid.append(bad)

        cases.append((n, forbid))

    return cases


def solve_one_case(n, forbid):
    # people[idx] 代表第 idx 個人（A, B, C...）。
    people = [chr(ord("A") + k) for k in range(n)]
    used = [False] * n
    cur = [""] * n
    out = []
    prev = None

    def emit(s):
        nonlocal prev

        # 第一筆輸出完整字串，後續只輸出和前一筆不同的尾巴。
        if prev is None:
            out.append(s)
        else:
            # p 是和上一筆答案的最長共同前綴長度。
            p = 0
            while p < n and s[p] == prev[p]:
                p += 1
            out.append(s[p:])
        prev = s

    def dfs(pos):
        if pos == n:
            emit("".join(cur))
            return

        place = pos + 1

        # 從 A 到 ... 依序嘗試，天然符合字典序。
        for idx in range(n):
            if used[idx]:
                continue
            # 第 idx 個人不允許站在 place，就不能放。
            if place in forbid[idx]:
                continue

            used[idx] = True
            cur[pos] = people[idx]
            dfs(pos + 1)
            used[idx] = False

    dfs(0)
    return out


def solve(text):
    ans = []
    for n, forbid in parse_cases(text):
        # 多筆測資直接接續輸出，符合本題格式。
        ans.extend(solve_one_case(n, forbid))
    return "\n".join(ans)


def main():
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
