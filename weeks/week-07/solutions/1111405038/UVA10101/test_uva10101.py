import os
import sys
import subprocess
import unittest


# ============================================================
# 本測試檔針對 UVA 10101 — 移動一根木棒使等式成立
#
# 題意重點：
#   - 輸入一個「不成立的等式」字串（以 # 結尾）。
#   - 式子只含數字、+、-、= 和最後的 #。
#   - 只能移動「數字部分」的一根木棒（+、-、= 不能動）。
#   - 移動後每個數字必須是合法的七段顯示器數字（0~9）。
#   - 若可使等式成立，輸出新等式（含 #）；否則輸出 No。
#
# 七段顯示器各數字使用的木棒數：
#   0→6, 1→2, 2→5, 3→5, 4→4, 5→5, 6→6, 7→3, 8→7, 9→6
#
# 木棒轉換關係（從 a 移一根到 b 得到 c→d）：
#   例如：把 7(3根) 加一根 → 可變成 1(2根)? 不行（7減一根）
#         把 0(6根) 移走一根→ 8的某一段 → 可能得到其他數字
#
# 測試方式：
#   - 預設測試 uva10101.py
#   - 環境變數 TARGET_SCRIPT 可切換：
#       $env:TARGET_SCRIPT='uva10101-easy.py'; python test_uva10101.py
# ============================================================


class TestUVA10101(unittest.TestCase):
    """針對 UVA 10101 移動木棒的測試案例。"""

    @classmethod
    def setUpClass(cls) -> None:
        """決定測試哪個程式檔。"""
        script_name = os.environ.get("TARGET_SCRIPT", "uva10101.py")
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
        actual = result.stdout.strip()
        expected = expected_output.strip()
        self.assertEqual(
            expected,
            actual,
            msg=(
                f"\n=== input ===\n{input_data}"
                f"=== expected ===\n{expected}\n"
                f"=== actual ===\n{actual}"
            ),
        )

    def test_simple_has_solution(self) -> None:
        """測試有解的簡單案例：1+1=3#

        1+1=3 不成立（1+1=2）。
        3（5根木棒）移走一根可變成 2（5根）→ 1+1=2 成立。
        所以答案為 1+1=2#。
        """
        self.run_case("1+1=3#\n", "1+1=2#")

    def test_no_solution(self) -> None:
        """測試無解的案例：1+1=1#

        1+1=1 不成立（1+1=2）。
        不管怎麼移動一根木棒都無法讓等式成立。
        答案為 No。
        """
        self.run_case("1+1=1#\n", "No")

    def test_subtract(self) -> None:
        """測試含減號的案例：3-1=3#

        3-1=3 不成立（3-1=2）。
        等號右邊的 3（5根）移走一根可變為 2（5根）→ 3-1=2 成立。
        答案為 3-1=2#。
        """
        self.run_case("3-1=3#\n", "3-1=2#")

    def test_already_no(self) -> None:
        """測試移動後無法整理為合法等式的案例：9=1+1#

        9=1+1 不成立（9≠2）。
        無法透過移動一根木棒使等式成立。
        答案為 No。
        """
        self.run_case("9=1+1#\n", "No")


if __name__ == "__main__":
    # 直接執行此檔案跑測試，並輸出 log：
    #   python test_uva10101.py
    # 測試其他程式：
    #   $env:TARGET_SCRIPT='uva10101-easy.py'; python test_uva10101.py

    script_name = os.environ.get("TARGET_SCRIPT", "uva10101.py")
    base = os.path.splitext(os.path.basename(script_name))[0]
    log_name = f"test_{base}_run.log"
    log_path = os.path.join(os.path.dirname(__file__), log_name)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"# UVA 10101 unittest 執行結果 ({script_name})\n")

        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestUVA10101)
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        result = runner.run(suite)

        f.write("\n--- 總結 ---\n")
        f.write(f"testsRun: {result.testsRun}\n")
        f.write(f"failures: {len(result.failures)}\n")
        f.write(f"errors: {len(result.errors)}\n")
        f.write(f"wasSuccessful: {result.wasSuccessful()}\n")

    print(f"測試已執行完成，詳細結果請見: {log_path}")
