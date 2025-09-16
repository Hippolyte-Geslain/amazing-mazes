from typing import List, Tuple
from PIL import Image

# Couleurs : ajuste si tu veux
# mur '#': noir, couloir '.': blanc, chemin 'o': vert, exploré '*': jaune
COLOR_MAP = {
    '#': (0, 0, 0),
    '.': (255, 255, 255),
    'o': (0, 180, 0),
    '*': (220, 200, 0),
}

def ascii_to_image(lines: List[str], out_path: str, cell: int = 8) -> None:
    if cell < 1:
        cell = 1
    H = len(lines)
    W = len(lines[0]) if H else 0
    img = Image.new("RGB", (W * cell, H * cell), (255, 255, 255))
    px = img.load()

    for r in range(H):
        row = lines[r]
        for c in range(W):
            ch = row[c]
            color = COLOR_MAP.get(ch, (255, 255, 255))
            # remplir le bloc cell x cell
            x0, y0 = c * cell, r * cell
            for dy in range(cell):
                for dx in range(cell):
                    px[x0 + dx, y0 + dy] = color

    if not out_path.lower().endswith(".png"):
        out_path += ".png"
    img.save(out_path)
