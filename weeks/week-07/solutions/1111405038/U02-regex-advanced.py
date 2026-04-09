# U02. 正則表達式進階技巧（2.4–2.6）
# ============================================================
# 本檔案涵蓋三個進階用法：
#   1. 預編譯（re.compile）提升重複使用時的效能
#   2. re.sub() 搭配回呼函數，實現動態替換邏輯
#   3. 大小寫感知替換：讓替換結果保持原字串的大小寫風格
# ============================================================

import re
import timeit
from calendar import month_abbr  # 月份縮寫對照表，month_abbr[1]='Jan'...month_abbr[12]='Dec'

# ============================================================
# 技巧 1：預編譯正則表達式提升效能（2.4）
# ============================================================
# re.compile(pattern) 將字串 pattern 編譯為 Pattern 物件，
# 內部會把正則轉換成有限自動機（NFA/DFA）並快取。
#
# 效能差異來源：
#   re.findall(pattern, text)   每次都需重新編譯（Python 有 _cache，
#                                 但 cache miss 時代價大）
#   datepat.findall(text)       直接使用已編譯的物件，省去編譯步驟
#
# 建議：pattern 若需重複使用（如迴圈中），一律預先 compile。
# ============================================================
text = "Today is 11/27/2012. PyCon starts 3/13/2013."
# 捕獲三組純數字，分別對應「月/日/年」
datepat = re.compile(r"(\d+)/(\d+)/(\d+)")


def using_module():
    # 每次呼叫都將 pattern 字串傳入 re 模組重新解析
    return re.findall(r"(\d+)/(\d+)/(\d+)", text)


def using_compiled():
    # 直接呼叫已編譯的 Pattern 物件，不重複解析
    return datepat.findall(text)


t1 = timeit.timeit(using_module, number=50_000)
t2 = timeit.timeit(using_compiled, number=50_000)
print(f"直接呼叫: {t1:.3f}s  預編譯: {t2:.3f}s")
# 預期預編譯版快約 10–30%


# ============================================================
# 技巧 2：re.sub() 搭配回呼函數實現動態替換（2.5）
# ============================================================
# re.sub(pattern, repl, string) 的 repl 除了可以是字串，
# 還可以是「可呼叫物件」（callable）。
#
# 當 repl 是函數時，每次找到一個符合的片段，
# Python 就會把對應的 Match 物件傳入函數，
# 函數的回傳值（字串）取代該片段。
#
# 使用時機：替換邏輯需要根據「比對到的內容」動態決定，
# 例如日期格式轉換、數字單位換算等。
#
# m.group(0) → 整個符合的字串（等同 m.group()）
# m.group(1) → 第 1 個括號的捕獲內容（本例：月份數字）
# m.group(2) → 第 2 個括號（日）
# m.group(3) → 第 3 個括號（年）
# ============================================================
def change_date(m: re.Match) -> str:
    # 將月份數字（如 "11"）轉為縮寫（如 "Nov"）
    # month_abbr[0] 是空字串，month_abbr[1..12] 才是月份
    mon_name = month_abbr[int(m.group(1))]
    # 重組為「日 月縮寫 年」格式
    return f"{m.group(2)} {mon_name} {m.group(3)}"


print(datepat.sub(change_date, text))
# 'Today is 27 Nov 2012. PyCon starts 13 Mar 2013.'


# ============================================================
# 技巧 3：大小寫感知替換——保持原字串的大小寫風格（2.6）
# ============================================================
# 問題情境：用 re.IGNORECASE 替換時，直接寫死替換字串會破壞原始大小寫。
#   例：「PYTHON」→「snake」（應為「SNAKE」才對）
#
# 解法：使用「閉包（closure）」回呼函數，讓替換邏輯感知原始文字的大小寫。
# matchcase(word) 回傳一個 replace 函數（閉包），
# 該函數在被 re.sub 呼叫時，會依據「比對到的原文」決定替換字的大小寫形式。
#
# 判斷邏輯（依優先順序）：
#   1. 原文全大寫 → 替換字全大寫（PYTHON → SNAKE）
#   2. 原文全小寫 → 替換字全小寫（python → snake）
#   3. 原文首字大寫 → 替換字首字大寫（Python → Snake）
#   4. 其餘情況   → 原樣回傳（不轉換）
# ============================================================
def matchcase(word: str):
    def replace(m: re.Match) -> str:
        t = m.group()       # 取出比對到的原始字串
        if t.isupper():
            return word.upper()        # 全大寫：PYTHON → SNAKE
        if t.islower():
            return word.lower()        # 全小寫：python → snake
        if t[0].isupper():
            return word.capitalize()   # 首字大寫：Python → Snake
        return word                    # 其他混合情況：維持替換字原樣

    return replace  # 回傳閉包，保存對 word 的引用


s = "UPPER PYTHON, lower python, Mixed Python"
# re.IGNORECASE 讓 pattern 不分大小寫都能比對；
# 回呼函數則負責依原文大小寫決定輸出格式。
print(re.sub("python", matchcase("snake"), s, flags=re.IGNORECASE))
# 'UPPER SNAKE, lower snake, Mixed Snake'
