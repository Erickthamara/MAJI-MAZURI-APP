from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.window import Window
from os import listdir


import kivy
import kivymd
import cProfile

from classes import WelcomeScreen
from classes import LoginScreen
from classes import SignupScreen
from classes import CustomerSignupScreen
from classes import SellerScreen
from classes import CustomerBrowse
from classes import Database
from classes import SalesGraph
from classes import ReportScreen
from classes import CheckoutScreen
from classes import PaymentScreen


Window.size=(350,600)


class CatalogueContent(Screen):
    pass

class OrdersContent(Screen):
    pass

class SalesContent(Screen):
    pass


    
class MyApp(MDApp):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style="Light"
        self.theme_cls.primary_palette="Blue"
        self.theme_cls.primary_hue='700'
        
     

    def build(self):

        #Creation of every style screen 
        kv_path = "./kv_files/"
        for kv in listdir(kv_path): 
            Builder.load_file(kv_path+kv)
        
        #Creation of every screen of the MAJI MAZURI APP
        sm=ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignupScreen(name="signup"))
        sm.add_widget(CustomerSignupScreen(name="customersignup"))
        sm.add_widget(SellerScreen(name="orders"))
        sm.add_widget(CustomerBrowse(name="customerbrowse"))
        sm.add_widget(SalesGraph(name="sales_graph"))
        sm.add_widget(ReportScreen(name="reports"))
        sm.add_widget(CheckoutScreen(name="checkout"))
        sm.add_widget(PaymentScreen(name="payment"))
        
        #Loading up every screen
        return sm
    
         
if __name__=="__main__":
    MyApp().run()
