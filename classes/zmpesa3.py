import requests
import base64
from datetime import datetime

from kivy.clock import Clock
from requests.auth import HTTPBasicAuth
import asyncio

class MpesaClient():
    def __init__(self):
        self.bs_shortcode = "174379"  # paybill number
        self.lnm_passkey = ""
        self.consumer_key = ''
        self.consumer_secret = ''
        self.access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    def format_time(self):
        unformatted_datetime = datetime.now()
        formatted_datetime = unformatted_datetime.strftime("%Y%m%d%H%M%S")
        return formatted_datetime

    def decode_password(self):
        pass_to_be_encoded = self.bs_shortcode + self.lnm_passkey + self.format_time()
        pass_encoded = base64.b64encode(pass_to_be_encoded.encode())
        pass_decoded = pass_encoded.decode('utf_8')
        return pass_decoded

    def generate_access_token(self):
        response = requests.get(self.access_token_url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
        res_json = response.json()
        filtered_access_token = res_json['access_token']
        return filtered_access_token

    def initiate_stk(self,phone_number, amount):
        token = self.generate_access_token()
        timestamp = self.format_time()

        password = self.decode_password()
        headers = {
            "Authorization": "Bearer " + token,
        }
        payload = {
            "BusinessShortCode": self.bs_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.bs_shortcode,
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

    async def check_stk_push(self,checkOutId):
        token = self.generate_access_token()

        while True:
            date = datetime.now()
            timestamp = date.strftime("%Y%m%d%H%M%S")

            shortcode = self.bs_shortcode
            passkey = self.lnm_passkey
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
                    success_message = "Success"
                    receipt_number = f"Receipt Number: {checkOutId}"

                    # store data in DB or perform other executions
                    return success_message, receipt_number
                    
                    #store data in DB or perform other executions
                    
                elif response.json().get("ResultDesc") != "The service request is being processed.":
                    # if payment not successful
                   success_message = "Payment not successful"
                   receipt_number = ""

                   return success_message, receipt_number

                # Check if the response indicates user cancellation or payment
                # You can access response data here and handle user actions accordingly

            await asyncio.sleep(5)

    def main(self, phone_number, amount):
        async def inner_main():
            checkOutId = self.initiate_stk(phone_number, amount)
            if checkOutId:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = await self.check_stk_push(checkOutId)
                return result
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(inner_main())
"""
if __name__ == "__main__":
    obj=MpesaClient()
    result=obj.main("",1)
    print(result[0])
"""
