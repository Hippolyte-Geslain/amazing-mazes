from typing import List, Tuple, Optional
import heapq
from .utils import (
    read_ascii, write_ascii, to_grid, to_lines,
    find_border_openings, pick_entrance_exit
)

Coord = Tuple[int, int]

# --------------------------
# Helpers communs
# --------------------------
def _neighbors(rc: Coord, H: int, W: int) -> List[Coord]:
    r, c = rc
    cand = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
    return [(x, y) for (x, y) in cand if 0 <= x < H and 0 <= y < W]

def _is_walkable(ch: str) -> bool:
    # On marche sur les couloirs '.'
    return ch == '.'

def _reconstruct_path(parent: dict[Coord, Optional[Coord]], goal: Coord) -> List[Coord]:
    path: List[Coord] = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path

def _mark(grid: List[List[str]], start: Coord, goal: Coord,
          visited: List[Coord], path: Optional[List[Coord]]) -> List[str]:
    visited_set = set(visited)
    path_set = set(path) if path else set()
    for (r, c) in visited_set:
        if (r, c) not in path_set and (r, c) != start and (r, c) != goal and grid[r][c] == '.':
            grid[r][c] = '*'
    if path:
        for (r, c) in path_set:
            if grid[r][c] != '#':
                grid[r][c] = 'o'
    return to_lines(grid)

# --------------------------
# DFS / Backtracking
# --------------------------
def dfs_solve_ascii(lines_in: List[str]) -> List[str]:
    grid = to_grid(lines_in)
    H, W = len(grid), len(grid[0])

    openings = find_border_openings(grid)
    start, goal = pick_entrance_exit(openings)

    stack: List[Coord] = [start]
    parent: dict[Coord, Optional[Coord]] = {start: None}
    visited: set[Coord] = set()
    visited_order: List[Coord] = []

    while stack:
        cur = stack.pop()
        if cur in visited:
            continue
        visited.add(cur)
        visited_order.append(cur)

        if cur == goal:
            break

        for nb in _neighbors(cur, H, W):
            if nb in visited:
                continue
            r, c = nb
            if (nb == goal) or (nb == start) or _is_walkable(grid[r][c]):
                if nb not in parent:
                    parent[nb] = cur
                stack.append(nb)

    path = _reconstruct_path(parent, goal) if goal in parent else None
    return _mark(grid, start, goal, visited_order, path)

def solve_file(input_path: str, output_path: str) -> None:
    lines = read_ascii(input_path)
    solved = dfs_solve_ascii(lines)
    write_ascii(solved, output_path)

# --------------------------
# A* (Manhattan)
# --------------------------
def _manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_solve_ascii(lines_in: List[str]) -> List[str]:
    grid = to_grid(lines_in)
    H, W = len(grid), len(grid[0])

    openings = find_border_openings(grid)
    start, goal = pick_entrance_exit(openings)

    open_heap: List[Tuple[int, Coord]] = []
    heapq.heappush(open_heap, (0, start))

    g: dict[Coord, int] = {start: 0}
    parent: dict[Coord, Optional[Coord]] = {start: None}
    in_open: set[Coord] = {start}
    closed: set[Coord] = set()
    visited_order: List[Coord] = []

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        closed.add(current)
        visited_order.append(current)

        if current == goal:
            break

        for nb in _neighbors(current, H, W):
            r, c = nb
            if not ((nb == start) or (nb == goal) or _is_walkable(grid[r][c])):
                continue
            tentative_g = g[current] + 1
            if nb in closed and tentative_g >= g.get(nb, 10**12):
                continue
            if tentative_g < g.get(nb, 10**12):
                parent[nb] = current
                g[nb] = tentative_g
                f = tentative_g + _manhattan(nb, goal)
                heapq.heappush(open_heap, (f, nb))
                in_open.add(nb)

    path = _reconstruct_path(parent, goal) if goal in parent else None
    return _mark(grid, start, goal, visited_order, path)

def solve_file_astar(input_path: str, output_path: str) -> None:
    lines = read_ascii(input_path)
    solved = astar_solve_ascii(lines)
    write_ascii(solved, output_path)
