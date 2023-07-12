import requests
import base64
from datetime import datetime

from kivy.clock import Clock
from requests.auth import HTTPBasicAuth
import asyncio

amount = 1
phone_number = "254796892684"
bs_shortcode = "174379"  # paybill number
lnm_passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
consumer_key = 'U3uZndIeO10CSUAyjahb6uHTTnTTA9Tx'
consumer_secret = 'lgJH0xs5hGoz5JE7'

access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

def format_time():
    unformatted_datetime = datetime.now()
    formatted_datetime = unformatted_datetime.strftime("%Y%m%d%H%M%S")
    return formatted_datetime

def decode_password():
    pass_to_be_encoded = bs_shortcode + lnm_passkey + format_time()
    pass_encoded = base64.b64encode(pass_to_be_encoded.encode())
    pass_decoded = pass_encoded.decode('utf_8')
    return pass_decoded

def generate_access_token():
    response = requests.get(access_token_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    res_json = response.json()
    filtered_access_token = res_json['access_token']
    return filtered_access_token

def initiate_stk(phone_number, amount):
    token = generate_access_token()
    timestamp = format_time()

    password = decode_password()
    headers = {
        "Authorization": "Bearer " + token,
    }
    payload = {
        "BusinessShortCode": bs_shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": bs_shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://ba27-41-212-28-227.ngrok-free.app",
        "AccountReference": "Cancer Support System",
        "TransactionDesc": "Payment of Appointment",
    }

    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers=headers
    )

    if response.status_code == 200:
        checkOutId = response.json().get("CheckoutRequestID")
        return checkOutId
    else:
        print(response.text)
        return None

async def check_stk_push(checkOutId):
    token = generate_access_token()

    while True:
        date = datetime.now()
        timestamp = date.strftime("%Y%m%d%H%M%S")

        shortcode = bs_shortcode
        passkey = lnm_passkey
        password = base64.b64encode((shortcode + passkey + timestamp).encode()).decode()

        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkOutId,
        }

        headers = {
            "Authorization": "Bearer " + token,
        }

        response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query",
            json=payload,
            headers=headers
        )

        if response.status_code == 200:
            if response.json().get("ResultDesc") == "The service request is processed successfully.":
                # if payment successful
                print("Success")
                break
            else:
                # if payment not successful
                print("Payment not successful")

            # Check if the response indicates user cancellation or payment
            # You can access response data here and handle user actions accordingly

        await asyncio.sleep(5)

async def main():
    checkOutId = initiate_stk(phone_number, amount)
    if checkOutId:
        await check_stk_push(checkOutId)

# Run the event loop
asyncio.run(main())