# UVA10242 優化對比分析

## 檔案對照

- 原始版: UVA10242-easy.py
- 優化版: UVA10242-optimized.py

## 核心不變

兩版都使用同一個正確解法骨架：
1. Kosaraju 求 SCC
2. 將原圖壓成 SCC DAG
3. 在 DAG 上做從起點出發的最大權重路徑 DP（只看可達且終點是酒吧的 SCC）

時間複雜度階級仍為 $O(n + m)$，優化重點是常數因子。

## 原始版缺點與優化點

### 1) SCC DAG 使用 set 儲存出邊，hash 成本高

原始版：
- `dag = [set() for _ in range(cc)]`
- 每條跨 SCC 邊都做 `set.add()`，涉及 hash 與桶查找。

缺點：
- 在邊數大的情境，set 的 hash 成本與記憶體碎片都偏高。

優化版：
- 改為 `dag = [[] for _ in range(cc)]`
- 以 `seen_to + stamp`（時間戳去重）保證同一個 `cu -> cv` 只加入一次。

效果：
- 去掉大量 hash 操作，DAG 建圖更快、記憶體更緊湊。

### 2) DFS 第一趟用 (node, idx) tuple stack，物件建立頻繁

原始版：
- `stack = [(st, 0)]`
- 迴圈中反覆建立/覆寫 tuple。

缺點：
- Python tuple 建立與解包在高頻迴圈有可觀常數成本。

優化版：
- 拆成兩個平行 stack：`stack`（節點）+ `it_idx`（鄰邊索引）。

效果：
- 降低暫時物件建立，SCC 第一趟 DFS 常數更小。

### 3) 多處布林旗標使用 Python bool list，記憶體與存取不夠緊湊

原始版：
- `seen = [False] * n`
- `reach = [False] * cc`
- `cbar = [False] * cc`

缺點：
- Python bool 物件與 list 結構開銷較大。

優化版：
- 改用 `bytearray`：`seen`, `reach`, `cbar`。

效果：
- 降低記憶體占用，快取友善，判斷也更輕量。

### 4) SCC DAG 去重方式隱含在 set，不可控且較重

原始版：
- 去重邏輯交給 set。

缺點：
- 去重雖然簡潔，但每次操作都要付 hash 代價。

優化版：
- 先將每個 SCC 的原始節點收集到 `nodes_in_comp`。
- 逐 SCC 掃描出邊，利用 `seen_to[cv] != stamp` 去重。

效果：
- 去重成本近似純陣列索引，效能穩定。

## 對比總結

- 原始版優點：可讀性好、寫法直觀。
- 原始版缺點：在 Python 下 `set/hash/tuple` 的常數成本偏高，對大資料壓力較大。
- 優化版優點：維持同演算法正確性，減少 hash 與暫時物件，通常會更快更省記憶體。
- 優化版代價：程式碼比原始版更偏競賽風格，可讀性稍降。

## 可能進一步優化（可選）

1. 以自訂快速整數讀取器取代 `text.split()`，降低峰值記憶體。
2. 在 DP 拓樸過程中維護候選答案，減少最後一輪掃描。
3. 若資料極大，可嘗試將圖儲存改成壓縮結構（例如 CSR 風格）。
