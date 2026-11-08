import numpy as np
import pandas as pd

class Grille:
    def __init__(self, nbr_lignes, nbr_colonnes) :
        self.nbr_lignes = nbr_lignes
        self.nbr_colonnes = nbr_colonnes
        self.nbr_bombes = int(round(self.nbr_lignes*self.nbr_colonnes)*(0.2))
        self.nbr_pas_bombes = (self.nbr_lignes*self.nbr_colonnes)-self.nbr_bombes
        self.compteur_bombes = 0
        self.compteur_pas_bombes = 0

        grille_np = np.zeros((self.nbr_lignes, self.nbr_colonnes), dtype=object)

        positions = np.random.choice(grille_np.size, self.nbr_bombes, replace=False)
        grille_np.flat[positions] = 11

        for i in range(self.nbr_lignes-1):
            for j in range(self.nbr_colonnes-1):
                if grille_np[i,j] != 11:
                    compteur = 0
                    if grille_np[i, j+1] == 11:
                        compteur +=1
                    if grille_np[i+1, j] == 11:
                        compteur +=1 
                    if grille_np[i, j-1] == 11:
                        compteur+=1
                    if grille_np[i-1, j] == 11: 
                        compteur+=1
                    if grille_np[i+1, j+1] == 11:
                        compteur +=1
                    if grille_np[i-1, j-1] == 11:
                        compteur +=1
                    if grille_np[i+1, j-1] == 11:
                        compteur +=1 
                    if grille_np[i-1, j+1] == 11:
                        compteur +=1
                    grille_np[i,j] = compteur

        self.grille = pd.DataFrame(grille_np)

        for i in range(self.nbr_lignes):
            for j in range(self.nbr_colonnes):
                if self.grille.iloc[i,j] == 11 :
                    valeur_case = int(self.grille.iloc[i,j])
                    self.grille.iloc[i,j] = Case(grille = self, valeur = valeur_case, bombe=True, etat=0)
                else : 
                    valeur_case = int(self.grille.iloc[i,j])
                    self.grille.iloc[i,j] = Case(grille = self, valeur=valeur_case, bombe=False, etat=0)

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
        if self.compteur_bombes == 0 or self.compteur_pas_bombes < self.nbr_pas_bombes:
            return True
        print("Fermeture de la fenêtre")


class Case:
    def __init__(self, grille, valeur, bombe, etat=0): 
        self.etat = etat
        self.bombe = bombe
        self.valeur = valeur
        self.grille = grille

    def reveler(self):
        if self.bombe :
            self.grille.compteur_bombes+=1
            print(self.grille.compteur_bombes)
        else:
            self.grille.compteur_pas_bombes+=1
            print(self.grille.compteur_pas_bombes)
        self.etat = 2

    def semi_reveler(self):
        if self.bombe :
            self.grille.compteur_bombes+=1
        else:
            self.grille.compteur_pas_bombes+=1
        self.etat = 1


if __name__ == "__main__":

    grille = Grille(5,6)
    print(grille)
