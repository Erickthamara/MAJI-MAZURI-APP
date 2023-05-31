from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.window import Window
from os import listdir
from kivy.clock import Clock

import kivy
import kivymd

from classes import WelcomeScreen
from classes import LoginScreen
from classes import SignupScreen
from classes import OrderScreen
from classes import CatalogueScreen
from classes import SalesScreen

Window.size=(350,600)


class MyScreen(Screen):
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
        Builder.load_file("style.kv")
        
        #Creation of every screen of the MAJI MAZURI APP
        sm=ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignupScreen(name="signup"))
        sm.add_widget(MyScreen(name="test"))
        sm.add_widget(OrderScreen(name="orders"))
        sm.add_widget(CatalogueScreen(name="catalogue"))
        sm.add_widget(SalesScreen(name="sales"))
        #Loading up every screen
        return sm
    
         
        
    
if __name__=="__main__":
    MyApp().run()
        