import os
import subprocess
import datetime

# Define CSS styles for the report
styles = '''
    <style>
body{font-family:sans-serif;}
h1{text-align:center;}
table{border-collapse:collapse;margin:auto;width:80%;}
th,td{border:1px solid black;padding:8px;text-align:left;vertical-align:top;}
th{background-color:#b2c2bf;color:white;}
tr:nth-child(even){background-color:#f2f2f2;}
</style>
'''

# Get a list of all .py files in the ICPAPI directory
scripts_dir = 'C:\\testicashapi\\Test_Case\\ICPAPI'
scripts = [os.path.join(scripts_dir, f) for f in os.listdir(scripts_dir) if f.endswith('.py')]

# Initialize counters and empty list to store test results
pass_count = 0
fail_count = 0
test_results = []

# Run each script and record the result
for script in scripts:
    start_time = datetime.datetime.now()
    process = subprocess.run(f'python {script}', shell=True, capture_output=True, text=True)
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    output = process.stdout
    if 'Test Failed' in output:
        print(f'{script}: Fail')
        fail_count += 1
        test_results.append(('Fail', script, duration))
    else:
        print(f'{script}: Pass')
        pass_count += 1
        test_results.append(('Pass', script, duration))

# Calculate total count and pass/fail percentages
total_count = len(scripts)
pass_percentage = round(pass_count / total_count * 100, 2)
fail_percentage = round(fail_count / total_count * 100, 2)

# Generate the HTML report
html_template = ("<html>"
                 "<head>"
                 "<title>Test Report</title>"
                 f"{styles}"
                 "</head>"
                 "<body>"
                 "<h1>API Test Report</h1>"
                 f"<p><strong>Total Scripts:</strong> {total_count}</p>"
                 f"<p><strong>Passed Scripts:</strong> {pass_count}</p>"
                 f"<p><strong>Failed Scripts:</strong> {fail_count}</p>"
                 "<table>"
                 "<tr>"
                 "<th>Result</th>"
                 "<th>Test</th>"
                 "<th>Duration</th>"
                 "</tr>"
                 f"{''.join([f'<tr><td>{result}</td><td>{test}</td><td>{duration}</td></tr>' for result, test, duration in test_results])}"
                 "</table>"
                 f"<p><strong>Pass Percentage:</strong> {pass_percentage:.2f}%</p>"
                 f"<p><strong>Fail Percentage:</strong> {fail_percentage:.2f}%</p>"
                 "<p>Thank you for reviewing the API Test Report!</p>"
                 "</body>"
                 "</html>")
# Save the report to a file
report_dir = os.path.join(os.getcwd(), 'apireport')
os.makedirs(report_dir, exist_ok=True)
report_path = os.path.join(report_dir, f"report_{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}.html")
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Report generated: {report_path}")