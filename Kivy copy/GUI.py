from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from game import Game
import random
from kivy.core.window import Window
from kivy.clock import Clock

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
        self.tick_speed = 0.2
        self.rows_cols = (10, 10)
        self.bind(size=self.update)
        self.square_list = []
        self.grid = []
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.direction = 'R'
        super().__init__(**kwargs)
        # self.new_game()

    def update(self, *args):
        for i in range(len(self.square_list)):
            self.square_list[i].size = (0.95 * self.size[0] / self.cols, 0.95 * self.size[1]/self.rows)
            self.square_list[i].pos = (self.game.snake_pos[i][0] * self.size[0] / self.cols,
                                         self.game.snake_pos[i][1] * self.size[1]/self.rows)
            

    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def move(self):
        if self.game.collision_check(self.direction):
            print("Game Over")

        else:
            ate_apple = self.game.move(self.direction)
            tuple = self.game.snake_pos[-1]
            self.add_square(*tuple, random.random(), random.random(), random.random())
        
            if ate_apple:
                self.remove_widget(self.apple)
                x, y = self.apple_pos
                self.game.grid[y][x] = False
                self.apple_pos = self.game.create_fruit()
                self.add_apple(*self.apple_pos)
    
                
             
            else:
                self.remove_widget(self.square_list[0])
                self.square_list.pop(0)
          
            




    def tick(self, dt):
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
        return True
        
    def new_game(self):
        self.rows, self.cols = self.rows_cols
        self.rows = int(self.rows)
        self.cols = int(self.cols)
        self.game = Game(self.rows, self.cols)
        self.snake_pos = self.game.snake_pos
        self.apple_pos = self.game.create_fruit()
            

        for i in range(self.rows):
            for j in range(self.cols):
                self.add_grid(j, i)
        
        self.add_apple(*self.apple_pos)
        for tuple in self.snake_pos:
            self.add_square(*tuple, random.random(), random.random(), random.random())
        self.timer = Clock.schedule_interval(self.tick, self.tick_speed)

    def add_square(self, x, y, r, g, b):
        self.square = Square(self.width / self.cols * x, self.height / self.rows * y,
                                0.95 * self.width / self.cols , 0.95 * self.height / self.rows, r, g, b)
        self.square_list.append(self.square)
        self.add_widget(self.square)
        
    def add_apple(self,x,y):
        self.apple = Square(120 * x, 80 * y, 105, 70, 1, 0, 0)
        self.add_widget(self.apple)

    def add_grid(self, x, y):
        square = Square(120 * x, 80 * y, 105, 70, 1, 1, 1)
        self.grid.append(square)
        self.add_widget(square)

    def reset(self):
        for square in self.square_list:
            self.remove_widget(square)
        self.square_list = []
        self.remove_widget(self.apple)
        self.timer.cancel()
        del self.game






class SnakeApp(App):
    def build(self):
        kv = Builder.load_file('gui.kv')
        return kv

