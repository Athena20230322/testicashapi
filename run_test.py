import subprocess
import os
from datetime import datetime
# 要執行的Python腳本
scripts = ['test1.py', 'test2.py','test3rtn.py']
# 計數器
pass_count = 0
fail_count = 0
# 依次執行腳本
for script in scripts:
    os.chdir(r'C:\testicashapi')  # 改變當前工作目錄
    process = subprocess.Popen(['python', script])
    process.wait()  # 等待腳本執行完成
    if process.returncode == 0:
        print(f'{script}: Pass')
        pass_count += 1
    else:
        print(f'{script}: Fail')
        fail_count += 1
# 生成HTML報告
report_dir = r'c:\apireport'
os.makedirs(report_dir, exist_ok=True)
report_file = os.path.join(report_dir, f'report_{datetime.now():%Y%m%d_%H%M%S}.html')
with open(report_file, 'w') as f:
    f.write('<html>\n')
    f.write('<head>\n')
    f.write(f'<title>Test Report - {datetime.now():%Y/%m/%d %H:%M:%S}</title>\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write(f'<p>Total scripts: {len(scripts)}</p>\n')
    f.write(f'<p>Pass count: {pass_count}</p>\n')
    f.write(f'<p>Fail count: {fail_count}</p>\n')
    f.write('</body>\n')
    f.write('</html>\n')
# 顯示報告的絕對路徑
report_path = os.path.abspath(report_file)
print(f'Report generated: {report_path}')