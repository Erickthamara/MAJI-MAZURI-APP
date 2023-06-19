from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp   #data pixels
from kivy.clock import Clock
from .zdatabase import Database
import datetime as dt
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

class CatalogueScreen(Screen,Database):
     def __init__(self, **kw):
         super().__init__(**kw)

         self.selected_rows2=[]
         self.instance_table2 = None  # Initialize instance_table variable
         self.current_row2 = None  # Initialize current_row variable


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
     
     def input_check(self):
        #Ensure the user only enters a numeral
        new_num=self.ids.num_update.text.strip()
        if not new_num.isdigit():
            print("Numerals only")
            self.ids.update_catalogue.disabled=True
        else:
           self.ids.update_catalogue.disabled=False

           
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
            


        

