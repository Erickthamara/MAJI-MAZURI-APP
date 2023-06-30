from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.factory import Factory
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.list import ThreeLineIconListItem,IconLeftWidget,TwoLineIconListItem
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.metrics import dp   #data pixels
from kivy.properties import StringProperty,NumericProperty



class CustomerBrowse(MDScreen): 
    num = StringProperty(0)
    dialog9=None
    cart_count = NumericProperty(0)

    def __init__(self, **kwargs):
        super(CustomerBrowse, self).__init__(**kwargs)

        #self.cart_dot=None
        #Clock.schedule_once(self.add_cart_dot, 0)
        
        self.num = str(0)
        self.widget_list=[]
    
    def increase_quantity(self, bottom_sheet):
        bottom_sheet.num = str(int(bottom_sheet.num) + 1)

    def decrease_quantity(self, bottom_sheet):
        if int(bottom_sheet.num) > 0:
            bottom_sheet.num = str(int(bottom_sheet.num) - 1)

    def show_example_custom_bottom_sheet(self,image,price,rating):
        bottom_sheet=Factory.ContentCustomSheet()
        bottom_sheet.image=image
        bottom_sheet.price=price
        bottom_sheet.rating=rating
        bottom_sheet.num = str(0) # Add a separate num property for each bottom sheet

        
        self.custom_sheet = MDCustomBottomSheet(screen=bottom_sheet)
        self.custom_sheet.open()






        
    def topbar_close2(self):   
        if self.dialog9 is None:
                self.dialog9 = MDDialog(
                    title="Log Out?",
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            on_press=self.dismiss9,
                            
                        ),
                        MDRaisedButton(
                            text="YES",
                            on_press=self.close_screen2
                            
                        ),
                    ],
                )
        self.dialog9.open()

    def dismiss9(self,instance):
        self.dialog9.dismiss()
    def close_screen2(self,instance):
        #calls a dialog that will go back to welcomescreen
        self.manager.current = 'welcome'
        self.manager.transition.direction = 'right'
        self.dismiss9(self)
    
    def cart_screen(self):
        #calls a dialog that will go back to welcomescreen
        self.manager.current = 'checkout'
        self.manager.transition.direction = 'left'
        
    
   
    def add_to_cart(self):
        
      
        item2=TwoLineIconListItem(
            IconLeftWidget(
                icon="language-python"
            ),
            text="Single-line item with avatar",
            secondary_text="Secondary text here"
        )
        #container = self.manager.get_screen("checkout").ids.container2
        #container.add_widget(item2,0)
        self.widget_list.insert(0,item2)
        self.update_container2()

    def update_container2(self):
        container = self.manager.get_screen("checkout").ids.container2
          
        container.clear_widgets()    
        for widget in self.widget_list:      
            container.add_widget(widget)

    def add_to_cart2(self, nav_item):
        # change to the MainScreen and switch to the spcified MDBottomNavigationItem
       
        button=self.ids.bottom_nav
        self.custom_sheet.dismiss()
        button.switch_tab(nav_item)
       