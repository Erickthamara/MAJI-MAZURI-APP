from kivy.uix.screenmanager import Screen

class CatalogueScreen(Screen):
    def switch_screen(self, screen_name):
        screen_manager = self.parent.parent
        screen_manager.current = screen_name