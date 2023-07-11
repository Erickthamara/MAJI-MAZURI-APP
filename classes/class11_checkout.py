from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp   #data pixels
from kivy.clock import Clock
from .zdatabase import Database
import datetime as dt
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.label import Label

from .class8_transactions import Transactions

class CheckoutScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.amount=0
        
    
    def browse_screen(self):
        
        self.manager.current = 'customerbrowse'
        self.manager.transition.direction = 'right'

    


        