import os
import sys
import subprocess
import unittest


# 單一測試檔：
# - 預設測試 uva10062.py
# - 若設定環境變數 TARGET_SCRIPT，例如：
#       $env:TARGET_SCRIPT = "uva10062-easy.py"
#   則會改測該檔案，並把結果寫到對應的 log 檔。


class TestUVA10062(unittest.TestCase):
    """針對 UVA 10062 題目的多組測試案例。"""

    @classmethod
    def setUpClass(cls) -> None:
        """在所有測試開始前，決定要測哪一個程式檔。"""
        script_name = os.environ.get("TARGET_SCRIPT", "uva10062.py")
        cls.script_name = script_name
        cls.script_path = os.path.join(os.path.dirname(__file__), script_name)
        if not os.path.exists(cls.script_path):
            raise FileNotFoundError(
                f"找不到 {script_name}，請確認檔案存在並已完成程式。"
            )

    def run_case(self, input_data: str, expected_output: str) -> None:
        """共用的測試執行函式。

        會執行：python <target_script>
        將 input_data 丟到 stdin，並比對 stdout 是否等於 expected_output。
        """
        result = subprocess.run(
            [sys.executable, self.script_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=2,
        )

        # 確認程式正常結束
        self.assertEqual(
            0,
            result.returncode,
            msg=f"程式非正常結束，stderr:\n{result.stderr}",
        )

        # 比對每一行輸出（去掉前後空白，再逐行比對）
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

    def test_small_example_n3(self) -> None:
        """基本測試：N=3 的小型案例。"""
        input_data = """3
0
2
"""
        expected_output = """2
1
3
"""
        self.run_case(input_data, expected_output)

    def test_increasing_order(self) -> None:
        """測試原本隊伍已經是 1..N 由小到大的情況。"""
        input_data = """5
1
2
3
4
"""
        expected_output = """1
2
3
4
5
"""
        self.run_case(input_data, expected_output)

    def test_random_order_n4(self) -> None:
        """另一組隨機排列測試：N=4。"""
        input_data = """4
0
2
1
"""
        expected_output = """3
1
4
2
"""
        self.run_case(input_data, expected_output)


if __name__ == "__main__":
    # 依照目標程式檔名決定 log 檔名稱
    script_name = os.environ.get("TARGET_SCRIPT", "uva10062.py")
    base = os.path.splitext(os.path.basename(script_name))[0]
    log_name = f"test_{base}_run.log"
    log_path = os.path.join(os.path.dirname(__file__), log_name)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"# UVA 10062 unittest 執行結果 ({script_name})\n")

        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestUVA10062)
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        result = runner.run(suite)

        f.write("\n--- 總結 ---\n")
        f.write(f"testsRun: {result.testsRun}\n")
        f.write(f"failures: {len(result.failures)}\n")
        f.write(f"errors: {len(result.errors)}\n")
        f.write(f"wasSuccessful: {result.wasSuccessful()}\n")

    print(f"測試已執行完成，詳細結果請見: {log_path}")
