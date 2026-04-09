import sys



STICKS = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]

FROM: dict[int, list[int]] = {}
for _d in range(10):
    FROM.setdefault(STICKS[_d], []).append(_d)


def calc(s: str) -> int:
    res, sign, i = 0, 1, 0
    while i < len(s):
        if s[i] in '+-':
            sign = 1 if s[i] == '+' else -1
            i += 1
        else:
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            res += sign * int(s[i:j])
            i = j
    return res


def ok(expr: str) -> bool:
    eq = expr.index('=')
    return calc(expr[:eq]) == calc(expr[eq + 1:])


def solve(expr: str) -> str | None:

    dpos = [i for i, c in enumerate(expr) if c.isdigit()]
    ch = list(expr)

    for i in range(len(dpos)):
        pi = dpos[i]
        di = int(ch[pi])
        si = STICKS[di]

        for nd in FROM.get(si, []):
            if nd == di:
                continue
            ch[pi] = str(nd)
            if ok(''.join(ch)):
                return ''.join(ch)
            ch[pi] = str(di)

        for nd_i in FROM.get(si - 1, []):
            ch[pi] = str(nd_i)
            for j in range(len(dpos)):
                if j == i:
                    continue
                pj = dpos[j]
                dj = int(expr[pj])
                for nd_j in FROM.get(STICKS[dj] + 1, []):
                    ch[pj] = str(nd_j)
                    if ok(''.join(ch)):
                        return ''.join(ch)
                    ch[pj] = str(dj)
            ch[pi] = str(di)

    return None


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        e = line.index('#')
        result = solve(line[:e])
        print((result + '#') if result else 'No')


if __name__ == '__main__':
    main()
