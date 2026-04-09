import os
import sys
import subprocess
import unittest


# 本檔是針對題目 10071（六元組 a + b + c + d + e = f 統計問題）的 unit test。
# 題意重點：
#   - 給定一個整數集合 S（元素互不重複）。
#   - 要計算所有 (a, b, c, d, e, f) ∈ S^6，且滿足 a + b + c + d + e = f 的組數。
#   - a, b, c, d, e, f 可以重複使用同一個元素。
#
# 測試方式：
#   - 假設同資料夾內有一個程式檔：uva10071.py
#   - 測試程式會用 subprocess 呼叫 `python uva10071.py`，
#     將測試輸入餵到 stdin，並比對 stdout 是否符合預期輸出。
# 學生只需要實作 uva10071.py（讀取標準輸入、輸出答案），
# 不需要修改本測試檔。


class TestUVA10071(unittest.TestCase):
    """針對 UVA 10071 題目的多組測試案例。"""

    @classmethod
    def setUpClass(cls) -> None:
        """在所有測試開始前，決定要測哪一個程式檔。"""
        script_name = os.environ.get("TARGET_SCRIPT", "uva10071.py")
        cls.script_name = script_name
        cls.script_path = os.path.join(os.path.dirname(__file__), script_name)
        if not os.path.exists(cls.script_path):
            raise FileNotFoundError(
                f"找不到 {script_name}，請在同一資料夾中建立並完成解題程式。"
            )

    def run_case(self, input_data: str, expected_output: str) -> None:
        """共用的測試執行函式。

        會執行：python uva10071.py
        將 input_data 丟到 stdin，並比對 stdout 是否等於 expected_output（逐行比對）。
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

    def test_single_zero(self) -> None:
        """測試 S = {0} 的最簡單情況。

        S = {0}
        只有一個元素 0，六元組中每個位置都只能選 0。
        唯一的六元組 (0,0,0,0,0,0) 會滿足 0+0+0+0+0 = 0。
        因此答案為 1。
        """
        input_data = """1
0
"""
        expected_output = """1
"""
        self.run_case(input_data, expected_output)

    def test_single_one(self) -> None:
        """測試 S = {1} 的情況。

        S = {1}
        左邊和永遠是 1+1+1+1+1 = 5，而右邊 f = 1。
        不可能滿足等式，因此答案為 0。
        """
        input_data = """1
1
"""
        expected_output = """0
"""
        self.run_case(input_data, expected_output)

    def test_zero_and_one(self) -> None:
        """測試 S = {0,1}，檢查多種組合。

        S = {0,1}
        a..e 為 0 或 1，共 2^5 = 32 種情況；f 也為 0 或 1。
        滿足 a+..+e = f 的情況：
        - 和為 0 且 f=0：只有全部是 0，1 種，f 只能選 0 → 1 組。
        - 和為 1 且 f=1：選一個位置是 1，其餘是 0，C(5,1)=5 種，f=1 → 5 組。
        總共 1 + 5 = 6 組。
        """
        input_data = """2
0
1
"""
        expected_output = """6
"""
        self.run_case(input_data, expected_output)


if __name__ == "__main__":
    # 允許直接執行此檔案來跑測試，並同時輸出 log 檔：
    #   python test_uva10071.py
    # 可透過環境變數 TARGET_SCRIPT 指定要測試的檔案：
    #   - 預設：uva10071.py
    #   - 手打版：先設 TARGET_SCRIPT=uva10071-hand.py 再執行本測試。

    script_name = os.environ.get("TARGET_SCRIPT", "uva10071.py")
    base = os.path.splitext(os.path.basename(script_name))[0]
    log_name = f"test_{base}_run.log"
    log_path = os.path.join(os.path.dirname(__file__), log_name)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"# UVA 10071 unittest 執行結果 ({script_name})\n")

        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestUVA10071)
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        result = runner.run(suite)

        f.write("\n--- 總結 ---\n")
        f.write(f"testsRun: {result.testsRun}\n")
        f.write(f"failures: {len(result.failures)}\n")
        f.write(f"errors: {len(result.errors)}\n")
        f.write(f"wasSuccessful: {result.wasSuccessful()}\n")

    print(f"測試已執行完成，詳細結果請見: {log_path}")
