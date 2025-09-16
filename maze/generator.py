import random
from typing import List, Tuple

Coord = Tuple[int, int]

# -----------------------------
# Helpers communs
# -----------------------------
def _init_ascii_grid(n: int) -> List[List[str]]:
    """Crée une grille ASCII pleine de murs avec cellules '.' aux coordonnées impaires."""
    H = 2 * n + 1
    W = 2 * n + 1
    grid = [['#'] * W for _ in range(H)]
    for i in range(n):
        for j in range(n):
            grid[2 * i + 1][2 * j + 1] = '.'
    return grid

def _carve_between(grid_ascii: List[List[str]], a: Coord, b: Coord) -> None:
    """Ouvre le mur entre deux cellules logiques (i,j)."""
    (i, j), (i2, j2) = a, b
    ax, ay = 2 * i + 1, 2 * j + 1
    bx, by = 2 * i2 + 1, 2 * j2 + 1
    wx, wy = (ax + bx) // 2, (ay + by) // 2
    grid_ascii[wx][wy] = '.'

def _open_entrance_exit(grid_ascii: List[List[str]], n: int) -> None:
    """Ouvre l’entrée (haut-gauche) et la sortie (bas-droite)."""
    grid_ascii[1][0] = '.'
    grid_ascii[2 * n - 1][2 * n] = '.'

# -----------------------------
# V1 : Recursive Backtracker
# -----------------------------
def generate_maze_recursive_backtracker(n: int, seed: int | None = None) -> List[str]:
    """
    Générateur V1 — Recursive Backtracker (DFS).
    Retourne le labyrinthe ASCII (liste de lignes).
    """
    if n < 2:
        raise ValueError("n doit être ≥ 2")

    rng = random.Random(seed)
    ascii_grid = _init_ascii_grid(n)

    def neighbors(cell: Coord) -> List[Coord]:
        i, j = cell
        cand = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
        return [(x, y) for (x, y) in cand if 0 <= x < n and 0 <= y < n]

    visited = set()
    stack: List[Coord] = [(0, 0)]
    visited.add((0, 0))

    while stack:
        cell = stack[-1]
        neigh = [v for v in neighbors(cell) if v not in visited]
        rng.shuffle(neigh)
        if not neigh:
            stack.pop()
            continue
        nxt = neigh[0]
        _carve_between(ascii_grid, cell, nxt)
        visited.add(nxt)
        stack.append(nxt)

    _open_entrance_exit(ascii_grid, n)
    return [''.join(row) for row in ascii_grid]

# -----------------------------
# V2 : Kruskal
# -----------------------------
class DSU:
    """Union-Find (Disjoint Set Union) pour l’algorithme de Kruskal."""
    def __init__(self, n: int):
        self.parent = list(range(n * n))
        self.rank = [0] * (n * n)
        self.n = n

    def _id(self, cell: Coord) -> int:
        i, j = cell
        return i * self.n + j

    def find(self, cell: Coord) -> int:
        x = self._id(cell)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: Coord, b: Coord) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True

def generate_maze_kruskal(n: int, seed: int | None = None) -> List[str]:
    """
    Générateur V2 — Algorithme de Kruskal.
    Retourne le labyrinthe ASCII (liste de lignes).
    """
    if n < 2:
        raise ValueError("n doit être ≥ 2")

    rng = random.Random(seed)
    ascii_grid = _init_ascii_grid(n)

    # 1) Lister toutes les arêtes entre cellules adjacentes
    edges: List[Tuple[Coord, Coord]] = []
    for i in range(n):
        for j in range(n):
            if i + 1 < n:   # vertical
                edges.append(((i, j), (i + 1, j)))
            if j + 1 < n:   # horizontal
                edges.append(((i, j), (i, j + 1)))

    # 2) Mélanger les arêtes
    rng.shuffle(edges)

    # 3) DSU : on ouvre si cellules dans ensembles différents
    dsu = DSU(n)
    opened = 0
    for a, b in edges:
        if dsu.union(a, b):
            _carve_between(ascii_grid, a, b)
            opened += 1
            if opened == n * n - 1:
                break

    _open_entrance_exit(ascii_grid, n)
    return [''.join(row) for row in ascii_grid]
