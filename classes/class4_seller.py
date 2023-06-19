
from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp   #data pixels
from kivy.clock import Clock


from .zdatabase import Database
from .class6_sales import SalesScreen
from .class7_catalogue import CatalogueScreen
from .class8_reports import Reports


from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.app import App
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import ThreeLineIconListItem,IconLeftWidget


from kivy.garden.matplotlib import FigureCanvasKivy


import matplotlib.pyplot as plt
import datetime as dt



class SellerScreen(SalesScreen,CatalogueScreen,Reports):
    dialog=None
    dialog2=None
    
    def __init__(self, **kwargs):
        super(SellerScreen, self).__init__(**kwargs)
       # self.graph_data()
        Clock.schedule_once(self.onmycall, 0)

        self.widget_list = []
        
        

       

        self.instance_table1 = None  # Initialize instance_table variable
        self.current_row1 = None  # Initialize current_row variable
        self.selected_rows=[]

        
        
    
    
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
    
    def handle_right_item(self):
        if self.ids.bar.focus:
            self.dropdown_bar()
        
    
    
    

    def onmycall(self,*args):
        self.catalogue_table()  
        self.order_table()
        self.sales_table()
        self.retrieve_exixting_reports()
         
   
         
    def order_table(self):
         
        # ORDERS TABLE
         headers=["cutomer_id","email","phone_no","first_name","last_name","password2","password3"]
         self.cursor.execute("SELECT * FROM maji_mazuri.customer")
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
 
 
    def delete_selected_rows(self, *args):
       if self.selected_rows:

        for row in self.selected_rows:
            delete_query = f"DELETE FROM maji_mazuri.customer WHERE customer_id = {row[0]}"
            self.cursor.execute(delete_query)
            self.connection.commit()

        self.selected_rows=[]

        float_layout = self.ids.my_float_layout
        float_layout.remove_widget(self.mytable_order)

         # ORDERS TABLE
        self.order_table()

        #update the records
        text=f"Order record Deleted"
        date=dt.datetime.now().strftime('%d-%m-%Y')
        time=dt.datetime.now().strftime('%I:%M:%S %p')
        self.insert_item_to_database(text,date,time)
        self.retrieve_exixting_reports()


       elif not self.selected_rows:
          print("select a row")

    

    
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



    
    
    

    def show_dialog_delete(self):
            
            if self.dialog is None:
                self.dialog = MDDialog(
                    text="Are you sure you want to delete a record?",
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            on_press=self.dismiss_dialog,
                            
                        ),
                        MDRaisedButton(
                            text="CONFIRM",
                            on_press=self.delete_row,
                            
                        ),
                    ],
                )
            self.dialog.open()

    def dismiss_dialog(self, instance):
        self.dialog.dismiss()

    def delete_row(self,instance):
        self.delete_selected_rows()
        self.dialog.dismiss()

    
    #code to remove shadows in future
    """
    def remove_item(self):
        Clock.schedule_once(self._remove_item, 1)  # delay to see the checkbox animation.

    def _remove_item(self, _):
        self.parent.remove_widget(self)
    """
  
    