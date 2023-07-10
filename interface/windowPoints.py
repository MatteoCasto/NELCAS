# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 17:09:09 2022

@author: matteo.casto
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem, QStandardItemModel
from interface import PopUpDoublons
import json
import xmltodict
from PyQt5 import uic
import sys
import os
import time
import numpy as np



class UI_ongletPoints(QtWidgets.QMainWindow):
    
    def __init__(self):
        
        super(UI_ongletPoints, self).__init__()
        # Charger le ui
        uic.loadUi(os.getcwd()+"\\interface\\OngletPoints.ui", self)
        
        # Désactiver le widget principal
        self.centralwidget.setEnabled(False)


        # connection bouton de la menu bar
        self.actionNouveau.triggered.connect(self.newFile)
        self.actionOuvrir.triggered.connect(self.openFile)
        self.actionEnregistrer.triggered.connect(self.saveFile)
        self.actionEnregistrer_sous.triggered.connect(self.saveAsFile)
        self.actionSupprimer_les_doublons.triggered.connect(self.openPopUpDoublons)
        
        
        # connection dès que le text de la barre de recherche est changé
        self.inputRecherchePoint.textChanged.connect(self.search)
        
        # Afficher la fenêtre
        self.show()
        
        
        
        
        
        
    def newFile(self):
        """
        Génére un fichier de points vide XML après avoir cliqué sur "nouveau".
        """
    
        # Générer le fichier vide avec la fonction d'export
        # Path d'export
        try:
            self.filePath = QtWidgets.QFileDialog().getSaveFileName(None,"Save", None, "*.xml")[0]
            self.exportPoints()
            
            # vider la QTable
            self.tableWidgetPoints.setRowCount(0)
            
            # Activer le tabwidget
            self.centralwidget.setEnabled(True)
            
            # Activer les boutons save et save as
            self.actionEnregistrer.setEnabled(True)
            self.actionEnregistrer_sous.setEnabled(True)
            
            # Set le nom du fichier lu
            self.setWindowTitle('Points  -  {:s}  -  enregistré'.format(self.filePath))
            time.sleep(0.5)
            self.setWindowTitle('Points  -  {:s}'.format(self.filePath))
        except:
            return None  
        
        
    def openFile(self):
        """
        Fonction d'import du fichier XML des points après avoir cliqué sur "ourvrir".
        """
        # import du fichier texte XML
        # try:
        self.filePath = QtWidgets.QFileDialog().getOpenFileName(None,"Open", None, "*.xml")[0]
        self.importPoints()
            
        # Set le nom du fichier lu
        self.setWindowTitle('Points  -  {:s}'.format(self.filePath))
        
        # Activer les boutons save et save as
        self.actionEnregistrer.setEnabled(True)
        self.actionEnregistrer_sous.setEnabled(True)
        
        # Activer le tabwidget
        self.centralwidget.setEnabled(True)
        # except:
            # return None
        
        
    def saveFile(self):
        """
        Sauvegarde le fichier et remplace celui qui a été importé avec le même nom. S'active après avoir cliqué sur "Enregistrer".
        """
        try:
            # Remplace le fichier courant avec sa nouvelle version de lui-même.
            self.exportPoints()
            # Set le nom du fichier lu
            self.setWindowTitle('Points  -  {:s}  -  enregistré'.format(self.filePath))
            time.sleep(0.5)
            self.setWindowTitle('Points  -  {:s}'.format(self.filePath))
            
        
        
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
            self.exportPoints()
            
            # Set le nom du fichier lu
            self.setWindowTitle('Points  -  {:s}  -  enregistré'.format(self.filePath))
            time.sleep(0.5)
            self.setWindowTitle('Points  -  {:s}'.format(self.filePath))
        except:
            return None
        
        
        
        
        
        
    
    def importPoints(self, dictPoints=False):
        """
        Fonction d'import du fichier XML des points après avoir cliqué sur "import".
        arg. optionnel dictPoints:  pour la suppression des doublons avec un novueau dict les fenêtre de pop-up
        """
        
        # si variable pas précisiée
        if not dictPoints :
            # import du fichier texte XML
            with open(self.filePath) as f:
                dictPoints = xmltodict.parse(f.read())
                
        dictPoints['points']['point'] = dictPoints['points']['point'] if type(dictPoints['points']['point']) is list else [dictPoints['points']['point']]
        
        # Initialisation QTableWidget
        self.tableWidgetPoints.setRowCount(len(dictPoints['points']['point']))
        for row, point in enumerate(dictPoints['points']['point']):
            H = point['H'] # Possible qu'il n'y ai pas d'alitude (=None)
            if point['H'] == None:
                H = ''
            
            # Thème et nature si existant
            if 'themeMO' in point.keys():
                theme = point['themeMO'] if point['themeMO'] is not None else ''
                self.tableWidgetPoints.setItem(row, 4, QtWidgets.QTableWidgetItem(theme))
            if 'natureMO' in point.keys():
                nature = point['natureMO'] if point['natureMO'] is not None else ''
                self.tableWidgetPoints.setItem(row, 5, QtWidgets.QTableWidgetItem(nature))
                
            
            # On set les item dans la Table
            self.tableWidgetPoints.setItem(row, 0, QtWidgets.QTableWidgetItem(point['pointName']))
            self.tableWidgetPoints.setItem(row, 1, QtWidgets.QTableWidgetItem(point['E']))
            self.tableWidgetPoints.setItem(row, 2, QtWidgets.QTableWidgetItem(point['N']))
            self.tableWidgetPoints.setItem(row, 3, QtWidgets.QTableWidgetItem(H))
            
    
    
    def exportPoints(self):
        """
        Fonction d'export des points après avoir cliqué sur "export".
        """
        # Path d'export
        # Initialisation du dictionnaire d'export
        self.dictPointsExport = {'points':{'point':[]}}
        # Nombre de lignes et parcours
        nrows = self.tableWidgetPoints.rowCount()
        for row in range(0, nrows):
            pointName, E, N, H = self.tableWidgetPoints.item(row,0), self.tableWidgetPoints.item(row,1), self.tableWidgetPoints.item(row,2), self.tableWidgetPoints.item(row,3)
            theme, nature = self.tableWidgetPoints.item(row,4), self.tableWidgetPoints.item(row,5)
            if pointName is None: # Si Aucune valeur entrée
                pointName = ''
            else: # Si une valeur
                pointName = pointName.text()
            if E is None: # Si Aucune valeur entrée
                E = ''
            else: # Si une valeur
                E = E.text()
            if N is None: # Si Aucune valeur entrée
                N = ''
            else: # Si une valeur
                N = N.text()
            if H is None: # Si Aucune valeur entrée
                H = ''
            else: # Si une valeur
                H = H.text()
                
            
            # Point correspondant à la row
            point = {'pointName': pointName, 
              'E': E, 
              'N': N, 
              'H': H}
            # Si pas vide ne pas ajouter les attibuts theme et nature
            if theme is not None :
                if theme.text() != '': # Ne pas ajouer si string vide
                    point.update({'themeMO':theme.text()})
            if nature is not None :
                if nature.text() != '':
                    point.update({'natureMO':nature.text()})
            
            # Aujout du pt au dict. d'exort
            self.dictPointsExport['points']['point'].append(point)
        
        # Export du fichier texte XML
        dictPointsString = xmltodict.unparse(self.dictPointsExport, pretty=True)
        with open(self.filePath, 'w') as f:
            f.write(dictPointsString)

       
        
       
    def search(self):
        """
        Fonction permettant d'effectuer une recherche selon une chaîne de caractère.
        """
        
        # Clear current selection.
        self.tableWidgetPoints.setCurrentItem(None)
        s = self.inputRecherchePoint.text()

        if not s:
            # Empty string, don't search.
            return

        matching_items = self.tableWidgetPoints.findItems(s, QtCore.Qt.MatchContains)
        if matching_items:
            # Si on a bien trouvé un résultat
            for item in matching_items:
                if item.column() == 0: # prendre le premier resultat quand celui-ci est dans la colonne des noms de pts
                    self.tableWidgetPoints.setCurrentItem(item)
                    return # quand trouvé, on sort de la fonction
                
            
    
    
    def openPopUpDoublons(self):
        
        # Ouvrir et init. le popup de l'outils de détection de doublons
        self.saveFile() # d'abord, sauvegarder
        self.popUpDoublons = PopUpDoublons.UI_PopUpDoublons(self.dictPointsExport, self, self.filePath)

        
    
    
    
    # def supprimerDoublons(self):
    #     """
    #     A REFAIRE POUR AFFICHER UN PETIT MENU QUI NOUS LISTE LES PTS DOUBLONS PAR 
    #     RAPPORT A UN NUMERO. FUSIONNER AVEC DOUBLONS GEOMETRIQUES

    #     Returns
    #     -------
    #     None.

    #     """
        
    #     # En premier, on export les points (stocker l'état actuel des pts)
    #     self.exportPoints()
        
    #     # Parcourir les points et delete les 2e occurence d'un point
    #     listePtsName = []
    #     for point in self.dictPointsExport['points']['point'].copy():
            
    #         if point['pointName'] not in listePtsName:
    #             listePtsName.append(point['pointName'])
    #         else: # le pt est doublons et supprimé
    #             self.dictPointsExport['points']['point'].remove(point)
        
    #     # Export du fichier texte XML
    #     dictPointsString = xmltodict.unparse(self.dictPointsExport, pretty=True)
    #     with open(self.filePath, 'w') as f:
    #         f.write(dictPointsString)
    #     # refresh la table en faisant un ré-import
    #     self.importPoints()
        
        
        
        
        
    
        
        
        
        
        
        
            
    
            
            
    def addRow(self, tableWidget):
        """
        Fonction permettant d'ajouter une ligne vide sous la ligne selectionnée.
        """
        currentRow = tableWidget.currentRow()
        tableWidget.insertRow(currentRow+1)
        
        
    def removeRow(self, tableWidget):
        """
        Fonction permettant de supprimer une ligne selectionée.
        """
        currentRow = tableWidget.currentRow()
        if tableWidget.rowCount() > 0: # Uniquement si il y'a au moins une row 
            tableWidget.removeRow(currentRow)
            
    
    def contextMenuEvent(self, event):
        '''
        Redéfinition de la fonction pour le menu contextuel au clic droit sur une QTable.
        Ajouter ou supprimer une row.        
        '''
        # print('MOUSE GLOBAL:', self.centralwidget.mapToGlobal(event.pos()))
        clicGlobal = self.centralwidget.mapToGlobal(event.pos())
        
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.centralwidget.mapToGlobal(self.tableWidgetPoints.geometry().topLeft()) # -> QPoint
        topLeftLocal = self.tableWidgetPoints.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetPoints.geometry().contains(clicGlobal-trans) :

            for i in self.tableWidgetPoints.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction('Supprimer la ligne selectionnée')
            addRowAction = menu.addAction('Ajouter une ligne en dessous')
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetPoints) 
                
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetPoints)
        
        
        
        
        
        
        
        
        # if self.tableWidgetPoints.selectionModel().selection().indexes():
        #     for i in self.tableWidgetPoints.selectionModel().selection().indexes():
        #         row, _ = i.row(), i.column()
        #     menu = QtWidgets.QMenu()
        #     deleteRowAction = menu.addAction("Supprimer la ligne selectionnée")
        #     addRowAction = menu.addAction("Ajouter une ligne en dessous")
        #     action = menu.exec_(QtGui.QCursor.pos())
        #     if action == addRowAction:
        #         self.addRow(self.tableWidgetPoints)
        #     if action == deleteRowAction:
        #         self.removeRow(self.tableWidgetPoints)

 
        
        
        
        