from __future__ import annotations

import heapq
import math
import sys
from collections import defaultdict


EPS = 1e-10
TWO_PI = 2.0 * math.pi
INF = 1e100


def cross(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx


def norm_angle(theta: float) -> float:
    theta %= TWO_PI
    if theta < 0:
        theta += TWO_PI
    return theta


def segment_intervals(segment: tuple[int, int, int, int]) -> list[tuple[float, float]]:
    """回傳線段在極角上的可見區間（拆成不跨 2pi 的形式）。"""
    sx, sy, ex, ey = segment
    a1 = norm_angle(math.atan2(sy, sx))
    a2 = norm_angle(math.atan2(ey, ex))
    diff = (a2 - a1) % TWO_PI

    if diff < EPS or abs(diff - TWO_PI) < EPS:
        return []

    if diff <= math.pi:
        left, right = a1, a1 + diff
    else:
        left, right = a2, a2 + (TWO_PI - diff)

    if right <= TWO_PI + EPS:
        return [(left, min(right, TWO_PI))]
    return [(left, TWO_PI), (0.0, right - TWO_PI)]


def distance_on_ray(segment: tuple[int, int, int, int], angle: float) -> float:
    """計算指定角度射線與線段相交時到原點的距離參數 t。"""
    sx, sy, ex, ey = segment
    dx = ex - sx
    dy = ey - sy
    rx = math.cos(angle)
    ry = math.sin(angle)

    denom = cross(rx, ry, dx, dy)
    if abs(denom) < EPS:
        return INF

    t_value = cross(sx, sy, dx, dy) / denom
    u_value = cross(sx, sy, rx, ry) / denom
    if t_value <= EPS:
        return INF
    if u_value < -EPS or u_value > 1.0 + EPS:
        return INF
    return t_value


def solve_case(segments: list[tuple[int, int, int, int]]) -> list[int]:
    """角度掃描：每段角度區間中最前面的鏡子可見。"""
    n = len(segments)
    visible = [0] * n

    adds: dict[float, list[int]] = defaultdict(list)
    removes: dict[float, list[int]] = defaultdict(list)
    event_angles = {0.0, TWO_PI}

    for i, seg in enumerate(segments):
        for left, right in segment_intervals(seg):
            if right - left < EPS:
                continue
            adds[left].append(i)
            removes[right].append(i)
            event_angles.add(left)
            event_angles.add(right)

    sorted_angles = sorted(event_angles)
    active = [False] * n
    heap: list[tuple[float, int, int]] = []
    version = [0] * n

    def push_segment(seg_id: int, angle: float) -> None:
        version[seg_id] += 1
        dist = distance_on_ray(segments[seg_id], angle)
        heapq.heappush(heap, (dist, seg_id, version[seg_id]))

    def clean_top(angle: float) -> None:
        while heap:
            dist, seg_id, stamp = heap[0]
            if (not active[seg_id]) or stamp != version[seg_id]:
                heapq.heappop(heap)
                continue

            current_dist = distance_on_ray(segments[seg_id], angle)
            if abs(current_dist - dist) > 1e-9:
                heapq.heappop(heap)
                heapq.heappush(heap, (current_dist, seg_id, stamp))
                continue
            break

    for idx in range(len(sorted_angles) - 1):
        angle = sorted_angles[idx]

        for seg_id in removes.get(angle, []):
            active[seg_id] = False
            version[seg_id] += 1

        probe = angle + 1e-7
        if probe >= TWO_PI:
            probe -= TWO_PI

        for seg_id in adds.get(angle, []):
            active[seg_id] = True
            push_segment(seg_id, probe)

        next_angle = sorted_angles[idx + 1]
        if next_angle - angle < EPS:
            continue

        mid = (angle + next_angle) * 0.5
        clean_top(mid)
        if heap:
            _, seg_id, _ = heap[0]
            visible[seg_id] = 1

    return visible


def parse_cases(values: list[int]) -> list[list[tuple[int, int, int, int]]]:
    cases: list[list[tuple[int, int, int, int]]] = []
    index = 0
    while index < len(values):
        n = values[index]
        index += 1
        if n <= 0:
            break
        case: list[tuple[int, int, int, int]] = []
        for _ in range(n):
            sx, sy, ex, ey = values[index : index + 4]
            index += 4
            case.append((sx, sy, ex, ey))
        cases.append(case)
    return cases


def main() -> None:
    raw = sys.stdin.read().strip()
    if not raw:
        return

    values = list(map(int, raw.split()))
    cases = parse_cases(values)
    outputs = []
    for case in cases:
        ans = solve_case(case)
        outputs.append(" ".join(map(str, ans)))
    print("\n".join(outputs))


if __name__ == "__main__":
    main()