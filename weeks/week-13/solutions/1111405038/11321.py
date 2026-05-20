from __future__ import annotations

import sys


class DisjointSet:
    """並查集，用來追蹤陷阱群組覆蓋了哪些列。"""

    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size
        self.rows = [0] * size

    def find(self, node: int) -> int:
        """路徑壓縮找代表元。"""
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, left: int, right: int) -> int:
        """合併兩個集合，並把邊界資訊一起帶上。"""
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left == root_right:
            return root_left

        if self.rank[root_left] < self.rank[root_right]:
            root_left, root_right = root_right, root_left

        self.parent[root_right] = root_left
        self.rows[root_left] |= self.rows[root_right]
        if self.rank[root_left] == self.rank[root_right]:
            self.rank[root_left] += 1
        return root_left


def solve_case(rows: int, cols: int, operations: list[tuple[int, int]]) -> str:
    """逐步放陷阱，若某個連通塊把每一列都蓋住，就拒絕該點。"""
    total_cells = rows * cols
    dsu = DisjointSet(total_cells)
    blocked = [False] * total_cells
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1),
    ]
    output_lines: list[str] = []

    def index(row: int, col: int) -> int:
        return row * cols + col

    for row, col in operations:
        cell = index(row, col)
        merged_roots: set[int] = set()
        would_cover_rows = 1 << row
        for dr, dc in directions:
            nr = row + dr
            nc = col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor = index(nr, nc)
                if blocked[neighbor]:
                    root = dsu.find(neighbor)
                    if root not in merged_roots:
                        merged_roots.add(root)
                        would_cover_rows |= dsu.rows[root]

        if would_cover_rows == (1 << rows) - 1:
            blocked[cell] = False
            output_lines.append(">_<")
        else:
            blocked[cell] = True
            dsu.rows[cell] = 1 << row
            root = cell
            for neighbor_root in merged_roots:
                root = dsu.union(root, neighbor_root)
            output_lines.append("<(_ _)>")

    return "\n".join(output_lines)


def main() -> None:
    """讀入單組測資並輸出每次放陷阱的結果。"""
    raw_text = sys.stdin.read().strip()
    if not raw_text:
        return

    values = list(map(int, raw_text.split()))
    rows, cols, count = values[:3]
    operations = [(values[i], values[i + 1]) for i in range(3, 3 + 2 * count, 2)]
    print(solve_case(rows, cols, operations))


if __name__ == "__main__":
    main()