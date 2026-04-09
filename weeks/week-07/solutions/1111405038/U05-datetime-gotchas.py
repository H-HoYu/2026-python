# U05. 日期時間的陷阱（3.12–3.15）
# ============================================================
# 本檔案涵蓋兩個常見陷阱：
#   1. timedelta 不支援「月份」參數，加減月份需自行處理跨月問題
#   2. datetime.strptime() 效能較差，格式固定時用手動解析更快
# ============================================================

import timeit
import calendar  # 提供 monthrange() 取得月份天數
from datetime import datetime, timedelta

# ============================================================
# 陷阱 1：timedelta 不支援「月份」（3.12）
# ============================================================
# timedelta 支援的單位：days、seconds、microseconds、
#   milliseconds、minutes、hours、weeks — 就是沒有 months！
#
# 原因：「1 個月」的天數不固定（可能是 28/29/30/31 天），
# 定義不明確，因此 Python 標準庫情愿不提供此功能。
# 常見替代方案：手動計算 / dateutil.relativedelta / arrow 等庫
# ============================================================
dt = datetime(2012, 9, 23)
try:
    dt + timedelta(months=1)  # type: ignore[call-arg]  months 不是有效參數
except TypeError as e:
    print(f"TypeError: {e}")  # 'months' is an invalid keyword argument


# 正確做法：手動實作「加一個月」逻輯
# 重點：需處理「日期超出目標月天數」的邊界情況（day clamp）
# 例：1 月 31 日 +1 月 → 2 月沒有 31 日，應設為 2 月最後一天
def add_one_month(dt: datetime) -> datetime:
    # 步驟 1：計算目標年與月
    year = dt.year
    month = dt.month + 1
    if month == 13:   # 月份超過 12 → 進位到明年 1 月
        year += 1
        month = 1

    # 步驟 2：取得目標月份的天數
    # calendar.monthrange(year, month) 回傳 (weekday_of_1st, total_days_in_month)
    # 下笪第一個元素用 _ 忽略，只取第二個（總天數）
    _, days_in_target_month = calendar.monthrange(year, month)

    # 步驟 3：將日期限定在目標月天數內（clamp）
    # 例：原日期為 31 但目標月只有 29 天 → day = min(31, 29) = 29
    day = min(dt.day, days_in_target_month)

    return dt.replace(year=year, month=month, day=day)


print(add_one_month(datetime(2012, 1, 31)))  # 2012-02-29（2012 是閏年，2 月有 29 天）
print(add_one_month(datetime(2012, 9, 23)))  # 2012-10-23（沒有跨月關題）

# ============================================================
# 陷阱 2：strptime 效能問題（3.15）
# ============================================================
# datetime.strptime(string, format) 內部每次呼叫都需要：
#   1. 解析 format 字串，建立格式解析器（使用內部缓存但仸有負擔）
#   2. 逗一匹配字元並提取數字
#   3. 建立 datetime 物件
#
# 手動解析的優勢：
#   格式固定時（如 ISO 8601 "YYYY-MM-DD"），
#   split('-') + int() 的操作成本証明比 strptime 快得多。
#
# 建議：格式固定配大量資料 → 手動解析；格式多構 / 不確定 → strptime
# ============================================================
# 測試料：2012 年每月 1–28 日（共 336 筆）
dates = [f"2012-{m:02d}-{d:02d}" for m in range(1, 13) for d in range(1, 29)]


def use_strptime(s: str) -> datetime:
    # 通用格式解析：每次呼叫都需解讀 "%Y-%m-%d" 格式字串
    return datetime.strptime(s, "%Y-%m-%d")


def use_manual(s: str) -> datetime:
    # 手動解析：直接 split 分割再轉型，简單且快
    y, m, d = s.split("-")
    return datetime(int(y), int(m), int(d))


assert use_strptime("2012-09-20") == use_manual("2012-09-20")  # 驗證兩種結果一致

t1 = timeit.timeit(lambda: [use_strptime(d) for d in dates], number=100)
t2 = timeit.timeit(lambda: [use_manual(d) for d in dates], number=100)
print(f"strptime: {t1:.3f}s  手動解析: {t2:.3f}s（快 {t1 / t2:.1f} 倍）")
# 預期手動解析速度約快 3–5 倍
