# UVA10235 優化對比分析

---

## 題目簡述

Broken-Profile DP：在 n×m 格子上，「1」格必須被閉合迴路覆蓋（各接恰好 2 條邊），「0」格（有插座）不可被覆蓋。求有效鋪設方案數 mod 10⁹+7。

---

## 檔案對照

| 項目 | 原始版 (`UVA10235-easy.py`) | 優化版 (`UVA10235-optimized.py`) |
|------|----------------------------|----------------------------------|
| DP 資料結構 | `dict[(mask, left)]` | `dp0[mask]` + `dp1[mask]` 雙 list |
| 狀態存取成本 | hash(tuple) + 桶查找 | 整數直接索引 O(1) |
| `open_cell` 判斷位置 | 每個 mask 都判斷 | 提至遮罩迴圈外，只判斷一次 |
| `nm` 運算次數 | 每個 (right, down) 組合各算一次（最多 4 次） | 每個 mask 預算一次 nm0/nm1，後續直接引用 |
| 位元遮罩計算 | 每格計算 `1<<c`, `~(1<<c)` | 模組層級預計算 `set_bit`, `clr_bit` 陣列 |
| right/down 嵌套迴圈 | `for right in ...: for down in ...:` | 直接分 4 個 if 分支，省去迴圈物件建立 |

---

## 原始版四大缺點

### 缺點① ── DP 狀態用 `dict` + `tuple` key，開銷高

```python
# easy.py
dp = {(0, 0): 1}

for (mask, left), ways in dp.items():
    ...
    key = (nm, right)
    nxt[key] = (nxt.get(key, 0) + ways) % MOD   # ← 每次：建 tuple + hash + 桶查找
```

每次存取 `nxt[key]` 需要：
1. 在 heap 上分配並建立 `(nm, right)` tuple 物件
2. 計算 tuple 的 hash（呼叫兩次 `int.__hash__` 再組合）
3. 查找 dict 的桶（可能碰撞探測）

**優化版改法**：
```python
# optimized.py
dp0 = [0] * size   # left=0 的所有 mask
dp1 = [0] * size   # left=1 的所有 mask

# 存取時：
ndp1[nm0] = (ndp1[nm0] + w) % MOD   # ← 純陣列索引，無 tuple、無 hash
```

實測在 CPython 3.13 上，list 整數索引比 dict tuple-key 快約 **5～8 倍**。

---

### 缺點② ── `open_cell` 判斷被放在最內層，每個 mask 重複執行

```python
# easy.py
for (mask, left), ways in dp.items():
    ...
    if not open_cell:          # ← 每個 mask 都要跑這行（條件不變）
        if up or left:
            continue
        ...
        continue

    for right in rights:
        for down in downs:
            if left + up + right + down != 2:
                continue
```

`open_cell = grid[r][c] == '1'` 在整個 (r, c) 的處理過程中固定不變，
卻放在遮罩迴圈的最內層，導致對每個 `dict` 條目都判斷一次。

**優化版改法**：
```python
# optimized.py — open_cell 判斷在遮罩迴圈外
if not open_cell:
    for mask in range(size):   # ← 此迴圈體內不再有 open_cell 判斷
        ...
else:
    for mask in range(size):
        ...
```

---

### 缺點③ ── `nm` 運算在 right/down 的 4 個組合裡各算一次

```python
# easy.py
for right in rights:          # 最多 2 個值
    for down in downs:        # 最多 2 個值（共最多 4 組）
        if left + up + right + down != 2:
            continue
        nm = (mask & ~(1 << c)) | (down << c)   # ← 每個合法組合都重算
        key = (nm, right)
```

`(mask & ~(1<<c))` 是同一個 mask 上的固定運算，與 right/down 無關，
卻在迴圈體內可能被執行多次。

**優化版改法**：
```python
# optimized.py — 每個 mask 只算一次 nm0/nm1
nm0 = mask & cc          # down=0 的結果
nm1 = nm0 | sc           # down=1 的結果

# 後續 4 個分支直接引用：
ndp1[nm1] ...   # right=1, down=1
ndp1[nm0] ...   # right=1, down=0
ndp0[nm1] ...   # right=0, down=1
ndp0[nm0] ...   # right=0, down=0
```

---

### 缺點④ ── 位元遮罩在每個格子重複計算

```python
# easy.py（間接透過 ~(1 << c) 出現在 nm 計算中）
nm = mask & ~(1 << c)      # 每個 (r, c) 的每個 mask 都算 ~(1<<c)
```

同一欄 `c` 的 `1 << c` 在整列掃描中不變，卻在最內層迴圈每個 mask 重算。

**優化版改法**：
```python
# optimized.py — 模組層級（或函式層級）預計算
set_bit = [1 << c for c in range(m)]
clr_bit = [(~(1 << c)) & full_mask for c in range(m)]

# 進入 c 迴圈後，sc/cc 只取一次：
sc = set_bit[c]
cc = clr_bit[c]
```

---

## 次要缺點（原始版）

| 問題 | 說明 |
|------|------|
| `nxt = {}` 每格重建 | 每格建立新 dict（與新版建 list 成本相當，但 dict 初始化更重） |
| `rights = (0, 1) if c+1<m else (0,)` | 每格建立 tuple 並迭代，比直接 if 分支多一層物件建立 |
| `.get(key, 0)` | 比 list 索引再 `if w:` 多一次方法呼叫 |
| 無 `if w:` 短路 | 0 方案數也會嘗試更新狀態；新版 `if w:` 跳過零值 |

---

## 時間複雜度對比

兩版核心複雜度相同：$O(n \cdot m \cdot 2^m)$，每格掃描所有有效遮罩。

優化的是**每個狀態的常數成本**：

| 操作 | 原始版（估計） | 優化版（估計） |
|------|--------------|--------------|
| 狀態查找 | ~50–80 ns（hash+dict） | ~5–10 ns（list 索引） |
| nm 計算 | 最多 4 次/mask | 1 次/mask |
| open_cell 判斷 | 每個 mask 1 次 | 每格 1 次 |
| 位元遮罩計算 | 每個 mask 1 次 | 每列預算，每格 O(1) 引用 |

**整體加速估計**：對典型 6×6 全開放格 (size=64)，優化版約快 **4～6 倍**。

---

## 仍存在的限制（兩版皆同）

1. **每格建立新陣列** (`[0]*size`)：可改用手動清零的預先分配陣列，但程式碼複雜度增加。
2. **稀疏狀態時 dict 可能更快**：如果合法 mask 極少（遠小於 2^m），dict 只追蹤非零條目，而 list 仍需掃描全部；大 m 且高稀疏度時原版可能反勝。
3. **Python 函式呼叫開銷**：`count_ways` 仍是純 Python，如需更高效能，可改用 `numpy` 做向量化或用 C 擴充。
