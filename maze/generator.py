import random

directions = {
    (0,1),
    (0,-1),
    (-1,0),
    (1,0)
}

def ask_user_size():
    size = int(input("what size is the maze ?"))
    return size

def ask_user_name():
    name = input("what is the name of the maze ?")
    return name+".txt"

class Grid():
    def __init__(self, size, name):
        self.size = ask_user_size()
        self.name = ask_user_name()
        self.wall = "#"
        self.path = "."
        self.grid = []
        self.stack = []
        self.neighbors = []
        self.visited = []

    def create_grid(self):
        self.grid = [[self.wall for _ in range(self.size)]for _ in range(self.size)]
        with open(self.name,'w') as f:
            for line in self.grid:
                f.write("".join(line)+"\n")


    def create_path_backtrack(self,cell):
        start = (1,1)
        self.stack.append(cell)


        while self.stack:
            x,y = self.stack[-1]
            self.neighbors = self.find_non_visited(x,y)
            if self.neighbors:
                nx,ny = random.choice(self.neighbors)
                self.grid[nx][ny] = self.path

    def find_non_visited(self,x,y,):
        for (dx,dy) in directions:
            nx, ny = x + dx, dy + y
            if 0<=nx<self.size and 0<=ny<self.size:
                if nx and ny not in self.stack:
                    self.neighbors.append((nx,ny))