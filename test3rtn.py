import os
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

#禁用警告信息
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#定義三個路徑變數
path1 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'LoginaccountGetMemberPaymentInfo', 'icashendurance', 'ConsoleApp1', 'bin', 'Debug', 'post1.txt')
path2 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'LoginaccountGetMemberPaymentInfo', 'icashendurance', 'ConsoleApp1', 'bin', 'Debug', 'post2.txt')
path3 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'LoginaccountGetMemberPaymentInfo', 'icashendurance', 'ConsoleApp1', 'bin', 'Debug', 'post3.txt')

#使用with開啟三個檔案，並取得檔案內容
with open(path1, 'r') as f1, open(path2, 'r') as f2, open(path3, 'r') as f3:
    enc_key_id = f1.read().strip()
    signature = f2.read().strip()
    enc_data = f3.read().strip()

#設定要請求的URL與請求標頭
url = 'https://icp-member-stage.icashpay.com.tw/app/Payment/GetMemberPaymentInfo'

headers = {
'X-ICP-EncKeyID': enc_key_id,
'X-iCP-Signature': signature
}

#設定要傳送的資料
data = {'EncData': enc_data}

#透過requests模組，撰寫POST請求傳送資料給伺服器，並忽略證書驗證
response = requests.post(url, headers=headers, data=data, verify=False)

print(response)
print("123123")
enc_text = ""  # 定義一個初始值

try:
    enc_text = response.json()["EncData"]
except json.JSONDecodeError as e:
    print(f"Failed to decode JSON: {e}")

with open("c:\\enc.txt", 'w') as f:
    f.write(enc_text)
