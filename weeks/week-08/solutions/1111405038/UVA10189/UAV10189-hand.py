def solve_minesweeper(grid):

    result = [row[:] for row in grid]
    rows, cols = len(grid), len(grid[0]) if grid else 0
    
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '.':
                count = sum(
                    1 for di, dj in directions
                    if 0 <= i + di < rows and 0 <= j + dj < cols
                    and grid[i + di][j + dj] == '*'
                )
                result[i][j] = str(count)
    
    return result


def solve(lines):

    results = []
    idx = 0
    case_num = 1
    
    while idx < len(lines):
        n, m = map(int, lines[idx].split())
        idx += 1
        

        if n == 0 and m == 0:
            break
        

        grid = [list(lines[idx + i]) for i in range(n)]
        idx += n
        
  
        solved = solve_minesweeper(grid)
        
  
        results.append(f"Field #{case_num}:")
        for row in solved:
            results.append(''.join(row))
        
        case_num += 1
    

    output = []
    for i, line in enumerate(results):
        if i > 0 and line.startswith("Field #"):
            output.append("")
        output.append(line)
    
    return '\n'.join(output)


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
