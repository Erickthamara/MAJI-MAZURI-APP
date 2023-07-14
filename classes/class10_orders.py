from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp   #data pixels
from kivy.clock import Clock
from .zdatabase import Database
import datetime as dt
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

from .class2_login import LoginScreen
from .class8_transactions import Transactions

class OrdersScreen(Transactions):
    def __init__(self, **kw):
        super().__init__(**kw)

        #Clock.schedule_once(self.order_table, 0)

        self.instance_table1 = None  # Initialize instance_table variable
        self.current_row1 = None  # Initialize current_row variable
        self.selected_rows=[]
    def order2(self):
        float_layout = self.ids.my_float_layout

    def order_table(self): 
        # ORDERS TABLE
        headers=["Order Status","Item","Amount","Street Address","House Number","Date","Order_ID"]
        if LoginScreen.main_seller_id:
            self.cursor.execute(f"SELECT order_status,ordered_item,amount,street_name,house_number,order_date,order_id FROM maji_mazuri.order WHERE seller_id={LoginScreen.main_seller_id} ORDER BY order_id DESC")
            myresult = self.cursor.fetchall()
            rows = [] 
            for row in myresult:
                rows.append(row)

            self.mytable_order=MDDataTable(
                size_hint=(.9,.7),
                pos_hint= {'center_x':0.5, 'center_y':0.55},
                check=True,
                use_pagination=True,
                pagination_menu_height="240dp",
                background_color_header="#65275d",
                background_color_selected_cell="#c7a7db",

                column_data=[(header, dp(30)) for header in headers],
                row_data=rows

            )
            float_layout = self.ids.my_float_layout
            #Here we bind the oncheck press to this table
            self.mytable_order.bind(on_check_press=self.on_check_press)
            # self.mytable.bind(on_row_press=self.on_row_press)
            float_layout.add_widget(self.mytable_order)
       

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''
        self.instance_table1=instance_table
        self.current_row1=current_row
        if current_row in self.selected_rows:
            self.selected_rows.remove(current_row)  # Deselect the row if already selected
        else:
            self.selected_rows.append(current_row)  # Select the row if not selected
 
 
    def update_selected_rows(self, *args):
        if self.selected_rows:
            for row in self.selected_rows:
                update_query = f"UPDATE maji_mazuri.order SET order_status = 'COMPLETE' WHERE order_id = {row[-1]}"
                self.cursor.execute(update_query)
                self.connection.commit()

            self.selected_rows = []

            float_layout = self.ids.my_float_layout
            float_layout.remove_widget(self.mytable_order)
            self.success_update_dialog()

            # ORDERS TABLE
            self.order_table()

            # Update the records
            text = "Order Completed"
            date = dt.datetime.now().strftime('%d-%m-%Y')
            time = dt.datetime.now().strftime('%I:%M:%S %p')
            self.insert_item_to_database(text, date, time)
            self.retrieve_exixting_reports()

        else:
            print("Select a row")

    def success_update_dialog(self):
            
            if self.dialog is None:
                self.dialog = MDDialog(
                    title="Order status updated",
                    buttons=[
                        MDRaisedButton(
                            text="CONFIRM",
                            on_press=self.dismiss_dialog1,
                            
                        ),
                    ],
                )
            self.dialog.open()

    def dismiss_dialog1(self, instance):
        self.dialog.dismiss()

    
