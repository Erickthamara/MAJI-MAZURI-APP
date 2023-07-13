from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp   #data pixels
from kivy.clock import Clock
from .zdatabase import Database
import datetime as dt
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineIconListItem,IconLeftWidget

from .class2_login import LoginScreen

class Transactions(Screen,Database):
  def __init__(self, **kw):
        super().__init__(**kw)
        self.widget_list = []
        
  


  def retrieve_exixting_reports(self):
        #this loads up all transactions alareday in the database
        #called from seller.py LINE 76 by 
        self.widget_list=[]
        if LoginScreen.main_seller_id:
            self.cursor.execute(f"SELECT * FROM maji_mazuri.seller_transactions WHERE seller_id={LoginScreen.main_seller_id} ORDER BY report_id DESC")
            reports=self.cursor.fetchall()

            for row in reports:
                  item = ThreeLineIconListItem(
                  IconLeftWidget(icon="account-details"),
                  text=row[1],
                  secondary_text=row[2],
                  tertiary_text=row[3]
                  )
                  self.widget_list.append(item)
            #self.widget_list.reverse()
            self.update_container()

  def insert_item_to_database(self,text,secondary_text,tertiary_text):
        #this is called inoreder to add transactions to the DB
        if LoginScreen.main_seller_id:
            query = f"INSERT INTO maji_mazuri.seller_transactions (text, secondary_text, tertiary_text,seller_id) VALUES (%s, %s, %s,%s);"
            values = (text,secondary_text,tertiary_text,LoginScreen.main_seller_id)

            self.cursor.execute(query, values)
            self.connection.commit()
            self.retrieve_exixting_reports()



         

  def update_container(self):
        container = self.ids.container
        container.clear_widgets()
        for widget in self.widget_list:
            container.add_widget(widget)
 
