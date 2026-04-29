# UVA10226 優化對比分析

---

## 檔案對照

| 項目 | 原始版 (`UVA10226-easy.py`) | 優化版 (`UVA10226-optimized.py`) |
|------|----------------------------|----------------------------------|
| 禁止位置資料結構 | `set` | `list[list[bool]]`（2D布林表） |
| `used` 陣列型別 | `list[bool]` | `bytearray` |
| 差異輸出前綴計算 | O(n) while 迴圈 | O(1) 變動深度追蹤 |
| 人名列表 | 每筆測資重建 | 模組層級預先計算 |
| 架構 | 兩階段（先 parse → 再 solve） | 單階段邊解析邊求解 |
| 遞迴深度保護 | ✗ | ✓ `sys.setrecursionlimit` |

---

## 原始版三大缺點

### 缺點① ── 禁止位置使用 `set`，有雜湊開銷

```python
# easy.py
bad = set()
for x in row:
    if x == 0:
        break
    bad.add(x)
forbid.append(bad)

# DFS 內每次做：
if place in forbid[idx]:   # ← 雜湊計算 + 桶查找，常數因子大
```

**問題**：`set` 的 `__contains__` 須計算雜湊值、處理碰撞，對整數（1 ~ n）這類小範圍資料，直接用布林陣列索引更快。

**優化版改法**：
```python
# optimized.py
allowed = [[True] * (n + 1) for _ in range(n)]
# ...
allowed[idx][x] = False

# DFS 內：
if not used[idx] and a_pos[idx][place]:   # ← 純陣列索引，O(1) 無雜湊
```

---

### 缺點② ── 差異輸出需 O(n) 逐字元掃描

```python
# easy.py – emit() 函式
p = 0
while p < n and s[p] == prev[p]:   # ← 最壞 O(n) 逐字元比對
    p += 1
out.append(s[p:])
prev = s                            # ← 還需保存整個字串
```

**問題**：每次產生一筆排列，都要從頭掃描與上一筆的共同前綴，最壞需比較 n 個字元。當 n 大或合法排列數量多時，累積時間顯著。

**優化版改法**：在 DFS **同一層第二次嘗試不同選項**時主動記錄「最淺變動深度」：

```python
# optimized.py – dfs() 內
first_try = True
for idx in range(n):
    if not used[idx] and a_pos[idx][place]:
        if not first_try and pos < state[0]:
            state[0] = pos          # ← O(1)，只做一次比較+賦值
        ...
        first_try = False

# emit 時：
out.append(s[state[0]:])           # ← 直接切片，不需掃描
state[0] = n                       # ← 重置
```

**正確性說明**：DFS 在 `pos` 層換下一個人時，從 `pos` 開始之後的字元全部改變；多層回溯後，最淺的換人位置就是真正的第一個差異點。

---

### 缺點③ ── 兩階段架構與重複物件建立

```python
# easy.py – 兩個獨立函式，parse 完把所有 case 存成 list 再 solve
def parse_cases(text):   # 先全部解析
    ...
    cases.append((n, forbid))     # ← 整個 forbid 列表存進 memory

def solve(text):
    for n, forbid in parse_cases(text):   # 再逐一求解
        ans.extend(solve_one_case(n, forbid))
```

以及每筆測資都重建人名列表：
```python
people = [chr(ord("A") + k) for k in range(n)]   # ← 每次 O(n) 建立
```

`list[bool]` 也比 `bytearray` 佔用更多記憶體（`bool` 物件 vs 單一 byte）。

**優化版改法**：
- 模組層級預計算 `_PEOPLE`（全部 26 個字母），每次只做 O(1) 切片。
- 使用 `bytearray` 取代 `list[bool]`（記憶體減少 ~8 倍，索引速度更快）。
- 單一函式邊解析邊求解，避免中間結果佔用記憶體。

---

## 次要缺點（原始版）

| 問題 | 說明 |
|------|------|
| 無 `sys.setrecursionlimit` | n 稍大時可能拋出 `RecursionError` |
| `list(map(int, ...))` | 建立中間 list 物件（`map` 惰性求值即可） |
| `nonlocal prev` 在 `emit` 中 | 增加閉包查找層次，程式碼可讀性稍差 |
| `used[idx] = True/False` | bool 賦值比 bytearray `1/0` 慢 |

---

## 時間複雜度對比

演算法核心仍是 DFS 全排列，複雜度無法突破 O(n!)。  
優化的是**每個節點的常數成本**：

```
原始版每個 DFS 節點：
  set.__contains__  → O(1) 但常數 ~3–5 ns（含雜湊）
  emit 中的 while   → O(n)（僅葉節點，但葉節點數 = 合法排列數）

優化版每個 DFS 節點：
  list index        → O(1)，常數 ~0.5–1 ns
  change_depth 更新 → O(1)，一次比較+賦值
  emit 切片         → O(n–p)，但 p 通常 > 0，平均比掃描短
```

---

## 仍存在的限制（優化版亦同）

1. **遞迴 DFS**：Python 函式呼叫本身有開銷，若需進一步加速可改為迭代式（itertools 或手動堆疊），但程式碼複雜度大增。
2. **輸出仍在記憶體中收集**：`out` list 最後 `'\n'.join(out)` 會建立一個大字串；如輸出極大，可改為逐行 `sys.stdout.write`。
3. **單執行緒**：Python GIL 限制，無法多核並行（對競程題影響不大）。
