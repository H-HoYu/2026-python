import sys


def main() -> None:
    """使用 Fenwick Tree 還原乳牛排隊順序的版本。

    題目給的是：每個位置前面，有幾頭牛「編號比它小」。
    這可以視為一種 inversion sequence，我們用 BIT 從後往前還原出排列。
    """

    # 讀入全部輸入並切成 token
    data = sys.stdin.read().strip().split()
    if not data:
        return

    it = iter(data)
    # 第一個數字是牛的總數 N
    n = int(next(it))

    # smaller[pos] 表示：第 pos 個位置這頭牛，前面有幾頭牛「編號比它小」
    smaller = [0] * (n + 1)
    for pos in range(2, n + 1):
        try:
            smaller[pos] = int(next(it))
        except StopIteration:
            # 正常測資不會發生，保險起見給 0
            smaller[pos] = 0

    # Fenwick Tree / BIT：tree[i] 紀錄某一段區間內「還沒被用掉的編號個數」
    size = n
    tree = [0] * (size + 1)

    def bit_add(idx: int, delta: int) -> None:
        """在 BIT 上對位置 idx 加上 delta。"""
        while idx <= size:
            tree[idx] += delta
            idx += idx & -idx

    def find_kth(k: int) -> int:
        """在目前仍為可用的編號中，找到「第 k 小」的那個編號。"""
        idx = 0
        bitmask = 1 << (size.bit_length() - 1)
        while bitmask:
            t = idx + bitmask
            if t <= size and tree[t] < k:
                idx = t
                k -= tree[t]
            bitmask >>= 1
        return idx + 1

    # 一開始 1..N 所有編號都是「可用」的，各自標成 1
    for i in range(1, size + 1):
        bit_add(i, 1)

    # result[pos] = 站在第 pos 個位置的牛編號
    result = [0] * (n + 1)

    # 從最後一個位置往前還原：
    # smaller[pos] = k → 代表它在可用編號中應該拿到「第 k+1 小」的編號
    for pos in range(n, 1, -1):
        k = smaller[pos] + 1
        idx = find_kth(k)
        result[pos] = idx
        # 這個編號已經被使用，從 BIT 中扣掉
        bit_add(idx, -1)

    # 剩下最後一個還沒用掉的編號，就是第 1 個位置的牛
    if n >= 1:
        idx = find_kth(1)
        result[1] = idx

    out = "\n".join(str(result[pos]) for pos in range(1, n + 1))
    sys.stdout.write(out)


if __name__ == "__main__":
    main()
