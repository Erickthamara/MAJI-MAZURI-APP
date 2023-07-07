import re
from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock

from .zdatabase import Database



class CustomerSignupScreen(Screen,Database):
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