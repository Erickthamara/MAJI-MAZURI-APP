
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
        self.dismiss2(self)
    
   
    def onmycall(self,*args):
        self.catalogue_table()  
        self.order_table()
        self.sales_table()
        self.retrieve_exixting_reports()
         
    
    def set_list(self, text=" "): 
        # text defaults to blank space to not show any icons initially
        # each OneLineListItem takes the pressed func on press
        cont=self.ids.container
        self.ids.container.clear_widgets() # refresh list

        children = list(self.ids.container.children)
        mylist= [type(widget) for widget in cont.walk(restrict=True)]
        print(mylist)
        for child in children:
            if text.casefold() in child.text.casefold():
                self.ids.container.add_widget(child)

    

    

    
    #code to remove shadows in future
    """
    def remove_item(self):
        Clock.schedule_once(self._remove_item, 1)  # delay to see the checkbox animation.

    def _remove_item(self, _):
        self.parent.remove_widget(self)
    """
  
    