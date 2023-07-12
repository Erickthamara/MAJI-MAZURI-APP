from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json
import pprint
from datetime import datetime
from urllib.parse import parse_qs

import requests
from requests.auth import HTTPBasicAuth
import urllib
from urllib.parse import parse_qs
import base64

consumer_key = 'U3uZndIeO10CSUAyjahb6uHTTnTTA9Tx'
consumer_secrete = 'lgJH0xs5hGoz5JE7'
lnm_passkey ="bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
bs_shortcode ="174379" # paybill number
acess_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
b2c_initiator = 'testapi' # initiator name
mon="asxasxasdashdaschabachdbcdhcsdcdccsdcsd"
mon2="ascasbcascbascjhcbajhcbasxchbascbas"
class MpesaClient:
    def format_time(self):
        unformatted_datetime = datetime.now()
        formatted_datetime = unformatted_datetime.strftime("%Y%m%d%H%M%S")
        return formatted_datetime

    def decode_password(self):
        pass_to_be_encoded = bs_shortcode + lnm_passkey + self.format_time()
        pass_encoded = base64.b64encode(pass_to_be_encoded.encode())
        pass_decoded = pass_encoded.decode('utf_8')
        return pass_decoded

    def generate_access_token(self):
        response = requests.get(acess_token_url, auth=HTTPBasicAuth(consumer_key, consumer_secrete))
        res_json = response.json()
        filtered_access_token = res_json['access_token']
        return filtered_access_token

    def initiate_stk(self, phone_number, amount):
        access_token = self.generate_access_token()
        api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {"Authorization": "Bearer %s" % access_token }

        request = {
            "BusinessShortCode": bs_shortcode,
            "Password": self.decode_password(),
            "Timestamp": self.format_time(),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": bs_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://0e6a-105-163-158-59.ngrok-free.app/",
            "AccountReference": "MAJI MAZURI",
            "TransactionDesc": "Pay for goods"
        }

        response = requests.post(api_url, json=request, headers=headers)
        if response.status_code == 200:
            string_response = response.text
            try:
                data_object = json.loads(string_response)
                merchant_request_id = data_object["MerchantRequestID"]
                checkout_request_id = data_object["CheckoutRequestID"]
                response_code = data_object["ResponseCode"]
                response_description = data_object["ResponseDescription"]
                customer_message = data_object["CustomerMessage"]

                data = {
                    "MerchantRequestID": merchant_request_id,
                    "CheckoutRequestID": checkout_request_id,
                    "ResponseCode": response_code,
                    "ResponseDescription": response_description,
                    "CustomerMessage": customer_message,
                }

                pprint.pprint(data)
                return data
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}")
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Response content: {response.text}")
    def simulate_response(self, access_token, checkout_request_id, simulate_success=True):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        }

        payload = {
            "BusinessShortCode": bs_shortcode,
            "Password": self.decode_password(),
            "Timestamp": self.format_time(),
            "CheckoutRequestID": checkout_request_id,
        }

        if simulate_success:
            # Simulate a successful response
            response = {
                "MerchantRequestID": checkout_request_id,
                "ResultCode": 0,
                "ResultDesc": "Success",
                "CallbackMetadata": {
                    "Item": [
                        {
                            "Name": "Amount",
                            "Value": "1"
                        },
                        {
                            "Name": "MpesaReceiptNumber",
                            "Value": "ABC123"
                        },
                        {
                            "Name": "TransactionDate",
                            "Value": "2023-07-11 23:30:45"
                        }
                    ]
                }
            }
        else:
            # Simulate an error response
            response = {
                "requestId": checkout_request_id,
                "errorCode": "500.001.1001",
                "errorMessage": "Error processing the transaction"
            }

        response = json.dumps(response)
        response = response.encode('utf-8')

        url = 'https://0e6a-105-163-158-59.ngrok-free.app/'  # Replace with your callback URL
        req = urllib.request.Request(url, data=response, headers=headers)
        urllib.request.urlopen(req)


#obj = MpesaClient()
#response_data = obj.initiate_stk("254796892684", 1)  # Call initiate_stk to get response data
#obj.simulate_response(obj.generate_access_token(), response_data["CheckoutRequestID"], simulate_success=False)


