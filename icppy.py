import requests
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import datetime
import unittest
from urllib.parse import urljoin




class CertificateApiTest(unittest.TestCase):

    def setUp(self):
        self.http_client = requests.Session()
        self.http_client.base_url = 'https://icp-member-stage.icashpay.com.tw/'
        self.rsa_crypto_helper = RsaCryptoHelper()
        self.aes_crypto_helper = AesCryptoHelper()
        self.server_public_key = None
        self.client_public_key = None
        self.client_private_key = None
        self.aes_client_cert_id = -1
        self.aes_key = None
        self.aes_iv = None

    def test_get_default_puc_cert(self):
        cert_id, public_key = self.get_default_puc_cert()
        self.assertGreater(cert_id, 0)
        self.assertIsNotNone(public_key)

    def test_exchange_puc_cert(self):
        result, self.client_private_key = self.exchange_puc_cert()
        self.assertEqual(result.rtn_code, 1)
        self.assertIsNotNone(self.client_private_key)

    def test_generate_aes(self):
        self.generate_aes()
        self.assertGreater(self.aes_client_cert_id, 0)
        self.assertIsNotNone(self.aes_key)
        self.assertIsNotNone(self.aes_iv)

    def call_certificate_api(self, action, cert_id, server_public_key, client_private_key, obj, cert_header_name):
        json_data = json.dumps(obj)
        encrypted_data = self.rsa_crypto_helper.encrypt(json_data, server_public_key)
        signature = self.rsa_crypto_helper.sign(encrypted_data, client_private_key)
        url = urljoin(self.http_client.base_url, action)

        headers = {
            cert_header_name: str(cert_id),
            'X-iCP-Signature': signature
        }

        #response = self.http_client.post(action, data={'EncData': encrypted_data}, headers=headers)
        response = self.http_client.post(url, data={'EncData': encrypted_data}, headers=headers)
        result = response.json()
        signature = response.headers['X-iCP-Signature']

        return result, signature

    def test_get_cellphone(self):
        self.generate_aes()

        url = "/app/MemberInfo/RefreshLoginToken"

        request = {
            "Timestamp": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            "CellPhone": "0977007001"
        }

        response = self.call_normal_api(url, request)

        print(response)

    def check_timestamp(self, timestamp):
        dt = datetime.datetime.strptime(timestamp, "%Y/%m/%d %H:%M:%S")
        delta = abs((dt - datetime.datetime.now()).total_seconds())
        if delta > 30:
            raise Exception('Timestamp error')

    def get_default_puc_cert(self):

        url = '/api/member/Certificate/GetDefaultPucCert'
        result, _ = self.call_certificate_api(url, 0, '', '', {}, 'X-iCP-DefaultPubCertID')

        cert_id = result['DefaultPubCertID']
        public_key = result['DefaultPubCert']

        return cert_id, public_key

    def exchange_puc_cert(self):
        cert_id, server_public_key = self.get_default_puc_cert()

        client_private_key, client_public_key = self.rsa_crypto_helper.generate_key_pair()

        request = {
            'ClientPubCert': client_public_key,
            'Timestamp': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        }

        url = '/api/member/Certificate/ExchangePucCert'
        result, _ = self.call_certificate_api(url, cert_id, server_public_key,
                                              client_private_key, request,
                                              'X-iCP-DefaultPubCertID')

        exchange_result = self.rsa_crypto_helper.decrypt(result['EncData'], client_private_key)
        exchange_result = json.loads(exchange_result)

        self.server_public_key = exchange_result['ServerPubCert']

        self.check_timestamp(exchange_result['Timestamp'])

        return exchange_result, client_private_key

    def generate_aes(self):
        result, client_private_key = self.exchange_puc_cert()

        request = {
            'Timestamp': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        }

        url = '/api/member/Certificate/GenerateAES'
        result, _ = self.call_certificate_api(url, result['ServerPubCertID'],
                                              self.server_public_key, client_private_key,
                                              request, 'X-iCP-ServerPubCertID')

        aes_result = self.rsa_crypto_helper.decrypt(result['EncData'], client_private_key)
        aes_result = json.loads(aes_result)

        self.check_timestamp(aes_result['Timestamp'])

        self.aes_client_cert_id = aes_result['EncKeyID']
        self.aes_key = aes_result['AES_Key']
        self.aes_iv = aes_result['AES_IV']

    def call_normal_api(self, url, obj):
        json_data = json.dumps(obj)
        encrypted_data = self.aes_crypto_helper.encrypt(json_data, self.aes_key, self.aes_iv)
        signature = self.rsa_crypto_helper.sign(encrypted_data, self.client_private_key)

        headers = {
            'X-iCP-EncKeyID': str(self.aes_client_cert_id),
            'X-iCP-Signature': signature
        }

        response = self.http_client.post(url, data={'EncData': encrypted_data}, headers=headers)
        result = response.json()
        signature = response.headers['X-iCP-Signature']

        self.rsa_crypto_helper.verify(result, signature, self.server_public_key)

        decrypted_data = self.aes_crypto_helper.decrypt(result['EncData'], self.aes_key, self.aes_iv)

        self.check_timestamp(json.loads(decrypted_data)['Timestamp'])

        return result


class RsaCryptoHelper:

    def generate_key_pair(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()

        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return pem_private, pem_public

    def encrypt(self, data, public_key):
        public_key = public_key.encode('utf-8')
        try:
            public_key = serialization.load_pem_public_key(public_key)
        except ValueError as e:
            print("Error loading public key: ", e)
            return

        public_key = serialization.load_pem_public_key(public_key)

        encrypted = public_key.encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt(self, encrypted_data, private_key):
        private_key = serialization.load_pem_private_key(
            private_key,
            password=None
        )
        decrypted = private_key.decrypt(
            base64.b64decode(encrypted_data),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode('utf-8')

    def sign(self, data, private_key):

        # 添加这一行,转换为bytes类型
        private_key = private_key.encode('utf-8')

        try:
            private_key = serialization.load_pem_private_key(
                private_key,
                password=None
            )
        except ValueError as e:
            print("Loading private key error:", e)
            return

        signature = private_key.sign(
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return base64.b64encode(signature).decode('utf-8')
    def verify(self, data, signature, public_key):
        public_key = serialization.load_pem_public_key(public_key)
        try:
            public_key.verify(
                base64.b64decode(signature),
                data.encode(),
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

    def encrypt(self, data, key, iv):
        cipher = Cipher(algorithms.AES(base64.b64decode(key)), modes.CBC(base64.b64decode(iv)))
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(data.encode()) + encryptor.finalize()
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt(self, encrypted_data, key, iv):
        cipher = Cipher(algorithms.AES(base64.b64decode(key)), modes.CBC(base64.b64decode(iv)))
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(base64.b64decode(encrypted_data)) + decryptor.finalize()
        return decrypted.decode('utf-8')


test = CertificateApiTest()
test.setUp()
test.test_get_default_puc_cert()
test.test_exchange_puc_cert()
test.test_generate_aes()