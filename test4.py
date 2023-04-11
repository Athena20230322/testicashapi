import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

path1 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'CreateBarcode', 'icashendurance', 'ConsoleApp1', 'bin', 'Debug', 'post1.txt')
path2 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'CreateBarcode', 'icashendurance', 'ConsoleApp1', 'bin', 'Debug', 'post2.txt')
path3 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'CreateBarcode', 'icashendurance', 'ConsoleApp1', 'bin', 'Debug', 'post3.txt')


with open(path1, 'r') as f1, open(path2, 'r') as f2, open(path3, 'r') as f3:
    enc_key_id = f1.read().strip()
    signature = f2.read().strip()
    enc_data = f3.read().strip()


url = 'https://icp-member-stage.icashpay.com.tw/app/MemberInfo/UserCodeLogin2022'


headers = {
    'X-ICP-EncKeyID': enc_key_id,
    'X-iCP-Signature': signature
}


data = {'EncData': enc_data}


response = requests.post(url, headers=headers, data=data, verify=False)
print(response)


enc_text = response.json()["EncData"]

with open("c:\\enc.txt", 'w') as f:
    f.write(enc_text)
