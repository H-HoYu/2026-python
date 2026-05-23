# Week 13 Solution - 1111405038

## 完成項目
- Task 1: 三年並排長條圖
- Task 2: 來源縣市熱力圖
- Unit tests: test_task1.py, test_task2.py

## 檔案結構
- task1_grouped_bar.py
- task2_zipcode_heatmap.py
- tests/test_task1.py
- tests/test_task2.py
- output/task1.png
- output/task2.png
- TEST_LOG.md
- REPORT.md
- AI_USAGE.md

## 執行方式
在本目錄執行：

```bash
python task1_grouped_bar.py
python task2_zipcode_heatmap.py
```

## 測試方式
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## 依賴套件
- matplotlib
- numpy

## 備註
- 讀取 CSV 使用 utf-8-sig。
- 圖表有加入中文字型 fallback，減少中文標籤缺字問題。
