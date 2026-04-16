# U1. 解包失敗的原因：變數數量 ≠ 元素數量（1.1）

# p 是一個 tuple，裡面只有兩個元素：4 與 5。
p = (4, 5)

# Python 的 sequence unpacking 規則是：
# 左邊要接收的變數數量，必須和右邊可解包的元素數量一致。
# 這裡右邊只有 2 個元素，但左邊想接到 x、y、z 共 3 個變數，
# 因此數量不相符，會拋出 ValueError。
#
# 如果真的執行下一行，錯誤訊息大意會是：
# not enough values to unpack (expected 3, got 2)
# x, y, z = p  # ValueError：元素只有 2 個但變數要 3 個
