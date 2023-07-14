
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem, QStandardItemModel
import json
import xmltodict
from PyQt5 import uic
import libUtils.processUtils as processUtils
import os
from interface import windowResGlobaux



class UI_ongletCalcul(QtWidgets.QMainWindow):
    
    def __init__(self):
        
        super(UI_ongletCalcul, self).__init__()
        # Charger le ui
        uic.loadUi(os.getcwd()+"\\interface\\OngletCalcul.ui", self)
        
        
        # Connection des boutons de fileDialog
        self.parcourirObs.clicked.connect(self.browseObsClicked)
        self.parcourirPoints.clicked.connect(self.browsePtsClicked)
        self.parcourirParam.clicked.connect(self.browseParamClicked)
        self.parcourirRes.clicked.connect(self.browseResDirClicked)
        
        # Conncetion du bouton de lancement de calcul
        self.runCalcul.clicked.connect(self.runClicked)
        
        
        # Afficher la fenêtre
        self.show()
        
        
        
    def openWindowResGlobaux(self):
        
        self.windowResGlobaux = windowResGlobaux.UI_ongletResGlobaux()
        self.windowResGlobaux.show()
        
        # try: # Si pas de calcul effectué précédemment
        self.windowResGlobaux.openFile(self.resDirPath.text() + "/results.xml") 
        # except:
            # pass
        
    
    """
    ENSEMBLE DE FONCTION PERMETTANT DE SAISIR DES EMPLACEMENTS DES FICHIERS SUR LES QLineEditDU DU VOLET "CALCUL."
    """
            
    def browseObsClicked(self):
        try:
            file = QtWidgets.QFileDialog().getOpenFileName(None,"Sélection du fichier XML des observations", None, "*.xml")[0]
            self.pathObs.setText(file)
        except:
            return None
    def browsePtsClicked(self):
        try:
            file = QtWidgets.QFileDialog().getOpenFileName(None,"Sélection du fichier XML des points", None, "*.xml")[0]
            self.pathPoints.setText(file)
        except:
            return None
    def browseParamClicked(self):
        try:
            file = QtWidgets.QFileDialog().getOpenFileName(None,"Sélection du fichier XML des paramètres", None, "*.xml")[0]
            self.pathParam.setText(file)
        except:
            return None
    def browseResDirClicked(self):
        try:
            directory = QtWidgets.QFileDialog().getExistingDirectory(None,"Sélection du dossier des résultats")
            self.resDirPath.setText(directory)
        except:
            return None
        
    
    def runClicked(self):
        """
        FONCTION QUI LANCE L'AJUSTEMENT.
        """
        
        # Remettre la progress bar à 0
        self.progressBar.setValue(0)
        
        nomsFichiers = {'fichierXMLCanevas':self.pathObs.text(),
                        'fichierXMLPoints':self.pathPoints.text(), 
                        'fichierXMLParametres':self.pathParam.text(),
                        'fichierXSDCanevas':os.getcwd()+"\\modeleDonnees\\observationsModel.xsd", 
                        'fichierXSDPoints':os.getcwd()+"\\modeleDonnees\\pointsModel.xsd", 
                        'fichierXSDParametres':os.getcwd()+"\\modeleDonnees\\parametersModel.xsd",
                        'dossierResultats': self.resDirPath.text()}
        
        # try: # éviter que le programme s'arrête si il y'a une erreur inexpliquée
        Process = processUtils.Process(nomsFichiers, self.progressBar)
        calculDone = Process.run()
        if calculDone:
            self.openWindowResGlobaux()
            # Remettre la progress bar à 0
            self.progressBar.setValue(100)
            
            
        # except:
            # print('!!! MAJOR PROBLEM IN CALCULATION, PLEASE RETRY OR RESTART THE PROGRAM !!!')
        
        
        
        