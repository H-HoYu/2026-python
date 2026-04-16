# Understand（理解）- 生成器概念

# 這份程式示範 Python 生成器（generator）的核心觀念：
# 1) 用 yield 逐步產生資料，而不是一次建立完整清單。
# 2) 生成器會「記住中斷位置」，下次 next() 會從上次暫停點繼續。
# 3) 用 yield from 可以把子可迭代物件或子生成器的值直接往外傳遞。
#
# 優點：
# - 節省記憶體（尤其是大量資料或無限序列）。
# - 程式可用「串流」方式處理資料。


def frange(start, stop, step):
    # frange: 浮點版本的 range。
    # 與 range 不同，這裡使用 while + yield 逐步吐出浮點值。
    # 注意：浮點數運算可能有精度誤差，真實專案常搭配 round() 或 Decimal。
    x = start
    while x < stop:
        yield x
        x += step


# 生成器可被 list() 一次取完，轉成一般清單。
result = list(frange(0, 2, 0.5))
print(f"frange(0, 2, 0.5): {result}")


def countdown(n):
    # countdown 會從 n 倒數到 1。
    # print 在 yield 前後，可觀察生成器何時真正執行。
    print(f"Starting countdown from {n}")
    while n > 0:
        yield n
        n -= 1
    # 當 while 結束後函式返回，生成器隨即拋出 StopIteration。
    print("Done!")


print("\n--- 建立生成器 ---")
# 呼叫 countdown(3) 並不會立刻跑完整函式，
# 只會回傳一個「生成器物件」。
c = countdown(3)
print(f"生成器物件: {c}")

print("\n--- 逐步迭代 ---")
# 每次 next(c) 只前進到下一個 yield。
# 可以清楚看到「惰性執行（lazy evaluation）」特性。
print(f"next(c): {next(c)}")
print(f"next(c): {next(c)}")
print(f"next(c): {next(c)}")

try:
    # 值已取完，再 next() 會觸發 StopIteration。
    next(c)
except StopIteration:
    print("StopIteration!")


def fibonacci():
    # 無限 Fibonacci 生成器。
    # while True 代表理論上不會自行停止，
    # 使用端要自行控制取用次數（例如搭配 for/range 或 itertools.islice）。
    a, b = 0, 1
    while True:
        yield a
        # 平行指定同時更新 a、b，避免覆蓋問題。
        a, b = b, a + b


print("\n--- Fibonacci 生成器 ---")
fib = fibonacci()
# 只取前 10 個值，避免無限迴圈。
for i in range(10):
    print(next(fib), end=" ")
print()


def chain_iter(*iterables):
    # *iterables 允許傳入任意數量的可迭代物件。
    # yield from it 等同於：for x in it: yield x
    # 寫法更精簡，也會正確轉交子生成器的迭代行為。
    for it in iterables:
        yield from it


print("\n--- yield from 用法 ---")
result = list(chain_iter([1, 2], [3, 4], [5, 6]))
print(f"chain_iter: {result}")


class Node:
    # 簡易樹節點：每個節點有一個值與多個子節點。
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __iter__(self):
        # 讓 Node 可直接被 for 走訪其 children。
        return iter(self.children)

    def depth_first(self):
        # 深度優先遍歷（DFS, pre-order）：
        # 先回傳自己，再遞迴回傳每個子樹。
        yield self
        for child in self:
            yield from child.depth_first()


print("\n--- 樹的深度優先遍歷 ---")
root = Node(0)
root.add_child(Node(1))
root.add_child(Node(2))
root.children[0].add_child(Node(3))
root.children[0].add_child(Node(4))

for node in root.depth_first():
    print(node.value, end=" ")
print()


def flatten(items):
    # 將巢狀可迭代結構攤平成一維序列。
    # 條件說明：
    # - 若元素本身可迭代且不是字串，視為需要繼續展開。
    # - 字串雖可迭代，但通常想視為單一值，因此排除 str。
    for x in items:
        if hasattr(x, "__iter__") and not isinstance(x, str):
            yield from flatten(x)
        else:
            yield x


print("\n--- 巢狀序列攤平 ---")
nested = [1, [2, [3, 4]], 5]
print(f"展開: {list(flatten(nested))}")
