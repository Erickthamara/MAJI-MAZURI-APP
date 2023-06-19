import re
from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock

from .zdatabase import Database



class SignupScreen(Screen,Database):
     #This are all the methods used in the signup screen backend
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
        if len(password) >= 8:
            return True
        return False
     
    def validate_email2(self):
        #Here we grab the data inputed using the .strip() function
        email=self.ids.email_signup.text.strip()
       

        if not email:
            self.ids.email_signup_error.text="Email is Required"
            self.ids.submit_button2.disabled=True
        elif not self.validate_email_re(email):
            self.ids.email_signup_error.text="Invalid Email"
            self.ids.submit_button2.disabled=True
       
        else:
            self.ids.email_signup_error.text=""
            self.ids.submit_button2.disabled=False

        

    def validate_phone_no(self):
        #Here we grab the data inputed using the .strip() function
        phone_no=self.ids.phone_no.text.strip()
        
        if not phone_no:
            self.ids.phone_no_error.text="Phone Number Required"
            self.ids.submit_button2.disabled=True
        elif not self.validate_phone_re(phone_no) :
            self.ids.phone_no_error.text="Invalid Phone Number"
            self.ids.submit_button2.disabled=True
        else:
            self.ids.phone_no_error.text=""
            self.ids.submit_button2.disabled=False

    def validate_first_name(self):
        #Here we grab the data inputed using the .strip() function
        first_name=self.ids.first_name.text.strip()
        
        if not first_name:
            self.ids.first_name_error.text="Input Required"
            self.ids.submit_button2.disabled=True
        elif self.ids.first_name.text.isalpha()==False:
            self.ids.first_name_error.text="Incorrect Input"
            self.ids.submit_button2.disabled=True
        else:
            self.ids.first_name_error.text=""
            self.ids.submit_button2.disabled=False

    def validate_last_name(self):
        #Here we grab the data inputed using the .strip() function
        last_name=self.ids.last_name.text.strip()
        
        if not last_name:
            self.ids.last_name_error.text="Input Required"
            self.ids.submit_button2.disabled=True
        elif self.ids.last_name.text.isalpha()==False:
            self.ids.last_name_error.text="Incorrect Input"
            self.ids.submit_button2.disabled=True
        else:
            self.ids.last_name_error.text=""
            self.ids.submit_button2.disabled=False

    def validate_password2(self):
        #Here we grab the data inputed using the .strip() function
        password2=self.ids.pswd_signup.text.strip()
        if not password2:
            self.ids.pswd_signup_error.text="Password is Required"
            self.ids.submit_button2.disabled=True
        elif not self.validate_password_re(password2):
            self.ids.pswd_signup_error.text="Passowrd Too Short" 
            self.ids.submit_button2.disabled=True
        else:
            self.ids.pswd_signup_error.text=""
            self.ids.submit_button2.disabled=False


    def validate_password3(self):
        #Here we grab the data inputed using the .strip() function
        password3=self.ids.pswd_confirm.text.strip()
        if not password3:
            self.ids.pswd_confirm_error.text="Password is Required"
            self.ids.submit_button2.disabled=True
        elif not self.validate_password_re(password3):
            self.ids.pswd_confirm_error.text="Passowrd Too Short" 
            self.ids.submit_button2.disabled=True
        elif self.ids.pswd_signup.text!=self.ids.pswd_confirm.text:
            self.ids.pswd_confirm_error.text="Passwords Do Not Match"
            self.ids.submit_button2.disabled=True
        else:
            self.ids.pswd_confirm_error.text=""
            self.ids.submit_button2.disabled=False

    def checkbox_checked (self):
         
        if self.ids.checkbox2.active or self.ids.checkbox3.active: 
            self.ids.checkbox_error.text=" "
            self.ids.submit_button2.disabled=False
        else: 
            self.ids.checkbox_error.text="Select Customer or Seller"
            self.ids.submit_button2.disabled=True
         

    def signup_validate(self):
         #Here we collect all te info entered by the user
         email=self.ids.email_signup.text.strip()
         phone_no=self.ids.phone_no.text.strip()
         first_name=self.ids.first_name.text.strip()
         last_name=self.ids.last_name.text.strip()
         password2=self.ids.pswd_signup.text.strip()
         password3=self.ids.pswd_confirm.text.strip()

        #Here we collect the customers emails
         self.cursor.execute("SELECT customer_email FROM maji_mazuri.customer;")
         email_customer=self.cursor.fetchall()
         email_customer_list=[]
         for eml in email_customer:
            email_customer_list.append(eml[0])
        
        #here we collect the seller emails
         self.cursor.execute("SELECT seller_email FROM maji_mazuri.seller;")
         email_seller=self.cursor.fetchall()
         email_seller_list=[]
         for eml in email_seller:
            email_seller_list.append(eml[0])

        #Here we ensure that all fields have data
         if not email:
             self.ids.submit_button2.disabled=True
             self.ids.email_signup_error.text="Email is Required"
             return False
         elif not phone_no:
             self.ids.submit_button2.disabled=True
             self.ids.phone_no_error.text="Phone Number Required"
             return False
         elif not first_name:
             self.ids.submit_button2.disabled=True
             self.ids.first_name_error.text="Input Required"
             return False
         elif not last_name:
             self.ids.submit_button2.disabled=True
             self.ids.last_name_error.text="Input Required"
             return False
         elif not password2:
             self.ids.submit_button2.disabled=True
             self.ids.pswd_signup_error.text="Password is Required"
             return False
         elif not password3:
             self.ids.submit_button2.disabled=True
             self.ids.pswd_confirm_error.text="Password is Required"
             return False
         elif  not self.ids.checkbox2.active and not self.ids.checkbox3.active:
            self.ids.checkbox_error.text="Select Customer or Seller"
            self.ids.submit_button2.disabled=True
            return False
         else:
             self.ids.submit_button2.disabled=False
             
            #Once all info is filled,i ensure the email does not already exist then add it
             if self.ids.checkbox2.active:
                #If the email is not already in the customer.databse then you can add the info
                if email not in email_customer_list:
                    exexute1="INSERT INTO maji_mazuri.customer(customer_email ,customer_phone_number ,customer_first_name ,customer_last_name ,customer_pswd ,customer_pswd_confirm) VALUES(%s,%s,%s,%s,%s,%s);"
                    value=(email,phone_no,first_name,last_name,password2,password3)
                    self.cursor.execute(exexute1,value)
                    self.connection.commit()
                    return True
                else:
                    self.ids.email_signup_error.text="Email is already Registered"
                    return False   
                
             elif self.ids.checkbox3.active:
                #If the email is not already in the seller.databse then you can add the info
                if email not in email_seller_list:
                    exexute1="INSERT INTO maji_mazuri.seller(seller_email ,seller_phone_number ,seller_first_name ,seller_last_name ,seller_pswd ,seller_pswd_confirm) VALUES(%s,%s,%s,%s,%s,%s);"
                    value=(email,phone_no,first_name,last_name,password2,password3)
                    self.cursor.execute(exexute1,value)
                    self.connection.commit()
                    return True
                else:
                     self.ids.email_signup_error.text="Email is already Registered"
                     return False
             else:
                return False
     
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
