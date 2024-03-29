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
import smtplib
from email.mime.text import MIMEText

from .class6_sales import SalesScreen
from .class11_checkout import CheckoutScreen
from .class12_customerwater import CustomerWater
from .zmpesa_failed import mpesa_call
from .zids_manager import CustomerIds
from .class2_login import LoginScreen
from.zdatabase import Database
from .class10_orders import OrdersScreen
from .zmpesa3 import MpesaClient

from kivymd.uix.list import ThreeLineIconListItem,IconLeftWidget

import re
import datetime as dt

class PaymentScreen(CustomerWater):
    dialog21=None
    dialog20=None
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

            obj=MpesaClient()

            result=obj.main(phone_no,amount)
            message,receipt_number=result
            if message=="Success":
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
                    order_status="Live"
                    execute_query = "INSERT INTO maji_mazuri.order(customer_id, seller_id, ordered_item, amount, street_name, house_number, order_date,order_status) VALUES (%s, %s,%s, %s, %s, %s, %s, %s);"
                    values = (LoginScreen.customer_id, LoginScreen.seller_id, item, amount, street_name, hs_num, order_date,order_status)
                    self.cursor.execute(execute_query, values)
                    self.connection.commit()

                    #adding the item to the order list
                    item = ThreeLineIconListItem(
                        IconLeftWidget(icon="order-bool-descending-variant"),
                        text=item,
                        secondary_text="Ksh: " + amount,
                        tertiary_text=order_date
                    )
                    self.widget_list.append(item)
                    #self.widget_list.reverse()
                    container = self.manager.get_screen("customerbrowse").ids.order_container
                    container.clear_widgets()
                    for widget in self.widget_list:
                        container.add_widget(widget)
                self.alert_dialog_order()
                    # Generate receipt content
                receipt_content = f"Receipt Number: {receipt_number}\n"
                receipt_content += f"Order Date: {order_date}\n"
                receipt_content += f"Street Name: {street_name}\n"
                receipt_content += f"House Number: {hs_num}\n\n"
                receipt_content += "Items:\n"
                for item, amount in zip(items, amounts):
                    receipt_content += f"- {item} - Ksh: {amount}\n"
                receipt_content += "\nTotal Amount: Ksh " + amount
                self.cursor.execute(f"SELECT customer_email FROM maji_mazuri.customer WHERE customer_id={LoginScreen.customer_id};")
                email=self.cursor.fetchone()
                
                # Send receipt via email
                sender_email = ''  # Replace with your email address
                sender_password = ''  # Replace with your email password
                receiver_email = email[0]
                subject = "MAJI MAZURI Receipt for Order completed."
                message = MIMEText(receipt_content)
                message["Subject"] = subject
                message["From"] = sender_email
                message["To"] = receiver_email

                try:
                    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
                    smtp_obj.ehlo()
                    smtp_obj.starttls()
                    smtp_obj.login(sender_email, sender_password)
                    smtp_obj.sendmail(sender_email, receiver_email, message.as_string())
                    smtp_obj.quit()
                    #print("Receipt sent successfully!")
                except smtplib.SMTPException:
                    print("Failed to send receipt.")

            elif message=="Payment not successful":
                self.alert_dialog_order_failed()
    

            
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

                #adding the item to the order list
                item = ThreeLineIconListItem(
                    IconLeftWidget(icon="order-bool-descending-variant"),
                    text=item,
                    secondary_text="Ksh: " + amount,
                    tertiary_text=order_date
                )
                self.widget_list.append(item)
                #self.widget_list.reverse()
                container = self.manager.get_screen("customerbrowse").ids.order_container
                container.clear_widgets()
                for widget in self.widget_list:
                    container.add_widget(widget)


            

                
    def load_customer_container(self):
        #this loads up all transactions alareday in the database
        #called from seller.py LINE 76 by 
        self.widget_list=[]

        if LoginScreen.customer_id:

            self.cursor.execute(f"SELECT ordered_item,amount,order_date FROM maji_mazuri.order WHERE customer_id={LoginScreen.customer_id} ORDER BY order_id DESC")
            reports=self.cursor.fetchall()

            for row in reports:
                item = ThreeLineIconListItem(
                    IconLeftWidget(icon="order-bool-descending-variant"),
                    text=row[0],
                    secondary_text="Ksh: " + str(row[1]),
                    tertiary_text=row[2]
                )
                self.widget_list.append(item)
            #self.widget_list.reverse()
            container = self.manager.get_screen("customerbrowse").ids.order_container
            container.clear_widgets()
            for widget in self.widget_list:
                container.add_widget(widget)

    def update_customer_container(self):
        container = self.manager.get_screen("customerbrowse").ids.order_container
        container.clear_widgets()
        for widget in self.widget_list:
            container.add_widget(widget)
    
    def alert_dialog_order(self):
          
          if not self.dialog21:
                self.dialog21 = MDDialog(
                    title="ORDER SUCCESS",
                    text="You will receive the receipt in the mail.",
                    radius=[20,7,20,7],
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_press=self.dismiss_dialog21,   
                        ),
                    ],
                )
          self.dialog21.open()

    def dismiss_dialog21(self, instance):
        self.dialog21.dismiss()
    def alert_dialog_order_failed(self):
          
          if not self.dialog20:
                self.dialog20 = MDDialog(
                    title="FAILED.Request cancelled",
                    
                    radius=[20,7,20,7],
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_press=self.dismiss_dialog20,   
                        ),
                    ],
                )
          self.dialog20.open()

    def dismiss_dialog20(self, instance):
        self.dialog20.dismiss()


   



    
