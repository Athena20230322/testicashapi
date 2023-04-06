import datetime
import os
import pytest
import certifi
from importlib_resources import files

_CACERT_CTX = files(certifi).joinpath("cacert.pem")

now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# 取得 tests 資料夾的完整路徑
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "tests"))


# 取得要執行的檔案名稱列表，按照您期望的順序排列
test_files = [
    os.path.join(tests_dir, "test1.py"),
    os.path.join(tests_dir, "test2.py"),
    os.path.join(tests_dir, "test3rtn.py"),
]

# 將要執行的檔案名稱列表作為 pytest.main() 的參數之一傳遞進去
pytest.main(["-v", "-rA", f"--html=report_{now}.html"] + test_files)
