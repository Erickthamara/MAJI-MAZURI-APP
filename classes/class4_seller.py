
from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp   #data pixels
from kivy.clock import Clock


from .zdatabase import Database
from .class6_sales import SalesScreen
from .class7_catalogue import CatalogueScreen
from .class8_transactions import Transactions
from .class10_orders import OrdersScreen


from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.app import App
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import ThreeLineIconListItem,IconLeftWidget


from kivy.garden.matplotlib import FigureCanvasKivy


import matplotlib.pyplot as plt
import datetime as dt




class SellerScreen(SalesScreen,CatalogueScreen,OrdersScreen,Transactions):
    dialog=None
    dialog2=None
    
    def __init__(self, **kwargs):
        super(SellerScreen, self).__init__(**kwargs)
       # self.graph_data()
        Clock.schedule_once(self.onmycall, 0)

        self.widget_list = []
        
    def on_enter(self, *args):
        self.catalogue_table()
        self.sales_table()
        self.retrieve_exixting_reports()
        self.order_table()
        self.logged_in()

    def logged_in(self): 
        text=f"Logged in"
        date=dt.datetime.now().strftime('%d-%m-%Y')
        time=dt.datetime.now().strftime('%I:%M:%S %p')
        self.insert_item_to_database(text,date,time)
    def log_out(self):  
        text=f"Logged Out"
        date=dt.datetime.now().strftime('%d-%m-%Y')
        time=dt.datetime.now().strftime('%I:%M:%S %p')
        self.insert_item_to_database(text,date,time)
        

    def onmycall(self,*args):
        pass
        
        
        
    def topbar_close(self):   
        if self.dialog2 is None:
                self.dialog2 = MDDialog(
                    title="Log Out?",
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            on_press=self.dismiss2,
                            
                        ),
                        MDRaisedButton(
                            text="YES",
                            on_press=self.close_screen
                            
                        ),
                    ],
                )
        self.dialog2.open()

    def dismiss2(self,instance):
        self.dialog2.dismiss()

    def close_screen(self,instance):
        #calls a dialog that will go back to welcomescreen
        self.manager.current = 'welcome'
        self.manager.transition.direction = 'right'

        
        #transaction details
        #logged out
        text=f"Logged out"
        date=dt.datetime.now().strftime('%d-%m-%Y')
        time=dt.datetime.now().strftime('%I:%M:%S %p')
        self.insert_item_to_database(text,date,time)

        self.dismiss2(self)
    
    
         
    
    def set_list(self, text=" "): 
        #grabb all children of the main widget in this case mdlist
        cont = self.ids.container.children
        #create a list to hold all the dates
        widget_date_list=[]

        for item in cont:
         widget_date_list.append(item.secondary_text)

        #print(widget_date_list)

        self.ids.container.clear_widgets()  # Clear the container before populating search results
        
        #for item, date in zip(cont, widget_date_list):
        if text in widget_date_list:
            for new_text in widget_date_list:
             if new_text==text:
              self.ids.container.add_widget(item)
            
        #find a way to compare the widget_text with its parent

    

    
    #code to remove shadows in future
    """
    def remove_item(self):
        Clock.schedule_once(self._remove_item, 1)  # delay to see the checkbox animation.

    def _remove_item(self, _):
        self.parent.remove_widget(self)
    """
  
    