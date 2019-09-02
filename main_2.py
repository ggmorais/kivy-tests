import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.core.window import Window


class Game(Widget):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        with self.canvas:
            self.background = Rectangle(pos=(0, 0), size=(Window.size[0], Window.size[1]), source='img/background_1.jpg') # BACKGROUND
            #self.player = Rectangle

class MyApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    MyApp().run()
