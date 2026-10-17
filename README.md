# BallSort Ultra Pro Max

<p align="center">
  <img src="assets/icone.png" alt="Icône de BallSort" width="200">
</p>

Un jeu de tri de balles (*ball sort puzzle*) en Python avec Pygame, avec 13 thèmes, des musiques et un chronomètre.

## But du jeu

Au départ, 24 balles (8 rouges, 8 bleues, 8 jaunes) sont mélangées dans 3 tubes, et 2 tubes sont vides.
Il faut ranger les balles pour que chaque couleur remplisse un tube à elle seule, le plus vite possible.

Règles d'un déplacement :
- on ne peut déplacer que la balle du **haut** d'un tube ;
- on ne peut la poser que dans un tube **vide** ou sur une balle de **la même couleur** ;
- un tube contient au maximum **8 balles**.

## Commandes

| Action | Comment |
|---|---|
| Choisir une balle | Cliquer sur un tube (la balle du haut se soulève) |
| Déplacer la balle | Cliquer sur le tube d'arrivée |
| Annuler la sélection | Cliquer à côté des tubes |
| **Recommencer** | Nouvelle partie mélangée, le chrono repart à zéro |
| **Scores** | Ouvre ou ferme le tableau des 10 meilleurs temps |
| **Changer de thème** | Passe au thème suivant (marche aussi après la victoire) |

À la victoire, le chrono s'arrête, la musique de victoire se lance et le tableau des scores s'ouvre avec votre temps surligné en jaune.

## Thèmes

USA, Chine, URSS, Allemagne, France, Japon, Streamer, Minecraft, The Finals, Pologne, Israël, Vietnam et IA.
Chaque thème a ses propres balles, son fond, sa musique et son message de victoire dans la langue du pays.

## Lancer le jeu

### Avec l'exécutable (Windows)

Double-cliquer sur `BallSort.exe`. Pas besoin d'installer Python.
Le premier lancement prend quelques secondes, le temps que le jeu décompresse ses images et musiques.

### Depuis le code source

Il faut Python 3.10 ou plus récent et `pygame-ce` :

```bash
pip install pygame-ce
python main.py
```

Le jeu doit être lancé depuis le dossier du projet (pour qu'il trouve le dossier `assets`).

## Compiler l'exécutable

```bash
pip install pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --name BallSort --icon assets/icone.ico --add-data "assets;assets" main.py
```

L'exécutable est créé dans le dossier `dist/`.

## Scores

Les temps des parties gagnées sont enregistrés dans `scores.csv` (date, thème, temps en secondes) :
dans le dossier du projet si on lance `main.py`, ou à côté de `BallSort.exe` si on lance l'exécutable.
Pour remettre les scores à zéro, il suffit de supprimer ce fichier.

## Organisation du code

```
ball_sort/
├── main.py      # Interface Pygame : affichage, clics, thèmes, chrono, scores
├── logique.py   # Règles du jeu : classes Pile et Plateau
└── assets/      # Polices et un dossier par thème (Bleu.png, Rouge.png, Jaune.png, Tube.png, Fond.png, music.mp3, win.mp3)
```

### Ajouter un thème

1. Créer un dossier `assets/<nom>` avec les mêmes fichiers que les autres thèmes. S'il en manque un, c'est celui du thème USA qui est utilisé.
   `Tube.png` doit garder les dimensions 100×489.
2. Ajouter le thème dans le dictionnaire `THEMES` de `main.py` (dossier, message de victoire, couleur du message).
3. L'ajouter dans l'enchaînement du bouton « Changer de thème », à la fin de `main.py`.

## Licence

Ce projet est sous licence GNU GPL v3, voir le fichier [LICENSE](LICENSE).
