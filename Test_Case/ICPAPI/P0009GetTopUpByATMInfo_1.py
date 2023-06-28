import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

postData = "C:\\postData\\postData31.txt"

with open(postData, 'r') as f:
    file_contents = f.read().strip().split(',')
    enc_key_id = file_contents[0]
    signature = file_contents[1]
    enc_data = file_contents[2]

url1 = 'https://icp-payment-stage.icashpay.com.tw/app/TopUpPayment/GetTopUpByATMInfo'

headers1 = {
    'X-ICP-EncKeyID': enc_key_id,
    'X-iCP-Signature': signature
}

data1 = {'EncData': enc_data}

response1 = requests.post(url1, headers=headers1, data=data1, verify=False)
print(response1)

response_json = response1.json()
rtn_code = response_json['RtnCode']
rtn_msg = response_json['RtnMsg']
enc_text = response_json['EncData']

print(f"RtnCode: {rtn_code}")
print(f"RtnMsg: {rtn_msg}")

with open("c:\\enc1.txt", 'w') as f:
    f.write(enc_text)



# Validate RtnCode value
test_data_file = "C:\\testicashapi\\Test_Data\\ICPAPI\\P0009GetTopUpByATMInfo_1.txt"
with open(test_data_file, 'r') as f:
    file_contents = f.read()
    expected_rtn_code = file_contents.strip().split(',')[1]

if expected_rtn_code == str(rtn_code):
    print("Test Passed")
else:
    print("Test Failed. Expected RtnCode: %s. Actual RtnCode: %s" % (expected_rtn_code, rtn_code))


