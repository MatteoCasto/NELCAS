# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 17:09:09 2022

@author: matteo.casto
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem, QStandardItemModel
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QRectF, QRect
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import xmltodict
from PyQt5 import uic
import os
import copy
import numpy as np
import time






class UI_ongletObs(QtWidgets.QMainWindow):
    
    def __init__(self):
        
        super(UI_ongletObs, self).__init__()
        # Charger le ui
        uic.loadUi(os.getcwd()+"\\interface\\OngletObservations.ui", self)

        # Désactiver le widget principal
        self.centralWidget.setEnabled(False)
        
        # connection bouton de la menu bar
        self.actionNouveau.triggered.connect(self.newFile)
        self.actionOuvrir.triggered.connect(self.openFile)
        self.actionEnregistrer.triggered.connect(self.saveFile)
        self.actionEnregistrer_sous.triggered.connect(self.saveAsFile)
        
        # Connection quand la séléction dans les header (stations, sessions, systèmes, etc.) change
        self.tableWidgetStations.selectionModel().selectionChanged.connect(self.onSelectionStationChanged)
        self.tableWidgetObsPolaires.itemChanged.connect(self.onCellObsPolaireChanged)
        self.tableWidgetSessions.selectionModel().selectionChanged.connect(self.onSelectionSessionChanged)
        self.tableWidgetObsGnss.itemChanged.connect(self.onCellObsGnssChanged)
        self.tableWidgetSystemes.selectionModel().selectionChanged.connect(self.onSelectionSystemsChanged)
        self.tableWidgetObsSysteme.itemChanged.connect(self.onCellObsSystemChanged)
        
        # Resize largeur des colonnes
        header = self.tableWidgetStations.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetObsPolaires.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetSessions.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetObsGnss.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetSystemes.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetObsSysteme.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetMesuresSimples.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetContraintes.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        
        # Connection des boutons de recherche
        self.buttonSearchSta.clicked.connect(lambda: self.searchInQTable(self.tableWidgetStations, self.inputSearchSta, [0]))
        self.buttonSearchPtVis.clicked.connect(lambda: self.searchInQTable(self.tableWidgetObsPolaires, self.inputSearchPtVis, [0]))
        self.buttonSearchSession.clicked.connect(lambda: self.searchInQTable(self.tableWidgetSessions, self.inputSearchSession, [0]))
        self.buttonSearchPtGnss.clicked.connect(lambda: self.searchInQTable(self.tableWidgetObsGnss, self.inputSearchPtGnss, [0]))
        self.buttonSearchSysLoc.clicked.connect(lambda: self.searchInQTable(self.tableWidgetSystemes, self.inputSearchSysLoc, [0]))
        self.buttonSearchPtSysLoc.clicked.connect(lambda: self.searchInQTable(self.tableWidgetObsSysteme, self.inputSearchPtSysLoc, [0]))
        self.buttonSearchPtMes.clicked.connect(lambda: self.searchInQTable(self.tableWidgetMesuresSimples, self.inputSearchPtMes, [0,1]))
        self.buttonSearchPtContr.clicked.connect(lambda: self.searchInQTable(self.tableWidgetContraintes, self.inputSearchPtContr, [1,2,3,4]))
        
        # Connection des boutons "suivants" de rechercher
        self.suivantStation.clicked.connect(lambda: self.onClickSearchNext(self.tableWidgetStations, self.inputSearchSta, [0]))
        self.suivantObsPolaire.clicked.connect(lambda: self.onClickSearchNext(self.tableWidgetObsPolaires, self.inputSearchPtVis, [0]))
        self.suivantSession.clicked.connect(lambda: self.onClickSearchNext(self.tableWidgetSessions, self.inputSearchSession, [0]))
        self.suivantObsGnss.clicked.connect(lambda: self.onClickSearchNext(self.tableWidgetObsGnss, self.inputSearchPtGnss, [0]))
        self.suivantSysLoc.clicked.connect(lambda: self.onClickSearchNext(self.tableWidgetSystemes, self.inputSearchSysLoc, [0]))
        self.suivantPtSysLoc.clicked.connect(lambda: self.onClickSearchNext(self.tableWidgetObsSysteme, self.inputSearchPtSysLoc, [0]))
        self.suivantCote.clicked.connect(lambda: self.onClickSearchNext(self.tableWidgetMesuresSimples, self.inputSearchPtMes, [0,1]))
        self.suivantContr.clicked.connect(lambda: self.onClickSearchNext(self.tableWidgetContraintes, self.inputSearchPtContr, [1,2,3,4]))
        
        
        # Init les pyqtGraph
        self.graphWidgetSysLoc.setBackground('w')
        self.graphWidgetSysLoc.setAspectLocked(True)
        self.graphWidgetSysLoc.setLabel('bottom', 'LY [m]')
        self.graphWidgetSysLoc.setLabel('left', 'LX [m]')
        
        # Init la rechercher précédente comme vide
        self.searchInputLast = ''
        
        
        # Intialiser les listes
        self.listePolaire = []
        self.listeGNSS = []
        self.listeSystemes = []
        self.listeMesSimples = []
        self.listeContr = []
    
        # Afficher la fenêtre
        self.show()
        
        

    
    def newFile(self):
        """
        Génére un fichier d'observation vide XML après avoir cliqué sur "nouveau".
        """

        try:
            # Path d'export
            self.filePath = QtWidgets.QFileDialog().getSaveFileName(None,"Save", None, "*.xml")[0]
            
            # Générer le fichier vide avec la fonction d'export
            self.dictObs = {'network':{}}
            dictExportEmpty = xmltodict.unparse(self.dictObs, pretty=True)
            with open(self.filePath, 'w') as f:
                f.write(dictExportEmpty) 
                
            # vider tous les QTable
            self.tableWidgetStations.setRowCount(0)
            self.tableWidgetObsPolaires.setRowCount(0)
            self.tableWidgetSessions.setRowCount(0)
            self.tableWidgetObsGnss.setRowCount(0)
            self.tableWidgetSystemes.setRowCount(0)
            self.tableWidgetObsSysteme.setRowCount(0)
            self.tableWidgetMesuresSimples.setRowCount(0)
            self.tableWidgetContraintes.setRowCount(0)
            
            # Activer le tabwidget
            self.centralWidget.setEnabled(True)
            # Activer les boutons save et save as
            self.actionEnregistrer.setEnabled(True)
            self.actionEnregistrer_sous.setEnabled(True)
            
            # Set le nom du fichier lu
            self.setWindowTitle('Observations  -  {:s}  -  enregistré'.format(self.filePath))
            time.sleep(0.5)
            self.setWindowTitle('Observations  -  {:s}'.format(self.filePath))
    
        except:
            return None

        
    def saveFile(self):
        """
        Sauvegarde le fichier et remplace celui qui a été importé avec le même nom. S'active après avoir cliqué sur "Enregistrer".
        """
        try:
            # Remplace le fichier courant avec sa nouvelle version de lui-même.
            self.exportAll()
            # Set le nom du fichier lu
            self.setWindowTitle('Observations  -  {:s}  -  enregistré'.format(self.filePath))
            time.sleep(0.5)
            self.setWindowTitle('Observations  -  {:s}'.format(self.filePath))
        except:
            return None
        
    
    def saveAsFile(self):
        """
        Sauvegarde le fichier sous un nouvel emplacement. S'active après avoir cliqué sur "Enregistrer sous".
        """
        
        # Path du nouveau fichier
        try:
            self.filePath = QtWidgets.QFileDialog().getSaveFileName(None,"Save as", None, "*.xml")[0]
            
            # Génère un nouveau fichier avec sa nouvelle version de lui-même.
            self.exportAll()
            
            # Set le nom du fichier lu
            self.setWindowTitle('Observations  -  {:s}  -  enregistré'.format(self.filePath))
            time.sleep(0.5)
            self.setWindowTitle('Observations  -  {:s}'.format(self.filePath))
        except:
            return None
        
    

    def openFile(self):
        """
        Fonction d'import du fichier XML des observations après avoir cliqué sur "ourvrir".
        """
        # import du fichier texte XML
        try:
            self.filePath = QtWidgets.QFileDialog().getOpenFileName(None,"Open", None, "*.xml")[0]
            with open(self.filePath) as f:
                self.dictObs = xmltodict.parse(f.read())
                
                
            # vider tous les QTable
            self.tableWidgetStations.setRowCount(0)
            self.tableWidgetObsPolaires.setRowCount(0)
            self.tableWidgetSessions.setRowCount(0)
            self.tableWidgetObsGnss.setRowCount(0)
            self.tableWidgetSystemes.setRowCount(0)
            self.tableWidgetObsSysteme.setRowCount(0)
            self.tableWidgetMesuresSimples.setRowCount(0)
            self.tableWidgetContraintes.setRowCount(0)
            
            # import des obs.
            self.importAll()
            
            # Set le nom du fichier lu
            self.setWindowTitle('Observations  -  {:s}'.format(self.filePath))
            # Activer les boutons save et save as
            self.actionEnregistrer.setEnabled(True)
            self.actionEnregistrer_sous.setEnabled(True)
            
            # Activer le tabwidget
            self.centralWidget.setEnabled(True)
        except:
            return None
        
    
    
    
    
    
    
    
    def importAll(self):
        """
        Fonction qui va importer toutes les mesures d'un fichier XML.
        """
        # -----------------------------
        #### POLAIRE 
        # -----------------------------
        
        #### ^---- Stations
        
        # Initialisation QTableWidget des stations
        if "polar" in self.dictObs['network'].keys():
            
            self.listePolaire = []
            # Si une seule balise, mettre sous forme de liste
            liste =  self.dictObs['network']['polar']['station'] if type(self.dictObs['network']['polar']['station']) is list else [self.dictObs['network']['polar']['station']]
            for rowSta, station in enumerate(liste):

                # Stockage de la station dans un dict
                station.update({'rowSta':rowSta}) # ajout du no de row
                self.listePolaire.append(station)
            
            # Update Data to table 
            # Nombre de lignes de stations
            self.tableWidgetStations.setRowCount(len(self.listePolaire))
            for data in self.listePolaire:
                rowSta = data['rowSta']
                
                self.tableWidgetStations.setItem(rowSta, 0, QtWidgets.QTableWidgetItem(data['stationName']))
                self.tableWidgetStations.setItem(rowSta, 1, QtWidgets.QTableWidgetItem(data['stationData']['I']))
                self.tableWidgetStations.setItem(rowSta, 2, QtWidgets.QTableWidgetItem(data['stationData']['stationCentring']['planiStdDev']['mm']))
                self.tableWidgetStations.setItem(rowSta, 3, QtWidgets.QTableWidgetItem(data['stationData']['stationCentring']['altiStdDev']['mm']))
                self.tableWidgetStations.setItem(rowSta, 4, QtWidgets.QTableWidgetItem(data['stationData']['distanceGroup']))
                self.tableWidgetStations.setItem(rowSta, 5, QtWidgets.QTableWidgetItem(data['stationData']['directionGroup']))
                self.tableWidgetStations.setItem(rowSta, 6, QtWidgets.QTableWidgetItem(data['stationData']['centringGroup']))

            
            
        
        # -----------------------------
        #### GNSS 
        # -----------------------------
        
        #### ^---- Sessions
        # Initialisation QTableWidget des sessions
        if "gnss" in self.dictObs['network'].keys():

            self.listeGNSS = []
            # Si une seule balise, mettre sous forme de liste
            liste =  self.dictObs['network']['gnss']['session'] if type(self.dictObs['network']['gnss']['session']) is list else [self.dictObs['network']['gnss']['session']]
            for rowSession, session in enumerate(liste):
                
                # Stockage de la station dans un dict
                session.update({'rowSession':rowSession}) # ajout du no de row
                self.listeGNSS.append(session)
            
            # Update Data to table 
            # Nombre de lignes de stations
            self.tableWidgetSessions.setRowCount(len(self.listeGNSS))
            for data in self.listeGNSS:
                row = data['rowSession']
                self.tableWidgetSessions.setItem(row, 0, QtWidgets.QTableWidgetItem(data['sessionName']))
                self.tableWidgetSessions.setItem(row, 1, QtWidgets.QTableWidgetItem(data['gnssGroup']))
                
                
                
        # -----------------------------
        #### SYSTEMES LOCAUX 
        # -----------------------------
        
        #### ^---- Systèmes
        # Initialisation QTableWidget des systèmes
        if "localSystems" in self.dictObs['network'].keys():

            self.listeSystemes = []
            # Si une seule balise, mettre sous forme de liste
            liste =  self.dictObs['network']['localSystems']['localSystem'] if type(self.dictObs['network']['localSystems']['localSystem']) is list else [self.dictObs['network']['localSystems']['localSystem']]
            for rowSysteme, systeme in enumerate(liste):
                
                # Stockage de la station dans un dict
                systeme.update({'rowSysteme':rowSysteme}) # ajout du no de row
                self.listeSystemes.append(systeme)
            
            # Update Data to table 
            # Nombre de lignes de stations
            self.tableWidgetSystemes.setRowCount(len(self.listeSystemes))
            for data in self.listeSystemes:
                row = data['rowSysteme']
                self.tableWidgetSystemes.setItem(row, 0, QtWidgets.QTableWidgetItem(data['localSystemName']))
                self.tableWidgetSystemes.setItem(row, 1, QtWidgets.QTableWidgetItem(data['localSystemGroup']))
                
                
                
        
        # -----------------------------
        #### MESURES SIMPLES
        # -----------------------------
        
        # Initialisation QTableWidget des stations
        if "simpleMeasures" in self.dictObs['network'].keys():

            # Si une seule balise, mettre sous forme de liste
            liste =  self.dictObs['network']['simpleMeasures']['simpleMeasure'] if type(self.dictObs['network']['simpleMeasures']['simpleMeasure']) is list else [self.dictObs['network']['simpleMeasures']['simpleMeasure']]
            self.tableWidgetMesuresSimples.setRowCount(len(liste))
            for row, mesure in enumerate(liste):
                
                # Update QTable avec la data importée
                self.tableWidgetMesuresSimples.setItem(row, 0, QtWidgets.QTableWidgetItem(mesure['measure']['pointName1']))
                self.tableWidgetMesuresSimples.setItem(row, 1, QtWidgets.QTableWidgetItem(mesure['measure']['pointName2']))
                self.tableWidgetMesuresSimples.setItem(row, 2, QtWidgets.QTableWidgetItem(mesure['simpleMeasureGroup']))
                self.tableWidgetMesuresSimples.setItem(row, 3, QtWidgets.QTableWidgetItem(mesure['measure']['DP']['value']))
                self.tableWidgetMesuresSimples.setItem(row, 4, QtWidgets.QTableWidgetItem(mesure['measure']['DP']['stdDev']['mm']))
                
                # Checkbox écarté ou non
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                if mesure['measure']['DP']['discarded'] == 'true':
                    item.setCheckState(Qt.CheckState.Checked)
                else: # Si pas = 'true', alors pas écarté
                    item.setCheckState(Qt.CheckState.Unchecked)
                
                self.tableWidgetMesuresSimples.setItem(row, 5, item)
                
                
                
            
        # -----------------------------
        #### CONTRAINTES GEOMETRIQUES
        # -----------------------------
        
        # Initialisation QTableWidget des stations
        if "constraints" in self.dictObs['network'].keys():

            # Si une seule balise, mettre sous forme de liste
            liste =  self.dictObs['network']['constraints']['constraint'] if type(self.dictObs['network']['constraints']['constraint']) is list else [self.dictObs['network']['constraints']['constraint']]
            self.tableWidgetContraintes.setRowCount(len(liste))
            for row, contr in enumerate(liste):
                
                # Nom de point selon le role (A,B, C ou P)
                noPtC = None  # Initlisation sans C, (=vide, donc pas importé, ni exporté)
                for pt in contr['point']:
                    if pt['pointTypeInConstraint'] == "A":
                        noPtA = pt['pointName']
                    if pt['pointTypeInConstraint'] == "B":
                        noPtB = pt['pointName']
                    if pt['pointTypeInConstraint'] == "C":
                        noPtC = pt['pointName']
                    if pt['pointTypeInConstraint'] == "P":
                        noPtP = pt['pointName']
                # valeur vide si pas de C
                if noPtC == None:
                    noPtC = ''
                    
                # Update QTable avec la data importée
                # Liste de choix des types de contraintes
                choiceList = QtWidgets.QComboBox()
                # choiceList.setStyleSheet('background-color: white;') # couleur de fond
                choiceList.addItem('alignment')
                choiceList.addItem('perpendicular')
                try: # si le type n'exsite pas, ne rien ajouter
                    choiceList.setCurrentText(contr['constraintType'])
                    self.tableWidgetContraintes.setCellWidget(row, 0, choiceList) # Ajout du widget QComboBox
                except:
                    pass
                self.tableWidgetContraintes.setItem(row, 1, QtWidgets.QTableWidgetItem(noPtA))
                self.tableWidgetContraintes.setItem(row, 2, QtWidgets.QTableWidgetItem(noPtB))
                self.tableWidgetContraintes.setItem(row, 3, QtWidgets.QTableWidgetItem(noPtC))
                self.tableWidgetContraintes.setItem(row, 4, QtWidgets.QTableWidgetItem(noPtP))
                self.tableWidgetContraintes.setItem(row, 5, QtWidgets.QTableWidgetItem(contr['dm1']['value']))
                
                # Checkbox écarté ou non
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                if contr['discarded'] == 'true':
                    item.setCheckState(Qt.CheckState.Checked)
                else: # Si pas = 'true', alors pas écarté
                    item.setCheckState(Qt.CheckState.Unchecked)
                
                self.tableWidgetContraintes.setItem(row, 6, item)

        
        
        
                
                
        
    def exportAll(self):
        """
        Fonction d'export des observations après avoir cliqué sur "save as".
        """

        # Initialisation du dictionnaire d'export
        dictExportObs = {'network':{}}
        
        #### POLAIRE
        
        # MAJ la data en fonction du QTable (avec ou sans modif.)
        copyListePolaire = copy.deepcopy(self.listePolaire) # deep copy pour récupérer les observations
        self.listePolaire = [] # Vider la liste
        nRowsStations = self.tableWidgetStations.rowCount()
        for rowSta in range(0,nRowsStations):
            
            # Attribution (avec condition si vide == '')
            stationName = self.tableWidgetStations.item(rowSta,0).text() if self.tableWidgetStations.item(rowSta,0) is not None else ''
            I = self.tableWidgetStations.item(rowSta,1).text() if self.tableWidgetStations.item(rowSta,1) is not None else ''
            sCentStaPlani = self.tableWidgetStations.item(rowSta,2).text() if self.tableWidgetStations.item(rowSta,2) is not None else ''
            sCentStaAlti= self.tableWidgetStations.item(rowSta,3).text() if self.tableWidgetStations.item(rowSta,3) is not None else ''
            groupeDist = self.tableWidgetStations.item(rowSta,4).text() if self.tableWidgetStations.item(rowSta,4) is not None else ''
            groupeDir = self.tableWidgetStations.item(rowSta,5).text() if self.tableWidgetStations.item(rowSta,5) is not None else ''
            groupeCent = self.tableWidgetStations.item(rowSta,6).text() if self.tableWidgetStations.item(rowSta,6) is not None else ''
            
            # Récupérer les obs. acutelles 
            for station in copyListePolaire:
                if station['rowSta'] == rowSta:
                    measureListe = station['stationData']['measure']
                    station['rowSta'] = rowSta
                    break
            
            # Sous dictionnairte par station
            sousDict = {}
            sousDict.update({'stationName':stationName})
            sousDict.update({'stationData':{'I':I,
                                            'stationCentring':{'planiStdDev':{'mm':sCentStaPlani},
                                                              'altiStdDev':{'mm':sCentStaAlti}
                                                              },
                                            'distanceGroup': groupeDist,
                                            'directionGroup': groupeDir,
                                            'centringGroup': groupeCent,
                                            'measure': measureListe # EN LISTE !!
                                            }
                                })
            self.listePolaire.append(sousDict)
            
        # Ajout au dict final pour export
        if len(self.listePolaire) > 0: # Il y'a au moins une station
            dictExportObs['network'].update({'polar':{
                                             'station':self.listePolaire}}) 
            self.listePolaire = copyListePolaire # Garder rowSta si on refait un export (sinon génère une erreur)
        
            
            
            
            
        #### GNSS
        
        # MAJ la data en fonction du QTable (avec ou sans modif.)
        copyListeGNSS = copy.deepcopy(self.listeGNSS) # deep copy pour récupérer les observations
        self.listeGNSS = [] # Vider la liste
        nRowsSessions = self.tableWidgetSessions.rowCount()
        for rowSession in range(0,nRowsSessions):
            
            # Attribution (avec condition si vide == '')
            sessionName = self.tableWidgetSessions.item(rowSession,0).text() if self.tableWidgetSessions.item(rowSession,0) is not None else ''
            gnssGroup = self.tableWidgetSessions.item(rowSession,1).text() if self.tableWidgetSessions.item(rowSession,1) is not None else ''
            
            # Récupérer les obs. acutelles 
            for session in copyListeGNSS:
                if session['rowSession'] == rowSession:
                    measureListe = session['measure']
                    session['rowSession'] = rowSession
                    break
                    
            
            # Sous dictionnairte par session
            sousDict = {}
            sousDict.update({'sessionName':sessionName}) 
            sousDict.update({'gnssGroup':gnssGroup})
            sousDict.update({'measure':measureListe}) # LISTE !!
            self.listeGNSS.append(sousDict)
    
        # Ajout au dict final pour export
        if len(self.listeGNSS) > 0: # Il y'a au moins une session
            dictExportObs['network'].update({'gnss':{
                                             'session':self.listeGNSS}}) 
            self.listeGNSS = copyListeGNSS # Garder rowSta si on refait un export (sinon génère une erreur)
            
            
            
        #### SYSTEMES LOCAUX
        
        # MAJ la data en fonction du QTable (avec ou sans modif.)
        copyListeSystemes = copy.deepcopy(self.listeSystemes) # deep copy pour récupérer les observations
        self.listeSystemes = [] # Vider la liste
        nRowsSystemes = self.tableWidgetSystemes.rowCount()
        for rowSysteme in range(0,nRowsSystemes):
            
            # Attribution (avec condition si vide == '')
            systemName = self.tableWidgetSystemes.item(rowSysteme,0).text() if self.tableWidgetSystemes.item(rowSysteme,0) is not None else ''
            systemGroup = self.tableWidgetSystemes.item(rowSysteme,1).text() if self.tableWidgetSystemes.item(rowSysteme,1) is not None else ''
            
            # Récupérer les obs. acutelles 
            for systeme in copyListeSystemes:
                if systeme['rowSysteme'] == rowSysteme:
                    measureListe = systeme['measure']
                    systeme['rowSysteme'] = rowSysteme
                    break
                    
            
            # Sous dictionnairte par système
            sousDict = {}
            sousDict.update({'localSystemName':systemName}) 
            sousDict.update({'localSystemGroup':systemGroup})
            sousDict.update({'measure':measureListe}) # LISTE !!
            self.listeSystemes.append(sousDict)
    
        # Ajout au dict final pour export
        if len(self.listeSystemes) > 0: # Il y'a au moins un système
            dictExportObs['network'].update({'localSystems':{
                                             'localSystem':self.listeSystemes}}) 
            self.listeSystemes = copyListeSystemes
            


        #### MESURES SIMPLES
        nRowsMes = self.tableWidgetMesuresSimples.rowCount()
        self.listeMesSimples = [] # Vider les data pour les remplacement par les valeurs de la QTable
        for rowMes in range(0,nRowsMes):
            
            # Attribution (avec condition si vide == '')
            pointName1 = self.tableWidgetMesuresSimples.item(rowMes, 0).text() if self.tableWidgetMesuresSimples.item(rowMes,0) is not None else ''
            pointName2 = self.tableWidgetMesuresSimples.item(rowMes, 1).text() if self.tableWidgetMesuresSimples.item(rowMes,1) is not None else ''
            mesGroup = self.tableWidgetMesuresSimples.item(rowMes, 2).text() if self.tableWidgetMesuresSimples.item(rowMes, 2) is not None else ''
            DPvalue = self.tableWidgetMesuresSimples.item(rowMes, 3).text() if self.tableWidgetMesuresSimples.item(rowMes, 3) is not None else ''
            DPstdDev = self.tableWidgetMesuresSimples.item(rowMes, 4).text() if self.tableWidgetMesuresSimples.item(rowMes, 4) is not None else ''
            # Case cochée ou non
            if self.tableWidgetMesuresSimples.item(rowMes,5).checkState() == 2:
                DPdiscarded = 'true'
            else:
                DPdiscarded = '' 
            
            
            # Sous dictionnairte par mesure
            sousDict = {}
            sousDict.update({'simpleMeasureGroup':mesGroup})
            sousDict.update({'measure':{'pointName1':pointName1,
                                        'pointName2':pointName2,
                                        'DP':{'stdDev':{'mm':DPstdDev},
                                              'value':DPvalue,
                                              'discarded':DPdiscarded}}}) 
            self.listeMesSimples.append(sousDict)
        # Ajout au dict final pour export
        if len(self.listeMesSimples) > 0: # Il y'a au moins une mesure simple
            dictExportObs['network'].update({'simpleMeasures':{
                                             'simpleMeasure':self.listeMesSimples}}) 
            
            
        
        #### CONTRAINTES GEOMETRIQUES
        nRowsContr = self.tableWidgetContraintes.rowCount()
        self.listeContr = [] # Vider les data pour les remplacement par les valeurs de la QTable
        for rowContr in range(0,nRowsContr):
            
            # Attribution (avec condition si vide == '')
            # typeContr = self.tableWidgetContraintes.item(rowContr, 0).text() if self.tableWidgetContraintes.item(rowContr,0) is not None else ''
            typeContr = self.tableWidgetContraintes.cellWidget(rowContr, 0).currentText()
            pointNameA = self.tableWidgetContraintes.item(rowContr, 1).text() if self.tableWidgetContraintes.item(rowContr,1) is not None else ''
            pointNameB = self.tableWidgetContraintes.item(rowContr, 2).text() if self.tableWidgetContraintes.item(rowContr, 2) is not None else ''
            pointNameC = self.tableWidgetContraintes.item(rowContr, 3).text() if self.tableWidgetContraintes.item(rowContr, 3) is not None else ''
            pointNameP = self.tableWidgetContraintes.item(rowContr, 4).text() if self.tableWidgetContraintes.item(rowContr, 4) is not None else ''
            dm1 = self.tableWidgetContraintes.item(rowContr, 5).text() if self.tableWidgetContraintes.item(rowContr, 5) is not None else ''
            # Case cochée ou non
            if self.tableWidgetContraintes.item(rowContr,6).checkState() == 2:
                discarded = 'true'
            else:
                discarded = ''
            
            # si le nom point C est vide, alors uniquement A,B et P (segment)
            if pointNameC == '':
                # Sous dictionnairte par contrainte
                sousDict = {'constraintType': typeContr,
                            'point':[{'pointName':pointNameA,
                                      'pointTypeInConstraint':'A'},
                                     {'pointName':pointNameB,
                                      'pointTypeInConstraint':'B'},
                                     {'pointName':pointNameP,
                                      'pointTypeInConstraint':'P'}
                                     ],
                            'discarded': discarded,
                            'dm1':{'value':dm1}
                            }
                
            # si le nom point C a une valeur, alors A,B,C et P (arc de cercle)
            else:
                # Sous dictionnairte par contrainte
                sousDict = {'constraintType': typeContr,
                            'point':[{'pointName':pointNameA,
                                      'pointTypeInConstraint':'A'},
                                     {'pointName':pointNameB,
                                      'pointTypeInConstraint':'B'},
                                     {'pointName':pointNameC,
                                      'pointTypeInConstraint':'C'},
                                     {'pointName':pointNameP,
                                      'pointTypeInConstraint':'P'}
                                     ],
                            'discarded': discarded,
                            'dm1':{'value':dm1}
                            }

            # Ajout de chaque contrainte
            self.listeContr.append(sousDict)
        # Ajout au dict final pour export
        if len(self.listeContr) > 0: # Il y'a au moins une mesure simple
            dictExportObs['network'].update({'constraints':{
                                             'constraint':self.listeContr}}) 






        # Export du fichier texte XML total des observations
        dictExportObsString = xmltodict.unparse(dictExportObs, pretty=True)
        with open(self.filePath, 'w') as f:
            f.write(dictExportObsString)      

        
                
                
            
                
                
        
                   
  
    def onSelectionStationChanged(self):
        """
        Fonction qui va déclencher l'update des observations polaires par rappport à la station sélectionnée (en bleu).
        Va chercher les données dans self.dictRowsStation.
        """
        currentRowStation = self.tableWidgetStations.currentRow() # station séléctionnée (cliquée et marquée en bleue)  
        
        # Le temps de la fonction qui va refresh les obs. on désactive la fonction qui va déclencher la MAJ des obs dans la data
        self.tableWidgetObsPolaires.itemChanged.disconnect(self.onCellObsPolaireChanged)
        
        # Parcourir les obs. de la station sélectionnée
        for station in self.listePolaire:
            rowSta = station['rowSta']
        
            if rowSta == currentRowStation: # Afficher uniquement les obs. par rapport à une station (selectionnée en bleu)
                
                # en liste si une seule mesure
                station['stationData']['measure'] = station['stationData']['measure'] if type(station['stationData']['measure']) is list else [station['stationData']['measure']]
                
                # On set les item de la Table
                self.tableWidgetObsPolaires.setRowCount(len(station['stationData']['measure'])) # Nombre de lignes d'obs. liées à la station selectionnée

                # en liste si une seule mesure
                station['stationData']['measure'] = station['stationData']['measure'] if type(station['stationData']['measure']) is list else [station['stationData']['measure']]
                for rowObs, obs in enumerate(station['stationData']['measure']):
                    
                    # Nom de point
                    self.tableWidgetObsPolaires.setItem(rowObs, 0, QtWidgets.QTableWidgetItem(obs['pointName']))
                    # RI
                    self.tableWidgetObsPolaires.setItem(rowObs, 1, QtWidgets.QTableWidgetItem(obs['RI']['value']))
                    self.tableWidgetObsPolaires.setItem(rowObs, 2, QtWidgets.QTableWidgetItem(obs['RI']['stdDev']['cc']))
                    # Checkbox écarté ou non
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    if obs['RI']['discarded'] == 'true':
                        item.setCheckState(Qt.CheckState.Checked)
                    else: # Si pas = 'true', alors pas écarté
                        item.setCheckState(Qt.CheckState.Unchecked)
                    self.tableWidgetObsPolaires.setItem(rowObs, 3, item)
                    
                    # DS
                    self.tableWidgetObsPolaires.setItem(rowObs, 4, QtWidgets.QTableWidgetItem(obs['DS']['value']))
                    # sigma distance composé mm+ppm
                    self.tableWidgetObsPolaires.setItem(rowObs, 5, QtWidgets.QTableWidgetItem(obs['DS']['stdDev']['mm']))
                    self.tableWidgetObsPolaires.setItem(rowObs, 6, QtWidgets.QTableWidgetItem(obs['DS']['stdDev']['ppm'])) 
                    # Checkbox écarté ou non
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    if obs['DS']['discarded'] == 'true':
                        item.setCheckState(Qt.CheckState.Checked)
                    else: # Si pas = 'true', alors pas écarté
                        item.setCheckState(Qt.CheckState.Unchecked)
                    self.tableWidgetObsPolaires.setItem(rowObs, 7, item)
                    
                    # ZD
                    self.tableWidgetObsPolaires.setItem(rowObs, 8, QtWidgets.QTableWidgetItem(obs['ZD']['value']))
                    self.tableWidgetObsPolaires.setItem(rowObs, 9, QtWidgets.QTableWidgetItem(obs['ZD']['stdDev']['cc']))
                    # Checkbox écarté ou non
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    if obs['ZD']['discarded'] == 'true':
                        item.setCheckState(Qt.CheckState.Checked)
                    else: # Si pas = 'true', alors pas écarté
                        item.setCheckState(Qt.CheckState.Unchecked)
                    self.tableWidgetObsPolaires.setItem(rowObs, 10, item)
                    # divers
                    self.tableWidgetObsPolaires.setItem(rowObs, 11, QtWidgets.QTableWidgetItem(obs['S']['value']))
                    self.tableWidgetObsPolaires.setItem(rowObs, 12, QtWidgets.QTableWidgetItem(obs['dm1']['value']))
                    self.tableWidgetObsPolaires.setItem(rowObs, 13, QtWidgets.QTableWidgetItem(obs['dm2']['value']))
                    self.tableWidgetObsPolaires.setItem(rowObs, 14, QtWidgets.QTableWidgetItem(obs['targetCentring']['planiStdDev']['mm']))
                    self.tableWidgetObsPolaires.setItem(rowObs, 15, QtWidgets.QTableWidgetItem(obs['targetCentring']['altiStdDev']['mm']))
                
        self.tableWidgetObsPolaires.itemChanged.connect(self.onCellObsPolaireChanged)
        
        
        
                    
        
        
    def onSelectionSessionChanged(self):
        """
        Fonction qui va mettre à jour le tableau des observations quand une session sera selectionnée.
        """
        
        # Get la row courante selectionnée (en bleu).
        currentRowSession = self.tableWidgetSessions.currentRow()
        # Déconnecter la MAJ des obs (Table to data) car trop prenant en temps et ne sert à rien. Réactivation à la fin de la cette fonction.
        self.tableWidgetObsGnss.itemChanged.disconnect(self.onCellObsGnssChanged)
        
        # Parcourir les obs. de la session sélectionnée
        for session in self.listeGNSS:
            if session['rowSession'] == currentRowSession:
                
                # en liste si une seule mesure
                session['measure'] = session['measure'] if type(session['measure']) is list else [session['measure']]
                
                # On set les item de la Table
                self.tableWidgetObsGnss.setRowCount(len(session['measure'])) # Nombre de lignes d'obs. liées à la ligne selectionnée
                
                for rowObs, obs in enumerate(session['measure']):

                    self.tableWidgetObsGnss.setItem(rowObs, 0, QtWidgets.QTableWidgetItem(obs['pointName']))
                    self.tableWidgetObsGnss.setItem(rowObs, 1, QtWidgets.QTableWidgetItem(obs['LY']['value']))
                    self.tableWidgetObsGnss.setItem(rowObs, 2, QtWidgets.QTableWidgetItem(obs['LY']['stdDev']['mm']))
                    # Checkbox écarté ou non
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    if obs['LY']['discarded'] == 'true':
                        item.setCheckState(Qt.CheckState.Checked)
                    else: # Si pas = 'true', alors pas écarté
                        item.setCheckState(Qt.CheckState.Unchecked)
                    self.tableWidgetObsGnss.setItem(rowObs, 3, item)
                    self.tableWidgetObsGnss.setItem(rowObs, 4, QtWidgets.QTableWidgetItem(obs['LX']['value']))
                    self.tableWidgetObsGnss.setItem(rowObs, 5, QtWidgets.QTableWidgetItem(obs['LX']['stdDev']['mm']))
                    # Checkbox écarté ou non
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    if obs['LX']['discarded'] == 'true':
                        item.setCheckState(Qt.CheckState.Checked)
                    else: # Si pas = 'true', alors pas écarté
                        item.setCheckState(Qt.CheckState.Unchecked)
                    self.tableWidgetObsGnss.setItem(rowObs, 6, item)
                    
                    # Si il y'a bien LH
                    if 'LH' in obs.keys():
                        self.tableWidgetObsGnss.setItem(rowObs, 7, QtWidgets.QTableWidgetItem(obs['LH']['value']))
                        self.tableWidgetObsGnss.setItem(rowObs, 8, QtWidgets.QTableWidgetItem(obs['LH']['stdDev']['mm']))
                        # Checkbox écarté ou non
                        item = QtWidgets.QTableWidgetItem()
                        item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                        if obs['LH']['discarded'] == 'true':
                            item.setCheckState(Qt.CheckState.Checked)
                        else: # Si pas = 'true', alors pas écarté
                            item.setCheckState(Qt.CheckState.Unchecked)
                        self.tableWidgetObsGnss.setItem(rowObs, 9, item)      
                    else: # sinon vide
                        self.tableWidgetObsGnss.setItem(rowObs, 7, QtWidgets.QTableWidgetItem(''))
                        self.tableWidgetObsGnss.setItem(rowObs, 8, QtWidgets.QTableWidgetItem(''))
                        # Checkbox écarté cochée si pas de LH
                        item = QtWidgets.QTableWidgetItem()
                        item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                        item.setCheckState(Qt.CheckState.Unchecked)
                        self.tableWidgetObsGnss.setItem(rowObs, 9, item)    
                    

        self.tableWidgetObsGnss.itemChanged.connect(self.onCellObsGnssChanged)
        
        
        
    
    def onSelectionSystemsChanged(self):
        """
        Fonction qui va mettre à jour le tableau des observations quand un système sera selectionné.
        """
        
        # Get la row courante selectionnée (en bleu).
        currentRowSysteme = self.tableWidgetSystemes.currentRow()
        # Déconnecter la MAJ des obs (Table to data) car trop prenant en temps et ne sert à rien. Réactivation à la fin de la cette fonction.
        self.tableWidgetObsSysteme.itemChanged.disconnect(self.onCellObsSystemChanged)
        
        # Parcourir les obs. du système sélectionnée
        for systeme in self.listeSystemes:
            if systeme['rowSysteme'] == currentRowSysteme:
                
                # en liste si une seule mesure
                systeme['measure'] = systeme['measure'] if type(systeme['measure']) is list else [systeme['measure']]
                
                # On set les item de la Table
                self.tableWidgetObsSysteme.setRowCount(len(systeme['measure'])) # Nombre de lignes d'obs. liées à la ligne selectionnée
                
                for rowObs, obs in enumerate(systeme['measure']):

                    self.tableWidgetObsSysteme.setItem(rowObs, 0, QtWidgets.QTableWidgetItem(obs['pointName']))
                    self.tableWidgetObsSysteme.setItem(rowObs, 1, QtWidgets.QTableWidgetItem(obs['LY']['value']))
                    self.tableWidgetObsSysteme.setItem(rowObs, 2, QtWidgets.QTableWidgetItem(obs['LY']['stdDev']['mm']))
                    # Checkbox écarté ou non
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    if obs['LY']['discarded'] == 'true':
                        item.setCheckState(Qt.CheckState.Checked)
                    else: # Si pas = 'true', alors pas écarté
                        item.setCheckState(Qt.CheckState.Unchecked)
                    self.tableWidgetObsSysteme.setItem(rowObs, 3, item)
                    self.tableWidgetObsSysteme.setItem(rowObs, 4, QtWidgets.QTableWidgetItem(obs['LX']['value']))
                    self.tableWidgetObsSysteme.setItem(rowObs, 5, QtWidgets.QTableWidgetItem(obs['LX']['stdDev']['mm']))
                    # Checkbox écarté ou non
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    if obs['LX']['discarded'] == 'true':
                        item.setCheckState(Qt.CheckState.Checked)
                    else: # Si pas = 'true', alors pas écarté
                        item.setCheckState(Qt.CheckState.Unchecked)
                    self.tableWidgetObsSysteme.setItem(rowObs, 6, item)
                    

        self.tableWidgetObsSysteme.itemChanged.connect(self.onCellObsSystemChanged)
        
        # Dessiner le plan du système local
        self.drawPointsSysLoc()
    




    def onCellObsPolaireChanged(self):
        """
        Fonction s'activant après une modification de cellule dans la QTable des obs. par station.
        Met à jour la liste des obs. pour la station courante (sélectionnée) dans self.listePolaire.
        Evite les MAJ quant les observation chargent (après sélection d'une station).
        """
   
        # Récupération d'éléments QTable courants
        rowSta = self.tableWidgetStations.currentRow()
        nRowsObs = self.tableWidgetObsPolaires.rowCount()
        
        # MAJ de la data selon QTable
        for station in self.listePolaire:
            if station['rowSta'] == rowSta:
                
                # Vider les measures
                station['stationData']['measure'] = []  
                for rowObs in range(0,nRowsObs):
                    
                    # Récupération des éléments
                    pointName = self.tableWidgetObsPolaires.item(rowObs,0).text() if self.tableWidgetObsPolaires.item(rowObs,0) is not None else ''
                    
                    RIvalue = self.tableWidgetObsPolaires.item(rowObs,1).text() if self.tableWidgetObsPolaires.item(rowObs,1) is not None else ''
                    RIstdDev = self.tableWidgetObsPolaires.item(rowObs,2).text() if self.tableWidgetObsPolaires.item(rowObs,2) is not None else ''
                    # Case cochée ou non
                    if self.tableWidgetObsPolaires.item(rowObs,3).checkState() == 2:
                        RIdiscarded = 'true'
                    else:
                        RIdiscarded = ''
                    
                    
                    DSvalue = self.tableWidgetObsPolaires.item(rowObs,4).text() if self.tableWidgetObsPolaires.item(rowObs,4) is not None else ''
                    DSstdDevMm = self.tableWidgetObsPolaires.item(rowObs,5).text() if self.tableWidgetObsPolaires.item(rowObs,5) is not None else ''
                    DSstdDevPpm = self.tableWidgetObsPolaires.item(rowObs,6).text() if self.tableWidgetObsPolaires.item(rowObs,6) is not None else ''
                    # Case cochée ou non
                    if self.tableWidgetObsPolaires.item(rowObs,7).checkState() == 2:
                        DSdiscarded = 'true'
                    else:
                        DSdiscarded = ''
                    
                    ZDvalue = self.tableWidgetObsPolaires.item(rowObs,8).text() if self.tableWidgetObsPolaires.item(rowObs,8) is not None else ''
                    ZDstdDev = self.tableWidgetObsPolaires.item(rowObs,9).text() if self.tableWidgetObsPolaires.item(rowObs,9) is not None else ''
                    # Case cochée ou non
                    if self.tableWidgetObsPolaires.item(rowObs,10).checkState() == 2:
                        ZDdiscarded = 'true'
                    else:
                        ZDdiscarded = ''
                    
                    S = self.tableWidgetObsPolaires.item(rowObs,11).text() if self.tableWidgetObsPolaires.item(rowObs,11) is not None else ''
                    dm1 = self.tableWidgetObsPolaires.item(rowObs,12).text() if self.tableWidgetObsPolaires.item(rowObs,12) is not None else ''
                    dm2 = self.tableWidgetObsPolaires.item(rowObs,13).text() if self.tableWidgetObsPolaires.item(rowObs,13) is not None else ''
                    targetCentPlani = self.tableWidgetObsPolaires.item(rowObs,14).text() if self.tableWidgetObsPolaires.item(rowObs,14) is not None else ''
                    targetCentAlti = self.tableWidgetObsPolaires.item(rowObs,15).text() if self.tableWidgetObsPolaires.item(rowObs,15) is not None else ''
                    
                    # création du sous-dict d'une measure
                    measure = {'pointName':pointName,
                               'RI':{'stdDev':{'cc':RIstdDev},
                                     'value':RIvalue,
                                     'discarded':RIdiscarded},
                               
                               'DS':{'stdDev':{'mm':DSstdDevMm,
                                               'ppm':DSstdDevPpm},
                                     'value':DSvalue,
                                     'discarded':DSdiscarded},
                               
                               'ZD':{'stdDev':{'cc':ZDstdDev},
                                     'value':ZDvalue,
                                     'discarded':ZDdiscarded},
                               
                               'S':{'value':S},
                               'dm1':{'value':dm1},
                               'dm2':{'value':dm2},
                               'targetCentring':{'planiStdDev':{'mm':targetCentPlani},
                                                 'altiStdDev':{'mm':targetCentAlti}}}
                    
                    # Ajout à la station
                    station['stationData']['measure'].append(measure)
                                        

                
                break # ne pas parcourir les autres station que celles courante
        
    def onCellObsGnssChanged(self):
        """
        Fonction qui va mettre à jour la data par rapport au tableau des observations GNSS.
        """
        
        # Récupération d'éléments QTable courants
        rowSession = self.tableWidgetSessions.currentRow()
        nRowsObs = self.tableWidgetObsGnss.rowCount()
        
        # MAJ de la data selon QTable
        for session in self.listeGNSS:
            if session['rowSession'] == rowSession:
                
                # Vider les measures
                session['measure'] = []  
                for rowObs in range(0,nRowsObs):
                    
                    # Récupération des éléments
                    pointName = self.tableWidgetObsGnss.item(rowObs,0).text() if self.tableWidgetObsGnss.item(rowObs,0) is not None else ''
                    LYvalue = self.tableWidgetObsGnss.item(rowObs,1).text() if self.tableWidgetObsGnss.item(rowObs,1) is not None else ''
                    LYstdDev = self.tableWidgetObsGnss.item(rowObs,2).text() if self.tableWidgetObsGnss.item(rowObs,2) is not None else ''
                    # Case cochée ou non
                    if self.tableWidgetObsGnss.item(rowObs,3).checkState() == 2:
                        LYdiscarded = 'true'
                    else:
                        LYdiscarded = ''                    
                    
                    
                    LXvalue = self.tableWidgetObsGnss.item(rowObs,4).text() if self.tableWidgetObsGnss.item(rowObs,4) is not None else ''
                    LXstdDev = self.tableWidgetObsGnss.item(rowObs,5).text() if self.tableWidgetObsGnss.item(rowObs,5) is not None else ''
                    # Case cochée ou non
                    if self.tableWidgetObsGnss.item(rowObs,6).checkState() == 2:
                        LXdiscarded = 'true'
                    else:
                        LXdiscarded = '' 
                    
                    
                    LHvalue = self.tableWidgetObsGnss.item(rowObs,7).text() if self.tableWidgetObsGnss.item(rowObs,7) is not None else ''
                    LHstdDev = self.tableWidgetObsGnss.item(rowObs,8).text() if self.tableWidgetObsGnss.item(rowObs,8) is not None else ''
                    # Case cochée ou non
                    if self.tableWidgetObsGnss.item(rowObs,9).checkState() == 2:
                        LHdiscarded = 'true'
                    else:
                        LHdiscarded = '' 
                    
                    # Si il y'a LH, on l'ajoute
                    if LHvalue != '':
                        # création du sous-dict d'une measure
                        measure = {'pointName':pointName,
                                   'LY':{'stdDev':{'mm':LYstdDev},
                                         'value':LYvalue,
                                         'discarded':LYdiscarded},
                                   
                                   'LX':{'stdDev':{'mm':LXstdDev},
                                         'value':LXvalue,
                                         'discarded':LXdiscarded},
                                   
                                   'LH':{'stdDev':{'mm':LHstdDev},
                                         'value':LHvalue,
                                         'discarded':LHdiscarded}}
                        
                    else: # Si pas de LH, on ne l'ajoute pas
                        # création du sous-dict d'une measure
                        measure = {'pointName':pointName,
                                   'LY':{'stdDev':{'mm':LYstdDev},
                                         'value':LYvalue,
                                         'discarded':LYdiscarded},
                                   
                                   'LX':{'stdDev':{'mm':LXstdDev},
                                         'value':LXvalue,
                                         'discarded':LXdiscarded}}
                            
                    
                    # Ajout à la nouvelle liste d'obs.
                    session['measure'].append(measure)
                    
                    
                    
    def onCellObsSystemChanged(self):
        """
        Fonction qui va mettre à jour la data par rapport au tableau des observations des systèmes locaux.
        """
        
        # Récupération d'éléments QTable courants
        rowSystem = self.tableWidgetSystemes.currentRow()
        nRowsObs = self.tableWidgetObsSysteme.rowCount()
        
        # MAJ de la data selon QTable
        for systeme in self.listeSystemes:
            if systeme['rowSysteme'] == rowSystem:
                
                # Vider les measures
                systeme['measure'] = []  
                for rowObs in range(0,nRowsObs):
                    
                    # Récupération des éléments
                    pointName = self.tableWidgetObsSysteme.item(rowObs,0).text() if self.tableWidgetObsSysteme.item(rowObs,0) is not None else ''
                    LYvalue = self.tableWidgetObsSysteme.item(rowObs,1).text() if self.tableWidgetObsSysteme.item(rowObs,1) is not None else ''
                    LYstdDev = self.tableWidgetObsSysteme.item(rowObs,2).text() if self.tableWidgetObsSysteme.item(rowObs,2) is not None else ''
                    # Case cochée ou non
                    if self.tableWidgetObsSysteme.item(rowObs,3).checkState() == 2:
                        LYdiscarded = 'true'
                    else:
                        LYdiscarded = '' 
                    
                    
                    
                    LXvalue = self.tableWidgetObsSysteme.item(rowObs,4).text() if self.tableWidgetObsSysteme.item(rowObs,4) is not None else ''
                    LXstdDev = self.tableWidgetObsSysteme.item(rowObs,5).text() if self.tableWidgetObsSysteme.item(rowObs,5) is not None else ''
                    # Case cochée ou non
                    if self.tableWidgetObsSysteme.item(rowObs,6).checkState() == 2:
                        LXdiscarded = 'true'
                    else:
                        LXdiscarded = '' 
                   
                    # création du sous-dict d'une measure
                    measure = {'pointName':pointName,
                               'LY':{'stdDev':{'mm':LYstdDev},
                                     'value':LYvalue,
                                     'discarded':LYdiscarded},
                               
                               'LX':{'stdDev':{'mm':LXstdDev},
                                     'value':LXvalue,
                                     'discarded':LXdiscarded} }
                    
                    # Ajout à la nouvelle liste d'obs.
                    systeme['measure'].append(measure)
        
        # Dessiner le plan du système local
        self.drawPointsSysLoc()    
       


    

        
        
            
    
    def addRow(self, tableWidget):
        """
        Fonction permettant d'ajouter une ligne vide sous la ligne selectionnée.
        """
        currentRow = tableWidget.currentRow()
        tableWidget.insertRow(currentRow+1)
        
        
        #### CHECKBNOXES OBSERRVATIONS POLAIRES
        if tableWidget == self.tableWidgetObsPolaires :
            # déconnecter la MAJ le temps de créer les checkbox
            self.tableWidgetObsPolaires.itemChanged.disconnect(self.onCellObsPolaireChanged)
            # Checkbox écarté déchochées 
            for col in [3,7,10] : # boucle pour éviter les copie de code inutes (col. x,x,x concernée par la case à cocher) 
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.tableWidgetObsPolaires.setItem(currentRow+1, col, item)
            # reconnecter la MAJ le temps de créer les checkbox
            self.tableWidgetObsPolaires.itemChanged.connect(self.onCellObsPolaireChanged)
            
        #### CHECKBNOXES OBSERRVATIONS GNSS
        if tableWidget == self.tableWidgetObsGnss :
            # déconnecter la MAJ le temps de créer les checkbox
            self.tableWidgetObsGnss.itemChanged.disconnect(self.onCellObsGnssChanged)
            # Checkbox écarté déchochées 
            for col in [3,6,9] : # boucle pour éviter les copie de code inutes (col. x,x,x concernée par la case à cocher) 
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.tableWidgetObsGnss.setItem(currentRow+1, col, item)
            # reconnecter la MAJ le temps de créer les checkbox
            self.tableWidgetObsGnss.itemChanged.connect(self.onCellObsGnssChanged)
            
        #### CHECKBNOXES OBSERRVATIONS SYSTEMES LOCAUX
        if tableWidget == self.tableWidgetObsSysteme :
            # déconnecter la MAJ le temps de créer les checkbox
            self.tableWidgetObsSysteme.itemChanged.disconnect(self.onCellObsSystemChanged)
            # Checkbox écarté déchochées 
            for col in [3,6] : # boucle pour éviter les copie de code inutes (col. x,x,x concernée par la case à cocher) 
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.tableWidgetObsSysteme.setItem(currentRow+1, col, item)
            # reconnecter la MAJ le temps de créer les checkbox
            self.tableWidgetObsSysteme.itemChanged.connect(self.onCellObsSystemChanged)
        
        #### CHECKBNOXES OBSERRVATIONS SIMPLE MEASURE
        if tableWidget == self.tableWidgetMesuresSimples :
            # Checkbox écarté déchochées 
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.tableWidgetMesuresSimples.setItem(currentRow+1, 5, item)

        #### CHECKBNOXES ET CHOICE LIST CONTRAINTES
        if tableWidget == self.tableWidgetContraintes :
            # Checkbox écarté déchochées 
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.tableWidgetContraintes.setItem(currentRow+1, 6, item)
            # Liste de choix pour le type
            choiceList = QtWidgets.QComboBox()
            # choiceList.setStyleSheet('background-color: white;') # couleur de fond
            choiceList.addItem('alignment')
            choiceList.addItem('perpendicular')
            self.tableWidgetContraintes.setCellWidget(currentRow+1, 0, choiceList) # Ajout du widget QComboBox
                

            
            
            
            
        
        
        
    def removeRow(self, tableWidget):
        """
        Fonction permettant de supprimer une ligne selectionée.
        """
        currentRow = tableWidget.currentRow()
        if tableWidget.rowCount() > 0: # Uniquement si il y'a au moins une row 
            tableWidget.removeRow(currentRow)
                
            
    def contextMenuEvent(self, event):
        """
        Fonction permettant de générer une menu pour l'ajout et la suppression de ligne.
        Je ne sais pas ce qu'elle fait exactement mais ça marche.
        """
        
        # # ONGLET COURANT
        # indexTab = self.tabWidget.currentIndex()
        # y = event.pos().y()
        # lp = self.tableWidgetStations.mapFromGlobal(event.pos())
        
    
        clicGlobal = self.centralWidget.mapToGlobal(event.pos())
        # print('MOUSE GLOBAL:', clicGlobal)
        # print(mapToGlobal(QPoint(self.tableWidgetStations.geometry().left(), self.tableWidgetStations.geometry().top())))
        

        # print(self.tableWidgetStations.left())
        
        
        # index = self.tableWidgetStations.indexAt(lp)
        # if index.isValid():
            
        #     print(index)
        
        # -----------------------------
        #### POLAIRE 
        # -----------------------------
        
        
        
        # # Si le clic a eu lieu dans la QTable de station
        
        # print(lp)
        # index = self.tabWidget.indexAt(event.pos())
        # print(index)

        #### ^---- Stations
        
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox.mapToGlobal(self.tableWidgetStations.geometry().topLeft()) # QPoint
        topLeftLocal = self.tableWidgetStations.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetStations.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 0:
            
            for i in self.tableWidgetStations.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            
            # Si la QTable est vide, set la row courante à -1 (-1 +1 = 0 (no de row))
            if self.tableWidgetStations.rowCount() == 0:
                row = -1
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction("Supprimer la ligne selectionnée")
            addRowAction = menu.addAction("Ajouter une ligne en dessous")
            action = menu.exec_(QtGui.QCursor.pos())

            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetStations) 
                # Sous dictionnairte pour la nouvelle station vide
                sousDict = {}
                sousDict.update({'stationName':''})
                sousDict.update({'rowSta':row+1}) # Numéro de row (QTable avec modif.)
                sousDict.update({'stationData':{'I':'',
                                                'stationCentring':{'planiStdDev':{'mm':''},
                                                                  'altiStdDev':{'mm':''}
                                                                  },
                                                'distanceGroup': '',
                                                'directionGroup': '',
                                                'centringGroup': '',
                                                'measure': [{'pointName':'',
                                                            'RI':{'stdDev':{'cc':''},
                                                                  'value':'',
                                                                  'discarded':''},
                                                           
                                                            'DS':{'stdDev':{'mm':'',
                                                                            'ppm':''},
                                                                  'value':'',
                                                                  'discarded':''},
                                                           
                                                            'ZD':{'stdDev':{'cc':''},
                                                                  'value':'',
                                                                  'discarded':''},
                                                           
                                                            'S':{'value':''},
                                                            'dm1':{'value':''},
                                                            'dm2':{'value':''},
                                                            'targetCentring':{'planiStdDev':{'mm':''},
                                                                              'altiStdDev':{'mm':''}}}] # EN LISTE, ici valeur d'obs vide après création!!
                                                }
                                    })
                self.listePolaire.append(sousDict)
                
                # MAJ des n° row dans data
                for i, station in enumerate(self.listePolaire):
                    if station['rowSta'] > (row) and i != (len(self.listePolaire)-1): # ne pas modifier la row de la station venant d'être ajoutée
                        station['rowSta'] += 1
                
              
                        
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetStations)
                # supprimer la station de la liste
                for station in self.listePolaire: 
                    if station['rowSta'] == row:
                        self.listePolaire.remove(station) 
                for station in self.listePolaire:     
                    if station['rowSta'] > (row) : 
                        station['rowSta'] -= 1 # Réduire de 1 row
                    
                self.onSelectionStationChanged()
                
                # for station in self.listePolaire:
                #     print(station['rowSta'], station['stationName'], len(station['stationData']['measure']))
               
                
        #### ^---- Observations   
        
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_2.mapToGlobal(self.tableWidgetObsPolaires.geometry().topLeft()) # QPoint
        topLeftLocal = self.tableWidgetObsPolaires.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetObsPolaires.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 0:            
            for i in self.tableWidgetObsPolaires.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction("Supprimer la ligne selectionnée")
            addRowAction = menu.addAction("Ajouter une ligne en dessous")
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetObsPolaires) 
                # MAJ data
                self.onCellObsPolaireChanged()
            
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetObsPolaires)
                # MAJ data
                self.onCellObsPolaireChanged()
                
               
                
               
                
               
        #### GNSS
        
        #### ^---- Sessions 

        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_5.mapToGlobal(self.tableWidgetSessions.geometry().topLeft()) # QPoint
        topLeftLocal = self.tableWidgetSessions.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetSessions.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 1:
            
            for i in self.tableWidgetSessions.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            # Si la QTable est vide, set la row courante à -1 (-1 +1 = 0 (no de row))
            if self.tableWidgetSessions.rowCount() == 0:
                row = -1
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction("Supprimer la ligne selectionnée")
            addRowAction = menu.addAction("Ajouter une ligne en dessous")
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetSessions) 
                # Sous dictionnairte pour la nouvelle session vide
                sousDict = {}
                sousDict.update({'sessionName':''})
                sousDict.update({'rowSession':row+1}) # Numéro de row (QTable avec modif.)
                sousDict.update({'measure': [{'pointName':'',
                                              'LY':{'stdDev':{'mm':''},
                                                    'value':'',
                                                    'discarded':''},
                                               'LX':{'stdDev':{'mm':''},
                                                     'value':'',
                                                     'discarded':''},
                                               'LH':{'stdDev':{'mm':''},
                                                     'value':'',
                                                     'discarded':''}                                              
                                              }]}) # EN LISTE, ici valeur d'obs vide après création!!                        
                self.listeGNSS.append(sousDict)
                
                # MAJ des n° row dans data
                for i, session in enumerate(self.listeGNSS):
                    if session['rowSession'] > (row) and i != (len(self.listeGNSS)-1): # ne pas modifier la row de la session venant d'être ajoutée
                        session['rowSession'] += 1

            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetSessions)
                # supprimer la session de la liste
                for session in self.listeGNSS: 
                    if session['rowSession'] == row:
                        self.listeGNSS.remove(session) 
                for session in self.listeGNSS:     
                    if session['rowSession'] > (row) : 
                        session['rowSession'] -= 1 # Réduire de 1 row
                    
                self.onSelectionSessionChanged()

    
        #### ^---- Observations   
        
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_6.mapToGlobal(self.tableWidgetObsGnss.geometry().topLeft()) # QPoint
        topLeftLocal = self.tableWidgetObsGnss.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetObsGnss.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 1:
            
            for i in self.tableWidgetObsGnss.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction("Supprimer la ligne selectionnée")
            addRowAction = menu.addAction("Ajouter une ligne en dessous")
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetObsGnss) 
                # MAJ data
                self.onCellObsGnssChanged()
            
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetObsGnss)
                # MAJ data
                self.onCellObsGnssChanged()
                
                
                
                
                
                
        #### SYSTEMES LOCAUX
        
        #### ^---- Systèmes (en-tête) 

        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_7.mapToGlobal(self.tableWidgetSystemes.geometry().topLeft()) # QPoint
        topLeftLocal = self.tableWidgetSystemes.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetSystemes.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 2:
            
            for i in self.tableWidgetSystemes.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            if self.tableWidgetSystemes.rowCount() == 0:
                row = -1
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction("Supprimer la ligne selectionnée")
            addRowAction = menu.addAction("Ajouter une ligne en dessous")
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetSystemes) 
                # Sous dictionnairte pour le nouveau système local vide
                sousDict = {}
                sousDict.update({'localSystemName':''})
                sousDict.update({'rowSysteme':row+1}) # Numéro de row (QTable avec modif.)
                sousDict.update({'measure': [{'pointName':'',
                                              'LY':{'stdDev':{'mm':''},
                                                    'value':'',
                                                    'discarded':''},
                                               'LX':{'stdDev':{'mm':''},
                                                     'value':'',
                                                     'discarded':''}                                             
                                              }]}) # EN LISTE, ici valeur d'obs vide après création!!                        
                self.listeSystemes.append(sousDict)
                
                # MAJ des n° row dans data
                for i, systeme in enumerate(self.listeSystemes):
                    if systeme['rowSysteme'] > (row) and i != (len(self.listeSystemes)-1): # ne pas modifier la row du système venant d'être ajoutée
                        systeme['rowSysteme'] += 1

            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetSystemes)
                # supprimer le système de la liste
                for systeme in self.listeSystemes: 
                    if systeme['rowSysteme'] == row:
                        self.listeSystemes.remove(systeme) 
                for systeme in self.listeSystemes:     
                    if systeme['rowSysteme'] > (row) : 
                        systeme['rowSysteme'] -= 1 # Réduire de 1 row
                    
                self.onSelectionSystemsChanged()
                
        #### ^---- Observations   
        
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_8.mapToGlobal(self.tableWidgetObsSysteme.geometry().topLeft()) # QPoint
        topLeftLocal = self.tableWidgetObsSysteme.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetObsSysteme.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 2:
            
            for i in self.tableWidgetObsSysteme.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction("Supprimer la ligne selectionnée")
            addRowAction = menu.addAction("Ajouter une ligne en dessous")
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetObsSysteme) 
                # MAJ data
                self.onCellObsSystemChanged()
            
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetObsSysteme)
                # MAJ data
                self.onCellObsSystemChanged()
                
                
                
                
                
        
        #### MESURES SIMPLES
        
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_10.mapToGlobal(self.tableWidgetMesuresSimples.geometry().topLeft()) # QPoint
        topLeftLocal = self.tableWidgetMesuresSimples.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetMesuresSimples.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 3:
            
            for i in self.tableWidgetMesuresSimples.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction("Supprimer la ligne selectionnée")
            addRowAction = menu.addAction("Ajouter une ligne en dessous")
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetMesuresSimples) 
            
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetMesuresSimples)
                
                
                
                
                
                
        #### CONTRAINTES GEOMETRIQUES
        
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_12.mapToGlobal(self.tableWidgetContraintes.geometry().topLeft()) # QPoint
        topLeftLocal = self.tableWidgetContraintes.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetContraintes.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 4:
            
            for i in self.tableWidgetContraintes.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction("Supprimer la ligne selectionnée")
            addRowAction = menu.addAction("Ajouter une ligne en dessous")
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetContraintes) 
            
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetContraintes)
                
 
    
    def onClickSearchNext(self, QTable, QLineEdit, listeCols):
        """
        Fonction générique permettant d'effectuer une recherche sur une QTable selon un input utilisateur et 
        une liste de colonne à chercher après avoir déjà cherché la première occurence
        S'active au clic sur un des boutons "suivant".
        
        Parameters
        ----------
        QTable : object
            QTable concernée.
        QLineEdit : object
            QLineEdit de l'input de la recherche saisie par l'utilisateur
        listeCols: list
            Liste qui contient les colonnes à concerner par la recherche
            exemples: [0,1] pour chercher dans la 1er et la 2eme. et [0] pour la première uniquement.
        """
        
        # Clear current selection.
        QTable.setCurrentItem(None)
        
        # Récupération de l'input de recherche
        searchInputNow = QLineEdit.text()
        
        # Empty string, don't search.
        if not searchInputNow:
            return None

        # Correspondances 
        matching_items = QTable.findItems(searchInputNow, QtCore.Qt.MatchContains)
        if matching_items:
            # Si on a bien trouvé un résultat
            i = 0
            for item in matching_items:
                # Dans la colonne définie
                if item.column() in listeCols: 
                    # Il faut que i soit supérieur à l'indice actuel de recherche
                    if i > self.indiceSearch :
                        QTable.setCurrentItem(item)
                        self.indiceSearch = i # incrémenter de 1
                        return None
                    else:
                        i += 1
        
    
    def searchInQTable(self, QTable, QLineEdit, listeCols):
        """
        Fonction générique permettant d'effectuer une recherche sur une QTable selon un input utilisateur et 
        une liste de colonne à chercher.
        S'active au clic sur un des boutons "rechercher".
        
        Parameters
        ----------
        QTable : object
            QTable concernée.
        QLineEdit : object
            QLineEdit de l'input de la recherche saisie par l'utilisateur
        listeCols: list
            Liste qui contient les colonnes à concerner par la recherche
            exemples: [0,1] pour chercher dans la 1er et la 2eme. et [0] pour la première uniquement.
        """
        
        # Clear current selection.
        QTable.setCurrentItem(None)
        
        # Récupération de l'input de recherche
        searchInputNow = QLineEdit.text()
        
        
        # Empty string, don't search.
        if not searchInputNow:
            return None

        # Correspondances 
        matching_items = QTable.findItems(searchInputNow, QtCore.Qt.MatchContains)
        if matching_items:
            # Si on a bien trouvé un résultat
            
            for item in matching_items:
                if item.column() in listeCols: # prendre le premier resultat quand celui-ci est dans la colonne définie
                    QTable.setCurrentItem(item)
                    self.indiceSearch = 0 # Indice à 0
                    return None
                   
                
                
    def emprise(self, points):
        """
        Petite fonction simple qui calcul les min en x et y d'un jeu de coorodonnées.
        """
        x_coordinates, y_coordinates = zip(*points)
        # return [(min(x_coordinates), min(y_coordinates)), (max(x_coordinates), max(y_coordinates))]
        return min(x_coordinates), min(y_coordinates), max(x_coordinates), max(y_coordinates)
        # return abs(max(x_coordinates) - min(x_coordinates) + 0.001), abs(max(y_coordinates) - min(y_coordinates) + 0.001)
                
        
    def drawPointsSysLoc(self):
        """
        Fonction qui va dessiner le réseau local courant au changement de sélection de système ou au changement/edit de sélection des obs. (live).
        """
        
        # Vider le plot
        self.graphWidgetSysLoc.clear()
        
        # Parcourir les obs. LY et LX du tableau et créer des points
        nRowsObs = self.tableWidgetObsSysteme.rowCount()
        listeCooY, listeCooX = [], []
        
        # première boucle -> on calcul les max y et x (pour dimensionner le dessin au grpahicView)
        for row in range(0,nRowsObs):
            # No du point
            try:
                noPt = self.tableWidgetObsSysteme.item(row,0).text() if self.tableWidgetObsSysteme.item(row,0) is not None else ''
            except:
                noPt = ''
            # Float en ne prenant pas compte les valeurs vides ou les erreurs de type (=0 pour le dessin)
            try:
                LY = float(self.tableWidgetObsSysteme.item(row,1).text().replace(' ','')) if self.tableWidgetObsSysteme.item(row,1) is not None  else 0.0
            except:
                LY = 0.0
            try:
                LX = float(self.tableWidgetObsSysteme.item(row,4).text().replace(' ','')) if self.tableWidgetObsSysteme.item(row,4) is not None else 0.0
            except:
                LX = 0.0
            
            # ajout aux listes
            listeCooY.append(LY) 
            listeCooX.append(LX) 
            # listeCooLabel.append([LY, LX, noPt])
            # Set label du pt
            text = pg.TextItem(text=noPt, color='r')
            text.setPos(LY,LX)
            self.graphWidgetSysLoc.addItem(text)
            
            
            
            
        # Set le style
        scatter = pg.ScatterPlotItem(
            size=10, brush='r', pen='r')
   
        # setting data to the scatter plot
        scatter.setData(listeCooY, listeCooX)

        # Add the scatter plot and text
        self.graphWidgetSysLoc.addItem(scatter)
        
        # Fitting items in view
        view = self.graphWidgetSysLoc.getViewBox()
        view.autoRange()

        
        
        
        
        
        
        
        

            
            

    
                        
                        
                
                


        
        
            
        
    
            
            
            
            
            
            
            

         
        
        
        
        
        
        
        
        