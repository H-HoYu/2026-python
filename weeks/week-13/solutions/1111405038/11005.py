from __future__ import annotations

import sys


def representation_cost(number: int, base: int, costs: list[int]) -> int:
    """計算 number 在指定進位表示時的總印刷成本。"""
    if number == 0:
        return costs[0]

    total_cost = 0
    current = number
    while current > 0:
        digit = current % base
        total_cost += costs[digit]
        current //= base
    return total_cost


def cheapest_bases(number: int, costs: list[int]) -> list[int]:
    """列舉 2 到 36 進位，找出所有最低成本的進位。"""
    best_cost = None
    best = []

    for base in range(2, 37):
        current_cost = representation_cost(number, base, costs)
        if best_cost is None or current_cost < best_cost:
            best_cost = current_cost
            best = [base]
        elif current_cost == best_cost:
            best.append(base)

    return best


def solve(data: list[int]) -> str:
    """依照 UVA 輸入格式解析資料並產生答案。"""
    index = 0
    test_cases = data[index]
    index += 1

    output_lines: list[str] = []
    for case_number in range(1, test_cases + 1):
        costs = data[index : index + 36]
        index += 36

        query_count = data[index]
        index += 1

        output_lines.append(f"Case {case_number}:")
        for _ in range(query_count):
            number = data[index]
            index += 1
            bases = cheapest_bases(number, costs)
            bases_text = " ".join(str(base) for base in bases)
            output_lines.append(f"Cheapest base(s) for number {number}: {bases_text}")

        if case_number != test_cases:
            output_lines.append("")

    return "\n".join(output_lines)


def main() -> None:
    """從標準輸入讀入所有整數後直接求解。"""
    raw_text = sys.stdin.read().strip()
    if not raw_text:
        return

    numbers = list(map(int, raw_text.split()))
    print(solve(numbers))


if __name__ == "__main__":
    main()