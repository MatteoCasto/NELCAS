
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem, QStandardItemModel
import json
import xmltodict
from PyQt5 import uic
import libUtils.processUtils as processUtils
import libUtils.approximatedCoordsUtils as approximatedCoordsUtils
import os
import pyqtgraph as pg
import time


class UI_ongletCoordsApproch(QtWidgets.QMainWindow):
    
    def __init__(self):
        
        super(UI_ongletCoordsApproch, self).__init__()
        # Charger le ui
        uic.loadUi(os.getcwd()+"\\interface\\OngletCoordsApproch.ui", self)
        
        
        # # Connection des boutons de fileDialog
        self.parcourirObs.clicked.connect(self.browseObsClicked)
        self.parcourirPoints.clicked.connect(self.browsePtsClicked)
        self.parcourirRes.clicked.connect(self.browseResDirClicked)
        
        # # Conncetion du bouton de lancement de calcul
        self.runCalcul.clicked.connect(self.runClicked)
        
        
        # Init les pyqtGraph
        self.plotLive.setBackground('w')
        self.plotLive.getPlotItem().hideAxis('bottom')
        self.plotLive.getPlotItem().hideAxis('left')
        self.plotLive.setAspectLocked(True)
        
        # Connection du bouton pour afficher les no de pts
        self.checkBoxNomsPoints.stateChanged.connect(self.plotPointsAtStep)
        
        # Connection au clic de la souris sur le graphe
        # self.plotLive.scene().sigMouseClicked.connect(self.mouse_clicked)
        self.plotLive.scene().sigMouseClicked.connect(self.mouse_clicked)

        
        # Afficher la fenêtre
        self.show()
        
    
    """
    ENSEMBLE DE FONCTION PERMETTANT DE SAISIR DES EMPLACEMENTS DES FICHIERS SUR LES QLineEditDU
    """
            
    def browseObsClicked(self):
        try:
            file = QtWidgets.QFileDialog().getOpenFileName(None,"Sélection du fichier XML des observations", None, "*.xml")[0]
            self.pathObs.setText(file)
        except:
            return None
    def browsePtsClicked(self):
        try:
            file = QtWidgets.QFileDialog().getOpenFileName(None,"Sélection du fichier XML des points connus", None, "*.xml")[0]
            self.pathPoints.setText(file)
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
        FONCTION QUI LANCE LE CALCUL DES COORDONNEES APPROCHEES
        """
        
        nomsFichiers = {'fichierXMLPoints':   self.pathPoints.text(),
                        'fichierXMLCanevas':  self.pathObs.text(),
                        'fichierXSDCanevas':  os.getcwd() +'\\modeleDonnees\\observationsModel.xsd', 
                        'fichierXSDPoints':   os.getcwd() +'\\modeleDonnees\\pointsModel.xsd',
                        'dossierResultats':   self.resDirPath.text(),
                        'residusLimite':      self.spinBoxViLimit.value()}
        
        # Init
        ApproxCoordinates = approximatedCoordsUtils.ApproxCoordinates(nomsFichiers)
        # Uniquement si les 3 contrôles de coh. sont remplis
        if ApproxCoordinates.check1[0] and ApproxCoordinates.check2[0] and ApproxCoordinates.check3[0] :
            
            try: # Si erreur, éviter que le programme s'arrête
        
               # Lancement du calcul de coord. approchées
                ApproxCoordinates.run()
                
                # Export des points XML connus
                ApproxCoordinates.exportPointsXML()
                
                # Export du log des pts si pas erreur
                ApproxCoordinates.exportPointsManquants()
                
                # Historique des steps
                self.historique = ApproxCoordinates.getHistorique()
                
                # Set maximum of Qslider et rendre modifiable, et connecter à la fonction
                stepMaximum = len(self.historique)-1
                self.horizontalSlider.setMaximum(stepMaximum)
                self.horizontalSlider.valueChanged.connect(self.plotPointsAtStep)
                
                # Plot à step=maximum
                self.horizontalSlider.setSliderPosition(stepMaximum)
                self.plotPointsAtStep()
                
                
        
            except:
                print('\n !!! MAJOR PROBLEM IN CALCULATION, PLEASE RETRY OR RESTART THE PROGRAM !!!')
                
                # Export des points XML connus
                ApproxCoordinates.exportPointsXML()
                
                # Export du log des pts si pas erreur
                ApproxCoordinates.exportPointsManquants()
            
            
        
        else:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('COMPLETE VALIDATION ONLY WITH CODE 100 TO 200 SUCCESSFUL')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        
        
        
    def plotPointsAtStep(self):
        """
        Function that display a map with the points from the previous step (blue) and the current points (en rouge).
        This depends on thew QSlider position.
        """
        
        # no de d'étape selon la position du curseur
        step = self.horizontalSlider.value()
        # Si c'est un système local, récupérer la liste des pts communs
        listeCommuns = self.historique[step][2]
        # Set le text des infos
        self.textInfoLog.setText('step : {:d} \n{:s}'.format(step, self.historique[step][0]))
        
        # Vider le plot
        self.plotLive.clear()
        
        
        listePtNamePrec = []
        if step == 0:
            stepPrec = 0
        else:
            stepPrec = step - 1
    
            
            
            
        #### STEP PRECEDENTE EN BLEU 
    
        listeCooElast, listeCooNlast = [], []
        for point in self.historique[stepPrec][1]['points']['point']:
        
            # Uniquement les pts non communs
            if point['pointName'] not in listeCommuns:
                listePtNamePrec.append(point['pointName'])
                listeCooElast.append(float(point['E']))
                listeCooNlast.append(float(point['N']))      
            
                if self.checkBoxNomsPoints.isChecked() :
                    # Set label du pt
                    text = pg.TextItem(text=point['pointName'], color='b')
                    text.setPos(float(point['E']),float(point['N']))
                    self.plotLive.addItem(text)
        
        # Set le style 
        scatter = pg.ScatterPlotItem(
            size=10, brush='b', pen='b')
        # setting data to the scatter plot
        if len(listeCooElast) >0:
            scatter.setData(listeCooElast, listeCooNlast)
            # Add the scatter plot and text
            self.plotLive.addItem(scatter)
            
            
            
        #### PTS COMMUNS EN VERT
    
        listeCooEcommun, listeCooNcommun = [], []
        for point in self.historique[stepPrec][1]['points']['point']:
            
            # Uniquement les pts communs
            if point['pointName'] in listeCommuns:
        
                listePtNamePrec.append(point['pointName'])
                listeCooEcommun.append(float(point['E']))
                listeCooNcommun.append(float(point['N']))      
            
                if self.checkBoxNomsPoints.isChecked() :
                    # Set label du pt
                    text = pg.TextItem(text=point['pointName'], color=(0, 181, 0))
                    text.setPos(float(point['E']),float(point['N']))
                    self.plotLive.addItem(text)
        
        # Set le style 
        scatter = pg.ScatterPlotItem(
            size=12, brush=(0, 181, 0), pen=(0, 181, 0), symbol='t1')
        # setting data to the scatter plot
        if len(listeCooEcommun) >0:
            scatter.setData(listeCooEcommun, listeCooNcommun)
            # Add the scatter plot and text
            self.plotLive.addItem(scatter)
        
        
        
    
        #### STEP COURANTE EN ROUGE

        listeCooE, listeCooN = [], []
        for point in self.historique[step][1]['points']['point']:
            
            if point['pointName'] not in listePtNamePrec:
                
                listeCooE.append(float(point['E']))
                listeCooN.append(float(point['N']))      
            
                if self.checkBoxNomsPoints.isChecked() :
                    # Set label du pt
                    text = pg.TextItem(text=point['pointName'], color='r')
                    text.setPos(float(point['E']),float(point['N']))
                    self.plotLive.addItem(text)
        
        # Set le style 
        scatter = pg.ScatterPlotItem(
            size=10, brush='r', pen='r')
        # setting data to the scatter plot
        if len(listeCooE) >0:
            scatter.setData(listeCooE, listeCooN)
            # Add the scatter plot and text
            self.plotLive.addItem(scatter)
        

    

        # Fitting items in view si step=0
        if step == 0:
            view = self.plotLive.getViewBox()
            view.autoRange()
            

    
    def mouse_clicked(self, evt):
        """
        Function that display the coordinates of the left click of the mouse on the graph
        """
        vb = self.plotLive.plotItem.vb
        scene_coords = evt.scenePos()
        if self.plotLive.sceneBoundingRect().contains(scene_coords):
            mouse_point = vb.mapSceneToView(scene_coords)
            self.coordinatesOfClick.setText('{:0.2f} / {:0.2f}'.format(mouse_point.x(), mouse_point.y()))
            
                
                
    
                
                

        
        
        
        
        
        
        
        
        