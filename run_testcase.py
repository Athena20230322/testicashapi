import os
import subprocess
import datetime

# Define CSS styles for the report
styles = '''
    <style>
        body {
            font-family: sans-serif;
        }
        h1 {
            text-align: center;
        }
        table {
            border-collapse: collapse;
            margin: auto;
            width: 80%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
            vertical-align: top;
        }
        th {
            background-color: #b2c2bf;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
    </style>
'''
#在這個代碼中，我使用 os.listdir('ICPAPI') 來獲取 ICPAPI 目錄下的所有文件和文件夾。
# 然後使用列表推導式和 endswith() 方法來過濾出所有以 .py 結尾的文件，並使用 os.path.join() 方法來獲取每個文件的完整路徑。
# 最後，將所有 .py 文件的
# Get a list of all .py files in the ICPAPI directory

scripts = [os.path.join('C:\\testicashapi\\Test_Case\\ICPAPI', f) for f in os.listdir('C:\\testicashapi\\Test_Case\\ICPAPI') if f.endswith('.py')]

# Initialize counters and empty list to store test results
pass_count = 0
fail_count = 0
test_results = []

# Run each script and record the result
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

# Generate the HTML report
html_template = f"""
<html>
    <head>
        <title>Test Report</title>
        {styles}
    </head>
    <body>
        <h1>API Test Report</h1>
        <p><strong>Total Scripts:</strong> {len(scripts)}</p>
        <p><strong>Passed Scripts:</strong> {pass_count}</p>
        <p><strong>Failed Scripts:</strong> {fail_count}</p>
        <table>
            <tr>
                <th>Result</th>
                <th>Test</th>
                <th>Duration</th>
            </tr>
            {''.join([f"<tr><td>{result}</td><td>{test}</td><td>{duration}</td></tr>" for result, test, duration in test_results])}
        </table>
        <p>Thank you for reviewing the API Test Report!</p>
    </body>
</html>
"""

# Save the report to a file
report_path = os.path.join(os.getcwd(), 'apireport', f"report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html")
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Report generated: {report_path}")
