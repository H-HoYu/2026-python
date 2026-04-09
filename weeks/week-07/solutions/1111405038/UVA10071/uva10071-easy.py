import sys
from collections import Counter


def main() -> None:
    """UVA 10071 的「好記版本」：用拆成兩邊三個數的方式統計。

    題目：
        給一個整數集合 S，要求六元組 (a, b, c, d, e, f) 的個數，
        使得 a + b + c + d + e = f，且六個值都來自 S（可重複）。

    觀念：
        把等式改寫成「三個數等於三個數」：
            a + b + c = f - d - e
        這樣就可以：
        1) 先把所有 a + b + c 的結果算出來，記錄每個和出現幾次。
        2) 再枚舉所有 (d, e, f)，算出 r = f - d - e，
           只要看看「有多少組 (a, b, c) 的和剛好等於 r」，
           全部加起來就是答案。

    口訣：
        「左三個加起來，右三個變形，
          左邊先數完，右邊來查表。」
    """

    data = sys.stdin.read().strip().split()
    if not data:
        return

    it = iter(data)
    # 第一個數字是集合大小 N
    n = int(next(it))

    # 讀入 S 的元素（互不重複，但這裡不影響演算法）
    nums = [int(next(it)) for _ in range(n)]

    # 第一步：統計所有 a + b + c 的結果
    # left_count[sum_value] = 「有幾種 (a, b, c) 可以湊出這個 sum_value」
    left_count: Counter[int] = Counter()

    for i in range(n):
        a = nums[i]
        for j in range(n):
            b = nums[j]
            for k in range(n):
                c = nums[k]
                s = a + b + c
                left_count[s] += 1

    # 第二步：枚舉所有 (d, e, f)，查表累加答案
    # 對於每個 (d, e, f)，把等式 a + b + c + d + e = f 改寫成：
    #   a + b + c = f - d - e
    # r = f - d - e
    # 只要把 left_count[r] 加進答案，就代表所有對應的 (a, b, c) 組合。
    total = 0

    for i in range(n):
        d = nums[i]
        for j in range(n):
            e = nums[j]
            for k in range(n):
                f_val = nums[k]
                r = f_val - d - e
                total += left_count.get(r, 0)

    # 最後印出統計到的六元組總數
    sys.stdout.write(str(total) + "\n")


if __name__ == "__main__":
    main()
