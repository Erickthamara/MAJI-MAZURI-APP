from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.clock import Clock
from .zdatabase import Database


class OrderScreen(Screen,Database):
    
    def __init__(self, **kwargs):
        super(OrderScreen, self).__init__(**kwargs)
        self.instance_table1 = None  # Initialize instance_table variable
        self.current_row1 = None  # Initialize current_row variable
        self.selected_rows=[]
        self.selected_rows2=[]
        self.instance_table2 = None  # Initialize instance_table variable
        self.current_row2 = None  # Initialize current_row variable

       

    def on_enter(self):
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
        
    """def on_row_press(self, instance_table1, current_row2):
        self.instance_table2=instance_table1
        self.current_row2=current_row2

        row_index = current_row2.index  # Get the index of the clicked row
        if row_index in self.selected_rows:
            selected_row_index = self.selected_rows.index(row_index)
            row_data = self.mytable.row_data[self.selected_rows[selected_row_index]]
            print(row_data)
        elif 0 <= row_index < len(self.mytable.row_data):
            row_data = self.mytable.row_data[row_index]  # Get the data of the clicked row
            print(row_data)
        else:
            print("Invalid row index")
    """    

    def delete_selected_rows(self, *args):
       if self.instance_table1 is not None and self.current_row1 is not None:

        for row in self.selected_rows:
            delete_query = f"DELETE FROM maji_mazuri.customer WHERE customer_id = {row[0]}"
            self.cursor.execute(delete_query)
            self.connection.commit()
        return self.on_enter()
       
   
   

    