import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
#禁用警告信息
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#定義三個路徑變數
path1 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'Loginaccountchange', 'icashendurance', 'ConsoleApp1', 'bin', 'Debug', 'post1.txt')
path2 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'Loginaccountchange', 'icashendurance', 'ConsoleApp1', 'bin', 'Debug', 'post2.txt')
path3 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'Loginaccountchange', 'icashendurance', 'ConsoleApp1', 'bin', 'Debug', 'post3.txt')
#使用with開啟三個檔案，並取得檔案內容
with open(path1, 'r') as f1, open(path2, 'r') as f2, open(path3, 'r') as f3:
    enc_key_id = f1.read().strip()
    signature = f2.read().strip()
    enc_data = f3.read().strip()

#設定要請求的URL與請求標頭
url = 'https://icp-member-stage.icashpay.com.tw/app/MemberInfo/UserCodeLogin2022'

headers = {
'X-ICP-EncKeyID': enc_key_id,
'X-iCP-Signature': signature
}
#設定要傳送的資料

data = {'EncData': enc_data}
#透過requests模組，撰寫POST請求傳送資料給伺服器，並忽略證書驗證

response = requests.post(url, headers=headers, data=data, verify=False)

#印出伺服器回應的內容

#print(response.text)

# Verify the server's response content and check the RtnCode value
if response.ok and "RtnCode\":1" in response.text:
    print("Server response: success")
else:
    print("Server response: error")