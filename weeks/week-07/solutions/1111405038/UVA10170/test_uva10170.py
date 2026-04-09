import os
import sys
import subprocess
import unittest


# ============================================================
# 本測試檔針對 UVA 10170 — The Hotel with Infinite Rooms
#
# 題意重點：
#   - 第 1 個旅行團有 S 人，住 S 天。
#   - 第 2 個旅行團有 S+1 人，住 S+1 天。
#   - 第 k 個旅行團有 S+k-1 人，住 S+k-1 天。
#   - 入住時間是連續的（前一團退房隔天早上下一團入住）。
#   - 第 k 個旅行團佔用的天數區間為：
#       開始天 = S + (S+1) + ... + (S+k-2) + 1
#              = (k-1)*S + (k-1)*(k-2)/2 + 1
#       結束天 = 開始天 + (S+k-1) - 1
#
#   問第 D 天是哪個旅行團（有幾人）在住。
#
#   解法：對 k 做二分搜尋
#     找最小的 k 使得「前 k 個旅行團佔用的總天數 ≥ D」
#
#   前 k 個旅行團總天數 = k*S + k*(k-1)/2
#
#   找到 k 後，答案 = S + k - 1（第 k 個旅行團的人數）
#
# 測試方式：
#   - 預設測試 uva10170.py
#   - 環境變數 TARGET_SCRIPT 可切換：
#       $env:TARGET_SCRIPT='uva10170-easy.py'; python test_uva10170.py
# ============================================================


class TestUVA10170(unittest.TestCase):
    """針對 UVA 10170 旅館問題的測試案例。"""

    @classmethod
    def setUpClass(cls) -> None:
        """決定測試哪個程式檔。"""
        script_name = os.environ.get("TARGET_SCRIPT", "uva10170.py")
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

    def test_first_group(self) -> None:
        """S=4, D=1：第 1 天 → 第 1 個旅行團（4 人）。

        第 1 團住第 1~4 天，第 1 天就是第 1 團。
        答案：4
        """
        self.run_case("4 1\n", "4\n")

    def test_last_day_first_group(self) -> None:
        """S=4, D=4：第 4 天 → 第 1 個旅行團最後一天（4 人）。

        第 1 團（4 人）住第 1~4 天。
        第 4 天仍是第 1 團。
        答案：4
        """
        self.run_case("4 4\n", "4\n")

    def test_second_group(self) -> None:
        """S=4, D=5：第 5 天 → 第 2 個旅行團（5 人）。

        第 1 團住 1~4 天，第 2 團（5 人）住第 5~9 天。
        第 5 天是第 2 團第 1 天。
        答案：5
        """
        self.run_case("4 5\n", "5\n")

    def test_third_group(self) -> None:
        """S=4, D=10：第 10 天 → 第 3 個旅行團（6 人）。

        第 1 團: 1~4（4天）
        第 2 團: 5~9（5天）
        第 3 團: 10~15（6天）
        第 10 天是第 3 團第 1 天。
        答案：6
        """
        self.run_case("4 10\n", "6\n")

    def test_large_d(self) -> None:
        """S=1, D=1000000000000000（10^15-1）：大數測試。

        S=1，前 k 個旅行團總天數 = k + k*(k-1)/2 = k*(k+1)/2
        找最小 k 使 k*(k+1)/2 ≥ 10^15
        k ≈ sqrt(2*10^15) ≈ 44721359
        精確答案需算出 k，再返回 S+k-1 = k（因為 S=1）。

        用二分法計算：
          k*(k+1)/2 >= 10^15 → k ≈ 44721359
          驗算：44721359*44721360//2 = 999999994648980 < 10^15
                44721360*44721361//2 = 1000000039370080 >= 10^15
          所以答案 = 1 + 44721360 - 1 = 44721360
        """
        self.run_case("1 1000000000000000\n", "44721360\n")

    def test_multiple_lines(self) -> None:
        """多行輸入測試（EOF 輸入格式）。

        4 1 → 4
        4 5 → 5
        4 10 → 6
        """
        self.run_case("4 1\n4 5\n4 10\n", "4\n5\n6\n")


if __name__ == "__main__":
    # 直接執行本檔案跑測試，並輸出 log：
    #   python test_uva10170.py
    # 測試其他程式：
    #   $env:TARGET_SCRIPT='uva10170-easy.py'; python test_uva10170.py

    script_name = os.environ.get("TARGET_SCRIPT", "uva10170.py")
    base = os.path.splitext(os.path.basename(script_name))[0]
    log_name = f"test_{base}_run.log"
    log_path = os.path.join(os.path.dirname(__file__), log_name)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"# UVA 10170 unittest 執行結果 ({script_name})\n")

        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestUVA10170)
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        result = runner.run(suite)

        f.write("\n--- 總結 ---\n")
        f.write(f"testsRun: {result.testsRun}\n")
        f.write(f"failures: {len(result.failures)}\n")
        f.write(f"errors: {len(result.errors)}\n")
        f.write(f"wasSuccessful: {result.wasSuccessful()}\n")

    print(f"測試已執行完成，詳細結果請見: {log_path}")
