import sys


def solve() -> None:
    # 一次讀入全部資料，依空白分割成 token 列表
    data = sys.stdin.read().strip().split()
    if not data:
        return

    count = int(data[0])   # 第一個 token 是測試組數
    index = 1
    results = []

    for _ in range(count):
        total = int(data[index])       # S：兩隊得分之和
        diff  = int(data[index + 1])   # D：兩隊得分之差（絕對值）
        index += 2

        # 無解條件：
        #   1. S < D（較小分會是負數）
        #   2. (S + D) 為奇數（無法整除，不是整數解）
        if total < diff or (total + diff) % 2 != 0:
            results.append("impossible")
            continue

        big   = (total + diff) // 2   # 較高分 = (S + D) / 2
        small = (total - diff) // 2   # 較低分 = (S - D) / 2

        # 再次確認較低分非負（理論上前面已過濾，保險起見）
        if small < 0:
            results.append("impossible")
        else:
            results.append(f"{big} {small}")   # 較大的先輸出

    sys.stdout.write("\n".join(results))


if __name__ == "__main__":
    solve()