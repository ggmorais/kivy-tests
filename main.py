from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen



def switchScreen(btn):
    if '->' in btn.id:
        x = btn.id.split('->')
        name = x[0]
        dir = x[1]
    else:
        name = btn.id
        dir = 'right'
    
    confirm = Confirm()
    popup = Popup(
        title='Tem certeza que desejá voltar ao menu?',
        content=confirm,
        size_hint=(None, None),
        size=(win_w / 2, win_h / 3),
        auto_dismiss=False,
        title_size=20
    )
    go_on = lambda btn: (manager.switch_to(screens[name], direction=dir), popup.dismiss())
    close = lambda btn: popup.dismiss() 
    
    confirm.no.bind(on_press=close)
    confirm.yes.bind(on_press=go_on)
    
    if name == 'Home' or name == 'Exit':
        popup.open()
    else:
        manager.switch_to(screens[name], direction=dir)

class Controller:
    def __init__(self, widget, player, movables = None):
        self.widget = widget
        self.player = player
        self.movables = movables
        self.pressed = set()
        
        self.buttons = {
            Button(text='Right', id='right', pos=(win_w - default_w - 20, 50), size=(default_w, default_h)),
            Button(text='Left', id='left', pos=(win_w - default_w * 2 - 20, 50), size=(default_w, default_h)),
            Button(text='Jump', id='jump', pos=(20, 50), size=(default_w, default_h)),
            Button(text='Attack', id='attack', pos=(default_w + 20, 50), size=(default_w, default_h)),
            Button(text='Pause', id='Pause->down', pos=(20, win_h - 70), size=(default_w, default_h), on_press=switchScreen),
        }
        
        for btn in self.buttons:
            btn.bind(state=self.on_press)
            widget.add_widget(btn)
        
    def on_press(self, btn, state):
        if state is 'down':
            self.pressed.add(btn.id)
        else:
            self.pressed.remove(btn.id)
            
    def start(self, ms):
        posx, posy = self.player.pos
        speed = ms * 500
        
        if 'right' in self.pressed:
            posx += speed
        if 'left' in self.pressed:
            posx -= speed
        
        self.player.pos = (posx, posy)

class Confirm(GridLayout):
    def __init__(self, **kwargs):
        self.name = self.__class__.__name__
        super(eval(self.name), self).__init__(**kwargs)
        
        self.cols = 2
        self.row_force_default = True
        self.row_default_height = 95
        
        self.yes = Button(text='Sim', size_hint=(100, None), height=default_h)
        self.no = Button(text='Não', size_hint=(100, None), height=default_h)
        
        self.add_widget(self.yes)
        self.add_widget(self.no)
    
class Home(Widget):
    def __init__(self, **kwargs):
        self.name = self.__class__.__name__
        super(eval(self.name), self).__init__(**kwargs)

        self.next = Button(text='Iniciar', id='Game->left', size=(default_w*2, default_h*2), pos=(win_w / 2 - default_w, win_h / 2 - default_h), on_release=switchScreen)
        self.add_widget(self.next)
        

class Game(Widget):
    def __init__(self, **kwargs):
        self.name = self.__class__.__name__
        super(eval(self.name), self).__init__(**kwargs)
        
        with self.canvas:
            self.player = Rectangle(size=(50, 50), pos=(100, 150))
            
        self.controller = Controller(self, self.player)
        
        Clock.schedule_interval(self.movement, 0)
        
    def movement(self, ms):
        self.controller.start(ms)
    
class Pause(Widget):
    def __init__(self, **kwargs):
        self.name = self.__class__.__name__
        self.index = list(screens.keys()).index(manager.current)
        super(eval(self.name), self).__init__(**kwargs)
        
        self.buttons = {
            Button(text='Continuar', id='Game->up', size=(default_w, default_h), pos=(20, win_h - default_h - 20), on_press=switchScreen),
            Button(text='Início', id='Home->right', size=(default_w, default_h), pos=(40 + default_w, win_h - default_h - 20), on_press=switchScreen),
            Button(text='Opções', id='Options->left', size=(default_w, default_h), pos=(win_w - default_w - 20, win_h - default_h - 20), on_press=switchScreen)
        }
        for btn in self.buttons:
            self.add_widget(btn)

class Options(Widget):
    def __init__(self, **kwargs):
        self.name = self.__class__.__name__
        super(eval(self.name), self).__init__(**kwargs)
        
        self.buttons = {
            Button(text='Voltar', id='Pause->right', size=(default_w, default_h), pos=(20, win_h - default_h - 20), on_press=switchScreen)
        }
        for btn in self.buttons:
            self.add_widget(btn)

manager = ScreenManager()

ACTUAL = None # actual screen

win_w = Window.size[0]
win_h = Window.size[1]

default_w = win_w * .15
default_h = win_h * .08

screens = {
    'Home': Screen(name='Home'),
    'Game': Screen(name='Game'),
    'Pause': Screen(name='Pause'),
    'Options': Screen(name='Options')
}

for x in screens:
    screens[x].add_widget(eval(x+'()'))
    manager.add_widget(screens[x])

    
class ScreenApp(App):
    def build(self):
        return manager
        

ScreenApp().run()
