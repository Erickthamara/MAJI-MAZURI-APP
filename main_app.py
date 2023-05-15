import kivy
import kivymd
import mysql.connector
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
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

    #This are all the methods used in the Login screen backend

    def validate_email(self):
        #Here we grab the data inputed using the .strip() function
        email=self.ids.email_login.text.strip()
        
        if self.ids.email_login.text=="":
            self.ids.email_login_error.text="Email is Required"
            self.ids.signin_button.disabled=True
            
        elif '@' not in email or '.' not in email:
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
        elif len(self.ids.pswd1.text) <4:
            self.ids.pswd1_error.text="Password Too Short" 
            self.ids.signin_button.disabled=True
        else:
            self.ids.pswd1_error.text=""
            self.ids.signin_button.disabled=False

    def sign_in(self):
        password1=self.ids.pswd1.text.strip()
        email=self.ids.email_login.text.strip()
       
        if not email:
            self.ids.signin_button.disabled=True
            self.ids.email_login_error.text="Email is Required"
       
        elif not password1 :
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
                    return True
                else:
                    self.ids.pswd1_error.text="Incorrect Password"
        elif email in email_seller_list:
            self.cursor.execute(f"SELECT seller_pswd FROM maji_mazuri.seller WHERE seller_email='{email}';")
            for j in self.cursor:
                if password1==j[0]:
                    print("SUCCSSFULLY LOGGED IN")
                    return True
                else:
                    self.ids.pswd1_error.text="Incorrect Password"
        else:
            return False
        
    def change_screen1(self):
            self.manager.current = 'sales'
            self.manager.transition.direction = 'left'
      
    # def next_page(self):
    #     print("New Page")

class SignupScreen(Screen,Database):
     #This are all the methods used in the signup screen backend
     
     def validate_email2(self):
        #Here we grab the data inputed using the .strip() function
        email=self.ids.email_signup.text.strip()
        
        if not email:
            self.ids.email_signup_error.text="Email is Required"
            self.ids.submit_button2.disabled=True
        elif '@' not in email or '.' not in email:
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
        elif self.ids.phone_no.text.isdigit()==False  :
            self.ids.phone_no_error.text="Invalid Phone Number"
            self.ids.submit_button2.disabled=True
        elif len(self.ids.phone_no.text)<10:
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
        elif len(self.ids.pswd_signup.text) <4:
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
        elif len(self.ids.pswd_confirm.text) <4:
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
         

     def checkbox_validate(self):
         
         email=self.ids.email_signup.text.strip()
         phone_no=self.ids.phone_no.text.strip()
         first_name=self.ids.first_name.text.strip()
         last_name=self.ids.last_name.text.strip()
         password2=self.ids.pswd_signup.text.strip()
         password3=self.ids.pswd_confirm.text.strip()

         if not email:
             self.ids.submit_button2.disabled=True
             self.ids.email_signup_error.text="Email is Required"
         elif not phone_no:
             self.ids.submit_button2.disabled=True
             self.ids.phone_no_error.text="Phone Number Required"
         elif not first_name:
             self.ids.submit_button2.disabled=True
             self.ids.first_name_error.text="Input Required"
         elif not last_name:
             self.ids.submit_button2.disabled=True
             self.ids.last_name_error.text="Input Required"
         elif not password2:
             self.ids.submit_button2.disabled=True
             self.ids.pswd_signup_error.text="Password is Required"
         elif not password3:
             self.ids.submit_button2.disabled=True
             self.ids.pswd_confirm_error.text="Password is Required"
         elif  not self.ids.checkbox2.active and not self.ids.checkbox3.active:
            self.ids.checkbox_error.text="Select Customer or Seller"
            self.ids.submit_button2.disabled=True
         else:
             self.ids.submit_button2.disabled=False
             
             
        
         if self.ids.checkbox2.active:
            exexute1="INSERT INTO maji_mazuri.customer(customer_email ,customer_phone_number ,customer_first_name ,customer_last_name ,customer_pswd ,customer_pswd_confirm) VALUES(%s,%s,%s,%s,%s,%s);"
            value=(email,phone_no,first_name,last_name,password2,password3)
            self.cursor.execute(exexute1,value)
            self.connection.commit()
            self.cursor.execute("SELECT * FROM maji_mazuri.customer;")
            for x in self.cursor:
                print(x)
            
            return True
         elif self.ids.checkbox3.active:
            exexute1="INSERT INTO maji_mazuri.seller(seller_email ,seller_phone_number ,seller_first_name ,seller_last_name ,seller_pswd ,seller_pswd_confirm) VALUES(%s,%s,%s,%s,%s,%s);"
            value=(email,phone_no,first_name,last_name,password2,password3)
            self.cursor.execute(exexute1,value)
            self.connection.commit()
            self.cursor.execute("SELECT * FROM maji_mazuri.seller;")
            for x in self.cursor:
                print(x)
            
            return True
         else:
             return False


     def change_screen2(self):
            self.manager.current = 'login'
            self.manager.transition.direction = 'right'


class SalesScreen(Screen,Database):
    def __init__(self, **kwargs):
        super(SalesScreen, self).__init__(**kwargs)
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
                
    def delete_row(self):
        row_index = self.on_check_press.current_row
        delete_query = f"DELETE FROM maji_mazuri.custome  WHERE id = {row_index}"
        self.cursor.execute(delete_query)
        self.connection.commit()

        # Update the DataTable view
        self.parent.parent.parent.update_datatable()




    



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
        sm.add_widget(SalesScreen(name="sales"))
        #Loading up every screen
        return Builder.load_file("style.kv")
    
if __name__=="__main__":
    MyApp().run()
        