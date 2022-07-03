from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from game import Game
import random
from kivy.core.window import Window

class WindowManager(ScreenManager):
    pass

class Square(Widget):
    def __init__(self, x, y, width, height, r, g, b):
        self.size = (width, height)
        self.pos = (x, y)
        self.r = r
        self.g = g
        self.b = b
        super().__init__()


class Snake(Widget):

    def __init__(self, **kwargs):
        self.square_list = []
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.direction = 'R'
        super().__init__(**kwargs)
        self.new_game()
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def move(self):
        ate_apple = self.game.move(self.direction)
        tuple = self.game.snake_pos[-1]
        self.add_square(*tuple, random.random(), random.random(), random.random())
      
        if ate_apple:
            x = 7
         
        else:
            self.remove_widget(self.square_list[0])
            self.square_list.pop(0)
          
            




    def tick(self):
        self.move()
        # if self.game.collision_check(self.direction) != True:
            
            
        


    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w' or keycode[1] == 'up':
            self.direction = 'U'
        elif keycode[1] == 's' or keycode[1] == 'down':
            self.direction = 'D'
        elif keycode[1] == 'a' or keycode[1] == 'left':
            self.direction = 'L'
        elif keycode[1] == 'd' or keycode[1] == 'right':
            self.direction = 'R'
        self.tick()
        return True
        
    def new_game(self):
        rows = 10
        cols = 10
        self.game = Game(rows, cols)
        self.x = 0
        self.y = 0
        self.snake_pos = self.game.snake_pos
        
        for tuple in self.snake_pos:
            self.add_square(*tuple, random.random(), random.random(), random.random())
            


        for x in range(cols + 2):
            self.add_border(x, 0, .1, .1, .1)
            self.add_border(x, rows + 1, .1, .1, .1)

        for y in range(rows):
            self.add_border(0, y + 1, .1 ,.1 ,.1)
            self.add_border(cols + 1, y + 1, .1, .1, .1)

        


    def add_square(self, x, y, r, g, b):
        x = x + 1
        y = y + 1
        self.square = Square(120 * x, 80 * y, 105, 70, r, g, b)
        self.square_list.append(self.square)
        self.add_widget(self.square)
    
    def add_border(self, x, y, r, g, b):
        self.square = Square(120 * x, 80 * y, 105, 70, r, g, b)
        self.add_widget(self.square)

    def reset(self):
        for square in self.square_list:
            self.remove_widget(square)
        self.square_list = []



        



class SnakeApp(App):
    def build(self):
        kv = Builder.load_file('gui.kv')
        return kv

