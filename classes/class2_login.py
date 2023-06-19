import re
from kivy.uix.screenmanager import Screen

from .zdatabase import Database



class LoginScreen(Screen,Database): 

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
            self.ids.signin_button.disabled=True
            
        elif not self.validate_email_re(email):
            self.ids.email_login_error.text="Invalid Email"
            self.ids.signin_button.disabled=True
        else:
            self.ids.email_login_error.text=""
            self.ids.signin_button.disabled=False

    def validate_password1(self):
        #Here we grab the data inputed using the .strip() functio
        password1=self.ids.pswd1.text.strip()
        if not password1:
            self.ids.pswd1_error.text="Password is Required"
            self.ids.signin_button.disabled=True
        elif not self.validate_password_re(password1):
            self.ids.pswd1_error.text="Password Too Short" 
            self.ids.signin_button.disabled=True
        else:
            self.ids.pswd1_error.text=""
            self.ids.signin_button.disabled=False
    def change_screen1(self):
        self.manager.current = 'customerbrowse'
        self.manager.transition.direction = 'left'

    def change_screen2(self):
         self.manager.current = 'orders'
         self.manager.transition.direction = 'left'

    def sign_in(self):
        password1=self.ids.pswd1.text.strip()
        email=self.ids.email_login.text.strip()
       
        if self.ids.email_login.text=="":
            self.ids.signin_button.disabled=True
            self.ids.email_login_error.text="Email is Required"
       
        elif self.ids.pswd1.text=="":
            self.ids.signin_button.disabled=True
            self.ids.pswd1_error.text="Password is Required"
        else:   
            self.ids.signin_button.disabled=False
        
            self.cursor.execute("SELECT customer_email FROM maji_mazuri.customer;")
            email_customer=self.cursor.fetchall()
            email_customer_list=[]
            
            for x in email_customer:
                email_customer_list.append(x[0])
            

            self.cursor.execute("SELECT seller_email FROM maji_mazuri.seller;")
            email_seller=self.cursor.fetchall()
            email_seller_list=[]
            for x in email_seller:
                email_seller_list.append(x[0])
        
            
            if email in email_customer_list:
                self.cursor.execute(f"SELECT customer_pswd FROM maji_mazuri.customer WHERE customer_email='{email}';")
                cust_pswd=self.cursor.fetchall()
                for j in cust_pswd:
                    if password1==j[0]:
                        self.change_screen1()
                        
                        return True
                    else:
                        self.ids.pswd1_error.text="Incorrect Password"
                
            elif email in email_seller_list:
                self.cursor.execute(f"SELECT seller_pswd FROM maji_mazuri.seller WHERE seller_email='{email}';")
                seller_pswd=self.cursor.fetchall()
                for j in seller_pswd:
                    if password1==j[0]:
                        self.change_screen2()
                        return True
                    else:
                        self.ids.pswd1_error.text="Incorrect Password"
                
            else:
                self.ids.email_login_error.text="Email is not Registered"
                return False
            
    