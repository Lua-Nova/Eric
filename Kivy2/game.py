import random
class Snake():
    def __init__(self, grid, rows, cols):
        # stack of positions
        self.grid = grid
        self.rows = rows
        self.cols = cols 
        self.snake_pos = [(rows//2, cols//2),(rows//2 - 1, cols//2)] # stack of (y, x)
        

    # collision check method
    # returns true if collision happened
    def collision_check(self, x, y):
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
    

    # get stack
    def get_snake_pos(self):
        return self.snake_pos

    # move method returns false if collision, true if all good
    # snake_pos -> new snake_pos
    # if there's a fruit dont get rid of tip of tail tht way you grow
    # make sure wherever you move is allowed

    def move(self, direction):
        head = self.snake_pos[0]
        new_x = head[0]
        new_y = head[1]
        
        if direction == "R": # x + 1
            new_x = new_x + 1

        elif direction == "L": # x - 1
            new_x = new_x -1

        elif direction == "U": # y - 1
            new_y = new_y -1
            
        elif direction == "D": # y + 1
            new_y = new_y +1

        self.snake_pos.append((new_x,new_y))
        if self.grid[new_y][new_x] == False:
            self.snake_pos.pop()
            return True
        
        return False
        
       

class Game():

    def __init__(self, rows, cols):
        # rows, cols = (10, 10)
        # 10x10 array of Booleans
        self.rows = rows
        self.cols = cols
        self.grid = [[False]*cols]*rows
        self.snake = Snake(self.grid, rows, cols)
        

    
    def create_fruit(self):

        # generate 2 random ints
        x = random.randint(0,self.cols -1)
        y = random.randint(0,self.rows -1)
        self.snake_pos = self.snake.get_snake_pos()
        
        # while fruit exists where random ints point to, generate new random ints
        while self.grid[y][x] == True:
            x = random.randint(0,self.cols -1)
            y = random.randint(0,self.rows -1)

        # while (x, y) points to a body part, reroll
        while (x, y) in self.snake_pos:
            x = random.randint(0,self.cols -1)
            y = random.randint(0,self.rows -1)
        
        self.grid[y][x] = True

    def get_snake(self):
        return self.snake.get_snake_pos()

    def get_fruit(self):
        fruit_pos = []
        for i in range(self.cols):
            for j in range(self.rows):
                if self.grid[j][i]:
                    fruit_pos.append(i, j)
        return fruit_pos

    def move(self, direction):
        return self.snake.move(direction)