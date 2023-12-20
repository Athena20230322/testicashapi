import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

postData = "C:\\testicashapi\\NegativepostData\\postData2.txt"

#postData = os.path.join('C:', os.sep, 'IcashPost', 'ICPAPIVS', 'CreateBarcode', 'icashendurance',
                        #'ConsoleApp1', 'bin', 'Debug', 'postData1.txt')

with open(postData, 'r') as f:
    # Read the contents of the file and split into the three variables
    file_contents = f.read().strip().split(',')
    enc_key_id = file_contents[0]
    signature = file_contents[1]
    enc_data = file_contents[2]


url = 'https://icp-member-stage.icashpay.com.tw/MemberInfo/VerifyForgotSecurityCode'


headers = {
    'X-ICP-EncKeyID': enc_key_id,
    'X-iCP-Signature': signature
}


data = {'EncData': enc_data}


response = requests.post(url, headers=headers, data=data, verify=False)
print(response)

# Parse the JSON response and extract RtnCode, RtnMsg, and EncData
response_json = response.json()
rtn_code = response_json['RtnCode']
rtn_msg = response_json['RtnMsg']
enc_text = response_json['EncData']

# Print the values of RtnCode, RtnMsg, and EncData
print(f"RtnCode: {rtn_code}")
print(f"RtnMsg: {rtn_msg}")
#print(f"EncData: {enc_text}")


#enc_text = response.json()["EncData"]

with open("c:\\Negativeenc.txt", 'w') as f:
    f.write(enc_text)

# Validate RtnCode value
test_data_file = "C:\\testicashapi\\NegativeTest_Data\\ICPAPI\\ML211_VerifyForgotSecurityCode_1.txt"
with open(test_data_file, 'r') as f:
    file_contents = f.read()
    expected_rtn_code = None
    expected_rtn_msg = None

# 解析文件內容，取得預期的 RtnCode 和 RtnMsg
for line in file_contents.strip().split('\n'):
    key, value = line.strip().split(',')
    if key == 'RtnCode':
        expected_rtn_code = value
    elif key == 'RtnMsg':
        expected_rtn_msg = value.rstrip(',')  # Remove trailing comma

# 驗證 RtnCode 和 RtnMsg 是否都符合預期值
if expected_rtn_code == str(rtn_code) and expected_rtn_msg == rtn_msg:
    print("Test Passed")
else:
    print("Test Failed. Expected RtnCode: %s, Actual RtnCode: %s. Expected RtnMsg: %s, Actual RtnMsg: %s" % (expected_rtn_code, rtn_code, expected_rtn_msg, rtn_msg))

