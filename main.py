import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Ellipse
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

import winsound
import random

class MainWidget(Widget):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        #Window.size = (1920, 1080)
        #Window.fullscreen = True

        self.kboard = Window.request_keyboard(self.kboardClosed, self)
        self.mouse = Window.bind(on_motion=self.onMouse)
        self.kboard.bind(on_key_down=self.keyDown)
        self.kboard.bind(on_key_up=self.keyUp)
        self.sound = SoundLoader.load('teste.mp3')

        with self.canvas: # PLAYER
            Color(0, 0, 1.)
            self.player = Ellipse(pos=(100, 100), size=(10, 10), color=(0, 1, 1)) # ELLIPSE PLAYER
            Color(1, 1, 1)
            self.enemy = Rectangle(pos=(300, 300 ), size=(5, 5))

        self.keyPressed = set()

        Clock.schedule_interval(self.move, 0)

    def onMouse(self, evtype, event, pos):
        self.mouse_x = pos.pos[0]
        self.mouse_y = pos.pos[1]
        if self.mouse_x > 0 and self.mouse_y > 0:
            self.player.pos = (self.mouse_x, self.mouse_y)

    def keyDown(self, kboard, keycode, text, mod):
        self.keyPressed.add(keycode[1])

    def keyUp(self, kboard, keycode):
        key = keycode[1]
        if key in self.keyPressed:
            self.keyPressed.remove(key)

    def kboardClosed(self):
        self.kboard.unbind(on_key_down=self.keyDown)
        self.kboard.unbind(on_key_up=self.keyUp)
        self.kboard = None

    def move(self, time):
        self.player_x = self.player.pos[0]
        self.player_y = self.player.pos[1]
        walk_x = self.player_x
        walk_y = self.player_y

        speed = 200 * time

        if self.enemyColision(self.player, self.enemy): # RANDOM POSITION OF THE ENEMY
            self.enemy.pos = (random.randrange(0, Window.size[0]), random.randrange(0, Window.size[1]))
            self.player.size = (self.player.size[0] + 5, self.player.size[1] + 5)
            #self.sound.play()

        if 'right' in self.keyPressed:
            self.player_x += speed
        elif 'left' in self.keyPressed:
            self.player_x -= speed
        if 'up' in self.keyPressed:
            self.player_y += speed
        elif 'down' in self.keyPressed:
            self.player_y -= speed

        self.player.pos = (self.player_x, self.player_y)

    def enemyColision(self, player, enemy):
        player_x = int(player.pos[0])
        player_y = int(player.pos[1])
        player_w = int(player.size[0])
        player_h = int(player.size[1])
        enemy_x = int(enemy.pos[0])
        enemy_y = int(enemy.pos[1])
        enemy_w = int(enemy.size[0])
        enemy_h = int(enemy.size[1])

        if player_y in range(enemy_y - player_h, enemy_y + enemy_h) and player_x in range(enemy_x - player_w, enemy_x + enemy_w):
            return True
        else:
            return False

class MyApp(App):
    def build(self):
        return MainWidget()


if __name__ == '__main__':
    MyApp().run()
