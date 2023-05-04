import kivy
import kivymd
import mysql.connector
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.text import LabelBase
from kivy.core.window import Window
Window.size=(350,600)

class WelcomeScreen(Screen): 
    pass


class LoginScreen(Screen): 
    #This are all the methods used in the Login screen backend
    def validate_email(self):
        #Here we grab the data inputed using the .strip() function
        email=self.ids.email_login.text.strip()
        
        if not email:
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


class SignupScreen(Screen):
     #This are all the methods used in the signup screen backend
     def validate_email2(self):
        #Here we grab the data inputed using the .strip() function
        email=self.ids.email_signup.text.strip()
        
        if not email:
            self.ids.email_signup_error.text="Email is Required"
        elif '@' not in email or '.' not in email:
            self.ids.email_signup_error.text="Invalid Email"
        else:
            self.ids.email_signup_error.text=""

     def validate_phone_no(self):
        #Here we grab the data inputed using the .strip() function
        phone_no=self.ids.phone_no.text.strip()
        
        if not phone_no:
            self.ids.phone_no_error.text="Phone Number Required"
        elif self.ids.phone_no.text.isdigit()==False  :
            self.ids.phone_no_error.text="Invalid Phone Number"
        else:
            self.ids.phone_no_error.text=""

     def validate_first_name(self):
        #Here we grab the data inputed using the .strip() function
        first_name=self.ids.first_name.text.strip()
        
        if not first_name:
            self.ids.first_name_error.text="Input Required"
        elif self.ids.first_name.text.isalpha()==False:
            self.ids.first_name_error.text="Incorrect Input"
        else:
            self.ids.first_name_error.text=""

     def validate_last_name(self):
        #Here we grab the data inputed using the .strip() function
        last_name=self.ids.last_name.text.strip()
        
        if not last_name:
            self.ids.last_name_error.text="Input Required"
        elif self.ids.last_name.text.isalpha()==False:
            self.ids.last_name_error.text="Incorrect Input"
        else:
            self.ids.last_name_error.text=""

     def validate_password2(self):
        #Here we grab the data inputed using the .strip() function
        password2=self.ids.pswd_signup.text.strip()
        if not password2:
            self.ids.pswd_signup_error.text="Password is Required"
        elif len(self.ids.pswd_signup.text) <4:
            self.ids.pswd_signup_error.text="Passowrd Too Short" 
        else:
            self.ids.pswd_signup_error.text=""

     def validate_password3(self):
        #Here we grab the data inputed using the .strip() function
        password3=self.ids.pswd_confirm.text.strip()
        if not password3:
            self.ids.pswd_confirm_error.text="Password is Required"
        elif len(self.ids.pswd_confirm.text) <4:
            self.ids.pswd_confirm_error.text="Passowrd Too Short" 
        elif self.ids.pswd_signup.text!=self.ids.pswd_confirm.text:
            self.ids.pswd_confirm_error.text="Passwords Do Not Match"
        else:
            self.ids.pswd_confirm_error.text=""

     def checkbox_validate(self):
         if  not self.ids.checkbox2.active and not self.ids.checkbox3.active:
             self.ids.checkbox_error.text="Select Customer or Seller"
         else:
             self.ids.checkbox_error.text=""

         if self.ids.checkbox2.active:
             print("You chose Customer!")
         elif self.ids.checkbox3.active:
             print("You chose seller")


sm=ScreenManager()
sm.add_widget(WelcomeScreen(name="welcome"))
sm.add_widget(LoginScreen(name="login"))
sm.add_widget(SignupScreen(name="signup"))

class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style="Light"
        self.theme_cls.primary_palette="Blue"
        self.theme_cls.primary_hue='700'
        
    
      
    def build(self):
        return Builder.load_file("style.kv")
    
if __name__=="__main__":
    MyApp().run()
        