import pygame


## Initialisation de l'interface ##

pygame.init()
# verticalement : 360, 315, 270, 225
# horizontalement: 150, 250 ,350 ,450, 550
# Le rectangle est repéré en haut à gauche
fenetre = pygame.display.set_mode((800,600))

## Création des éléments visuels ##
ballR = pygame.image.load("assets/Rouge.png").convert_alpha()
ballR_rect = ballR.get_rect()
ballR_rect = ballR_rect.move(150,270)
ballB = pygame.image.load("assets/Bleu.png").convert_alpha()
ballB_rect = ballB.get_rect()
ballB_rect = ballB_rect.move(150,315)
ballJ = pygame.image.load("assets/Jaune.png").convert_alpha()
ballJ_rect = ballJ.get_rect()
ballJ_rect = ballJ_rect.move(150,360)
tube = pygame.image.load("assets/Tube.png").convert_alpha()
tube_rect = tube.get_rect()
tube_rect = tube_rect.move(42,200)

## Chargement des 5 tubes et des balles ##
# Les tubes sont dessinés en premier pour que les balles passent par-dessus
for i in range(5):
	xt =  100
	tube_rect = tube_rect.move(xt,0)
	fenetre.blit(tube, tube_rect)

fenetre.blit(ballR,ballR_rect)
fenetre.blit(ballB,ballB_rect)
fenetre.blit(ballJ,ballJ_rect)

for i in range(2):
	xt = 100
	ballR_rect = ballR_rect.move(xt,0)
	ballJ_rect = ballJ_rect.move(xt,0)
	ballB_rect = ballB_rect.move(xt,0)
	fenetre.blit(ballR,ballR_rect)
	fenetre.blit(ballB,ballB_rect)
	fenetre.blit(ballJ,ballJ_rect)

pygame.display.flip()

en_jeu = True
while en_jeu:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			en_jeu = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			(x,y) = event.pos
			print(x,y)

pygame.quit()
