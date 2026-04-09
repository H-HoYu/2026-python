import sys


def main() -> None:
    """較容易記的版本：用「清單」來模擬所有可用的牛編號。

    重點觀念：
    - 題目給的是「前面有幾頭牛編號比自己小」，這是一種 inversion sequence。
    - 只要準備一個可用編號的清單 available = [1, 2, ..., N]，
      然後從最後一個位置往前處理，每次從 available.pop(smaller[pos]) 拿號碼即可。
    """

    # 一次把所有輸入讀進來並切開
    data = sys.stdin.read().strip().split()
    if not data:
        return

    it = iter(data)
    # 第 1 個數字是 N（乳牛總數）
    n = int(next(it))

    # smaller[pos]：第 pos 個位置這頭牛，前面有幾頭牛「編號比它小」
    smaller = [0] * (n + 1)
    for pos in range(2, n + 1):
        try:
            smaller[pos] = int(next(it))
        except StopIteration:
            # 正常不會發生，保險起見給 0
            smaller[pos] = 0

    # 可用的牛編號，初始為 [1, 2, ..., N]
    available = list(range(1, n + 1))

    # result[pos] = 站在第 pos 個位置的牛編號
    result = [0] * (n + 1)

    # 從「最後一個位置」開始往前還原：
    # smaller[pos] = k 表示：這頭牛在「目前還沒被用掉的編號」裡是第 k+1 小，
    # 所以直接從 available.pop(k) 取出該編號即可。
    for pos in range(n, 1, -1):
        k = smaller[pos]
        result[pos] = available.pop(k)

    # 迴圈結束後，available 剩下最後一個數字，就是第 1 個位置的牛
    if n >= 1:
        result[1] = available.pop(0)

    # 依序輸出每個位置的牛編號，每行一個
    out = "\n".join(str(result[pos]) for pos in range(1, n + 1))
    sys.stdout.write(out)


if __name__ == "__main__":
    main()
