
from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp   #data pixels
from kivy.clock import Clock
from .zdatabase import Database
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.app import App
from kivymd.uix.menu import MDDropdownMenu

from kivy.garden.matplotlib import FigureCanvasKivy

from datetime import datetime
import matplotlib.pyplot as plt



class SellerScreen(Screen,Database):
    dialog=None
    
    def __init__(self, **kwargs):
        super(SellerScreen, self).__init__(**kwargs)
       # self.graph_data()
        Clock.schedule_once(self.onmycall, 0)

       

        self.instance_table1 = None  # Initialize instance_table variable
        self.current_row1 = None  # Initialize current_row variable
        self.selected_rows=[]

        self.selected_rows2=[]
        self.instance_table2 = None  # Initialize instance_table variable
        self.current_row2 = None  # Initialize current_row variable
        
    def dropdown(self):   
        self.menu_items = [
            {
                "height": dp(56),
                "viewclass": "OneLineListItem",
                "text": f"Price",
                "on_release": lambda x=f"Price ": self.set_item(x)
            },
            {
                "height": dp(56),
                "viewclass": "OneLineListItem",
                "text": f"Quantity",
                "on_release": lambda x=f"Quantity ": self.set_item(x)
            }
           
              ]
        self.menu = MDDropdownMenu(
            caller=self.ids.field,
            items=self.menu_items,
            position="bottom",
            width_mult=4,
        )
        self.menu.open()

    def set_item(self, text__item):
        self.ids.field.text = text__item
        self.menu.dismiss()
    
    def dropdown_bar(self):   
        self.menu_items = [
            {
                "height": dp(56),
                "viewclass": "OneLineListItem",
                "text": f"Log Out",
                "on_release":  self.close_screen()
            }
           
              ]
        self.menu = MDDropdownMenu(
            caller=self.ids.bar,
            items=self.menu_items,
            position="bottom",
            width_mult=4,
        )
        self.menu.open()

    def close_screen(self):
        self.manager.current = 'welcome'
        self.manager.transition.direction = 'right'
    
    def handle_right_item(self):
        if self.ids.bar.focus:
            self.dropdown_bar()
        
    def input_check(self):
        #Ensure the user only enters a numeral
        new_num=self.ids.num_update.text.strip()
        if not new_num.isdigit():
            print("Numerals only")
            self.ids.update_catalogue.disabled=True
        else:
           self.ids.update_catalogue.disabled=False
    
    def sales_input_check(self):
        #Ensure the user only enters a numeral
        new_num=self.ids.sales_entry.text.strip()
        if not new_num.isdigit():
            print("Numerals only")
            self.ids.submit_sales.disabled=True
        else:
           self.ids.submit_sales.disabled=False
    


    def onmycall(self,*args):
        self.catalogue_table()  
        self.order_table()
        self.sales_table()
         
    def catalogue_table(self):
         
         
         headers=["ID","SIZE","PRICE (Ksh)","Quantity"]
         self.cursor.execute("SELECT * FROM maji_mazuri.catalogue")
         result = self.cursor.fetchall()
         row_data = [] 
         for row in result:
            row_data.append(row)
        
         self.mytable_catalogue=MDDataTable(
            size_hint=(.9,.5),
            pos_hint= {'center_x':0.5, 'center_y':0.63},
            check=True,
            use_pagination=True,
            pagination_menu_height="240dp",
            

            column_data=[(header, dp(30)) for header in headers],
            row_data=row_data
        )
         layout=self.ids.catalogue_layout
         self.mytable_catalogue.bind(on_check_press=self.on_check_press2)
         layout.add_widget(self.mytable_catalogue)

    def on_check_press2(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''
        self.instance_table2=instance_table
        self.current_row2=current_row
        if current_row in self.selected_rows2:
            self.selected_rows2.remove(current_row)  # Deselect the row if already selected
        else:
            self.selected_rows2.append(current_row)  # Select the row if not selected
        
        return self.selected_rows2
    
    def update_data(self):
        text=self.ids.field.text.strip()
        amount=self.ids.num_update.text.strip()
        new_amount=float(amount)

        if not amount or not text:
          self.ids.update_catalogue.disabled = True
        else:
            new_amount = float(amount)
       
            if text=="Price" and amount:
                if len(self.selected_rows2)==1:
                    row=self.selected_rows2[0]
                    row_id=row[0]
                    
                    self.cursor.execute(f"UPDATE maji_mazuri.catalogue SET price = {new_amount} WHERE id ={row_id}")
                    self.connection.commit() 

                    # remove then recall the catalogue table
                    layout=self.ids.catalogue_layout
                    
                    layout.remove_widget(self.mytable_catalogue)

                    # Catalogue TABLE
                    self.catalogue_table()



                else:
                    print("Select only a single row")


            elif text=="Quantity" and amount:
                if len(self.selected_rows2)==1:
                    row=self.selected_rows2[0]
                    row_id=row[0]
                    
                    self.cursor.execute(f"UPDATE maji_mazuri.catalogue SET remaining = {new_amount} WHERE id ={row_id}")
                    self.connection.commit()

                    # remove then recall the catalogue table
                    layout=self.ids.catalogue_layout
                    
                    layout.remove_widget(self.mytable_catalogue)

                    # Catalogue TABLE
                    self.catalogue_table()
                            
                else:
                    print("Select only a single row")
            


        


         
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
       elif not self.selected_rows:
          print("select a row")

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
        date=datetime.datetime.now().strftime('%d-%m-%Y')
        time=datetime.datetime.now().strftime('%I:%M:%S %p')
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
    
    
    

    def show_alert_dialog_delete(self):
            
            if not self.dialog:
                self.dialog = MDDialog(
                    text="Are you sure you want to delete a record?",
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            on_press=self.dismiss_dialog,
                            
                        ),
                        MDFlatButton(
                            text="DISCARD",
                            on_press=self.delete,
                            
                        ),
                    ],
                )
            self.dialog.open()

    def dismiss_dialog(self, instance):
        self.dialog.dismiss()

    def delete(self,instance):
        self.delete_selected_rows()
        self.dialog.dismiss()

    def show_alert_dialog_update(self):
            
            if not self.dialog:
                self.dialog = MDDialog(
                    text="Are you sure you want to update a record?",
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            on_press=self.dismiss_dialog,
                            
                        ),
                        MDFlatButton(
                            text="Confirm",
                            on_press=self.delete,
                            
                        ),
                    ],
                )
            self.dialog.open()
   
    

    """def graph_data(self):

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
        canvas = FigureCanvasKivy(figure=fig)
        layout.add_widget(canvas)
        """

    
       
    

   
   

    