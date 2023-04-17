import os
import subprocess
import datetime
import base64
import matplotlib.pyplot as plt

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
        fail_count += 1
        # Get the RtnMsg from the error message
        try:
            rtnmsg = output.split('RtnMsg:')[1].strip()
        except:
            rtnmsg = 'N/A'
        # Append the test result to the list
        test_results.append(('Fail', script, duration, rtnmsg))
    else:
        pass_count += 1
        test_results.append(('Pass', script, duration, 'N/A'))

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
                 "<h1>ICP API Test Report</h1>"
                 f"<p><strong>Total Scripts:</strong> {total_count}</p>"
                 f"<p><strong>Passed Scripts:</strong> {pass_count}</p>"
                 f"<p><strong>Failed Scripts:</strong> {fail_count}</p>"
                 "<table>"
                 "<tr>"
                 "<th>Result</th>"
                 "<th>Test</th>"
                 "<th>Duration</th>"
                 "<th>Log Result</th>"
                 "</tr>"
                 f"{''.join([f'<tr><td>{result}</td><td>{test}</td><td>{duration}</td><td>{log_result}</td></tr>' for result, test, duration, log_result in test_results])}"
                 "</table>"
                 f"<p><strong>Pass Percentage:</strong> {pass_percentage:.2f}%</p>"
                 f"<p><strong>Fail Percentage:</strong> {fail_percentage:.2f}%</p>"
                 "<div>"
                 "<h2>Pass/Fail Percentage</h2>"
                 "</div>"
                 "</body>"
                 "</html>")

# Generate the pie chart
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie([pass_percentage, fail_percentage], labels=['Pass', 'Fail'], autopct='%1.2f%%')
ax.set_title('Pass/Fail Ratio')

# Save the chart to a file
chart_dir = os.path.join(os.getcwd(), 'apichart')
os.makedirs(chart_dir, exist_ok=True)
chart_path = os.path.join(chart_dir, f"chart_{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}.png")
fig.savefig(chart_path)
print(f"Chart generated: {chart_path}")

# Save the chart to a file and read it as a base64-encoded string
with open(chart_path, 'rb') as f:
    chart_data = base64.b64encode(f.read()).decode()

# Generate the HTML report with the chart embedded
html_template = ("<html>"
                 "<head>"
                 "<title>Test Report</title>"
                 f"{styles}"
                 "</head>"
                 "<body>"
                 "<h1>ICP API Test Report</h1>"
                 f"<p><strong>Total Scripts:</strong> {total_count}</p>"
                 f"<p><strong>Passed Scripts:</strong> {pass_count}</p>"
                 f"<p><strong>Failed Scripts:</strong> {fail_count}</p>"
                 f"<p><strong>Pass Percentage:</strong> {pass_percentage:.2f}%</p>"
                 f"<p><strong>Fail Percentage:</strong> {fail_percentage:.2f}%</p>"
                 "<div style='text-align: center;'>"
                 f"<img src='data:image/png;base64,{chart_data}'/>"
                 "<table>"
                 "<tr>"
                 "<th>Result</th>"
                 "<th>Test</th>"
                 "<th>Duration</th>"
                 "<th>Log Result</th>"
                 "</tr>"
                 f"{''.join([f'<tr><td>{result}</td><td>{test}</td><td>{duration}</td><td>{log_result}</td></tr>' for result, test, duration, log_result in test_results])}"
                 "</table>"
                
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

