from __future__ import annotations

import sys


def convert_xyz(red: int, green: int, blue: int) -> tuple[float, float, float]:
    """依照題目提供的線性轉換公式，將 RGB 轉成 XYZ。"""
    x_value = 0.5149 * red + 0.3244 * green + 0.1607 * blue
    y_value = 0.2654 * red + 0.6704 * green + 0.0642 * blue
    z_value = 0.0248 * red + 0.1248 * green + 0.8504 * blue
    return x_value, y_value, z_value


def solve(values: list[int]) -> str:
    """解析輸入影像，逐像素輸出 XYZ，最後輸出平均亮度 Y。"""
    size = values[0]
    index = 1
    pixel_count = size * size
    total_y = 0.0
    lines: list[str] = []

    for _ in range(pixel_count):
        red = values[index]
        green = values[index + 1]
        blue = values[index + 2]
        index += 3

        x_value, y_value, z_value = convert_xyz(red, green, blue)
        total_y += y_value
        lines.append(f"{x_value:.4f} {y_value:.4f} {z_value:.4f}")

    average_y = total_y / pixel_count
    lines.append(f"The average of Y is {average_y:.4f}")
    return "\n".join(lines)


def main() -> None:
    """一次讀完所有整數，再交給主解法處理。"""
    raw_text = sys.stdin.read().strip()
    if not raw_text:
        return

    values = list(map(int, raw_text.split()))
    print(solve(values))


if __name__ == "__main__":
    main()