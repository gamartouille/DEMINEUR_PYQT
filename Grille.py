import numpy as np
import pandas as pd

class Grille:
    def __init__(self, nbr_lignes, nbr_colonnes) :
        self.nbr_lignes = nbr_lignes
        self.nbr_colonnes = nbr_colonnes
        self.nbr_bombes = int(round(self.nbr_lignes*self.nbr_colonnes)*(0.2))
        self.nbr_pas_bombes = (self.nbr_lignes*self.nbr_colonnes)-self.nbr_bombes
        self.compteur_bombes_revelees = 0
        self.compteur_pas_bombes_revelees = 0
        self.compteur_bombes_semi_revelees = 0
        self.compteur_pas_bombes_semi_revelees = 0
        self.nbr_drapeau_correct = 0

        grille_np = np.zeros((self.nbr_lignes, self.nbr_colonnes), dtype=object)

        positions = np.random.choice(grille_np.size, self.nbr_bombes, replace=False)
        grille_np.flat[positions] = 11

        for i in range(self.nbr_lignes):
            for j in range(self.nbr_colonnes):
                if grille_np[i,j] != 11:
                    compteur = 0
                    for voisin_i in range(max(0, i - 1), min(self.nbr_lignes, i + 2)):
                        for voisin_j in range(max(0, j - 1), min(self.nbr_colonnes, j + 2)):
                            if (voisin_i, voisin_j) != (i, j) and grille_np[voisin_i, voisin_j] == 11:
                                compteur += 1
                    grille_np[i,j] = compteur

        self.grille = pd.DataFrame(grille_np)

        for i in range(self.nbr_lignes):
            for j in range(self.nbr_colonnes):
                if self.grille.iloc[i,j] == 11 :
                    valeur_case = int(self.grille.iloc[i,j])
                    self.grille.iloc[i,j] = Case(grille=self, valeur=valeur_case, bombe=True, etat=0, ligne=i, colonne=j)
                else : 
                    valeur_case = int(self.grille.iloc[i,j])
                    self.grille.iloc[i,j] = Case(grille=self, valeur=valeur_case, bombe=False, etat=0, ligne=i, colonne=j)

    def __str__(self) : 
        mat = np.zeros([self.nbr_lignes, self.nbr_colonnes])
        for i in range(self.nbr_lignes):
            for j in range(self.nbr_colonnes):
                mat[i,j] = self.grille.iloc[i,j].valeur

        return np.array2string(mat)

    def __len__(self):
        return [self.nbr_lignes, self.nbr_colonnes]

    def element(self, i, j):
        return self.grille.iloc[i,j]

    def nbr_bombres(self):
        return self.nbr_bombes

    def condition_fin(self):
        toutes_bombes_drapeau = True
        toutes_cases_sures_revelees = True

        for i in range(self.nbr_lignes):
            for j in range(self.nbr_colonnes):
                case = self.element(i, j)
                if case.bombe:
                    if case.etat == 2:
                        return True
                    if case.etat != 1:
                        toutes_bombes_drapeau = False
                else:
                    if case.etat == 1:
                        toutes_bombes_drapeau = False
                    if case.etat != 2:
                        toutes_cases_sures_revelees = False

        return toutes_bombes_drapeau or toutes_cases_sures_revelees


class Case:
    def __init__(self, grille, valeur, bombe, etat=0, ligne=0, colonne=0):
        self.etat = etat
        self.bombe = bombe
        self.valeur = valeur
        self.grille = grille
        self.ligne = ligne
        self.colonne = colonne

    def reveler(self):
        if self.etat == 1:
            self.etat = 0
            return
        if self.etat != 0:
            return

        if self.bombe:
            self.grille.compteur_bombes_revelees = 1
            self.grille.compteur_bombes_semi_revelees = 0
            self.etat = 2
            self.grille.nbr_drapeau_correct += 1
            return

        self.grille.compteur_pas_bombes_revelees = 1
        self.grille.compteur_pas_bombes_semi_revelees = 0
        self.etat = 2

        if self.valeur == 0:
            for voisin_i in range(max(0, self.ligne - 1), min(self.grille.nbr_lignes, self.ligne + 2)):
                for voisin_j in range(max(0, self.colonne - 1), min(self.grille.nbr_colonnes, self.colonne + 2)):
                    voisin = self.grille.element(voisin_i, voisin_j)
                    if voisin.etat == 0 and not voisin.bombe:
                        voisin.reveler()

    def semi_reveler(self):
        """
        But = ne pas semi révéler si ça a déjà été révélé
        """
        if self.etat == 0 :
            if self.bombe :
                self.grille.compteur_bombes_semi_revelees=1
                self.grille.compteur_bombes_revelees=0
            else:
                self.grille.compteur_pas_bombes_revelees=0
                self.grille.compteur_pas_bombes_semi_revelees=1
            self.etat = 1

        elif self.etat == 1 :
            if self.bombe:
                self.grille.compteur_bombes_revelees=0
                self.grille.compteur_bombes_semi_revelees=0
            else:
                self.grille.compteur_pas_bombes_revelees = 0
                self.grille.compteur_pas_bombes_semi_revelees=0
            self.etat = 0

        elif self.etat == 2:
            self.etat = 2

if __name__ == "__main__":

    grille = Grille(5,6)
    print(grille)
