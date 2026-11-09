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
                self.setIcon(QIcon('/home/formation/Bureau/DEMINEUR_PYQT/flag.png'))
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

class InterfaceDialog(QtWidgets.QMainWindow):
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

        widget_central = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget_central)

        for i in range(grille.nbr_lignes):
            for j in range(grille.nbr_colonnes):
                case = grille.element(i,j)
                self.bouton_case = BoutonCase(case, grille)
                self.boutons.append(self.bouton_case)
                layout.addWidget(self.bouton_case, i,j)
                self.bouton_case.signal_fin.connect(self.interface_fin_jeu)
                self.bouton_case.signal_actualiser.connect(self.actualiser_boutons)

        self.setCentralWidget(widget_central)

    def interface_fin_jeu(self):
        icone_bombe = QIcon(os.path.join(os.path.dirname(__file__), "bombe.jpeg"))
        for bouton in self.boutons:
            if bouton.case.bombe:
                bouton.nouvel_icone(icone_bombe)

        sortir_jeu = QMessageBox.question(self, "Fin du jeu", "Voulez-vous quitter ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No,)
        if sortir_jeu == QMessageBox.Yes :
            self.close()
                
    def actualiser_boutons(self):
        for bouton in self.boutons:
            bouton.fixer_valeur_case()

    def keyPressEvent(self, event) :
        if event.key() == QtCore.Qt.Key.Key_Escape :
            print('Coucou, échap a été pressée')
            self.close()

if __name__=='__main__':
    app = QApplication(sys.argv)
    grille = Grille.Grille(8,8)
    print(grille)
    fenetre = InterfaceDialog(grille)
    fenetre.show()
    sys.exit(app.exec())
