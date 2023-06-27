from kivymd.uix.screen import MDScreen
from kivy.factory import Factory
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.properties import StringProperty

class CustomerBrowse(MDScreen): 
    num = StringProperty(0)
    dialog9=None

    def __init__(self, **kwargs):
        super(CustomerBrowse, self).__init__(**kwargs)
        Clock.schedule_once(self.add_to_cart, 0)
        
        self.num = str(int(0))






        
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
    
    def add_to_cart(self,instance):
        # Add the cart functionality here
        # For example, you can toggle the opacity of the red dot label
        self.cart_dot = MDLabel(text='●', theme_text_color='Error', halign='center')
        self.cart_dot.font_style = 'Caption'
        self.cart_dot.font_size = '10sp'
        self.cart_dot.opacity = 0
        self.ids.bar.ids.right_actions.add_widget(self.cart_dot)


        if self.cart_dot.opacity == 0:
            self.cart_dot.opacity = 1
        else:
            self.cart_dot.opacity = 0
        print("working")
    

    def change_text(self):
       # self.random_number = str(random.randint(1, 100))
        pass
    def increase_quantity(self):
        self.quantity += 1

    def decrease_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1