import random

class Pile():
    def __init__(self):
        self.contenu = []

    def est_vide(self):
        return len(self.contenu) == 0

    def taille(self):
        return len(self.contenu)

    def empiler(self, element):
        self.contenu.append(element)

    def depiler(self):
        return self.contenu.pop()

    def sommet(self):
        return self.contenu[-1]


class Plateau():
    # Les 5 tubes du jeu, chacun étant une Pile
    # Mêmes codes couleur que dans ui.py : R = rouge, B = bleu, J = jaune
    COULEURS = ["R", "B", "J"]
    NB_TUBES = 5
    CAPACITE = 8

    def __init__(self):
        self.tubes = []
        for i in range(self.NB_TUBES):
            self.tubes.append(Pile())
        self.repartition()

    def repartition(self):
        # CAPACITE balles de chaque couleur, mélangées puis réparties dans les premiers tubes
        # (un tube par couleur, rempli au maximum)
        balles = self.COULEURS * self.CAPACITE
        random.shuffle(balles)
        for i in range(len(self.COULEURS)):
            for j in range(self.CAPACITE):
                self.tubes[i].empiler(balles.pop())

    def deplacer(self, depart, arrivee):
        # Déplace la balle du sommet du tube depart vers le tube arrivee
        # Renvoie True si le déplacement a eu lieu, False sinon
        tube_depart = self.tubes[depart]
        tube_arrivee = self.tubes[arrivee]
        if tube_depart.est_vide():
            return False
        if tube_arrivee.taille() >= self.CAPACITE:
            return False
        if not tube_arrivee.est_vide() and tube_arrivee.sommet() != tube_depart.sommet():
            return False
        tube_arrivee.empiler(tube_depart.depiler())
        return True

    def a_gagne(self):
        # Gagné quand chaque couleur remplit un tube à elle seule
        nbr_tube_plein = 0
        for tube in self.tubes:
            for couleur in self.COULEURS:
                if tube.contenu == [couleur] * self.CAPACITE:
                    nbr_tube_plein += 1
        return nbr_tube_plein == len(self.COULEURS)
