import requests
import json
import pprint
from datetime import datetime
import base64
from requests.auth import HTTPBasicAuth

consumer_key = 'U3uZndIeO10CSUAyjahb6uHTTnTTA9Tx'
consumer_secret = 'lgJH0xs5hGoz5JE7'
lnm_passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
bs_shortcode = "174379"  # paybill number
access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
b2c_initiator = 'testapi'  # initiator name

class MpesaClient:
    def __init__(self):
        self.access_token = None

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
        response = requests.get(access_token_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
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
            "CallBackURL": "https://2a70-105-163-158-59.ngrok-free.app/payment_result/",
            "AccountReference": "MAJI MAZURI",
            "TransactionDesc": "Pay for goods"
        }

        response = requests.post(api_url, json=request, headers=headers)
        string_response = response.text
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

    def simulate_response(self, access_token, checkout_request_id):
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

        response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query', headers=headers, json=payload)
        print(response.text.encode('utf8'))


# Usage example
#mpesa_client = MpesaClient()
#checkout_request_id = mpesa_client.initiate_stk('25496892684', '1')  # Replace with appropriate phone number and amount
#mpesa_client.simulate_response(mpesa_client.access_token, checkout_request_id)