import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

path7 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'GetAccountStatusInfo', 'icashendurance',
                     'ConsoleApp1', 'bin', 'Debug', 'post7.txt')
path8 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'GetAccountStatusInfo', 'icashendurance',
                     'ConsoleApp1', 'bin', 'Debug', 'post8.txt')
path9 = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'GetAccountStatusInfo', 'icashendurance',
                     'ConsoleApp1', 'bin', 'Debug', 'post9.txt')

with open(path7, 'r') as f4, open(path8, 'r') as f5, open(path9, 'r') as f6:
    enc_key_id1 = f4.read().strip()
    signature1 = f5.read().strip()
    enc_data1 = f6.read().strip()

url1 = 'https://icp-payment-stage.icashpay.com.tw/app/Payment/CreateBarcode'

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
