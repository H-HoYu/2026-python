from __future__ import annotations

import sys


def 計算某進位的成本(數字: int, 進位: int, 成本表: list[int]) -> int:
    """把十進位整數轉成指定進位後，累加每一位的印刷成本。"""
    if 數字 == 0:
        return 成本表[0]

    總成本 = 0
    目前數字 = 數字

    # 反覆取餘數，就能依序取得此進位表示下的每一位數字。
    while 目前數字 > 0:
        目前位數 = 目前數字 % 進位
        總成本 += 成本表[目前位數]
        目前數字 //= 進位

    return 總成本


def 找出最便宜進位(數字: int, 成本表: list[int]) -> list[int]:
    """枚舉 2 到 36 進位，保留所有最低成本的答案。"""
    最低成本 = None
    最佳進位: list[int] = []

    for 進位 in range(2, 37):
        目前成本 = 計算某進位的成本(數字, 進位, 成本表)

        # 第一次計算到答案，或找到更便宜的進位時，就更新最佳答案。
        if 最低成本 is None or 目前成本 < 最低成本:
            最低成本 = 目前成本
            最佳進位 = [進位]
        elif 目前成本 == 最低成本:
            最佳進位.append(進位)

    return 最佳進位


def 主程式(所有數字: list[int]) -> str:
    """依照題目的整數輸入格式逐段解析並組裝輸出。"""
    位置 = 0
    測試組數 = 所有數字[位置]
    位置 += 1
    輸出行: list[str] = []

    for 組別 in range(1, 測試組數 + 1):
        # 每組測資固定先給 36 個字元成本。
        成本表 = 所有數字[位置 : 位置 + 36]
        位置 += 36

        查詢數量 = 所有數字[位置]
        位置 += 1

        輸出行.append(f"Case {組別}:")

        for _ in range(查詢數量):
            查詢數字 = 所有數字[位置]
            位置 += 1
            最佳進位 = 找出最便宜進位(查詢數字, 成本表)
            進位文字 = " ".join(str(進位) for 進位 in 最佳進位)
            輸出行.append(f"Cheapest base(s) for number {查詢數字}: {進位文字}")

        # 題目要求不同測資之間要空一行。
        if 組別 != 測試組數:
            輸出行.append("")

    return "\n".join(輸出行)


def main() -> None:
    """把標準輸入全部讀進來，切成整數後交給主流程處理。"""
    文字 = sys.stdin.read().strip()
    if not 文字:
        return

    所有數字 = list(map(int, 文字.split()))
    print(主程式(所有數字))


if __name__ == "__main__":
    main()