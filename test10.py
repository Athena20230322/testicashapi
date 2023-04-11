import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

path10 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'CreateBarcode', 'icashendurance',
                     'ConsoleApp1', 'bin', 'Debug', 'post10.txt')
path11 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'CreateBarcode', 'icashendurance',
                     'ConsoleApp1', 'bin', 'Debug', 'post11.txt')
path12 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'CreateBarcode', 'icashendurance',
                     'ConsoleApp1', 'bin', 'Debug', 'post12.txt')

with open(path10, 'r') as f4, open(path11, 'r') as f5, open(path12, 'r') as f6:
    enc_key_id1 = f4.read().strip()
    signature1 = f5.read().strip()
    enc_data1 = f6.read().strip()

url1 = 'https://icp-Member-stage.icashpay.com.tw/app/MemberInfo/GetListBankInfo'

headers1 = {
    'X-ICP-EncKeyID': enc_key_id1,
    'X-iCP-Signature': signature1
}

data1 = {'EncData': enc_data1}

response1 = requests.post(url1, headers=headers1, data=data1, verify=False)
print(response1)

try:
    enc_text1 = response1.json()["EncData"]
    print(enc_text1)

    with open("c:\\enc1.txt", 'w') as f:
        f.write(enc_text1)

except requests.exceptions.RequestException as e:
    print("Error: could not decode JSON response from server")
    print("Response content:", response1.content)
    print("Exception:", e)
