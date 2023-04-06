import os
import subprocess
import datetime
# 儲存所有的腳本
scripts = ['test1.py', 'test2.py','test3rtn']
# 計數器
pass_count = 0
fail_count = 0
test_results = []
# 依次執行腳本
for script in scripts:
    start_time = datetime.datetime.now()
    process = subprocess.run(f'python {script}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    if process.returncode == 0:
        print(f'{script}: Pass')
        pass_count += 1
        test_results.append(('Pass', script, duration))
    else:
        print(f'{script}: Fail')
        fail_count += 1
        test_results.append(('Fail', script, duration))
# 生成HTML報告
html_template = f"""
<html>
    <head>
        <title>Test Report</title>
    </head>
    <body>
        <h1>Test Report</h1>
        <p>Total Scripts: {len(scripts)}</p>
        <p>Passed Scripts: {pass_count}</p>
        <p>Failed Scripts: {fail_count}</p>
        <table>
            <tr>
                <th>Result</th>
                <th>Test</th>
                <th>Duration</th>
            </tr>
            {''.join([f"<tr><td>{result}</td><td>{test}</td><td>{duration}</td></tr>" for result, test, duration in test_results])}
        </table>
    </body>
</html>
"""
report_path = os.path.join(os.getcwd(), 'apireport', f"report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html")
with open(report_path, 'w',encoding='utf-8') as f:
    f.write(html_template)
print(f"Report generated: {report_path}")