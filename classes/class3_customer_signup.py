import re
from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.dialog import MDDialog

from .zdatabase import Database
from .zids_manager import CustomerIds
import datetime as dt


class CustomerSignupScreen(Screen,Database):
     #This are all the methods used in the signup screen backend
    dialog6=None
    def validate_email_re(self,email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern,email):
            return True
        return False
    
    def validate_phone_re(self,phone):
        pattern = r'^\d{10}$'
        if re.match(pattern, phone):
            return True
        return False
    
    def validate_password_re(self,password):
        # Add your password validation rules here
        if len(password) >= 8 and re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return True
        else:
            return False
     
    

    def validate_customer_email2(self):
        #Here we grab the data inputed using the .strip() function
        email=self.ids.email_customer_signup.text.strip()
       

        if not email:
            self.ids.email_customer_signup_error.text="Email is Required"
            self.ids.submit_button3.disabled=True
        elif not self.validate_email_re(email):
            self.ids.email_customer_signup_error.text="Invalid Email"
            self.ids.submit_button3.disabled=True
       
        else:
            self.ids.email_customer_signup_error.text=""
            self.ids.submit_button3.disabled=False

        

    def validate_phone_no(self):
        #Here we grab the data inputed using the .strip() function
        phone_no=self.ids.customer_phone_no.text.strip()
        
        if not phone_no:
            self.ids.customer_phone_no_error.text="Phone Number Required"
            self.ids.submit_button3.disabled=True
        elif not self.validate_phone_re(phone_no) :
            self.ids.customer_phone_no_error.text="Invalid Phone Number"
            self.ids.submit_button3.disabled=True
        else:
            self.ids.customer_phone_no_error.text=""
            self.ids.submit_button3.disabled=False

    def validate_first_name(self):
        #Here we grab the data inputed using the .strip() function
        first_name=self.ids.customer_first_name.text.strip()
        
        if not first_name:
            self.ids.customer_first_name_error.text="Input Required"
            self.ids.submit_button3.disabled=True
        elif self.ids.customer_first_name.text.isalpha()==False:
            self.ids.customer_first_name_error.text="Incorrect Input"
            self.ids.submit_button3.disabled=True
        else:
            self.ids.customer_first_name_error.text=""
            self.ids.submit_button3.disabled=False

    def validate_last_name(self):
        #Here we grab the data inputed using the .strip() function
        last_name=self.ids.customer_last_name.text.strip()
        
        if not last_name:
            self.ids.customer_last_name_error.text="Input Required"
            self.ids.submit_button3.disabled=True
        elif self.ids.customer_last_name.text.isalpha()==False:
            self.ids.customer_last_name_error.text="Incorrect Input"
            self.ids.submit_button3.disabled=True
        else:
            self.ids.customer_last_name_error.text=""
            self.ids.submit_button3.disabled=False

    def validate_password2(self):
        #Here we grab the data inputed using the .strip() function
        password2=self.ids.customer_pswd_signup.text.strip()
        if not password2:
            self.ids.customer_pswd_signup_error.text="Password is Required"
            self.ids.submit_button3.disabled=True
        elif not self.validate_password_re(password2):
            self.ids.customer_pswd_signup_error.text="Should have 8 characters and a special character" 
            self.ids.submit_button3.disabled=True
        else:
            self.ids.customer_pswd_signup_error.text=""
            self.ids.submit_button3.disabled=False


    def validate_password3(self):
        #Here we grab the data inputed using the .strip() function
        password3=self.ids.customer_pswd_confirm.text.strip()
        if not password3:
            self.ids.customer_pswd_confirm_error.text="Password is Required"
            self.ids.submit_button3.disabled=True
        elif not self.validate_password_re(password3):
            self.ids.customer_pswd_confirm_error.text="Should have 8 characters and a special character" 
            self.ids.submit_button3.disabled=True
        elif self.ids.customer_pswd_signup.text!=self.ids.customer_pswd_confirm.text:
            self.ids.customer_pswd_confirm_error.text="Passwords Do Not Match"
            self.ids.submit_button3.disabled=True
        else:
            self.ids.customer_pswd_confirm_error.text=""
            self.ids.submit_button3.disabled=False

    def validate_seller_id(self):
        #Here we grab the data inputed using the .strip() function
        seller_id_input = self.ids.seller_id.text.strip()

        if not seller_id_input:
            self.ids.seller_id_error.text = "Input Required"
            self.ids.submit_button3.disabled = True
            return

        try:
            seller_id = int(seller_id_input)
        except ValueError:
            self.ids.seller_id_error.text = "Incorrect Input"
            self.ids.submit_button3.disabled = True
            return

        self.cursor.execute("SELECT seller_id FROM maji_mazuri.seller;")
        data = self.cursor.fetchall()
        seller_ids_list = [id[0] for id in data]

        if seller_id not in seller_ids_list:
            self.ids.seller_id_error.text = "Seller ID is not registered!"
            self.ids.submit_button3.disabled = True
        else:
            self.ids.seller_id_error.text = ""
            self.ids.submit_button3.disabled = False
            

    def signup_validate(self):
         #Here we collect all te info entered by the user
         email=self.ids.email_customer_signup.text.strip()
         phone_no=self.ids.customer_phone_no.text.strip()
         first_name=self.ids.customer_first_name.text.strip()
         last_name=self.ids.customer_last_name.text.strip()
         password2=self.ids.customer_pswd_signup.text.strip()
         password3=self.ids.customer_pswd_confirm.text.strip()
         seller_id=self.ids.seller_id.text.strip()

        #Here we collect the customers emails
         self.cursor.execute("SELECT customer_email FROM maji_mazuri.customer;")
         email_customer=self.cursor.fetchall()
         email_customer_list=[]
         for eml in email_customer:
            email_customer_list.append(eml[0])
        
       

        #Here we ensure that all fields have data
         if not email:
             self.ids.submit_button3.disabled=True
             self.ids.email_customer_signup_error.text="Email is Required"
             return False
         elif not phone_no:
             self.ids.submit_button3.disabled=True
             self.ids.customer_phone_no_error.text="Phone Number Required"
             return False
         elif not first_name:
             self.ids.submit_button3.disabled=True
             self.ids.seller_id_error.text="Input Required"
             return False
         elif not last_name:
             self.ids.submit_button3.disabled=True
             self.ids.customer_last_name_error.text="Input Required"
             return False
         elif not password2:
             self.ids.submit_button3.disabled=True
             self.ids.customer_pswd_signup_error.text="Password is Required"
             return False
         elif not password3:
             self.ids.submit_button3.disabled=True
             self.ids.customer_pswd_confirm_error.text="Password is Required"
             return False
         elif  not seller_id:
             self.ids.submit_button3.disabled=True
             self.ids.seller_id_error.text="Seller ID is Required"
             return False
         else:
             self.ids.submit_button3.disabled=False
             
            #Once all info is filled,ensure the email does not already exist then add it
             date=dt.datetime.now().strftime('%d-%m-%Y')
             if email not in email_customer_list:
                exexute1="INSERT INTO maji_mazuri.customer(customer_email ,customer_phone_number ,customer_first_name ,customer_last_name ,customer_pswd ,customer_pswd_confirm,seller_id,signup_dates) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"
                value=(email,phone_no,first_name,last_name,password2,password3,seller_id,date)
                self.cursor.execute(exexute1,value)
                self.connection.commit()
                self.send_registration_email(email,seller_id)
                return True
             else:
                self.ids.email_customer_signup_error.text="Email is already Registered"
                return False   
                
    def send_registration_email(self,email, seller_id):
        # Email details
        sender_email = 'allantham897@gmail.com'  # Replace with your email address
        sender_password = 'nmrfycjjqjjgbihw'  # Replace with your email password
        subject = 'MAJI MAZURI Customer Registration Successful'
        message = f'''
        Dear Customer,
        
        Congratulations! Your registration with MAJI MAZURI Corporation was successful.
        
        You have been registered to seller id {seller_id}
        
        Thank you for joining us. If you have any questions or need further assistance, feel free to contact us.
        
        Best regards,
        MAJI MAZURI Corporation
        '''

        try:
            # Create a multipart message
            email_message = MIMEMultipart()
            email_message['From'] = sender_email
            email_message['To'] = email
            email_message['Subject'] = subject

            # Attach the message to the email
            email_message.attach(MIMEText(message, 'plain'))

            # Connect to the SMTP server and send the email
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(sender_email, sender_password)
                smtp.send_message(email_message)

            print('Email sent successfully')
        except Exception as e:
            print('Error sending email:', str(e))
     
    def show_success_message(self):
       
       snackbar=Snackbar(
          text="REGISTRATION SUCCESSFUL",
          snackbar_x="10dp",
          snackbar_y="10dp",
          pos_hint={'center_x': 0.5, 'center_y': 0.5},
          #bg_color=(1,0,0,1),
          radius=[13,13,13,13],
          duration=3,
          #auto_dismiss=False

      )
       snackbar.open()
    

    def change_screen2(self):
            #this is the function called in the kv file
            self.show_success_message()
            Clock.schedule_once(lambda dt: self.transition1(), 4)


    def transition1(self):
            #to actually change the screen
            self.manager.current = 'login'
            self.manager.transition.direction = 'right'
    
    def email_dialog(self):
          
          if not self.dialog6:
                self.dialog6= MDDialog(
                    title="REGISTRATION SUCCESSFULL!!",
                    text="You will recieve an email shortly.",
                    radius=[20,7,20,7],
                    buttons=[
                        MDRaisedButton(
                            text="OK",
                            on_press=self.dismiss_email_dialog3,   
                        ),
                    ],
                )
          self.dialog6.open()

    def dismiss_email_dialog3(self, instance):
        self.dialog6.dismiss()
        self.transition1()
