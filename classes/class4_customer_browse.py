from kivymd.uix.screen import MDScreen
from kivy.factory import Factory
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivy.properties import StringProperty

class CustomerBrowse(MDScreen): 
    num = StringProperty(0)

    def __init__(self, **kwargs):
        super(CustomerBrowse, self).__init__(**kwargs)
        self.num = str(int(0))

    def change_text(self):
       # self.random_number = str(random.randint(1, 100))
        pass
    def increase_quantity(self):
        self.quantity += 1

    def decrease_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1