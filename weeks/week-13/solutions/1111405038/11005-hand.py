import sys


def cost(number, base, costs):
    if number == 0:
        return costs[0]
    total = 0
    current = number
    while current > 0:
        total += costs[current % base]
        current //= base
    return total


def best_bases(number, costs):
    best_cost = None
    result = []
    for base in range(2, 37):
        current_cost = cost(number, base, costs)
        if best_cost is None or current_cost < best_cost:
            best_cost = current_cost
            result = [base]
        elif current_cost == best_cost:
            result.append(base)
    return result


def solve(values):
    index = 0
    cases = values[index]
    index += 1
    lines = []
    for case_no in range(1, cases + 1):
        costs = values[index:index + 36]
        index += 36
        query_count = values[index]
        index += 1
        lines.append(f"Case {case_no}:")
        for _ in range(query_count):
            number = values[index]
            index += 1
            bases = best_bases(number, costs)
            lines.append(f"Cheapest base(s) for number {number}: {' '.join(str(base) for base in bases)}")
        if case_no != cases:
            lines.append("")
    return "\n".join(lines)


def main():
    data = sys.stdin.read().strip()
    if not data:
        return
    values = list(map(int, data.split()))
    print(solve(values))


if __name__ == "__main__":
    main()