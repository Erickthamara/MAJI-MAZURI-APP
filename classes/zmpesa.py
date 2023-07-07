from kivy.app import App
from kivy.uix.label import Label
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json
import pprint
from datetime import datetime
from urllib.parse import parse_qs
import zcredentials
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import parse_qs
import base64

class MpesaClient:
    def format_time(self):
        unformatted_datetime = datetime.now()
        formatted_datetime = unformatted_datetime.strftime("%Y%m%d%H%M%S")
        return formatted_datetime

    def decode_password(self):
        pass_to_be_encoded = zcredentials.bs_shortcode + zcredentials.lnm_passkey + self.format_time()
        pass_encoded = base64.b64encode(pass_to_be_encoded.encode())
        pass_decoded = pass_encoded.decode('utf_8')
        return pass_decoded

    def generate_access_token(self):
        response = requests.get(zcredentials.acess_token_url, auth=HTTPBasicAuth(zcredentials.consumer_key, zcredentials.consumer_secrete))
        res_json = response.json()
        filtered_access_token = res_json['access_token']
        return filtered_access_token

    def initiate_stk(self):
        access_token = self.generate_access_token()
        api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {"Authorization": "Bearer %s" % access_token }

        request = {
            "BusinessShortCode": zcredentials.bs_shortcode,
            "Password": self.decode_password(),
            "Timestamp": self.format_time(),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            "PartyA": 254796892684,
            "PartyB": zcredentials.bs_shortcode,
            "PhoneNumber": 254796892684,
            "CallBackURL": "https://5c69-41-89-10-241.ngrok-free.app/payment_result/",
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
    transaction_date_str =str(payment_details.get('TransactionDate', ''))
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

        # Perform additional processing or save the data to the database
        # ...

    if 'option_name' in cache:
        del cache['option_name']
    if 'user' in cache:
        del cache['user']
    if 'user' in cache:
        del cache['user']

    return "Okay"

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        obj = MpesaClient()
        obj.initiate_stk()
        
    def build(self):
        label = Label(text="Waiting for requests...")
        

        class MyRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                response = b"<html><body><h1>Hello from Kivy!</h1></body></html>"
                self.wfile.write(response)

            def do_POST(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                response = payment_result(self)
                self.wfile.write(response.encode())
               

        server_address = ('', 8000)
        httpd = HTTPServer(server_address, MyRequestHandler)

        def start_server():
            httpd.serve_forever()

        import threading
        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()

        return label

if __name__ == '__main__':
    MyApp().run()