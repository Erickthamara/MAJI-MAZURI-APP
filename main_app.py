import kivy
import kivymd
import mysql.connector
import re
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.window import Window
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock

Window.size=(350,600)

class WelcomeScreen(Screen): 
    pass

class Database():

   connection = None
   cursor = None

   def __init__(self):
      if Database.connection is None:
         try:
            Database.connection = mysql.connector.connect(host="localhost",port=3307, user="root", password="erick1", database="maji_mazuri")
            Database.cursor = Database.connection.cursor()
         except Exception as error:
            print(f"Error: Connection not established {error}")
         else:
            pass

      self.connection = Database.connection
      self.cursor = Database.cursor
    


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
        self.manager.current = 'customers'
        self.manager.transition.direction = 'left'

    def change_screen2(self):
         self.manager.current = 'shop'
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
                for j in self.cursor:
                    if password1==j[0]:
                        print("SUCCSSFULLY LOGGED IN")
                        self.change_screen1()
                        return True
                    else:
                        self.ids.pswd1_error.text="Incorrect Password"
                self.cursor.close()
            elif email in email_seller_list:
                self.cursor.execute(f"SELECT seller_pswd FROM maji_mazuri.seller WHERE seller_email='{email}';")
                for j in self.cursor:
                    if password1==j[0]:
                        print("SUCCSSFULLY LOGGED IN")
                        self.change_screen2()
                        return True
                    else:
                        self.ids.pswd1_error.text="Incorrect Password"
                self.cursor.close()
            else:
                self.ids.email_login_error.text="Email is not Registered"
                return False
            
    

      
    # def next_page(self):
    #     print("New Page")

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
         
         email=self.ids.email_signup.text.strip()
         phone_no=self.ids.phone_no.text.strip()
         first_name=self.ids.first_name.text.strip()
         last_name=self.ids.last_name.text.strip()
         password2=self.ids.pswd_signup.text.strip()
         password3=self.ids.pswd_confirm.text.strip()

         self.cursor.execute("SELECT customer_email FROM maji_mazuri.customer;")
         email_customer=self.cursor.fetchall()
         email_customer_list=[]
         for eml in email_customer:
            email_customer_list.append(eml[0])
        
         self.cursor.execute("SELECT seller_email FROM maji_mazuri.seller;")
         email_seller=self.cursor.fetchall()
         email_seller_list=[]
         for eml in email_seller:
            email_seller_list.append(eml[0])

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
             
             
             if self.ids.checkbox2.active:
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
       snackbar = Snackbar(text="Details successfully authenticated",)
       snackbar.duration = 2  # Optional: Set the duration in seconds
       snackbar.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
       self.ids.my_layout3.add_widget(snackbar)

    def submit_info(self):
        # Validation logic
        if self.details_authenticated():
            self.show_success_message()
            self.screen_manager.current = 'next_screen'


    def change_screen2(self):
            self.show_success_message()
            Clock.schedule_once(lambda dt: self.transition1(), 2)


    def transition1(self):
            self.manager.current = 'login'
            self.manager.transition.direction = 'right'

        
            







class CustomerScreen(Screen,Database):
    def __init__(self, **kwargs):
        super(CustomerScreen, self).__init__(**kwargs)
        self.instance_table = None  # Initialize instance_table variable
        self.current_row = None  # Initialize current_row variable
        self.selected_rows=[]

       

    def on_enter(self):
        headers=["cutomer_id","email","phone_no","first_name","last_name","password2","password3"]
        self.cursor.execute("SELECT * FROM maji_mazuri.customer")
        myresult = self.cursor.fetchall()
        rows = [] 
        for row in myresult:
            rows.append(row)
 
        self.mytable=MDDataTable(
            size_hint=(.9,.7),
            pos_hint= {'center_x':0.5, 'center_y':0.6},
            check=True,
            use_pagination=True,
            pagination_menu_height="240dp",

            column_data=[(header, dp(30)) for header in headers],
            row_data=rows


        )
        
        float_layout=self.ids.my_float_layout
        self.mytable.bind(on_check_press=self.on_check_press)

        float_layout.add_widget(self.mytable)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''
        self.instance_table=instance_table
        self.current_row=current_row
        if current_row in self.selected_rows:
            self.selected_rows.remove(current_row)  # Deselect the row if already selected
        else:
            self.selected_rows.append(current_row)  # Select the ro
        
        
    
    def delete_selected_rows(self, *args):
       if self.instance_table is not None and self.current_row is not None:

        for row in self.selected_rows:
            delete_query = f"DELETE FROM maji_mazuri.customer WHERE customer_id = {row[0]}"
            self.cursor.execute(delete_query)
            self.connection.commit()
            self.update_datatable()

    def update_datatable(self):
        return self.on_enter()
    
class ShoppingScreen(Screen):
    pass
                

class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style="Light"
        self.theme_cls.primary_palette="Blue"
        self.theme_cls.primary_hue='700'
        
      
    def build(self):
        #Creation of every screen of the MAJI MAZURI APP
        sm=ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignupScreen(name="signup"))
        sm.add_widget(CustomerScreen(name="customers"))
        sm.add_widget(ShoppingScreen(name="shop"))
        #Loading up every screen
        return Builder.load_file("style.kv")
    
if __name__=="__main__":
    MyApp().run()
        