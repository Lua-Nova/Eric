from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from game import Game
from kivy.clock import Clock

class Fruit(Widget):
    def __init__(self, x, y, size):
        super().__init__()
        self.size = (size, size)
        self.pos = (x, y)

class SnakeBodyPart(Widget):
    def __init__(self, x, y, size):
        super().__init__()
        self.size = (size, size)
        self.pos = (100*x, 100*y)

class WindowManager(ScreenManager):
    pass

class GameLayout(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tick_speed = 2
        self.snake_parts = []
        self.fruits = []
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.timer = Clock.schedule_interval(self.tick, self.tick_speed)
        self.direction='R'
        self.new_game()
    
    def new_game(self):
        self.game = Game(10, 10)

        for rect in self.snake_parts:
            self.remove_widget(rect)
            self.snake_parts.remove(rect)

        for fruit in self.fruits:
            self.remove_widget(fruit)
            self.snake_parts.remove(fruit)

        for body_part in self.game.get_snake():
            self.snake_parts.append(SnakeBodyPart(body_part[0], body_part[1], 50))
            self.add_widget(self.snake_parts[-1])

        for fruit in self.game.get_fruit():
            self.fruits.append(Fruit(fruit[0], fruit[1], 10))
            self.add_widget(self.fruits[-1])
        self.timer.cancel()
        self.timer = Clock.schedule_interval(self.tick, self.tick_speed)


    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
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
    
    def tick(self, dt):
        t = self.game.move(self.direction)
        if not t:
            self.remove_widget(self.snake_parts[0])
            self.snake_parts.pop()
        self.snake_parts.append(SnakeBodyPart(self.game.get_snake()[-1][0] + 2, self.game.get_snake()[-1][1], 50))
        self.add_widget(self.snake_parts[-1])
        
        
            

class AwesomeApp(App):
    def build(self):
        return Builder.load_file('gui.kv')

if __name__ == '__main__':
    AwesomeApp().run()