"""
UVA 10190 - 自動傘 簡易版本
更簡潔易記的實現

核心邏輯：
1. 計算每把傘在 T 時間內覆蓋的左右邊界
2. 合併所有重疊區域
3. 計算總面積和降雨體積
"""


def solve(N, W, T, V, umbrellas):
    """
    計算總雨水體積
    
    參數：
        N: 傘數量
        W: 馬路寬度
        T: 統計時間
        V: 單位面積單位時間的降雨
        umbrellas: 傘的列表 [(初始位置x, 長度l, 速度v), ...]
    
    返回值：
        float: 雨水體積（精確到小數點後第二位）
    """
    
    # 計算每把傘的覆蓋區間
    intervals = []
    
    for x, l, v in umbrellas:
        # 傘的左端點在時間內的範圍
        if v >= 0:
            left_min = x
            left_max = x + v * T
        else:
            left_min = x + v * T
            left_max = x
        
        # 傘的右端點 = 左端點 + 長度
        right_min = left_min + l
        right_max = left_max + l
        
        # 考慮邊界限制 [0, W]
        left_min = max(0, left_min)
        right_max = min(W, right_max)
        
        # 有效區間：左 < 右
        if left_min < right_max:
            intervals.append((left_min, right_max))
    
    # 合併重疊區間
    if not intervals:
        return 0.0
    
    intervals.sort()
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            # 重疊，合併
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            # 不重疊，加入新區間
            merged.append((start, end))
    
    # 計算總覆蓋長度
    total_length = sum(end - start for start, end in merged)
    
    # 覆蓋面積 = 長度 × 寬度
    # 降雨體積 = 面積 × 降雨速率 × 時間
    total_volume = total_length * W * V * T
    
    return round(total_volume, 2)
