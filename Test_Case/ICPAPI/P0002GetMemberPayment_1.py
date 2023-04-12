import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

postData = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'CreateBarcode', 'icashendurance',
                        'ConsoleApp1', 'bin', 'Debug', 'postData2.txt')

with open(postData, 'r') as f:
    # Read the contents of the file and split into the three variables
    file_contents = f.read().strip().split(',')
    enc_key_id = file_contents[0]
    signature = file_contents[1]
    enc_data = file_contents[2]
url1 = 'https://icp-payment-stage.icashpay.com.tw/app/Payment/GetMemberPaymentInfo'

headers1 = {
    'X-ICP-EncKeyID': enc_key_id,
    'X-iCP-Signature': signature
}

data1 = {'EncData': enc_data}

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
