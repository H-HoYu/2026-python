"""
UVA 10189 - Minesweeper（踩地雷）
簡易版本 - 核心邏輯清晰易記

核心概念：
  對每個空白格子，數一下周圍8個方向有幾個地雷
"""


def solve_minesweeper(grid):
    """
    計算踩地雷網格
    空白格 '.' 改成周圍地雷數（0-8），地雷格 '*' 不變
    """
    # 複製網格
    result = [row[:] for row in grid]
    rows, cols = len(grid), len(grid[0]) if grid else 0
    
    # 8個方向：上下左右 + 4個斜角
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    # 遍歷每個格子
    for i in range(rows):
        for j in range(cols):
            # 如果是空白格子
            if grid[i][j] == '.':
                # 數周圍的地雷
                count = sum(
                    1 for di, dj in directions
                    if 0 <= i + di < rows and 0 <= j + dj < cols
                    and grid[i + di][j + dj] == '*'
                )
                result[i][j] = str(count)
    
    return result


def solve(lines):
    """
    處理完整輸入，輸出格式化結果
    """
    results = []
    idx = 0
    case_num = 1
    
    while idx < len(lines):
        # 讀網格大小
        n, m = map(int, lines[idx].split())
        idx += 1
        
        # 遇到 0 0 就結束
        if n == 0 and m == 0:
            break
        
        # 讀網格
        grid = [list(lines[idx + i]) for i in range(n)]
        idx += n
        
        # 解題
        solved = solve_minesweeper(grid)
        
        # 加到結果
        results.append(f"Field #{case_num}:")
        for row in solved:
            results.append(''.join(row))
        
        case_num += 1
    
    # 在多個案例之間加空行
    output = []
    for i, line in enumerate(results):
        if i > 0 and line.startswith("Field #"):
            output.append("")
        output.append(line)
    
    return '\n'.join(output)


# 測試用範例
if __name__ == "__main__":
    test_input = [
        "4 4",
        "*...",
        "....",
        ".*...",
        "....",
        "3 5",
        "**...",
        ".....",
        ".*...",
        "0 0"
    ]
    
    print(solve(test_input))
