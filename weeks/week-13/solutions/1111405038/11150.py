from __future__ import annotations

import sys


INF = 10**9


def compress_stones(length: int, max_jump: int, stones: list[int]) -> tuple[list[int], int]:
    """把過大的空白區間壓縮，避免直接在 10^9 的數線上做 DP。"""
    limit = max_jump * (max_jump - 1)
    compressed_positions: list[int] = []
    current = 0
    previous = 0

    for stone in stones:
        gap = stone - previous
        current += min(gap, limit)
        compressed_positions.append(current)
        previous = stone

    compressed_length = current + min(length - previous, limit)
    return compressed_positions, compressed_length


def solve_case(length: int, min_jump: int, max_jump: int, stones: list[int]) -> int:
    """計算青蛙過河時最少需要踩到多少顆石子。"""
    stones.sort()

    # 當每次跳躍距離固定時，落點唯一，直接數會踩到的石子即可。
    if min_jump == max_jump:
        return sum(1 for stone in stones if stone % min_jump == 0)

    compressed_stones, compressed_length = compress_stones(length, max_jump, stones)
    stone_marks = [0] * (compressed_length + max_jump + 1)
    for position in compressed_stones:
        stone_marks[position] = 1

    dp = [INF] * (compressed_length + max_jump + 1)
    dp[0] = 0

    for position in range(1, compressed_length + max_jump + 1):
        extra_cost = stone_marks[position]
        for jump in range(min_jump, max_jump + 1):
            previous = position - jump
            if previous < 0:
                continue
            candidate = dp[previous] + extra_cost
            if candidate < dp[position]:
                dp[position] = candidate

    return min(dp[compressed_length : compressed_length + max_jump + 1])


def main() -> None:
    """讀入單筆測資並輸出答案。"""
    raw_text = sys.stdin.read().strip()
    if not raw_text:
        return

    values = list(map(int, raw_text.split()))
    length = values[0]
    min_jump, max_jump, stone_count = values[1:4]
    stones = values[4 : 4 + stone_count]
    print(solve_case(length, min_jump, max_jump, stones))


if __name__ == "__main__":
    main()