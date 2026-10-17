import os # Pour les fichiers
import csv # Pour la sauvegarde des temps
from datetime import datetime # Pour la date des scores
import pygame
from logique import Plateau


## Initialisation de l'interface ##

pygame.init()
pygame.display.set_caption('BallSort Utlra Pro Max') # Titre de la fenêtre
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
	"streamer": {"dossier": "assets/streamer", "message": "Tu es devenu top 1 twitch France !", "couleur": (145, 70, 255)},
	"minecraft": {"dossier": "assets/minecraft", "message": "Ender Dragon vaincu !", "couleur": (255, 255, 85)},
	"finals": {"dossier": "assets/finals", "message": "Vous avez gagne THE FINALS !", "couleur": (230, 25, 40)},
	"pologne": {"dossier": "assets/pologne", "message": "Zjadłeś wszystkie pierogi !", "couleur": (220, 20, 60)},
	# L'hébreu se lit de droite à gauche mais pygame affiche de gauche à droite, donc on retourne la phrase avec [::-1]
	"israel": {"dossier": "assets/israel", "message": "ניצחת את כולם"[::-1], "couleur": (0, 56, 184)},
	"vietnam": {"dossier": "assets/vietnam", "message": "Bạn đã đánh bại nước Mỹ !", "couleur": (255, 205, 0)},
	"ia": {"dossier": "assets/ia", "message": "Quota depasse", "couleur": (255, 0, 200)},
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

# Bouton du tableau des scores, entre "Recommencer" et le chronomètre
SCORES = pygame.Rect(180, 555, 150, 35)
# Tableau des scores affiché par-dessus les tubes
TABLEAU = pygame.Rect(150, 70, 500, 465)
police_tableau = pygame.font.Font("assets/NotoSansSC-Bold.otf", 20)
police_titre = pygame.font.Font("assets/NotoSansSC-Bold.otf", 30)
NB_SCORES = 10 # Nombre de meilleurs temps affichés (pour être affiché faut être bon !)

# Fichier csv avec les scores (date, thème, temps en secondes)
FICHIER_SCORES = "scores.csv"

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
	elif nom == "vietnam":
		police = pygame.font.Font("assets/BeVietnamPro-Bold.ttf", 55) # Police avec les accents vietnamiens (ạ, đ, ư, ỹ...)
	elif nom == "urss" or nom == "pologne":
		police = pygame.font.Font("assets/RussoOne-Regular.ttf", 55) # Police avec des caractères russes (cyrilique) et polonais (ł, ś...)
	elif nom == "israel":
		police = pygame.font.Font("assets/NotoSansHebrew-Bold.ttf", 55) # Police avec des caractères hébreux (pas de "!" dedans)
	else:
		police = pygame.font.Font("assets/Impact.ttf", 55) # Police avec nos lettres (je sais pas le nom de notre alphabet)
	# Si la partie est déjà gagnée, on garde la musique de victoire 
	if plateau.a_gagne():
		pygame.mixer.music.load(chemin("win.mp3"))
	else:
		pygame.mixer.music.load(chemin("music.mp3"))
	pygame.mixer.music.play()

def sauvegarder_temps(secondes) -> dict:
	# Ajoute le temps de la partie gagnée à la fin du fichier csv (on le crée avec l'en-tête s'il n'existe pas)
	# Renvoie la ligne ajoutée, pour pouvoir la surligner dans le tableau
	score = {"date": datetime.now().strftime("%d/%m/%Y %H:%M"), "theme": theme_actuel, "temps": secondes}
	nouveau = not os.path.exists(FICHIER_SCORES)
	with open(FICHIER_SCORES, "a", newline="", encoding="utf-8") as fichier:
		ecrivain = csv.DictWriter(fichier, fieldnames=["date", "theme", "temps"])
		if nouveau:
			ecrivain.writeheader()
		ecrivain.writerow(score)
	return score

def charger_scores() -> list:
	# Renvoie la liste des scores du fichier csv, du plus rapide au plus lent
	if not os.path.exists(FICHIER_SCORES):
		return []
	with open(FICHIER_SCORES, newline="", encoding="utf-8") as fichier:
		scores = list(csv.DictReader(fichier))
	for score in scores:
		score["temps"] = int(score["temps"]) # Le csv ne stocke que du texte
	scores.sort(key=lambda score: score["temps"])
	return scores

def format_temps(secondes) -> str:
	# Temps au format minutes:secondes
	return f"{secondes // 60:02d}:{secondes % 60:02d}"

def afficher_tableau(scores, dernier):
	# Dessine le tableau des NB_SCORES meilleurs temps, avec le temps de la partie qui vient d'être gagnée (dernier) en jaune
	fond_tableau = pygame.Surface(TABLEAU.size, pygame.SRCALPHA)
	fond_tableau.fill((20, 20, 20, 225)) # Noir un peu transparent
	fenetre.blit(fond_tableau, TABLEAU.topleft)
	pygame.draw.rect(fenetre, (255, 255, 255), TABLEAU, 2, border_radius=8)
	texte = police_titre.render("Meilleurs temps", True, (255, 255, 255))
	fenetre.blit(texte, texte.get_rect(center=(TABLEAU.centerx, TABLEAU.top + 30)))
	# Colonnes : rang, temps, thème, date
	colonnes = [TABLEAU.left + 25, TABLEAU.left + 75, TABLEAU.left + 165, TABLEAU.left + 300]
	y = TABLEAU.top + 70
	for x, titre in zip(colonnes, ["#", "Temps", "Theme", "Date"]):
		fenetre.blit(police_tableau.render(titre, True, (160, 160, 160)), (x, y))
	if len(scores) == 0:
		texte = police_tableau.render("Aucune partie gagnee pour l'instant", True, (255, 255, 255))
		fenetre.blit(texte, texte.get_rect(center=(TABLEAU.centerx, TABLEAU.centery)))
	for rang, score in enumerate(scores[:NB_SCORES], start=1):
		y = TABLEAU.top + 70 + 32*rang
		couleur = (255, 215, 0) if score == dernier else (255, 255, 255)
		valeurs = [str(rang), format_temps(score["temps"]), score["theme"].capitalize(), score["date"]]
		for x, valeur in zip(colonnes, valeurs):
			fenetre.blit(police_tableau.render(valeur, True, couleur), (x, y))
	texte = police_tableau.render("Cliquer pour fermer", True, (160, 160, 160))
	fenetre.blit(texte, texte.get_rect(center=(TABLEAU.centerx, TABLEAU.bottom - 22)))

def tube_clique(x, y) -> int|None:
	# Renvoie le numéro du tube cliqué (de 0 à 4), ou None si on a cliqué à côté
	for i in range(5):
		# Rectangle du tube i, placé comme dans afficher() ; pygame.collidepoint dit si le point (x,y) est à l'intérieur
		if tube.get_rect(topleft=(TUBE_X + ECART_TUBES*i, TUBE_Y)).collidepoint(x, y):
			return i
	return None

def afficher(depart, secondes, scores=None, dernier=None):
	# Redessine toute la fenêtre à partir du plateau, avec le chronomètre à secondes
	# La balle du sommet du tube depart est dessinée au-dessus du tube pour montrer qu'elle est sélectionnée
	# Si scores n'est pas None, le tableau des scores est dessiné par-dessus les tubes
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
	# Bouton du tableau des scores
	pygame.draw.rect(fenetre, (40,40,40), SCORES, border_radius=8)
	texte = police_bouton.render("Scores", True, (255,255,255))
	fenetre.blit(texte, texte.get_rect(center=SCORES.center))
	# Chronomètre au format minutes:secondes
	pygame.draw.rect(fenetre, (40,40,40), CHRONO, border_radius=8)
	texte = police_chrono.render(format_temps(secondes), True, (255,255,255))
	fenetre.blit(texte, texte.get_rect(center=CHRONO.center))
	if scores != None:
		afficher_tableau(scores, dernier)
	pygame.display.flip()


if __name__ == "__main__":
	charger_theme("usa")
	# Tube choisi au premier clic, None tant qu'aucun n'est choisi
	depart = None
	# Le chronomètre part du lancement du jeu (en millisecondes), et s'arrête à la victoire
	debut = pygame.time.get_ticks()
	fin = None
	# Liste des scores quand le tableau est ouvert, None quand il est fermé
	scores = None
	# Score de la dernière partie gagnée, surligné dans le tableau
	dernier = None
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
					elif theme_actuel == "japon":
						charger_theme("streamer")
					elif theme_actuel == "streamer":
						charger_theme("minecraft")
					elif theme_actuel == "minecraft":
						charger_theme("finals")
					elif theme_actuel == "finals":
						charger_theme("pologne")
					elif theme_actuel == "pologne":
						charger_theme("israel")
					elif theme_actuel == "israel":
						charger_theme("vietnam")
					elif theme_actuel == "vietnam":
						charger_theme("ia")
					else:
						charger_theme("usa")
				elif SCORES.collidepoint(x, y):
					# Ouvre ou ferme le tableau des scores (on relit le csv à chaque ouverture)
					if scores == None:
						scores = charger_scores()
					else:
						scores = None
				elif RECOMMENCER.collidepoint(x, y):
					# Nouvelle partie
					plateau = Plateau()
					depart = None
					debut = pygame.time.get_ticks()
					fin = None
					scores = None
					dernier = None
					pygame.mixer.music.load(chemin("music.mp3"))
					pygame.mixer.music.play()
				elif scores != None:
					# Un clic ailleurs ferme le tableau des scores (sans toucher aux tubes)
					scores = None
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
							# On sauvegarde le temps et on ouvre le tableau pour voir son classement
							dernier = sauvegarder_temps((fin - debut) // 1000)
							scores = charger_scores()
		# On redessine à chaque tour de boucle pour que le chronomètre avance même sans clic
		if fin == None:
			secondes = (pygame.time.get_ticks() - debut) // 1000
		else:
			secondes = (fin - debut) // 1000
		afficher(depart, secondes, scores, dernier)
		# 30 images par seconde suffisent, ça évite d'utiliser tout le processeur (surtout avec les pc du lycée ça explose sinon)
		horloge.tick(30)
	pygame.quit()
