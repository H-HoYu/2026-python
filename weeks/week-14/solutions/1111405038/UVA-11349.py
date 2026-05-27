"""UVA 11349 - Symmetric Matrix
一般解題版本
"""

import sys


def is_symmetric_matrix(matrix):
    """檢查矩陣是否符合題目的對稱定義。"""
    n = len(matrix)

    # 先檢查所有元素是否非負，且同時檢查中心對稱
    for i in range(n):
        for j in range(n):
            if matrix[i][j] < 0:
                return False
            if matrix[i][j] != matrix[n - 1 - i][n - 1 - j]:
                return False

    return True


def solve(data):
    lines = data.strip().splitlines()
    t = int(lines[0].strip())
    idx = 1
    ans = []

    for case_no in range(1, t + 1):
        # 輸入格式為 "N = n"，取出等號右側的 n
        n = int(lines[idx].split("=")[1].strip())
        idx += 1

        matrix = []
        for _ in range(n):
            matrix.append(list(map(int, lines[idx].split())))
            idx += 1

        if is_symmetric_matrix(matrix):
            ans.append(f"Test #{case_no}: Symmetric.")
        else:
            ans.append(f"Test #{case_no}: Non-symmetric.")

    return "\n".join(ans)


if __name__ == "__main__":
    input_data = sys.stdin.read()
    print(solve(input_data))
