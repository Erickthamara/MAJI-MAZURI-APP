from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.window import Window
from os import listdir
from kivy.clock import Clock
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.factory import Factory
from kivymd.uix.bottomsheet import MDCustomBottomSheet

import kivy
import kivymd

from classes import WelcomeScreen
from classes import LoginScreen
from classes import SignupScreen
from classes import SellerScreen
from classes import CustomerBrowse


Window.size=(350,600)


class MyScreen(Screen):
    pass

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

    def show_example_custom_bottom_sheet(self,image,price,rating):
        bottom_sheet=Factory.ContentCustomSheet()
        bottom_sheet.image=image
        bottom_sheet.price=price
        bottom_sheet.rating=rating

        self.custom_sheet = MDCustomBottomSheet(screen=bottom_sheet)
        self.custom_sheet.open()

    
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
        sm.add_widget(MyScreen(name="test"))
        sm.add_widget(SellerScreen(name="orders"))
        sm.add_widget(CustomerBrowse(name="customerbrowse"))
        #Loading up every screen
        return sm
    
         
if __name__=="__main__":
    MyApp().run()
        