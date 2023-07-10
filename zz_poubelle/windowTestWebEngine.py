# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 13:42:33 2022

@author: matteo.casto
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem, QStandardItemModel
# from interface import windowResMap
from PyQt5 import uic
import sys
import os
import ctypes




class UI(QtWidgets.QMainWindow):

    def __init__(self):
        
        super(UI, self).__init__()
        
        # Charger le ui de la page d'acceuil
        uic.loadUi(os.getcwd()+"\\interface\\OngletAcceuil.ui", self)
        
        # 2 commandes ctypes pour permettre d'avoir l'icone sur la barre des tâches
        myappid = 'NELCAS_vProto' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Connecter les boutons qui ouvrent chaque fenêtre
        # self.boutonOuvrirResMap.clicked.connect(self.openWindowResMap)

        # Afficher la fenêtre d'acceuil
        self.show()
        
    
    """
    Ensemble de fonctions permettant d'ouvrir les divers fenêtre de l'interface.
    """

    
        

        
if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()
