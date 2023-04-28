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
    pass


sm=ScreenManager()
sm.add_widget(WelcomeScreen(name="welcome"))
sm.add_widget(LoginScreen(name="login"))

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
        