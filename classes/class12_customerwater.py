from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.factory import Factory
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.list import TwoLineAvatarIconListItem,OneLineAvatarIconListItem,IconLeftWidget,IconRightWidget
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.metrics import dp   #data pixels
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.button import MDIconButton
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty,NumericProperty
from kivymd.uix.menu import MDDropdownMenu
from .class6_sales import SalesScreen
from .zcheckout_manager import CheckoutManager

import re

class CustomerWater(SalesScreen):
     def __init__(self, **kw):
         super().__init__(**kw)
         self.added_water_cash=[]
         self.added_water_widget=[]
         self.zcheckout_manager = CheckoutManager()
         self.zcheckout_manager.checkout_total = 0  # Initialize the checkout total to 
         

     def dropdown2(self):   
        self.menu_items2 = [
            {
                "height": dp(56),
                "viewclass": "OneLineListItem",
                "text": f"1L",
                "on_release": lambda x=f"1L ": self.set_item(x)
            },
            {
                "height": dp(56),
                "viewclass": "OneLineListItem",
                "text": f"5L",
                "on_release": lambda x=f"5L ": self.set_item(x)
            },
             {
                "height": dp(56),
                "viewclass": "OneLineListItem",
                "text": f"10L",
                "on_release": lambda x=f"10L": self.set_item(x)
            },
             {
                "height": dp(56),
                "viewclass": "OneLineListItem",
                "text": f"18.9L",
                "on_release": lambda x=f"18.9L ": self.set_item(x)
            },
             {
                "height": dp(56),
                "viewclass": "OneLineListItem",
                "text": f"20L",
                "on_release": lambda x=f"20L ": self.set_item(x)
            },
             {
                "height": dp(56),
                "viewclass": "OneLineListItem",
                "text": f"20L Hard",
                "on_release": lambda x=f"20L Hard ": self.set_item(x)
            }
           
              ]
        self.menu = MDDropdownMenu(
            caller=self.ids.field2,
            items=self.menu_items2,
            position="bottom",
            width_mult=4,
        )
        self.menu.open()

     def set_item(self, text__item):
        self.ids.field2.text = text__item
        self.menu.dismiss()

     def entry_warning(self):
          #Ensure the user only enters a numeral
        new_text=self.ids.amount_field.text.strip()
        if new_text:
            if not new_text.isdigit():
                self.show_numeral_message()
                self.ids.submit_order.disabled = True
                return False
            else:
                #self.update_total()
                #self.update_water_total()
                self.ids.submit_order.disabled = False
                return True
        else:
            self.ids.submit_order.disabled = True

     def checkbox_checked2 (self):
        size=self.ids.field2.text.strip()
        amount=self.ids.amount_field.text.strip()

        """if amount and size:
            self.ids.submit_order.disabled=False
        else:
            self.ids.submit_order.disabled=False
            """

        if self.ids.checkbox3.active or self.ids.checkbox4.active: 
            #self.ids.checkbox_error.text=" "
            self.ids.submit_order.disabled=False
            return True   
        else: 
            self.ids.checkbox_error.text="Select Purchase or Exchange"
            self.ids.submit_order.disabled=True
            return False
        

     def update_total(self):
        size=self.ids.field2.text.strip()
        new_amount=self.ids.amount_field.text.strip()
        if new_amount and size:
            amount = int(new_amount)
            if size == "1L":
                new = amount * 10
            elif size == "5L":
                new = amount * 50
            elif size == "10L":
                new = amount * 100
            elif size == "18.9L":
                new = amount * 190
            elif size == "20L":
                new = amount * 200
            elif size == "20L Hard":
                new = amount * 200
            else:
                new = 0
        else:
            new = 0

        self.ids.submit_order.text = f"CHECKOUT : Ksh {new}"

        # Update the checkout button text directly
        #checkout_button = self.manager.get_screen("checkout").ids.checkout_btn
        #checkout_button.text = f"CHECKOUT : Ksh {new:.2f}"
        #self.added_water.append(new)

        return new
        
     def add_to_cart2(self):
        size=self.ids.field2.text.strip()
        new_amount=self.ids.amount_field.text.strip()

        if size and new_amount:
            pass
        else:
             self.ids.submit_order.disabled=True
             print("fill in details")
             return
        
        if self.checkbox_checked2():
            pass
        else:
            self.ids.checkbox_error.text="Select Purchase or Exchange"
            self.ids.submit_order.disabled=True
            return


        cash=self.update_total()
        
        text1=f"WATER ORDER: {size}: {new_amount}"
        text2=f"CASH TOTAL : {cash}"

        #self.added_water_cash.append(cash)  # Add the cash total to the list


        self.item2=TwoLineAvatarIconListItem(
        IconLeftWidget(
            icon="trash-can",
            on_press=lambda instance: self.delete_item2(instance.parent.parent) if instance.parent else None
        ),
      
       
        text=text1,
        secondary_text=text2
   )
        
        
        #container = self.manager.get_screen("checkout").ids.container2
        #container.add_widget(item2,0)
        
        container = self.manager.get_screen("checkout").ids.container2
        container.add_widget(self.item2)

        self.update_water_total(cash)
        self.added_water_widget.append(self.item2)  # Add the item to your widget list

        #self.update_checkout_total()
 
     def delete_item2(self, item):
        container = self.manager.get_screen("checkout").ids.container2
        container.remove_widget(item)
        self.added_water_widget.remove(item)
        text=item.secondary_text
        pattern = r"CASH TOTAL : ([\d.]+)"
        matches = re.findall(pattern, text)
        if matches:
            number_str = matches[0]
            number = float(number_str)
            self.zcheckout_manager.checkout_total-=number

            checkout_button = self.manager.get_screen("checkout").ids.checkout_btn
            
            checkout_button.text = f"CHECKOUT: Ksh {self.zcheckout_manager.checkout_total:.2f}"
        
          
        
        
        #self.widget_list.remove(item)  # Remove the item from the widget list
        #self.update_checkout_total()  # Update the checkout total
     
     

     def update_water_total(self,amount):
          # Convert values to integers before summing
        self.zcheckout_manager.checkout_total+=amount
        checkout_button = self.manager.get_screen("checkout").ids.checkout_btn
       
        checkout_button.text = f"CHECKOUT: Ksh {self.zcheckout_manager.checkout_total:.2f}"
       
     def minus_water_total(self,amount):
          # Convert values to integers before summing
        if self.zcheckout_manager.checkout_total>0:
            self.zcheckout_manager.checkout_total-=amount
            checkout_button = self.manager.get_screen("checkout").ids.checkout_btn
        
            checkout_button.text = f"CHECKOUT: Ksh {self.zcheckout_manager.checkout_total:.2f}"
        
       
            
