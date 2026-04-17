import sys


# 一次把整份輸入資料讀進來，並全部轉成整數。
# 這種寫法很適合競程題，因為可以用 index 依序取值，
# 不需要一直呼叫 input()。
data = list(map(int, sys.stdin.read().split()))

if data:
    # n 代表函數數量，q 代表操作次數。
    n = data[0]
    q = data[1]

    # index 用來記錄目前讀到輸入串列的哪個位置。
    index = 2

    # tree 只記錄「減函數個數的奇偶性」。
    # 0 代表偶數個減函數，1 代表奇數個減函數。
    # 題目問的是複合函數最後是增還是減，
    # 本質上只和區間內「減函數的數量是奇數還是偶數」有關：
    # - 偶數個減函數合成後會變回增函數，輸出 0
    # - 奇數個減函數合成後會是減函數，輸出 1
    # 所以我們完全不需要知道確切有幾個，只要知道奇偶性即可。
    tree = [0] * (n + 1)

    # answers 用來收集所有查詢操作的輸出答案。
    answers = []

    def toggle(position: int) -> None:
        # 這是一個 Fenwick Tree(Binary Indexed Tree) 的單點更新。
        # 由於我們只記奇偶性，因此翻轉一個位置時，
        # 只要把經過的 Fenwick Tree 節點做 xor 1 即可。
        # 這比記錄完整數量更直觀，也更貼近題目本質。
        while position <= n:
            tree[position] ^= 1
            position += position & -position

    def prefix_xor(position: int) -> int:
        # 取得前綴區間 [1..position] 內的奇偶性。
        # 回傳 0 代表目前這段區間內減函數數量為偶數，
        # 回傳 1 代表目前這段區間內減函數數量為奇數。
        result = 0
        while position > 0:
            result ^= tree[position]
            position -= position & -position
        return result

    for _ in range(q):
        # 每筆操作第一個數字是 command：
        # 1 表示翻轉某一個函數的增減性
        # 2 表示查詢某個區間合成後是增還是減
        command = data[index]
        index += 1

        if command == 1:
            # 翻轉第 position 個函數。
            # 因為增 <-> 減 就是奇偶狀態切換一次，
            # 所以直接呼叫 toggle() 即可。
            position = data[index]
            index += 1
            toggle(position)
        else:
            # 查詢區間 [left, right] 的答案。
            # Fenwick Tree 能先求出 [1..right] 的奇偶性，
            # 再 xor 掉 [1..left-1]，就得到 [left..right] 的奇偶性。
            # 若結果是 0，代表複合函數為增函數；
            # 若結果是 1，代表複合函數為減函數。
            left = data[index]
            right = data[index + 1]
            index += 2
            answers.append(str(prefix_xor(right) ^ prefix_xor(left - 1)))

    # 題目要求每個查詢答案各輸出一行，所以用換行字元串接。
    sys.stdout.write("\n".join(answers))