# U06. 時區操作最佳實踐：UTC 優先（3.16）
# ============================================================
# 核心原則：程式內部所有時間一律用 UTC 儲存與計算，
#   只有在「輸出給使用者」時才轉換成本地時區。
#
# 為什麼？本地時間存在以下問題：
#   1. 夏令時（DST）：時鐘會跳躍（如 1:59 → 3:00），
#      在跳躍區間做加減會產生「不存在的時間」
#   2. 時區切換：國家/地區可能更改時區規則
#   3. UTC 永遠單調遞增，沒有以上問題
# ============================================================

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+ 內建時區資料庫（取代 pytz）

# 建立常用時區物件（可重複使用，避免重複建立）
utc = ZoneInfo("UTC")
central = ZoneInfo("America/Chicago")  # 美國中部時區（UTC-6 / 夏令時 UTC-5）

# ============================================================
# 陷阱示範：直接在本地時間做加減，夏令時邊界會出錯
# ============================================================
# 背景：美國中部時間 2013-03-10
#   凌晨 1:59 → 下一秒直接跳到 3:00（夏令時開始，時鐘往前撥 1 小時）
#   2:00 ~ 2:59 這段時間「不存在」
#
# 問題：若直接對帶時區的 datetime 做 timedelta 加法，
#   Python 只是在「時鐘數字」上加，不感知 DST 跳躍，
#   結果可能落在一個「現實中不存在」的時間點。
local_dt = datetime(2013, 3, 10, 1, 45, tzinfo=central)  # 夏令時前 15 分鐘
wrong = local_dt + timedelta(minutes=30)  # 直接加 30 分鐘 → 2:15（這個時間不存在！）
print(f"錯誤結果：{wrong}")  # 2:15（不存在的時間！）

# ============================================================
# 正確做法：先轉 UTC → 在 UTC 計算 → 再轉回本地時區
# ============================================================
# astimezone(utc)：將 aware datetime 轉換成 UTC 表示
# UTC 軸上沒有夏令時跳躍，加減保證正確
utc_dt = local_dt.astimezone(utc)          # 轉換成 UTC：07:45 UTC
correct = utc_dt + timedelta(minutes=30)   # UTC 加 30 分鐘 → 08:15 UTC
# 轉回中部時間：跨越 DST 邊界後已是夏令時（UTC-5），所以 08:15 UTC = 03:15 CDT
print(f"正確結果：{correct.astimezone(central)}")  # 3:15（正確跳過了不存在的 2:xx）

# ============================================================
# 最佳實踐流程：輸入 → UTC → 計算 → 輸出時轉本地
# ============================================================
# 步驟說明：
#   1. 從使用者輸入取得 naive datetime（無時區資訊）
#   2. replace(tzinfo=...) 標記輸入的時區（非轉換，只是貼上標籤）
#   3. astimezone(utc) 轉換成 UTC 儲存
#   4. 輸出時才用 astimezone(target_tz) 轉成目標時區
#
# 注意：replace() 與 astimezone() 的差異：
#   replace(tzinfo=tz)  → 強制設定時區標籤，不改變時鐘數字（假設輸入已是該時區）
#   astimezone(tz)      → 轉換時區，時鐘數字隨之改變（代表同一個時間點）
user_input = "2012-12-21 09:30:00"
naive = datetime.strptime(user_input, "%Y-%m-%d %H:%M:%S")  # naive：無時區資訊
aware = naive.replace(tzinfo=central).astimezone(utc)        # 標記為中部時間後轉 UTC
print(f"存 UTC：{aware}")
print(f"顯示台北：{aware.astimezone(ZoneInfo('Asia/Taipei'))}")  # 輸出時轉台北時區顯示
