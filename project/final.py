from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
from gesture import basicCamera   #basicCamera function is imported
from open import runPackman       #runPackman function is imported
from open import jsonlocation     #jsonlocation function is imported
from drive import advanceCamera   #advacneCamera function is imported

store = JsonStore('location.json')

class MainWindow(Screen):
    pass

class BasicGames(Screen):
    def cam(self):
        basicCamera()    #basicCamera function is called

    def pac(self):
        runPackman()     #runPackam function is called
        basicCamera()    #basicCamera function is called


class AdvancedGames(Screen):

    def btn(self):
        if(store):
            jsonlocation()    #jsonlocation function is called
            advanceCamera()   #advanceCamera function is called
        else:
            show_popup()    #show_popup function is called

    def change(self):
        if(store):
            store.clear()    #data in location.json is removed

    def cam(self):
        advanceCamera()    #advanceCamera function is called

class WindowManager(ScreenManager):
    pass


class P(FloatLayout):
    location = ObjectProperty(None)
    def call(self):
        print("Location:", self.location.text)
        store.put(self.location.text)



def show_popup():
    show = P()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size = (400, 400))

    popupWindow.open()

kv = Builder.load_file("final.kv")   #loading kv file


class MyMainApp(App):
    def build(self):
         return kv


if __name__ == "__main__":
    MyMainApp().run()