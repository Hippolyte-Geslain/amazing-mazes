import random

directions = [
    (0, 2),   
    (0, -2),  
    (2, 0),   
    (-2, 0)   
]

def ask_user_size():
    size = int(input("what size is the maze ?"))
    if size % 2 == 0:
        size+= 1
    return size

def ask_user_name():
    name = input("what is the name of the maze ?")
    return name + ".txt"

class Grid():
    def __init__(self):
        self.size = ask_user_size()
        self.name = ask_user_name()
        self.wall = "#"
        self.path = "."
        self.grid = []
        self.stack = []
        self.visited = set()

    def create_grid(self):
        self.grid = [[self.wall for _ in range(self.size)] for _ in range(self.size)]
        self.create_path_backtrack((1, 1))
        self.grid[0][1] = self.path
        self.grid[self.size-1][self.size-2] = self.path
        with open(self.name, 'w') as f:
            for line in self.grid:
                f.write("".join(line) + "\n")

    def create_path_backtrack(self, cell):
        x, y = cell
        self.grid[x][y] = self.path
        self.stack.append(cell)
        self.visited.add(cell)

        while self.stack:
            x, y = self.stack[-1]
            neighbors = self.find_non_visited(x, y)
            if neighbors:
                nx, ny = random.choice(neighbors)
                wall_x, wall_y = (x + nx) // 2, (y + ny) // 2
                self.grid[wall_x][wall_y] = self.path
                self.grid[nx][ny] = self.path
                self.stack.append((nx, ny))
                self.visited.add((nx, ny))
            else:
                self.stack.pop()

    def find_non_visited(self, x, y):
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < self.size - 1 and 1 <= ny < self.size - 1:
                if (nx, ny) not in self.visited:
                    neighbors.append((nx, ny))
        return neighbors

if __name__ == "__main__":
    maze = Grid()
    maze.create_grid()