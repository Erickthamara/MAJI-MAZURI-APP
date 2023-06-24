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
from kivy.properties import StringProperty


import kivy
import kivymd
import cProfile

from classes import WelcomeScreen
from classes import LoginScreen
from classes import SignupScreen
from classes import SellerScreen
from classes import CustomerBrowse
from classes import Database
from classes import SalesGraph
from classes import ReportScreen


Window.size=(350,600)




class CatalogueContent(Screen):
    pass

class OrdersContent(Screen):
    pass


class SalesContent(Screen):
    pass


    
class MyApp(MDApp):
    num = StringProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style="Light"
        self.theme_cls.primary_palette="Blue"
        self.theme_cls.primary_hue='700'
        
        self.num = str(0)

    
    
    def increase_quantity(self):
        self.num = str(int(self.num) + 1)

    def decrease_quantity(self):
        if int(self.num) > 0:
            self.num = str(int(self.num) - 1)

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
        sm.add_widget(SellerScreen(name="orders"))
        sm.add_widget(CustomerBrowse(name="customerbrowse"))
        sm.add_widget(SalesGraph(name="sales_graph"))
        sm.add_widget(ReportScreen(name="reports"))
        
        #Loading up every screen
        return sm
    
         
if __name__=="__main__":
    MyApp().run()
        