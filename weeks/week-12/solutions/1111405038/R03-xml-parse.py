# R03. XML 解析基礎（6.3）
# xml.etree.ElementTree：find / findall / get / text / iter

import xml.etree.ElementTree as ET

# ET 是 Python 內建的 XML 解析工具，適合基本查找與讀取

# ── 範例 XML ─────────────────────────────────────────────
xml_data = """
<rss version="2.0">
  <channel>
    <title>Planet Python</title>
    <item>
      <title>討論 Python 型別提示</title>
      <link>https://example.com/1</link>
      <author>Alice</author>
    </item>
    <item>
      <title>asyncio 最佳實踐</title>
      <link>https://example.com/2</link>
      <author>Bob</author>
    </item>
  </channel>
</rss>
"""

# ── 解析字串 ─────────────────────────────────────────────
# fromstring 會把 XML 字串轉成根節點 Element
root = ET.fromstring(xml_data)
print("根標籤：", root.tag)           # rss
print("屬性：",   root.attrib)        # {'version': '2.0'}

# ── find / findall ────────────────────────────────────────
# find 取第一個符合的子節點，找不到時回傳 None
channel = root.find("channel")
print("頻道名稱：", channel.find("title").text)

# 取得所有 item
# findall 會回傳符合路徑的所有節點清單
for item in root.findall("channel/item"):
    title  = item.find("title").text
    author = item.find("author").text
    print(f"  [{author}] {title}")

# ── iter：遍歷所有同名標籤 ───────────────────────────────
print("\n所有 <title>：")
# iter("title") 會在整棵樹中巡訪所有 title 標籤
for elem in root.iter("title"):
    print(" ", elem.text)

# ── 從檔案解析 ───────────────────────────────────────────
# tree = ET.parse("data.xml")
# root = tree.getroot()

# ── 取得屬性 .get() ───────────────────────────────────────
# get(key, default) 可在屬性不存在時回傳預設值
version = root.get("version")
print("\nRSS 版本：", version)        # 2.0
print("不存在的屬性：", root.get("missing", "預設值"))
