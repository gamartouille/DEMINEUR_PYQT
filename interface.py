import os
import sys
from PyQt5.QtWidgets import *
from qgis.PyQt import QtWidgets, QtCore, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import Grille 

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(
        os.path.dirname(__file__),
        'interface.ui'),
    from_imports=True,
    import_from='DEMINEUR')

class BoutonCase(QPushButton):

    signal_fin = pyqtSignal()
    signal_actualiser = pyqtSignal()

    def __init__(self, case, grille, parent=None):
        super().__init__(parent)
        self.case = case
        self.grille = grille
        self.setFixedSize(30,30)
        self.fixer_valeur_case()

    def nouvel_icone(self, icone):
        self.setIcon(icone)

    def fixer_valeur_case(self):
        if self.case.etat == 2:
            self.setText(str(self.case.valeur))
            self.setIcon(QIcon())
        else:
            self.setText(" ")
            if self.case.etat == 1:
                self.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "flag.png")))
            else:
                self.setIcon(QIcon())

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clic_gauche()
            self.fixer_valeur_case()
        elif event.button() == Qt.RightButton:
            self.clic_droit()
            self.fixer_valeur_case()
            return
        super().mousePressEvent(event)

    def clic_gauche(self):
        self.case.reveler()
        self.signal_actualiser.emit()
        self.setText(str(self.case.valeur))
        self.setIcon(QIcon())
        if self.grille.condition_fin():
            print(self.grille.condition_fin())
            self.signal_fin.emit()

    def clic_droit(self):
        self.case.semi_reveler()
        if self.grille.condition_fin():
            self.signal_fin.emit()

class BoutonPause(QPushButton):

    def __init__(self, etat, interface, parent=None):
        # etat = 0 : le timer fonctionne, etat = 1, il est en pause
        super().__init__(parent)
        self.etat = etat
        self.interface = interface
        self.clicked.connect(self.pause)

    def pause(self):
        if self.etat == 0 :
            self.etat = 1
            self.interface.timer.stop()
            self.interface.temps_total_ms += self.interface.chrono.elapsed()
            self.interface.chrono.invalidate()
        else :
            self.etat = 0
            self.interface.chrono.restart()
            self.interface.timer.start()   

class InterfaceNiveau(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Choix du niveau")

        widget_central = QtWidgets.QWidget()
        self.layout_central = QtWidgets.QVBoxLayout(widget_central)

        self.bouton_niv_1 = QPushButton("Niveau 1")
        self.bouton_niv_2 = QPushButton("Niveau 2")
        self.bouton_niv_3 = QPushButton("Niveau 3")
        self.layout_central.addWidget(self.bouton_niv_1)
        self.layout_central.addWidget(self.bouton_niv_2)
        self.layout_central.addWidget(self.bouton_niv_3)

        self.grille_niv_1 = Grille.Grille(5,5)
        self.grille_niv_2 = Grille.Grille(15,15)
        self.grille_niv_3 = Grille.Grille(30,30)

        self.bouton_niv_1.clicked.connect(self.ouverture_interface_niv_1)
        self.bouton_niv_2.clicked.connect(self.ouverture_interface_niv_2)
        self.bouton_niv_3.clicked.connect(self.ouverture_interface_niv_3)

        self.setCentralWidget(widget_central)

    def ouverture_interface_niv_1(self):
        self.close()
        fenetre = InterfaceJeu(self.grille_niv_1)
        fenetre.show()

    def ouverture_interface_niv_2(self):
        self.close()
        fenetre = InterfaceJeu(self.grille_niv_2)
        fenetre.show()

    def ouverture_interface_niv_3(self):
        self.close()
        fenetre = InterfaceJeu(self.grille_niv_3)
        fenetre.show()


class InterfaceJeu(QtWidgets.QMainWindow):

    def __init__(self, grille):
        """Constructor."""
        super().__init__()
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.grille = grille
        self.setWindowTitle("Démineur")
        self.boutons = []

        # GESTION DU TEMPS
        self.timer = QTimer()
        self.temps_depart = QElapsedTimer()
        self.temps_total_ms = 0
        self.chrono = QElapsedTimer()
        self.chrono.start()
        self.timer.timeout.connect(self.maj_timer)
        self.temps_depart.start()
        self.timer.start(1000)

        # GESTION DE L'ESTHETIQUE

        # Corps de la fenetre
        widget_central = QtWidgets.QWidget()
        self.layout_principal = QtWidgets.QVBoxLayout(widget_central)

        # Barre du haut
        widget_haut = QtWidgets.QWidget()
        layout_haut = QtWidgets.QHBoxLayout(widget_haut)
        self.horloge = QLabel("00")
        bouton_pause = BoutonPause(etat=0, interface = self)
        bouton_pause.setText("Pause")
        bouton_recommencer = QPushButton("Recommencer")
        bouton_recommencer.clicked.connect(self.recommencer_partie)
        layout_haut.addWidget(self.horloge)
        layout_haut.addWidget(bouton_pause)
        layout_haut.addWidget(bouton_recommencer)
        layout_haut.addStretch()

        # Grille
        layout_central = QtWidgets.QGridLayout()

        for i in range(grille.nbr_lignes):
            for j in range(grille.nbr_colonnes):
                case = grille.element(i,j)
                self.bouton_case = BoutonCase(case, grille)
                self.boutons.append(self.bouton_case)
                layout_central.addWidget(self.bouton_case, i,j)
                self.bouton_case.signal_fin.connect(self.interface_fin_jeu)
                self.bouton_case.signal_actualiser.connect(self.actualiser_boutons)

        self.layout_principal.addWidget(widget_haut)
        self.layout_principal.addLayout(layout_central)

        self.setCentralWidget(widget_central)

    def maj_timer(self):
        temps = (self.temps_total_ms + self.chrono.elapsed()) // 1000
        self.horloge.setText(f"Temps : {str(temps)}s")

    def interface_fin_jeu(self):
        self.timer.stop()
        icone_bombe = QIcon(os.path.join(os.path.dirname(__file__), "bombe.jpeg"))
        for bouton in self.boutons:
            if bouton.case.bombe:
                bouton.nouvel_icone(icone_bombe)

        sortir_jeu = QMessageBox.question(self, "Fin du jeu", "Voulez-vous réessayer ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes,)
        if sortir_jeu == QMessageBox.No :
            self.close()
        else:
            self.recommencer_partie()
                
    def actualiser_boutons(self):
        for bouton in self.boutons:
            bouton.fixer_valeur_case()

    def recommencer_partie(self):
        self.close()
        for i in range(self.grille.nbr_lignes):
            for j in range(self.grille.nbr_colonnes):
                self.grille.element(i,j).etat = 0
        new_grille = self.grille
        fenetre = InterfaceJeu(new_grille)
        fenetre.show()

    def keyPressEvent(self, event) :
        if event.key() == QtCore.Qt.Key.Key_Escape :
            self.close()

if __name__=='__main__':
    app = QApplication(sys.argv)
    fenetre_niveau = InterfaceNiveau()
    fenetre_niveau.show()
    sys.exit(app.exec())
