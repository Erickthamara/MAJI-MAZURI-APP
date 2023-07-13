from kivy.uix.screenmanager import Screen

from .zdatabase import Database

from .zids_manager import CustomerIds,SellerIds
from .zshareddata import main_seller_id2

import datetime as dt
import re



class LoginScreen(Screen,Database): 
    customer_id=None
    seller_id=None
    main_seller_id=None
    main_seller_id2=None
    def __init__(self, **kw):
        super().__init__(**kw)
        

    #This are all the methods used in the Login screen 
    
    def validate_email_re(self,email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern,email):
            return True
        return False

    def validate_password_re(self,password):
        # Add your password validation rules here
        if len(password) >= 8:
            return True
        return False

    def validate_email(self):
        #Here we grab the data inputed using the .strip() function
        email=self.ids.email_login.text.strip()
        
        if self.ids.email_login.text=="":
            self.ids.email_login_error.text="Email is Required"
            self.ids.login_seller_button.disabled=True
            self.ids.login_customer_button.disabled=True
            
        elif not self.validate_email_re(email):
            self.ids.email_login_error.text="Invalid Email"
            self.ids.login_seller_button.disabled=True
            self.ids.login_customer_button.disabled=True
        else:
            self.ids.email_login_error.text=""
            self.ids.login_seller_button.disabled=False
            self.ids.login_customer_button.disabled=False

    def validate_password1(self):
        #Here we grab the data inputed using the .strip() functio
        password1=self.ids.pswd1.text.strip()
        #if password is empty
        if not password1:
            self.ids.pswd1_error.text="Password is Required"
            self.ids.login_seller_button.disabled=True
            self.ids.login_customer_button.disabled=True
        #if password is too short
        elif not self.validate_password_re(password1):
            self.ids.pswd1_error.text="Password Too Short" 
            self.ids.login_seller_button.disabled=True
            self.ids.login_customer_button.disabled=True
        else:
            self.ids.pswd1_error.text=""
            self.ids.login_seller_button.disabled=False
            self.ids.login_customer_button.disabled=False
    def customer_screen1(self):
        self.manager.current = 'customerbrowse'
        self.manager.transition.direction = 'left'

    def seller_screen2(self):
         self.manager.current = 'orders'
         self.manager.transition.direction = 'left'

    def seller_sign_in(self):
        password1=self.ids.pswd1.text.strip()
        email=self.ids.email_login.text.strip()
       
        if self.ids.email_login.text=="":
            self.ids.login_seller_button.disabled=True
            self.ids.email_login_error.text="Email is Required"
       
        elif self.ids.pswd1.text=="":
            self.ids.login_seller_button.disabled=True
            self.ids.pswd1_error.text="Password is Required"
        else:   
            self.ids.login_seller_button.disabled=False
        
         
            
            #collect all seller emails
            self.cursor.execute("SELECT seller_email FROM maji_mazuri.seller;")
            email_seller=self.cursor.fetchall()
            email_seller_list=[]
            for x in email_seller:
                email_seller_list.append(x[0])

            
           
            #check if email is present
            if email in email_seller_list:
                self.cursor.execute(f"SELECT seller_id,seller_pswd FROM maji_mazuri.seller WHERE seller_email='{email}';")
                seller_pswd=self.cursor.fetchall()
                for j in seller_pswd:
                    if password1==j[1]:
                        self.seller_screen2()
                        LoginScreen.main_seller_id=j[0]
                        #this is for transactions screen
                        self.update_main_seller_id=j[0]
                        return True
                    else:
                        self.ids.pswd1_error.text="Incorrect Password"
                
            else:
                self.ids.email_login_error.text="Email is not Registered"
                return False
            
    def customer_sign_in(self):
        password1=self.ids.pswd1.text.strip()
        email=self.ids.email_login.text.strip()
       
        if self.ids.email_login.text=="":
            self.ids.login_customer_button.disabled=True
            self.ids.email_login_error.text="Email is Required"
       
        elif self.ids.pswd1.text=="":
            self.ids.login_customer_button.disabled=True
            self.ids.pswd1_error.text="Password is Required"
        else:   
            self.ids.login_customer_button.disabled=False
            #Get all emails in customer
            self.cursor.execute("SELECT customer_email FROM maji_mazuri.customer;")
            email_customer=self.cursor.fetchall()
            email_customer_list=[]
            
            for x in email_customer:
                email_customer_list.append(x[0])
            

            #check if email is valid
            
            if email in email_customer_list:
                self.cursor.execute(f"SELECT customer_pswd,customer_id,seller_id FROM maji_mazuri.customer WHERE customer_email='{email}';")
                cust_pswd=self.cursor.fetchall()
                for j in cust_pswd:
                    if password1==j[0]:
                        #call this to change the screen
                        self.customer_screen1()

                        LoginScreen.customer_id=j[1]
                        LoginScreen.seller_id=j[2]
                        
                        
                        return True
                    else:
                        self.ids.pswd1_error.text="Incorrect Password"
                
                
            else:
                self.ids.email_login_error.text="Email is not Registered"
                return False
    