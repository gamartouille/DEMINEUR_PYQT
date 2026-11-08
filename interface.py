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

    def __init__(self, case, grille, parent=None):
        super().__init__(parent)
        self.case = case
        self.grille = grille
        self.setFixedSize(30,30)
        if self.case.etat != 0 : 
            self.setText(str(case.valeur))

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clic_gauche()
        elif event.button() == Qt.RightButton:
            self.clic_droit()
            return
        super().mousePressEvent(event)

    def clic_gauche(self):
        self.case.reveler()
        self.setText(str(self.case.valeur))
        self.setIcon(QIcon())

    def clic_droit(self):
        self.case.semi_reveler()
        self.setIcon(QIcon('/home/garance/Documents/PERSO/DEMINEUR/flag.png'))

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

        widget_central = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget_central)

        for i in range(grille.nbr_lignes):
            for j in range(grille.nbr_colonnes):
                case = grille.element(i,j)
                bouton_case = BoutonCase(case, grille)
                layout.addWidget(bouton_case, i,j)

        self.setCentralWidget(widget_central)

    def keyPressEvent(self, event) :
        if event.key() == QtCore.Qt.Key.Key_Escape :
            print('Coucou, échap a été pressée')
            self.close()


if __name__=='__main__':
    app = QApplication(sys.argv)
    grille = Grille.Grille(20,18)
    fenetre = InterfaceDialog(grille)
    fenetre.show()
    sys.exit(app.exec())
