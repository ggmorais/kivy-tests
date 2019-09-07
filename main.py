import os
os.environ['KIVY_IMAGE'] = 'sdl2'

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_sdl2 import SoundSDL2
from kivy.uix.screenmanager import ScreenManager, Screen


class Game(Widget):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # SCREEN
        self.sm = ScreenManager()
        for i in range(4):
            self.screen = Screen(name='Title{0}'.format(i))
            self.sm.add_widget(self.screen)

        self.player_side = 'r'

        # KEYBOARD
        self.kboard = Window.request_keyboard(self.keyboardClosed, self)
        self.kboard.bind(on_key_down=self.keyDown)
        self.kboard.bind(on_key_up=self.keyUp)
        self.keyPressed = set()

        # PLAYER CONTROL VARIABLES
        self.g_up = False
        self.g_down = False
        self.jump_limit = 286
        self.speed = 300
        self.floor = 95
        self.d_jspeed= 650 # default jump speed
        self.bg_speed = 5
        self.bg_size = 500

        # OBJECTS AND IMAGES
        with self.canvas:
            self.bg = Image(source='assets/img/background_1.png', size=(Window.size[0] + self.bg_size, Window.size[1]), allow_stretch=True, keep_ratio=False, pos=(0, 0))
            self.player = Image(source='assets/img/mage_turnright.png', size=(50, 65))

        # SOUNDS
        self.sounds = {
            'jump': SoundSDL2(source='assets/audio/player/jump.ogg'),
            'land': SoundSDL2(source='assets/audio/player/jump.ogg')
        }

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
            self.player.source = ('assets/img/mage_turnright.png')
        elif 'left' in self.keyPressed:
            self.player.source = ('assets/img/mage_turnleft.png')



    def move(self, time):

        speed = time * self.speed

        self.player_x = self.player.pos[0]
        self.player_y = self.player.pos[1]

        self.win_stages = [Window.size[0] / 3, Window.size[0] - Window.size[0] / 3]

        #print(self.player.pos[0], self.player.pos[1])

        if self.g_up is True and self.player_y > self.floor:
            self.jspeed -= self.d_jspeed / 20
        elif self.g_down is True and self.player_y > self.floor:
            self.jspeed += self.d_jspeed / 20
        else:
            self.jspeed = self.d_jspeed

        # PLAYER LANDING
        if self.player_y < self.floor:
            self.player_y = self.floor

        if self.g_up is True:
            self.player_y += time * self.jspeed
        elif self.g_down is True:
            self.player_y -= time * self.jspeed

        if self.player_y >= self.jump_limit:
            self.g_up = False
            self.g_down = True
        elif self.player_y <= self.floor:
            self.g_up = False
            self.g_down = False

        self.changeSide()

        if 'up' in self.keyPressed and self.g_up is False and self.g_down is False:
            self.g_up = True
            self.sounds['jump'].play()
        if 'right' in self.keyPressed:
            #if self.player_x > self.win_stages[0] and self.player_x < self.win_stages[1] and self.bg.pos[0] > - self.bg_size:
            if self.player_x > Window.size[0] / 2 - 3 and self.player_x < Window.size[0] / 2 + 3 and self.bg.pos[0] > - self.bg_size:
                self.bg.pos = (self.bg.pos[0] - self.bg_speed, self.bg.pos[1])
                self.player_x = self.player_x
            else:
                self.player_x += speed
            if self.player_x < 0 or self.player_x > Window.size[0] - 60:
                #self.player_x = self.player_x - 5
                self.player_x = Window.size[0] - 60
        if 'left' in self.keyPressed:
            #if self.player_x > self.win_stages[0] and self.player_x < self.win_stages[1] and self.bg.pos[0] != 0:
            if self.player_x > Window.size[0] / 2 - 3 and self.player_x < Window.size[0] / 2 + 3 and self.bg.pos[0] != 0:
                self.bg.pos = (self.bg.pos[0] + self.bg_speed, self.bg.pos[1])
                self.player_x = self.player_x
            else:
                self.player_x -= speed
            if self.player_x < 0 or self.player_x > Window.size[0] - 60:
                #self.player_x = self.player_x + 5
                self.player_x = Window.size[0] - Window.size[0] + 0



        self.player.pos = (self.player_x, self.player_y)

class MyApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    MyApp().run()

input()
