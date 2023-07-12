from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.factory import Factory
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.list import TwoLineAvatarIconListItem,OneLineAvatarIconListItem,IconLeftWidget,IconRightWidget
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.metrics import dp   #data pixels
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.button import MDIconButton
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty,NumericProperty
from kivymd.uix.screen import MDScreen

from .class6_sales import SalesScreen
from .class11_checkout import CheckoutScreen
from .class12_customerwater import CustomerWater
from .zmpesa import mpesa_call
from .zids_manager import CustomerIds
from .class2_login import LoginScreen
from.zdatabase import Database
from .class10_orders import OrdersScreen

import re
import datetime as dt

class PaymentScreen(OrdersScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
       # Clock.schedule_once(self.on, 0)


    def validate_phone_re(self,phone):
        pattern = r'^\d{12}$'
        if re.match(pattern, phone):
            return True
        return False

    def checkout_screen(self):
        #calls a dialog that will go back to welcomescreen
        self.manager.current = 'checkout'
        self.manager.transition.direction = 'right'

    def validate_street_name(self):
        #Here we grab the data inputed using the .strip() function
        street_name=self.ids.street_name.text.strip()
        
        if not street_name:
            self.ids.street_name_error.text="Input Required"
            self.ids.mpesa_button.disabled=True
        else:
            self.ids.street_name_error.text=""
            self.ids.mpesa_button.disabled=False

    def validate_house_name(self):
        #Here we grab the data inputed using the .strip() function
        hs_num=self.ids.hs_num.text.strip()
        
        if not hs_num:
            self.ids.hs_num_error.text="Input Required"
            self.ids.mpesa_button.disabled=True
        else:
            self.ids.hs_num_error.text=""
            self.ids.mpesa_button.disabled=False

    def validate_phone_no(self):
        #Here we grab the data inputed using the .strip() function
        phone_no=self.ids.pay_num.text.strip()
        
        if not phone_no:
            self.ids.pay_num_error.text="Phone Number Required"
            self.ids.mpesa_button.disabled=True
        elif not phone_no.startswith("254"):
            self.ids.pay_num_error.text = "Phone Number should start with 254"
            self.ids.mpesa_button.disabled = True
        elif not self.validate_phone_re(phone_no) :
            self.ids.pay_num_error.text="Invalid Phone Number"
            self.ids.mpesa_button.disabled=True
        else:
            self.ids.pay_num_error.text=""
            self.ids.mpesa_button.disabled=False
    
    def mpesa_payment(self):
        
        string=self.ids.total_amount.text
        amount = re.search(r'\d+', string).group()
        actual_amount=float(amount)
        street_name=self.ids.street_name.text.strip()
        phone_no=self.ids.pay_num.text.strip()
        hs_num=self.ids.hs_num.text.strip()

        
        if not street_name:
            self.ids.mpesa_button.disabled=True
            self.ids.street_name_error.text="Street name required"
       
        elif not phone_no:
            self.ids.mpesa_button.disabled=True
            self.ids.pay_num_error.text="Phone Number Required"
        elif not hs_num:
            self.ids.mpesa_button.disabled=True
            self.ids.street_name_error.text="House number/name required"
        else:   
            self.ids.mpesa_button.disabled=False

            result_code,data=mpesa_call(phone_no,amount)

            if result_code == 0:
                print("SUCCESS")
                print(data)
                
                

                

            elif result_code==1032:
                # If the result code is not 0, set all the results to None
                print("REQUEST HAS BEEN CANCELLED")
            elif result_code==1037:
                print("REQUEST TIMED OUT")
    def mpesa_payment2(self):
        street_name=self.ids.street_name.text.strip()
        phone_no=self.ids.pay_num.text.strip()
        hs_num=self.ids.hs_num.text.strip()

        
        string=self.ids.total_amount.text
        amount = re.search(r'\d+', string).group()

        
        if not street_name:
            self.ids.mpesa_button.disabled=True
            self.ids.street_name_error.text="Street name required"
       
        elif not phone_no:
            self.ids.mpesa_button.disabled=True
            self.ids.pay_num_error.text="Phone Number Required"
        elif not hs_num:
            self.ids.mpesa_button.disabled=True
            self.ids.street_name_error.text="House number/name required"
        else:   
            self.ids.mpesa_button.disabled=False

            order_date=dt.datetime.now().strftime('%d-%m-%Y')
            
            
            #get the items
            container=self.manager.get_screen("checkout").ids.container2
            items=[]
            amounts=[]
            for item in container.children:
                items.append(item.text)
                amounts.append(item.secondary_text.split(" ")[-1])

            # Insert items and amounts into the database
            for item, amount in zip(items, amounts):
                execute_query = "INSERT INTO maji_mazuri.order(customer_id, seller_id, ordered_item, amount, street_name, house_number, order_date) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                values = (LoginScreen.customer_id, LoginScreen.seller_id, item, amount, street_name, hs_num, order_date)
                self.cursor.execute(execute_query, values)
                self.connection.commit()
                
            

    def items(self):
        container=self.manager.get_screen("checkout").ids.container2
        items=[]
        for item in container.children:
            items.append(item.text)
        print(items)



    