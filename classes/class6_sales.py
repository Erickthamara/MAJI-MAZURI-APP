from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp   #data pixels
from kivy.clock import Clock
from .zdatabase import Database
import datetime as dt
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from .class8_reports import Reports

class SalesScreen(Reports):
    dialog3=None
    def sales_table(self):
         
         headers=["SALES_ID","AMOUNT","DATE","TIME"]
         self.cursor.execute("SELECT * FROM maji_mazuri.cash_sales3")
         result = self.cursor.fetchall()
         row_data = [] 
         for row in result:
            row_data.append(row)
        
         self.mytable_catalogue=MDDataTable(
            size_hint=(.9,.6),
            pos_hint= {'center_x':0.5, 'center_y':0.42},
            check=True,
            use_pagination=True,
            pagination_menu_height="240dp",

            column_data=[(header, dp(30)) for header in headers],
            row_data=row_data
        )
         layout=self.ids.sales_layout
         self.mytable_catalogue.bind(on_check_press=self.on_check_press2)
         layout.add_widget(self.mytable_catalogue)

    def input_sales(self):
        #sale is the value entered by the seller
        sale=self.ids.sales_entry.text.strip()
        date=dt.datetime.now().strftime('%d-%m-%Y')
        time=dt.datetime.now().strftime('%I:%M:%S %p')
        if not sale:
            self.ids.submit.disabled=True
        else:
             exexute1="INSERT INTO maji_mazuri.cash_sales3(amount,entry_date,entry_time) VALUES(%s,%s,%s);"
             value=(sale,date,time)
             self.cursor.execute(exexute1,value)
             self.connection.commit()

             layout=self.ids.sales_layout
             layout.remove_widget(self.mytable_catalogue)
             self.sales_table()
             self.alert_dialog_sale()

             #here we update the report
             transaction_sale=f"Sales Record Updated:{sale}"
             self.insert_item_to_database(transaction_sale,date,time)
             self.retrieve_exixting_reports()

    def alert_dialog_sale(self):
          
          if not self.dialog3:
                self.dialog3 = MDDialog(
                    title="SALES RECORD UPDATED!",
                    radius=[20,7,20,7],
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_press=self.dismiss_dialog3,   
                        ),
                    ],
                )
          self.dialog3.open()

    def dismiss_dialog3(self, instance):
        self.dialog3.dismiss()

    def sales_input_check(self):
        #Ensure the user only enters a numeral
        new_num=self.ids.sales_entry.text.strip()
        if not new_num.isdigit():
            self.show_numeral_message()
            self.ids.submit_sales.disabled=True
        else:
           self.ids.submit_sales.disabled=False

    def show_numeral_message(self):
      snackbar=Snackbar(
          text="Enter Numerals Only!",
          snackbar_x="10dp",
          snackbar_y="10dp",
          pos_hint={'center_x': 0.5, 'center_y': 0.5},
          #bg_color=(1,0,0,1),
          radius=[20,7,20,7],
          duration=3,
          auto_dismiss=False

      )
      snackbar.buttons=[
          MDFlatButton(text="OK",
          text_color=(1,0,0,1),
          on_release=snackbar.dismiss
            )
        ]
      snackbar.open()
