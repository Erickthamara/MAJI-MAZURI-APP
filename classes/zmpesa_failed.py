from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json
import pprint
from datetime import datetime
from urllib.parse import parse_qs

import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import parse_qs
import base64

consumer_key = ''
consumer_secrete = ''
lnm_passkey =""
bs_shortcode ="174379" # paybill number
acess_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
b2c_initiator = 'testapi' # initiator name
mon=""
mon2=""
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
            "CallBackURL": "https://bfb0-41-89-10-241.ngrok-free.app/",
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

        pprint.pprint(data)
        return data

cache = {}

def payment_result(request):
    content_length = int(request.headers['Content-Length'])
    body = request.rfile.read(content_length).decode('utf-8')
    params = json.loads(body)

    result_code = int(params['Body']['stkCallback']['ResultCode'])
    option_name = cache.get('option_name')
    user = cache.get('user')

    if 'CallbackMetadata' in params['Body']['stkCallback']:
        callback_metadata = params['Body']['stkCallback']['CallbackMetadata']['Item']
        # Extract the payment details from CallbackMetadata
        payment_details = {}
        for item in callback_metadata:
            name = item['Name']
            value = item.get('Value')
            if value is not None:
                payment_details[name] = value
    else:
        payment_details = {}

    returned_amount = float(payment_details.get('Amount', 0))
    receipt_number = payment_details.get('MpesaReceiptNumber', '')
    transaction_date_str = str(payment_details.get('TransactionDate', ''))
    phone_number = payment_details.get('PhoneNumber', '')

    if transaction_date_str:
        transaction_date = datetime.strptime(transaction_date_str, "%Y%m%d%H%M%S")
    else:
        transaction_date = None

    if result_code == 0:
        if option_name is not None:
            print("Option Name:", option_name)
        
        if returned_amount != 0.0:
            print("Returned Amount:", returned_amount)
        
        if receipt_number:
            print("Receipt Number:", receipt_number)
        
        if transaction_date is not None:
            print("Transaction Date:", transaction_date)
      
        if phone_number:
            print("Phone Number:", phone_number)
        

    elif result_code==1032:
        # If the result code is not 0, set all the results to None
        print("REQUEST HAS BEEN CANCELLED")
    elif result_code==1037:
        print("REQUEST TIMED OUT")


        # Perform additional processing or save the data to the database
        # ...

    if 'option_name' in cache:
        del cache['option_name']
    if 'user' in cache:
        del cache['user']
    if 'user' in cache:
        del cache['user']

    return "Okay"

def start_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyRequestHandler)
    httpd.handle_request()

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        response = b"<html><body><h1>Hello from Kivy!</h1></body></html>"
        self.wfile.write(response)
        # Stop the server after sending the response
        self.server.shutdown()

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        response = payment_result(self)
        self.wfile.write(response.encode())

def mpesa_call(phone_number,pay_amount):
    obj = MpesaClient()
    phn_number = phone_number  # Replace with the desired phone number
    amount = pay_amount  # Replace with the desired amount
    obj.initiate_stk(phn_number, amount)
    start_server()
    #print("working")



#mpesa_call("",1)
