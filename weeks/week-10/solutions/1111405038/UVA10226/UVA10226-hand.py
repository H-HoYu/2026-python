import sys


def parse_cases(text):
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
    people = [chr(ord("A") + k) for k in range(n)]
    used = [False] * n
    cur = [""] * n
    out = []
    prev = None

    def emit(s):
        nonlocal prev

        if prev is None:
            out.append(s)
        else:
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

        for idx in range(n):
            if used[idx]:
                continue
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
        ans.extend(solve_one_case(n, forbid))
    return "\n".join(ans)


def main():
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
