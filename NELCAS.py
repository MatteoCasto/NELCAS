# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 17:23:19 2022

@author: matteo.casto
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem, QStandardItemModel
from interface import windowParametres, windowCalcul, windowResGlobaux, windowPoints, windowObservations, windowConversions, windowCoordsApproch
import json
import xmltodict
from PyQt5 import uic
import libUtils.processUtils as processUtils
import sys
import os
import ctypes
import webbrowser
import numpy



class UI(QtWidgets.QMainWindow):

    def __init__(self):
        
        super(UI, self).__init__()
        
        # Charger le ui de la page d'acceuil
        uic.loadUi(os.getcwd()+"\\interface\\OngletAcceuil.ui", self)
        
        # 2 commandes ctypes pour permettre d'avoir l'icone sur la barre des tâches
        myappid = 'NELCAS_vProto' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Connecter les boutons qui ouvrent chaque fenêtre
        self.boutonOuvrirParam.clicked.connect(self.openWindowParam)
        self.boutonOuvrirCalcul.clicked.connect(self.openWindowCalcul)
        self.boutonOuvrirResGlobaux.clicked.connect(self.openWindowResGlobaux)
        self.boutonOuvrirPoints.clicked.connect(self.openWindowPoints)
        self.boutonOuvrirObs.clicked.connect(self.openWindowObs)
        self.boutonOuvrirResMap.clicked.connect(self.openWindowResMap)
        self.boutonOuvrirConversions.clicked.connect(self.openWindowConversions)
        self.boutonOuvrirCoordsApproch.clicked.connect(self.openWindowCoordsApproch)

        # Afficher la fenêtre d'acceuil
        self.show()
        

    """
    Ensemble de fonctions permettant d'ouvrir les divers fenêtre de l'interface.
    """
    def openWindowParam(self):
        
        self.windowParam = windowParametres.UI_ongletParam()
        self.windowParam.show()
        
    def openWindowCalcul(self):
        
        self.windowCal = windowCalcul.UI_ongletCalcul()
        self.windowCal.show()
        
        # Récupération des noms de fichiers des dernier fichier ouverts (obs., pts, param.)
        try: # Si pas de fichier obs. ouvert précédemment
            self.windowCal.pathObs.setText(self.windowObs.filePath)
        except:
            pass
        
        try: # Si pas de fichier pts ouvert précédemment
            self.windowCal.pathPoints.setText(self.windowPoints.filePath)
        except:
            pass
        
        try: # Si pas de fichier paramètres ouvert précédemment
            self.windowCal.pathParam.setText(self.windowParam.filePath)
        except:
            pass
    
    def openWindowResGlobaux(self):
        
        self.windowResGlobaux = windowResGlobaux.UI_ongletResGlobaux()
        self.windowResGlobaux.show()
        
        try: # Si pas de calcul effectué précédemment
            self.windowResGlobaux.openFile(self.windowCal.resDirPath.text() + "/results.xml") 
        except:
            pass

    def openWindowPoints(self):
        
        self.windowPoints = windowPoints.UI_ongletPoints()
        self.windowPoints.show()
        
    def openWindowObs(self):
        
        self.windowObs = windowObservations.UI_ongletObs()
        self.windowObs.show()
    
    def openWindowResMap(self):
        
        # Open default navigator with local relative URL of ResMap
        url = os.getcwd() + '\\resMap\\ResMap_BETA.html'
        webbrowser.open(url)
        
    def openWindowConversions(self):
        
        self.windowConversions = windowConversions.UI_ongletConversions()
        self.windowConversions.show()
    
    def openWindowCoordsApproch(self):
        
        self.windowCoordsApproch = windowCoordsApproch.UI_ongletCoordsApproch()
        self.windowCoordsApproch.show()
            
        
        
if __name__ == "__main__" :
    
    # Lancement de l'application
    app = QtWidgets.QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()



        




