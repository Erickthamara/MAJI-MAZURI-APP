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
from datetime import datetime
import matplotlib.pyplot as plt
from kivy.garden.matplotlib import FigureCanvasKivyAgg

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


Window.size=(350,600)


class MyScreen(Screen):
    pass

class CatalogueContent(Screen):
    pass

class OrdersContent(Screen):
    pass


class SalesContent(Screen):
    pass

"""class SalesGraph(Screen,Database):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.graph_data()
    def graph_data(self):

        self.cursor.execute("SELECT amount FROM maji_mazuri.cash_sales3;")
        data=self.cursor.fetchall()
        sales=[]
        for x in data:
            sales.append(x[0])

        self.cursor.execute("SELECT entry_date FROM maji_mazuri.cash_sales3;")
        data=self.cursor.fetchall()
        dates=[]
        for x in data:
            dates.append(x[0])

        actual_date=[]
        for act in dates:
            datetime.strptime(act, "%d-%m-%Y")
            actual_date.append(act)

       

        #create the graph
        fig, ax = plt.subplots()
        ax.plot(actual_date, sales)
        ax.set_xlabel('Time')
        ax.set_ylabel('Sales')
        ax.set_title('Sales over Time')

        #set the graph
        layout=self.ids.sale_graph
        canvas = FigureCanvasKivyAgg(figure=fig)
        layout.add_widget(canvas)
        """
        

    
       
    

   
    


    
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
       # sm.add_widget(MyScreen(name="test"))
        sm.add_widget(SellerScreen(name="orders"))
        sm.add_widget(CustomerBrowse(name="customerbrowse"))
        sm.add_widget(SalesGraph(name="sales_graph"))
        #sm.add_widget(MyGraph(name="my"))
        #Loading up every screen
        return sm
    
         
if __name__=="__main__":
    MyApp().run()
        