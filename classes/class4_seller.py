
from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp   #data pixels
from kivy.clock import Clock
from .zdatabase import Database
from kivymd.uix.list import OneLineIconListItem

from kivymd.uix.menu import MDDropdownMenu



class SellerScreen(Screen,Database):
    
    def __init__(self, **kwargs):
        super(SellerScreen, self).__init__(**kwargs)
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
    
    def input_check(self):
        #Ensure the user only enters a numeral
        new_num=self.ids.num_update.text.strip()
        if not new_num.isdigit():
            print("Numerals only")
            self.ids.update_catalogue.disabled=True
        else:
           self.ids.update_catalogue.disabled=False
    
    def data_update(self):
        #to upadate the data checcked by the user
        pass


    def dat_update(self):
        #Here we check which option the user has chosen and update it accordingly
        if self.ids.field=="Quantity" :
         pass


    
   

    def on_enter(self):
         
         headers=["ID","SIZE","PRICE (Ksh)","Quantity"]
         self.cursor.execute("SELECT * FROM maji_mazuri.catalogue")
         result = self.cursor.fetchall()
         row_data = [] 
         for row in result:
            row_data.append(row)
        
         mytable=MDDataTable(
            size_hint=(.9,.5),
            pos_hint= {'center_x':0.5, 'center_y':0.63},
            check=True,
            use_pagination=True,
            pagination_menu_height="240dp",
            elevation=3,

            column_data=[(header, dp(30)) for header in headers],
            row_data=row_data
        )
         layout=self.ids.catalogue_layout
         mytable.bind(on_check_press=self.on_check_press2)
         layout.add_widget(mytable)


         

        # ORDERS TABLE
         headers=["cutomer_id","email","phone_no","first_name","last_name","password2","password3"]
         self.cursor.execute("SELECT * FROM maji_mazuri.customer")
         myresult = self.cursor.fetchall()
         rows = [] 
         for row in myresult:
            rows.append(row)
 
         self.mytable=MDDataTable(
            size_hint=(.9,.7),
            pos_hint= {'center_x':0.5, 'center_y':0.6},
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
         self.mytable.bind(on_check_press=self.on_check_press)
        # self.mytable.bind(on_row_press=self.on_row_press)
         float_layout.add_widget(self.mytable)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''
        self.instance_table1=instance_table
        self.current_row1=current_row
        if current_row in self.selected_rows:
            self.selected_rows.remove(current_row)  # Deselect the row if already selected
        else:
            self.selected_rows.append(current_row)  # Select the row if not selected


   
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
       
        #myrow=self.on_check_press2(self.instance_table2, self.current_row2)


        if text=="Price" and amount:
             if len(self.selected_rows2)==1:
                row=self.selected_rows2[0]
                row_id=row[0]
                
                self.cursor.execute(f"UPDATE maji_mazuri.catalogue SET price = {new_amount} WHERE id ={row_id}")
                self.connection.commit()
                
                myresult = self.cursor.fetchall()
                row=[]
                for r in myresult:
                    row.append(r[0])
                print(row)

             else:
                 print("Select only a single row")


        elif text=="Quantity" and amount:
             self.cursor.execute("SELECT remaining FROM maji_mazuri.catalogue")
             myresult = self.cursor.fetchall()
             row=[]
             for r in myresult:
                 row.append(r)

             print(row)
        
   
    

    def delete_selected_rows(self, *args):
       if self.selected_rows:

        for row in self.selected_rows:
            delete_query = f"DELETE FROM maji_mazuri.customer WHERE customer_id = {row[0]}"
            self.cursor.execute(delete_query)
            self.connection.commit()

        self.selected_rows=[]

        float_layout = self.ids.my_float_layout
        float_layout.remove_widget(self.mytable)

         # ORDERS TABLE
        headers=["cutomer_id","email","phone_no","first_name","last_name","password2","password3"]
        self.cursor.execute("SELECT * FROM maji_mazuri.customer")
        myresult = self.cursor.fetchall()
        rows = [] 
        for row in myresult:
            rows.append(row)
 
        self.mytable=MDDataTable(
            size_hint=(.9,.7),
            pos_hint= {'center_x':0.5, 'center_y':0.6},
            check=True,
            use_pagination=True,
            pagination_menu_height="240dp",
            background_color_header="#65275d",
            background_color_selected_cell="#c7a7db",

            column_data=[(header, dp(30)) for header in headers],
            row_data=rows

        )
        
        
        
        self.mytable.bind(on_check_press=self.on_check_press)
        # self.mytable.bind(on_row_press=self.on_row_press)
        float_layout.add_widget(self.mytable)
    
       elif not self.selected_rows:
          print("select a row")

    
       
    

   
   

    