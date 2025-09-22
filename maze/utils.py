from typing import List, Tuple

Coord = Tuple[int, int]

def ask_int(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    while True:
        try:
            v = int(input(prompt).strip())
            if min_val is not None and v < min_val:
                print(f"Veuillez entrer un entier ≥ {min_val}.")
                continue
            if max_val is not None and v > max_val:
                print(f"Veuillez entrer un entier ≤ {max_val}.")
                continue
            return v
        except ValueError:
            print("Entrez un entier valide.")

def ask_filename(prompt: str, default: str = "maze.txt") -> str:
    name = input(prompt).strip()
    if not name:
        name = default
    if not name.lower().endswith(".txt"):
        name += ".txt"
    return name

def read_ascii(filepath: str) -> List[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    # on enlève les lignes vides terminales éventuelles
    while lines and lines[-1] == "":
        lines.pop()
    if not lines:
        raise ValueError("Fichier vide.")
    # vérifier largeur constante
    w = len(lines[0])
    if any(len(row) != w for row in lines):
        raise ValueError("ASCII invalide : lignes de longueurs différentes.")
    return lines

def write_ascii(lines: List[str], filepath="ascii") -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

def to_grid(lines: List[str]) -> List[List[str]]:
    return [list(row) for row in lines]

def to_lines(grid: List[List[str]]) -> List[str]:
    return ["".join(row) for row in grid]

def find_border_openings(grid: List[List[str]]) -> List[Coord]:
    """Toutes les positions '.' sur les bords (haut/bas/gauche/droite)."""
    H, W = len(grid), len(grid[0])
    openings: List[Coord] = []
    for c in range(W):
        if grid[0][c] == '.':
            openings.append((0, c))
        if grid[H - 1][c] == '.':
            openings.append((H - 1, c))
    for r in range(1, H - 1):
        if grid[r][0] == '.':
            openings.append((r, 0))
        if grid[r][W - 1] == '.':
            openings.append((r, W - 1))
    # dédup coins
    openings = sorted(set(openings))
    return openings

def pick_entrance_exit(openings: List[Coord]) -> Tuple[Coord, Coord]:
    """
    Convention du sujet : entrée en haut-gauche, sortie en bas-droite.
    On prend l'ouverture avec le (r+c) minimal pour l'entrée,
    et le (r+c) maximal pour la sortie.
    """
    if len(openings) < 2:
        raise ValueError("Labyrinthe invalide : moins de deux ouvertures sur les bords.")
    openings_sorted = sorted(openings, key=lambda rc: (rc[0] + rc[1], rc[0], rc[1]))
    return openings_sorted[0], openings_sorted[-1]
