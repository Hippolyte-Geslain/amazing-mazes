wall = "#"
path = "."


def ask_user_size():
    size = int(input("what size is the maze ?"))
    return size

def ask_user_name():
    name = input("what is the name of the maze ?")
    return name+".txt"


def create_maze():
    size = ask_user_size()
    name = ask_user_name()
    grid = [[wall for _ in range(size)]for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if i%2==1 and j%2==1:
                grid[i][j] = path
    start = (1,1)
    create
    with open(name, 'w') as f:
        for line in grid:
            f.write("".join(line)+"\n")


def create_path_backtrack(grid,cell):
    visited = []
    visited.append(cell)

    while visited:
        x,y = visited[-1]
        neighbors = find_non_visited(x,y,visited)

def find_non_visited(x,y,visited):
    directions = {
        "up":(0,1),
        "down":(0,-1),
        "left":(-1,0),
        "right":(1,0)
    }
    neighbors = []
    for direction,(dx,dy) in directions.items():
        



create_maze()