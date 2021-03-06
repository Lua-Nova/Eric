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
import time
from kivy.uix.label import Label

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
        self.square_list = []
        self.grid_list = []
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.direction = 'R'
        self.apple = None
        self.label = None
        self.bind(size=self.update)
        self.paused = True
        self.timer = Clock.schedule_interval(self.tick, self.tick_speed)
        self.timer.cancel()
        super().__init__(**kwargs)

    def update(self, *args):
        print(self.size)
        rows, cols = self.rows_cols
        width, height = self.size # width and height of widget
        square_size = (0.95 * width / cols, 0.95 * height / rows)
        if self.apple != None:
            self.apple.size = square_size
            self.apple.pos = (self.apple_pos[0] * width / cols, self.apple_pos[1] * height / rows)
        for i, grid_square in enumerate(self.grid_list):
            grid_square.size = square_size
            x = i % rows
            y = i // rows
            grid_square.size = square_size
            grid_square.pos = (x * width / cols, y * height / rows)
            

        for i in range(len(self.square_list)):
            snake = self.square_list[i]
            snake.size = square_size
            snake.pos = (self.snake_pos[i][0] * width / cols, self.snake_pos[i][1] * height / rows)

        

        
    def play_pause(self):
        if self.paused == True:
            self.timer.schedule_interval(self.tick, self.tick_speed)
        else:
            self.timer.cancel()
            



    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def move(self):
        if self.game.collision_check(self.direction):
            self.timer.cancel()
            self.label = Label(text="Game Over", 
                            color=(1,0,0,1),
                            font_size=self.size[0]/10,
                            pos=(self.size[0]/2, self.size[1]/2))
            self.add_widget(self.label)
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
        # if self.game.collision_check(self.direction) != True

    
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
        rows, cols = self.rows_cols
        self.game = Game(rows, cols)
        self.direction = "R"
        self.snake_pos = self.game.snake_pos
        self.apple_pos = self.game.create_fruit()
        if self.label != None:
            self.remove_widget(self.label)
        
           

        for i in range(rows):
            for j in range(cols):
                self.add_grid(j, i)

        
        self.add_apple(*self.apple_pos)
        for tuple in self.snake_pos:
            self.add_square(*tuple, random.random(), random.random(), random.random())
        


    def add_square(self, x, y, r, g, b):
        width, height = self.size
        rows, cols = self.rows_cols
        self.square = Square(x * width / cols, y * height / rows, 0.95 * width / cols, 0.95 * height / rows, r, g, b)
        self.square_list.append(self.square)
        self.add_widget(self.square)
        
    def add_apple(self,x,y):
        width, height = self.size
        rows, cols = self.rows_cols
        self.apple = Square(x * width / cols, y * height / rows, 0.95 * width / cols, 0.95 * height / rows, 1, 0, 0)
        self.add_widget(self.apple)

    def add_grid(self, x, y):
        width, height = self.size
        rows, cols = self.rows_cols
        square = Square(x * width / cols, y * height / rows, 0.95 * width / cols, 0.95 * height / rows, 1, 1, 1)
        self.grid_list.append(square)
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

