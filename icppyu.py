import requests
import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography import x509
from urllib.parse import urlencode
import datetime
import time
import base64

key = """
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4pgu8gTfBSM1HA69jakqet6YXtyy6ChqrVuhfaYUYLoxogbcz7QGrAAB/eRc4Ft9rdoh2xC4BEqeOqYTmm4mR+EIF+d+SQXPH79DP8QoTiBvZFcfeckGBsOEFkk6W0LGqhXIKXg/pQ1wilfh1iWybBx7j5Teo3X7s6pTIf11GmL8BkjkQvdVeDX8s/bQBtKjRvLIUMROeuUEuWvq3rJP7o5E5n2tyw/IeT91Q7thoj691CQbJetZF0Nnj9pJgSw4u1EyvQDxbjRZkuh6PwRAy5Ik6sJ97ghdlrNAkFilYr8kPJoFdqf9bxNa9YpsjptahWNAGvPKViDNbyq8SuR42QIDAQAB
"""

key_bytes = key.encode('utf-8')

pem_key = "-----BEGIN PUBLIC KEY-----\n" + base64.b64encode(key_bytes).decode('utf-8') + "\n-----END PUBLIC KEY-----"

class RsaCryptoHelper:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_pem_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()
        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return {
            "PrivateKey": pem_private.decode('utf-8'),
            "PublicKey": pem_public.decode('utf-8')
        }

    def import_pem_public_key(self, pem_key: object) -> object:
        public_key = serialization.load_pem_public_key(pem_key.encode('utf-8'))
        self.public_key = public_key

    def import_pem_private_key(self, pem_key):
        private_key = serialization.load_pem_private_key(pem_key.encode('utf-8'), password=None)
        self.private_key = private_key

    def encrypt(self, plaintext):
        ciphertext = self.public_key.encrypt(
            plaintext.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext.hex()

    def decrypt(self, ciphertext):
        plaintext = self.private_key.decrypt(
            bytes.fromhex(ciphertext),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode('utf-8')

    def sign_data(self, data):
        signature = self.private_key.sign(
            data.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature.hex()

    def verify_sign(self, data, signature):
        try:
            self.public_key.verify(
                bytes.fromhex(signature),
                data.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except:
            return False


class AesCryptoHelper:
    def __init__(self):
        self.key = None
        self.iv = None

    def encrypt(self, plaintext):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
        return ciphertext.hex()

    def decrypt(self, ciphertext):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(bytes.fromhex(ciphertext)) + decryptor.finalize()
        return plaintext.decode('utf-8')


rsa_helper = RsaCryptoHelper()
aes_helper = AesCryptoHelper()

http_client = requests.Session()
http_client.base_url = 'https://icp-member-stage.icashpay.com.tw/'
server_public_key = None
client_private_key = None
client_public_key = None
aes_client_cert_id = None
aes_key = None
aes_iv = None


def get_default_puc_cert():
    url = "https://icp-member-stage.icashpay.com.tw/api/member/Certificate/GetDefaultPucCert"

    resp = http_client.post(url)
    resp_json = resp.json()

    cert_id = resp_json['DefaultPubCertID']
    public_key = resp_json['DefaultPubCert']

    return cert_id, public_key


def exchange_puc_cert():
    default_cert_id, default_public_key = get_default_puc_cert()
    print(default_public_key)
    default_public_key = get_default_puc_cert()

    try:
        rsa_helper.import_pem_public_key(default_public_key)
    except ValueError as e:
        print(f"Error importing public key: {e}")
        return None

    keys = rsa_helper.generate_pem_key()
    client_private_key = keys['PrivateKey']
    client_public_key = keys['PublicKey']
    print(client_public_key)

    # Create the client's public key PEM format
    client_public_pem = """
     -----BEGIN PUBLIC KEY-----
      {}
      -----END PUBLIC KEY-----
      """.format(client_public_key)

    try:
        rsa_helper.import_pem_public_key(default_public_key)
    except ValueError as e:
        print(f"Error importing public key: {e}")
        return None  # Return None or an appropriate error value

    enc_data = rsa_helper.encrypt(json.dumps({
        'ClientPubCert': client_public_key,
        'Timestamp': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    }))

    rsa_helper.import_pem_private_key(client_private_key)
    signature = rsa_helper.sign_data(enc_data)

    headers = {
        'X-iCP-DefaultPubCertID': default_cert_id,
        'X-iCP-Signature': signature
    }
    data = {'EncData': enc_data}

    url = "https://icp-member-stage.icashpay.com.tw/api/member/Certificate/ExchangePucCert"
    resp = http_client.post(url, data=data, headers=headers)
    resp_json = resp.json()

    if resp_json['RtnCode'] != 1:
        raise Exception(resp_json['RtnMsg'])

    enc_data = resp_json['EncData']
    rsa_helper.import_pem_private_key(client_private_key)
    resp_data = rsa_helper.decrypt(enc_data)
    resp_obj = json.loads(resp_data)

    global server_public_key
    server_public_key = resp_obj['ServerPubCert']

    return server_public_key


def generate_aes():
    exchange_puc_cert_result = exchange_puc_cert()

    if exchange_puc_cert_result is not None:
        try:
            rsa_helper.import_pem_public_key(exchange_puc_cert_result.get('ServerPubCert', ''))
            enc_data = rsa_helper.encrypt(json.dumps({
                'Timestamp': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            }))

            rsa_helper.import_pem_private_key(client_private_key)
            signature = rsa_helper.sign_data(enc_data)

            headers = {
                'X-iCP-ServerPubCertID': exchange_puc_cert_result.get('ServerPubCertID', ''),
                'X-iCP-Signature': signature
            }
            data = {'EncData': enc_data}

            url = "https://icp-member-stage.icashpay.com.tw/api/member/Certificate/GenerateAES"
            resp = http_client.post(url, data=data, headers=headers)
            resp_json = resp.json()

            if resp_json.get('RtnCode', 0) != 1:
                raise Exception(resp_json.get('RtnMsg', 'Unknown error'))

            enc_data = resp_json.get('EncData', '')
            rsa_helper.import_pem_private_key(client_private_key)
            resp_data = rsa_helper.decrypt(enc_data)
            resp_obj = json.loads(resp_data)

            global aes_client_cert_id, aes_key, aes_iv
            aes_client_cert_id = resp_obj.get('EncKeyID', '')

            # Ensure that the aes_key and aes_iv are bytes
            aes_key = bytes.fromhex(resp_obj.get('AES_Key', ''))
            aes_iv = bytes.fromhex(resp_obj.get('AES_IV', ''))
        except Exception as e:
            print(f"An error occurred during AES generation: {e}")
    else:
        print("Error during exchange_puc_cert. Unable to proceed.")


def call_normal_api(url, data):
    aes_helper.key = aes_key
    aes_helper.iv = aes_iv

    enc_data = aes_helper.encrypt(json.dumps(data))

    rsa_helper.import_pem_private_key(client_private_key)
    signature = rsa_helper.sign_data(enc_data)

    headers = {
        'X-iCP-EncKeyID': aes_client_cert_id,
        'X-iCP-Signature': signature
    }

    resp = http_client.post(url, data={'EncData': enc_data}, headers=headers)
    resp_json = resp.json()

    if resp_json['RtnCode'] != 1:
        raise Exception(resp_json['RtnMsg'])

    enc_data = resp_json['EncData']
    dec_data = aes_helper.decrypt(enc_data)

    rsa_helper.import_pem_public_key(server_public_key)
    if not rsa_helper.verify_sign(resp.text, resp.headers['X-iCP-Signature']):
        raise Exception('簽章驗證失敗')

    return json.loads(dec_data)


generate_aes()

data = {
    'Timestamp': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    'CellPhone': '0977007001'
}

url = "https://icp-member-stage.icashpay.com.tw/app/MemberInfo/RefreshLoginToken"
result = call_normal_api(url, data)
print(result)