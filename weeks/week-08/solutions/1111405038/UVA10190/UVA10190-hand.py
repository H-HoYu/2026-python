def solve(N, W, T, V, umbrellas):

    
    intervals = []
    
    for x, l, v in umbrellas:
        if v >= 0:
            left_min = x
            left_max = x + v * T
        else:
            left_min = x + v * T
            left_max = x
        
        right_min = left_min + l
        right_max = left_max + l
        
        left_min = max(0, left_min)
        right_max = min(W, right_max)
        
        if left_min < right_max:
            intervals.append((left_min, right_max))
    
    if not intervals:
        return 0.0
    
    intervals.sort()
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    
    total_length = sum(end - start for start, end in merged)
    
    total_volume = total_length * W * V * T
    
    return round(total_volume, 2)
