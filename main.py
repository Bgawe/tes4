from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from landing_page import LandingPage
from lowercase_letter_screen import LowercaseLetterScreen 
from menu_page import MenuPage
from AbcAlpha import FlashCardScreen

class SupernovaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LandingPage(name='landing'))
        sm.add_widget(MenuPage(name='menu'))
        sm.add_widget(LowercaseLetterScreen(name='lowercase_letter_screen'))
        sm.add_widget(FlashCardScreen(name='Flashcard'))
        return sm

if __name__ == '__main__':
    SupernovaApp().run()