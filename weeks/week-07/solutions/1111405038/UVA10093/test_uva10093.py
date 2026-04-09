import os
import sys
import subprocess
import unittest


# ============================================================
# 本測試檔針對 UVA 10093 — 炮兵佈陣（Artillery）
#
# 題意重點：
#   - N×M 的地圖，每格是 P（平原）或 H（山地）。
#   - 只有平原可以放炮兵，每格最多一支。
#   - 炮兵攻擊範圍：橫向左右各 2 格、縱向上下各 2 格。
#   - 任何兩支炮兵不能互相攻擊（即距離超過 2 才安全）。
#   - 求最多可放幾支炮兵。
#
# 測試方式：
#   - 預設測試 uva10093.py
#   - 可用環境變數 TARGET_SCRIPT 切換：
#       TARGET_SCRIPT=uva10093-easy.py python test_uva10093.py
# ============================================================


class TestUVA10093(unittest.TestCase):
    """針對 UVA 10093 炮兵佈陣的測試案例。"""

    @classmethod
    def setUpClass(cls) -> None:
        """決定要測哪一個程式檔。"""
        script_name = os.environ.get("TARGET_SCRIPT", "uva10093.py")
        cls.script_name = script_name
        cls.script_path = os.path.join(os.path.dirname(__file__), script_name)
        if not os.path.exists(cls.script_path):
            raise FileNotFoundError(
                f"找不到 {script_name}，請先建立解題程式。"
            )

    def run_case(self, input_data: str, expected_output: str) -> None:
        """執行程式並比對輸出。"""
        result = subprocess.run(
            [sys.executable, self.script_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=10,
        )
        self.assertEqual(
            0,
            result.returncode,
            msg=f"程式非正常結束，stderr:\n{result.stderr}",
        )
        actual_lines = result.stdout.strip().splitlines()
        expected_lines = expected_output.strip().splitlines()
        self.assertEqual(
            expected_lines,
            actual_lines,
            msg=(
                "輸出與預期不符\n"
                f"=== input ===\n{input_data}\n"
                f"=== expected ===\n{expected_output}\n"
                f"=== actual ===\n{result.stdout}"
            ),
        )

    def test_single_P(self) -> None:
        """測試 1×1 全是平原 P。

        只有一格且是平原，直接放 1 支炮兵，答案為 1。
        """
        self.run_case("1 1\nP\n", "1\n")

    def test_single_H(self) -> None:
        """測試 1×1 全是山地 H。

        只有一格且是山地，無法放任何炮兵，答案為 0。
        """
        self.run_case("1 1\nH\n", "0\n")

    def test_classic_5x4(self) -> None:
        """測試經典 5×4 樣例。

        地圖：
          PHPP  ← 第 1 列 H 不能放
          PPHH  ← 第 3,4 列 H 不能放
          PPPP  ← 全平原
          PHPP  ← 第 2 列 H
          PHHP  ← 第 2,3 列 H

        最佳放法（6 支）示意：
          P . P P  → 放第 1, 3, 4 格（待行間距限制）
          搭配動態規劃找出最優組合，答案為 6。
        """
        input_data = (
            "5 4\n"
            "PHPP\n"
            "PPHH\n"
            "PPPP\n"
            "PHPP\n"
            "PHHP\n"
        )
        self.run_case(input_data, "6\n")


if __name__ == "__main__":
    # 允許直接執行此檔案跑測試，並輸出 log 檔：
    #   python test_uva10093.py
    # 或指定測試檔：
    #   TARGET_SCRIPT=uva10093-easy.py python test_uva10093.py

    script_name = os.environ.get("TARGET_SCRIPT", "uva10093.py")
    base = os.path.splitext(os.path.basename(script_name))[0]
    log_name = f"test_{base}_run.log"
    log_path = os.path.join(os.path.dirname(__file__), log_name)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"# UVA 10093 unittest 執行結果 ({script_name})\n")

        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestUVA10093)
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        result = runner.run(suite)

        f.write("\n--- 總結 ---\n")
        f.write(f"testsRun: {result.testsRun}\n")
        f.write(f"failures: {len(result.failures)}\n")
        f.write(f"errors: {len(result.errors)}\n")
        f.write(f"wasSuccessful: {result.wasSuccessful()}\n")

    print(f"測試已執行完成，詳細結果請見: {log_path}")
