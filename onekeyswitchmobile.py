import subprocess
import time

# 定义要执行的C#应用程序的路径
app_paths = [
    r'C:\GetToken-and change mobile\ConsoleApp1\bin\Debug\ConsoleApp1.exe',
    r'C:\SendAuthSMS-and change mobile\ConsoleApp1\bin\Debug\ConsoleApp1.exe',
    r'C:\Login-and change mobile\ConsoleApp1\bin\Debug\ConsoleApp1.exe'
]

# 依序执行每个应用程序
for app_path in app_paths:
    try:
        # 使用subprocess运行C#应用程序
        subprocess.run(app_path, check=True)
        print(f'{app_path} 執行成功')

        # 延迟5秒
        time.sleep(5)
    except subprocess.CalledProcessError as e:
        print(f'{app_path} 執行失敗：{e}')
