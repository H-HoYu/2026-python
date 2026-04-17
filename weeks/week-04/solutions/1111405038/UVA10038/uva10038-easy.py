import sys


def main():
    # 題目沒有先給測資筆數，所以直接一路讀到 EOF。
    for line in sys.stdin:
        # 每一行的第一個數字是 n，後面接著 n 個整數。
        nums = list(map(int, line.split()))
        if not nums:
            continue

        # n 代表這個序列有幾個數字。
        n = nums[0]

        # 真正的數列內容放在後面。
        arr = nums[1:]

        # 用集合收集所有相鄰兩數差的絕對值。
        # 使用集合的好處是可以自動去掉重複值，方便最後直接比較。
        diffs = set()
        for i in range(1, n):
            # 相鄰兩數的差要取絕對值，因為題目不分正負。
            diffs.add(abs(arr[i] - arr[i - 1]))

        # 如果這個序列是 jolly jumper，
        # 那麼差值集合必須剛好等於 1 到 n-1。
        # 例如 n=4 時，就必須剛好出現 {1, 2, 3}。
        if diffs == set(range(1, n)):
            print("Jolly")
        else:
            print("Not jolly")


if __name__ == "__main__":
    main()