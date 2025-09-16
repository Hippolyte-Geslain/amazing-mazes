# main.py
import os, csv, time, tracemalloc, re
from datetime import datetime

from maze.utils import ask_int, write_ascii
from maze.generator import generate_maze_recursive_backtracker, generate_maze_kruskal
from maze.solver import dfs_solve_ascii, astar_solve_ascii
from maze.image_export import ascii_to_image

DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "experiments.csv")

# ---------- Helpers ----------
def slugify(s: str) -> str:
    return re.sub(r'[^a-zA-Z0-9._-]+', '_', s).strip('._-') or "run"

def time_and_mem(fn, *args, **kwargs):
    os.makedirs(DATA_DIR, exist_ok=True)
    tracemalloc.start()
    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    dt = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, dt, int(peak / 1024)

# ---------- CSV ----------
def append_experiment_row(row: dict) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    fieldnames = [
        "timestamp","n","ascii_size",
        "generator","gen_time_s","gen_peak_kb","maze_txt","maze_png",
        "solver","solve_time_s","solve_peak_kb","solution_txt","solution_png"
    ]
    write_header = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            w.writeheader()
        w.writerow(row)

def make_row(n, gen_name, gen_dt, gen_kb, maze_txt, maze_png,
             solver_name, solve_dt, solve_kb, sol_txt, sol_png):
    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "n": str(n),
        "ascii_size": f"{2*n+1}x{2*n+1}",
        "generator": gen_name,
        "gen_time_s": f"{gen_dt:.6f}",
        "gen_peak_kb": str(gen_kb),
        "maze_txt": maze_txt,
        "maze_png": maze_png,
        "solver": solver_name,
        "solve_time_s": (f"{solve_dt:.6f}" if solve_dt is not None else ""),
        "solve_peak_kb": (str(solve_kb) if solve_kb is not None else ""),
        "solution_txt": (sol_txt or ""),
        "solution_png": (sol_png or ""),
    }

def load_all_rows():
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def print_table(rows):
    if not rows:
        print("Aucune session enregistrée pour l’instant.")
        return
    cols = [
        "timestamp","n","ascii_size","generator","solver",
        "gen_time_s","solve_time_s","maze_txt","solution_txt"
    ]
    widths = {c: max(len(c), max((len(r.get(c, "")) for r in rows), default=0)) for c in cols}
    header = " | ".join(c.ljust(widths[c]) for c in cols)
    print("\n=== Historique des sessions ===")
    print(header)
    print("-" * len(header))
    for r in rows:
        line = " | ".join(r.get(c, "").ljust(widths[c]) for c in cols)
        print(line)

# ---------- Session complète ----------
def action_full_session():
    print("=== Session complète ===")

    # Générateur
    print("Générateur : 1) Backtracker   2) Kruskal")
    g_choice = input("Choix (1/2) : ").strip()
    if g_choice not in ("1","2"):
        print("⛔ Choix invalide.")
        return
    gen_name = "Backtracker" if g_choice == "1" else "Kruskal"
    gen_tag = "backtracker" if gen_name == "Backtracker" else "kruskal"

    # Solveur
    print("Solveur : 0) Aucun   1) DFS   2) A*")
    s_choice = input("Choix (0/1/2) : ").strip()
    if s_choice not in ("0","1","2"):
        print("⛔ Choix invalide.")
        return
    solver_name = {"0":"None","1":"DFS","2":"A*"}[s_choice]
    solver_tag = {"None":"none","DFS":"dfs","A*":"astar"}[solver_name]

    n = ask_int("Taille n (≥ 2) : ", min_val=2)
    base = slugify(input("Nom de base (sans extension, ex: run1) : ").strip() or "run")

    # Génération
    if gen_name == "Backtracker":
        lines, gen_dt, gen_kb = time_and_mem(generate_maze_recursive_backtracker, n)
    else:
        lines, gen_dt, gen_kb = time_and_mem(generate_maze_kruskal, n)

    maze_txt = f"{base}_maze_{gen_tag}.txt"
    write_ascii(lines, maze_txt)
    maze_png = f"{base}_maze_{gen_tag}.png"
    ascii_to_image(lines, maze_png, cell=8)

    # Résolution (optionnelle)
    sol_lines = None
    solve_dt = solve_kb = None
    sol_txt = sol_png = None

    if solver_name == "DFS":
        sol_lines, solve_dt, solve_kb = time_and_mem(dfs_solve_ascii, lines)
    elif solver_name == "A*":
        sol_lines, solve_dt, solve_kb = time_and_mem(astar_solve_ascii, lines)

    if sol_lines is not None:
        sol_txt = f"{base}_solution_{solver_tag}.txt"
        write_ascii(sol_lines, sol_txt)
        sol_png = f"{base}_solution_{solver_tag}.png"
        ascii_to_image(sol_lines, sol_png, cell=8)

    # Résumé
    print("\n--- RÉSUMÉ ---")
    print(f"Générateur : {gen_name} | n={n} | temps={gen_dt:.6f}s | pic={gen_kb}KB")
    print(f"Fichiers   : {maze_txt}  |  {maze_png}")
    if solver_name != "None":
        print(f"Solveur    : {solver_name} | temps={solve_dt:.6f}s | pic={solve_kb}KB")
        print(f"Fichiers   : {sol_txt}  |  {sol_png}")
    else:
        print("Solveur    : (aucun)")

    # Enregistrement + Historique
    row = make_row(
        n, gen_name, gen_dt, gen_kb, maze_txt, maze_png,
        solver_name, solve_dt, solve_kb, sol_txt, sol_png
    )
    append_experiment_row(row)
    print_table(load_all_rows())

def main():
    while True:
        print("\n=== Amazing Mazes ===")
        print("1) Session complète (générer → résoudre → PNG → chrono/CSV → tableau)")
        print("0) Quitter")
        choice = input("Ton choix : ").strip()
        if choice == "1":
            action_full_session()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("⛔ Choix invalide.")

if __name__ == "__main__":
    main()
