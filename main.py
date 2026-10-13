import os # Pour les fichiers
import pygame
from logique import Plateau


## Initialisation de l'interface ##

pygame.init()
# Le rectangle est repéré en haut à gauche
fenetre = pygame.display.set_mode((800,600))

#! Précision sur les variables en majuscules : selon la norme PEP8, une variable en maj = une constante (donc aucun effet technique)
# Donc on a choisi de nommer les variables qu'il ne faut pas changer en majuscule pour éviter les bêtises²

## Dictionnaires des thèmes ##
# Chaque thème a son dossier d'assets, avec les mêmes noms de fichiers dans chaque dossier
THEMES = {
	"usa": {"dossier": "assets/usa", "message": "You are GREAT AGAIN", "couleur": (208,32,48)},
	"chine": {"dossier": "assets/chine", "message": "你真棒 !", "couleur": (255,215,0)},
	"urss": {"dossier": "assets/urss", "message": "Ты завоевал Украину. !", "couleur": (205, 0, 0)},
	"allemagne": {"dossier": "assets/allemagne", "message": "Du hast Europa annektiert", "couleur": (255, 204, 0)},
	"france": {"dossier": "assets/france", "message": "Vous avez rembourse la dette !", "couleur": (205, 0, 0)},
	"japon": {"dossier": "assets/japon", "message": "お前は真珠湾を破壊した !", "couleur": (255, 255, 255)},
}
theme_actuel = "usa"

###! Claude à un peu aidé sur les coordonnées
# Position des tubes : coin haut-gauche du tube i en (TUBE_X + ECART_TUBES*i, TUBE_Y)
TUBE_X = 50
TUBE_Y = 55
ECART_TUBES = 150
# Dans l'image du tube (100x489) : l'intérieur va de x=31 à x=68, de y=158 (haut) à y=464 (fond)
# Le Tube.png de chaque thème doit garder ces dimensions
HAUT_TUBE = 158
FOND_TUBE = 464
# Les balles sont réduites pour rentrer dans le tube, et empilées tous les ECART_BALLES pixels
TAILLE_BALLE = 34
ECART_BALLES = 36

# Bouton de changement de thème (avec la police impact parce qu'on parle pas chinois ou russe)
BOUTON = pygame.Rect(630, 555, 160, 35)
police_bouton = pygame.font.Font("assets/Impact.ttf", 20)

# Bouton pour recommencer
RECOMMENCER = pygame.Rect(10, 555, 160, 35)

# Chronomètre, centré sous les tubes
CHRONO = pygame.Rect(340, 555, 120, 35)
police_chrono = pygame.font.Font("assets/Impact.ttf", 26)

plateau = Plateau()

def chemin(nom_fichier):
	# Renvoie le chemin du fichier dans le dossier du thème actuel (thème usa par défaut au cas où il manque un truc)
	fichier = THEMES[theme_actuel]["dossier"] + "/" + nom_fichier
	if not os.path.exists(fichier):
		fichier = THEMES["usa"]["dossier"] + "/" + nom_fichier
	return fichier

def charger_theme(nom):
	# Charge les images, la police et la musique du thème "nom"
	global theme_actuel, fond, tube, images, police
	theme_actuel = nom
	# Image de fond, mise à la taille de la fenêtre (heureusement qu'il y a la fonction smoothscale)
	fond = pygame.image.load(chemin("Fond.png")).convert()
	fond = pygame.transform.smoothscale(fond, fenetre.get_size())
	tube = pygame.image.load(chemin("Tube.png")).convert_alpha()
	# Pour retrouver l'image d'une balle à partir de sa couleur, au moment d'afficher (on scale aussi pour éviter les problèmes de tailles car toutes les images ne font pas 40x40, Romain ne les a pas toute resize)
	images = {}
	for lettre, fichier in [("R", "Rouge"), ("B", "Bleu"), ("J", "Jaune")]:
		balle = pygame.image.load(chemin(fichier + ".png")).convert_alpha()
		images[lettre] = pygame.transform.smoothscale(balle, (TAILLE_BALLE, TAILLE_BALLE))
	# Police du message de victoire
	if nom == "chine" or nom == "japon":
		police = pygame.font.Font("assets/NotoSansSC-Bold.otf", 55) # Police avec caractères chinois (et japonais : kanji + hiragana)
	elif nom == "urss":
		police = pygame.font.Font("assets/RussoOne-Regular.ttf", 55) # Police avec des caractères russes (cyrilique)
	else:
		police = pygame.font.Font("assets/Impact.ttf", 55) # Police avec nos lettres (je sais pas le nom de notre alphabet)
	# Si la partie est déjà gagnée, on garde la musique de victoire 
	if plateau.a_gagne():
		pygame.mixer.music.load(chemin("win.mp3"))
	else:
		pygame.mixer.music.load(chemin("music.mp3"))
	pygame.mixer.music.play()

def tube_clique(x, y) -> int|None:
	# Renvoie le numéro du tube cliqué (de 0 à 4), ou None si on a cliqué à côté
	for i in range(5):
		# Rectangle du tube i, placé comme dans afficher() ; pygame.collidepoint dit si le point (x,y) est à l'intérieur
		if tube.get_rect(topleft=(TUBE_X + ECART_TUBES*i, TUBE_Y)).collidepoint(x, y):
			return i
	return None

def afficher(depart, secondes):
	# Redessine toute la fenêtre à partir du plateau, avec le chronomètre à secondes
	# La balle du sommet du tube depart est dessinée au-dessus du tube pour montrer qu'elle est sélectionnée
	fenetre.blit(fond, (0, 0))
	for i in range(5):
		# On dessine les 5 tubes
		x_tube = TUBE_X + ECART_TUBES*i
		fenetre.blit(tube, (x_tube, TUBE_Y))
		pile = plateau.tubes[i]
		# Balles centrées dans le tube, la première posée sur le fond
		x = x_tube + (tube.get_width() - TAILLE_BALLE) // 2
		for j in range(pile.taille()):
			y = TUBE_Y + FOND_TUBE - 2 - TAILLE_BALLE - ECART_BALLES*j
			if i == depart and j == pile.taille() - 1:
				# On affiche la balle choisie au dessus du tube
				y = TUBE_Y + HAUT_TUBE + 4
			fenetre.blit(images[pile.contenu[j]], (x, y))
	if plateau.a_gagne():
		# Message centré en haut de la fenêtre, au-dessus des tubes
		texte = police.render(THEMES[theme_actuel]["message"], True, THEMES[theme_actuel]["couleur"])
		fenetre.blit(texte, texte.get_rect(center=(fenetre.get_width() // 2, TUBE_Y // 2)))
	# Bouton de changement de thème
	pygame.draw.rect(fenetre, (40,40,40), BOUTON, border_radius=8)
	texte = police_bouton.render("Changer de theme", True, (255,255,255))
	fenetre.blit(texte, texte.get_rect(center=BOUTON.center))
	# Bouton pour recommencer
	pygame.draw.rect(fenetre, (40,40,40), RECOMMENCER, border_radius=8)
	texte = police_bouton.render("Recommencer", True, (255,255,255))
	fenetre.blit(texte, texte.get_rect(center=RECOMMENCER.center))
	# Chronomètre au format minutes:secondes
	pygame.draw.rect(fenetre, (40,40,40), CHRONO, border_radius=8)
	texte = police_chrono.render(f"{secondes // 60:02d}:{secondes % 60:02d}", True, (255,255,255))
	fenetre.blit(texte, texte.get_rect(center=CHRONO.center))
	pygame.display.flip()


if __name__ == "__main__":
	charger_theme("usa")
	# Tube choisi au premier clic, None tant qu'aucun n'est choisi
	depart = None
	# Le chronomètre part du lancement du jeu (en millisecondes), et s'arrête à la victoire
	debut = pygame.time.get_ticks()
	fin = None
	horloge = pygame.time.Clock()
	en_jeu = True
	while en_jeu:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				en_jeu = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				(x,y) = event.pos
				if BOUTON.collidepoint(x, y):
					# Le bouton marche même après la victoire
					if theme_actuel == "usa":
						charger_theme("chine")
					elif theme_actuel == "chine":
						charger_theme("urss")
					elif theme_actuel == "urss":
						charger_theme("allemagne")
					elif theme_actuel == "allemagne":
						charger_theme("france")
					elif theme_actuel == "france":
						charger_theme("japon")
					else:
						charger_theme("usa")
				elif RECOMMENCER.collidepoint(x, y):
					# Nouvelle partie
					plateau = Plateau()
					depart = None
					debut = pygame.time.get_ticks()
					fin = None
					pygame.mixer.music.load(chemin("music.mp3"))
					pygame.mixer.music.play()
				elif not plateau.a_gagne():
					# Une fois la partie gagnée, les clics sur les tubes ne font plus rien
					i = tube_clique(x,y)
					if i == None:
						# Clic à côté des tubes
						depart = None
					elif depart == None:
						# Premier clic (il doit y avoir une balle)
						if not plateau.tubes[i].est_vide():
							depart = i
					else:
						# Second clic (on peut pas déplacer si il est plein)
						plateau.deplacer(depart, i)
						depart = None
						if plateau.a_gagne():
							fin = pygame.time.get_ticks()
							# La musique de victoire est lancée une seule fois, au coup gagnant
							pygame.mixer.music.load(chemin("win.mp3"))
							pygame.mixer.music.play()
		# On redessine à chaque tour de boucle pour que le chronomètre avance même sans clic
		if fin == None:
			secondes = (pygame.time.get_ticks() - debut) // 1000
		else:
			secondes = (fin - debut) // 1000
		afficher(depart, secondes)
		# 30 images par seconde suffisent, ça évite d'utiliser tout le processeur (surtout avec les pc du lycée ça explose sinon)
		horloge.tick(30)
	pygame.quit()
