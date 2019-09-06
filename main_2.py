import os
os.environ['KIVY_IMAGE'] = 'sdl2'

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.clock import Clock


class Game(Widget):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.kboard = Window.request_keyboard(self.keyboardClosed, self)
        self.kboard.bind(on_key_down=self.keyDown)
        self.kboard.bind(on_key_up=self.keyUp)

        self.keyPressed = set()

        self.g_up = False
        self.g_down = False
        self.jump_limit = 286
        self.speed = 300
        self.floor = 100
        self.j_speed = 700

        with self.canvas:
            self.background = Rectangle(pos=(0, 0), size=(Window.size[0], Window.size[1]), source='img/background_1.jpg') # BACKGROUND
            self.player = Rectangle(pos=(100, 100), size=(50, 65), source=('img/mage_turnright.png'))

        Clock.schedule_interval(self.move, 0)

    def keyDown(self, kboard, keycode, text, mod):
        self.keyPressed.add(keycode[1])

    def keyUp(self, kboard, keycode):
        key = keycode[1]
        if key in self.keyPressed:
            self.keyPressed.remove(key)

    def keyboardClosed(self):
        self.kboard.unbind(on_key_down=self.keyDown)
        self.kboard.unbind(on_key_up=self.keyUp)
        self.kboard = None

    def changeSide(self):
        if 'right' in self.keyPressed:
            self.player.source = ('img/mage_turnright.png')
        elif 'left' in self.keyPressed:
            self.player.source = ('img/mage_turnleft.png')

    def jump(self, speed):
        self.jumping = True
        dest = self.player_y + 100
        while self.player_y < dest:
            self.player_y += speed

    def move(self, time):

        speed = time * self.speed

        self.player_x = self.player.pos[0]
        self.player_y = self.player.pos[1]

        if self.player_y > 250:
            #self.j_speed /= 1.1
            self.j_speed = 600
        if self.player_y > 260:
            #self.j_speed /= 1.2
            self.j_speed = 500
        if self.player_y > 280:
            #self.j_speed /= 1.3
            self.j_speed = 300
        if self.player_y > 290:
            #self.j_speed /= 1.7
            self.j_speed = 50

        if self.g_up is True:
            self.player_y += time * self.j_speed
        elif self.g_down is True:
            self.player_y -= time * self.j_speed

        print(self.player_y, self.j_speed)

        if self.player_y >= self.jump_limit:
            self.g_up = False
            self.g_down = True
        elif self.player_y <= self.floor:
            self.g_up = False
            self.g_down = False
        #if 'up' in self.keyPressed and self.player_y == 100 and self.g_down is False:
        if 'up' in self.keyPressed and self.g_up is False and self.g_down is False:
            self.g_up = True
        if 'right' in self.keyPressed:
            self.player_x += speed
        if 'left' in self.keyPressed:
            self.player_x -= speed

        self.changeSide()

        self.player.pos = (self.player_x, self.player_y)

class MyApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    MyApp().run()

input()
