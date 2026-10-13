import pygame
from logique import Plateau


## Initialisation de l'interface ##

pygame.init()
# Le rectangle est repéré en haut à gauche
fenetre = pygame.display.set_mode((800,600))

## Création des éléments visuels ##
ballR = pygame.image.load("assets/Rouge.png").convert_alpha()
ballB = pygame.image.load("assets/Bleu.png").convert_alpha()
ballJ = pygame.image.load("assets/Jaune.png").convert_alpha()
tube = pygame.image.load("assets/Tube.png").convert_alpha()

# Image de fond, mise à la taille de la fenêtre (elle a déjà les mêmes proportions, donc pas de déformation)
fond = pygame.image.load("assets/Fond.png").convert()
fond = pygame.transform.smoothscale(fond, fenetre.get_size())

# Position des tubes : coin haut-gauche du tube i en (TUBE_X + ECART_TUBES*i, TUBE_Y)
TUBE_X = 50
TUBE_Y = 55
ECART_TUBES = 150
# Dans l'image du tube (100x489) : l'intérieur va de x=31 à x=68, de y=158 (haut) à y=464 (fond)
HAUT_TUBE = 158
FOND_TUBE = 464
# Les balles sont réduites pour rentrer dans le tube, et empilées tous les ECART_BALLES pixels
TAILLE_BALLE = 34
ECART_BALLES = 36
ballR = pygame.transform.smoothscale(ballR, (TAILLE_BALLE, TAILLE_BALLE))
ballB = pygame.transform.smoothscale(ballB, (TAILLE_BALLE, TAILLE_BALLE))
ballJ = pygame.transform.smoothscale(ballJ, (TAILLE_BALLE, TAILLE_BALLE))

# Pour retrouver l'image d'une balle à partir de sa couleur, au moment d'afficher (à l'aide d'un dictionnaire)
images = {"R":ballR, "B":ballB, "J":ballJ}

# Police utilisée pour le message de victoire
police = pygame.font.Font("assets/Impact.ttf", 55)

plateau = Plateau()

def tube_clique(x, y) -> int|None:
	# Renvoie le numéro du tube cliqué (de 0 à 4), ou None si on a cliqué à côté
	for i in range(5):
		# Rectangle du tube i, placé comme dans afficher() ; pygame.collidepoint dit si le point (x,y) est à l'intérieur
		if tube.get_rect(topleft=(TUBE_X + ECART_TUBES*i, TUBE_Y)).collidepoint(x, y):
			return i
	return None

def afficher(depart):
	# Redessine toute la fenêtre à partir du plateau
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
		texte = police.render("You are GREAT AGAIN", True, (36,51,122))
		fenetre.blit(texte, texte.get_rect(center=(fenetre.get_width() // 2, TUBE_Y // 2)))
	pygame.display.flip()


if __name__ == "__main__":
	# Tube choisi au premier clic, None tant qu'aucun n'est choisi
	depart = None
	afficher(depart)
	en_jeu = True
	while en_jeu:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				en_jeu = False
			elif event.type == pygame.MOUSEBUTTONDOWN and not plateau.a_gagne():
				# Une fois la partie gagnée, les clics ne font plus rien
				(x,y) = event.pos
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
				afficher(depart)
	pygame.quit()
