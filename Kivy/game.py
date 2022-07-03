import random

class Game():

    def __init__(self, rows, cols):
        # rows, cols = (10, 10)
        # 10x10 array of Booleans
        self.rows = rows
        self.cols = cols
        self.new_game()

    
    def create_fruit(self):

        # generate 2 random ints
        x = random.randint(0,self.cols -1)
        y = random.randint(0,self.rows -1)

        # while (x, y) points to a body part, reroll
        while (x, y) in self.snake_pos:
            x = random.randint(0,self.cols -1)
            y = random.randint(0,self.rows -1)
        
        self.grid[y][x] = True

    # move the snake
    # remove fruits that the snake head eats
    # returns true if snake eats apple. returns false otherwise
    def move(self, direction):
        new_x, new_y = self.snake_pos[-1]
        
        if direction == "R": # x + 1
            new_x = new_x + 1

        elif direction == "L": # x - 1
            new_x = new_x -1

        elif direction == "U": # y - 1
            new_y = new_y +1
            
        elif direction == "D": # y + 1
            new_y = new_y -1
        else:
            print('Error Key not Found')

        print(self.snake_pos)
        self.snake_pos.append((new_x,new_y))
        if self.grid[new_y][new_x] == False:
            self.snake_pos.pop(0)
            return False
        else:
            return True
        
        

    def new_game(self):
        self.grid = [[False]*self.cols]*self.rows
        self.snake_pos = [(self.rows//2 - 1, self.cols//2), (self.rows//2, self.cols//2), (self.rows//2 +1, self.cols//2)] # stack of (y, x)
        # self.create_fruit()


    def collision_check(self, direction):
        x,y = self.snake_pos[-1]
        # hit a wall
        if x >= self.rows and x < 0:
            return True
        elif y >= self.cols and y < 0:
            return True

        # hit yourself

        elif (x, y) in self.snake_pos:
            return True
        else:
            return False
        

            
        


