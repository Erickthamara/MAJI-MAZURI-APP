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


class Transations(Screen,Database):
  def __init__(self, **kw):
        super().__init__(**kw)
        self.widget_list = []


  def retrieve_exixting_reports(self):
        self.widget_list=[]

        self.cursor.execute("SELECT * FROM maji_mazuri.report ORDER BY report_id DESC")
        reports=self.cursor.fetchall()

        for row in reports:
            item = ThreeLineIconListItem(
                IconLeftWidget(icon="language-python"),
                text=row[1],
                secondary_text=row[2],
                tertiary_text=row[3]
            )
            self.widget_list.append(item)
        #self.widget_list.reverse()
        self.update_container()

  def insert_item_to_database(self,text,secondary_text,tertiary_text):
        query = "INSERT INTO maji_mazuri.report (text, secondary_text, tertiary_text) VALUES (%s, %s, %s)"
        values = (text,secondary_text,tertiary_text)

        self.cursor.execute(query, values)
        self.connection.commit()


  def report_test(self):
        item=ThreeLineIconListItem(
                IconLeftWidget(
                    icon="language-python"
                ), text="Number1",
                secondary_text="Secondary text here",
                tertiary_text="fit more text than usual"
             )
        

        self.widget_list.insert(0, item)
        self.insert_item_to_database(item.text,item.secondary_text,item.tertiary_text)
        self.update_container()
        
        
  def report_test2(self):
         item2=ThreeLineIconListItem(
                IconLeftWidget(
                    icon="language-python"
                ), text="Number2",
                secondary_text="Secondary text here",
                tertiary_text="fit more text than usual"
             )
        
         self.widget_list.insert(0, item2)
         self.insert_item_to_database(item2.text,item2.secondary_text,item2.tertiary_text)
         self.update_container()
         

  def update_container(self):
        container = self.ids.container
        container.clear_widgets()
        for widget in self.widget_list:
            container.add_widget(widget)
            
