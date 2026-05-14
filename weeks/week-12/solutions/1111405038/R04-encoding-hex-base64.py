# R04. 十六進位與 Base64 編碼解碼（6.9–6.10）
# binascii / base64 / bytes.hex() / bytes.fromhex()

import binascii
import base64

# binascii: 位元組與二進位/十六進位表示互轉
# base64: 將位元組轉成可安全傳輸的 ASCII 文字格式

# ── 6.9 十六進位（Hex）────────────────────────────────────
data = b"Hello, \xe4\xb8\x96\xe7\x95\x8c"   # "Hello, 世界" in UTF-8

# bytes → hex 字串
# b2a_hex 回傳 bytes 型態的十六進位內容
hex_str = binascii.b2a_hex(data)
print("b2a_hex：", hex_str)                   # b'48656c6c6f2c ...'

hex_str2 = data.hex()                         # Python 3.5+ 內建方法
print(".hex()：", hex_str2)

# hex 字串 → bytes
# a2b_hex 可把十六進位內容還原回原始 bytes
restored = binascii.a2b_hex(hex_str)
print("a2b_hex：", restored)

restored2 = bytes.fromhex(hex_str2)           # Python 3.5+
print("fromhex：", restored2)

assert restored == data     # 驗證 round-trip（轉換再還原）結果一致

# ── 6.10 Base64 ───────────────────────────────────────────
msg = b"Python Cookbook"

# 編碼
# Base64 編碼後仍是 bytes，需要時可再 decode 成字串
encoded = base64.b64encode(msg)
print("\nb64encode：", encoded)               # b'UHl0aG9uIENvb2tib29r'

# 解碼
# 可逆轉回原始 bytes
decoded = base64.b64decode(encoded)
print("b64decode：", decoded)                 # b'Python Cookbook'

# URL-safe Base64（不含 +/，改用 -_）
# 常用於 URL、檔名或 token，避免特殊字元衝突
url_encoded = base64.urlsafe_b64encode(msg)
print("urlsafe：  ", url_encoded)

# ── 應用場景比較 ──────────────────────────────────────────
# Hex    → 可讀性高，長度 2x，常見於 hash / MAC 位址
# Base64 → 長度約 1.33x，常見於 email 附件、HTTP 認證、JWT
# 兩者都只是「表示方式」，不是加密！
