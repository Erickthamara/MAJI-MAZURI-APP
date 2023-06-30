from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp   #data pixels
from kivy.clock import Clock
from .zdatabase import Database
import datetime as dt
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from .class8_transactions import Transactions

class CheckoutScreen(Screen):
    def browse_screen(self):
        #calls a dialog that will go back to welcomescreen
        self.manager.current = 'customerbrowse'
        self.manager.transition.direction = 'right'
        