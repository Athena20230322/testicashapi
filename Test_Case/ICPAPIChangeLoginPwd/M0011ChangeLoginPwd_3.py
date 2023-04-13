import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

postData = os.path.join('C:', os.sep, 'Final_IcashEndurance', 'icash', 'M0011ChangeLoginPwd', 'icashendurance',
                        'ConsoleApp1', 'bin', 'Debug', 'postData3.txt')

with open(postData, 'r') as f:
    # Read the contents of the file and split into the three variables
    file_contents = f.read().strip().split(',')
    enc_key_id = file_contents[0]
    signature = file_contents[1]
    enc_data = file_contents[2]


url = 'https://icp-member-stage.icashpay.com.tw/app/MemberInfo/ChangeLoginPwd'


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
