import sys
from collections import Counter


def main() -> None:
    """計算滿足 a + b + c + d + e = f 的六元組個數。

    題目：給定一個整數集合 S，要數出所有 (a, b, c, d, e, f) ∈ S^6，
    且滿足 a + b + c + d + e = f 的組數（元素可重複使用）。

    解法概念（拆成 3 + 3）：
    - 將等式改寫為 a + b + c = f - d - e。
    - 左邊：枚舉所有 (a, b, c) 計算其和，記錄在 left_sum_counter 中。
    - 右邊：枚舉所有 (d, e, f)，計算 r = f - d - e，
      每次把 left_sum_counter[r] 累加進答案。
    如此總複雜度約為 O(N^3)，在 N ≤ 100 時可以接受。
    """

    data = sys.stdin.read().strip().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))

    # 讀入集合 S 的元素，題目保證互不重複
    nums = [int(next(it)) for _ in range(n)]

    # left_sum_counter[sum] = 能湊出該 sum 的三元組 (a, b, c) 的個數
    left_sum_counter: Counter[int] = Counter()

    # 三重迴圈列舉所有 (a, b, c)
    for i in range(n):
        a = nums[i]
        for j in range(n):
            b = nums[j]
            for k in range(n):
                c = nums[k]
                s = a + b + c
                left_sum_counter[s] += 1

    # 接著列舉所有 (d, e, f)，計算 r = f - d - e，
    # 對於每個 r，加上 left_sum_counter[r] 即為對應的六元組數量。
    total = 0
    for i in range(n):
        d = nums[i]
        for j in range(n):
            e = nums[j]
            for k in range(n):
                f_val = nums[k]
                r = f_val - d - e
                total += left_sum_counter.get(r, 0)

    # 輸出總組數
    sys.stdout.write(str(total) + "\n")


if __name__ == "__main__":
    main()
