
#  Amazing Mazes

##  Objectif du projet
Ce projet explore la **génération et la résolution de labyrinthes** en Python.  
Il implémente différents algorithmes de graphes et permet de comparer leurs performances en temps et en mémoire.

##  Structure du projet
amazing-mazes/
├─ main.py # Menu principal (génération, résolution, chrono, CSV, export PNG)
├─ data/ # Résultats sauvegardés (CSV + fichiers .txt/.png)
└─ maze/
├─ generator.py # Algorithmes de génération (Backtracker, Kruskal)
├─ solver.py # Algorithmes de résolution (DFS, A*)
├─ utils.py # Fonctions utilitaires (I/O ASCII, conversions)
└─ image_export.py # Export ASCII → PNG (Pillow)

## Utilisation

Lancer le menu principal :

python main.py


## Fonctionnalités :

Choisir un générateur (Backtracker, Kruskal)

Choisir un solveur (DFS, A* ou aucun)

Exporter en .txt et .png

Mesurer temps + mémoire

Sauvegarder l’expérience dans data/experiments.csv avec affichage d’un historique

## Algorithmes implémentés
Génération

Backtracker (DFS) : simple, rapide, génère de longs couloirs.

Kruskal (Union-Find) : évite les cycles, labyrinthe plus équilibré.

Résolution

DFS : trouve une sortie, pas forcément optimale.

A* : guidé par l’heuristique Manhattan, trouve le plus court chemin.

## Exemple de sortie
ASCII
#########
#...#...#
###.#.#.#
#.#.#.#.#
#.#...#.#
#.#####.#
#.......#
#########

PNG

(Exemple d’image générée du labyrinthe, exportée automatiquement)

## Données collectées

À chaque session, le programme enregistre :

Taille du labyrinthe

Temps d’exécution

Mémoire utilisée

Noms des fichiers exportés

Les résultats sont sauvegardés dans data/experiments.csv.

## Conclusion

Backtracker : simple, rapide mais couloirs longs.

Kruskal : plus équilibré.

DFS : trouve une sortie mais pas optimale.

A* : efficace et optimal.

Le projet exporte et compare automatiquement les résultats.