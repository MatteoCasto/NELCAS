# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 08:42:55 2023

@author: matteo.casto
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem, QStandardItemModel
from PyQt5 import uic
import os
import numpy as np
from interface import windowPoints # pour supprimer un point identique p.ex.
import xmltodict


def extract_duplicates(data):
    count_dict = {}
    duplicates = []

    # Compter le nombre d'occurrences de chaque élément
    for item in data:
        count_dict[item] = count_dict.get(item, 0) + 1

    # Extraire les éléments qui apparaissent au moins deux fois
    for item, count in count_dict.items():
        if count >= 2:
            duplicates.append(item)

    return duplicates






class UI_PopUpDoublonsNoPts(QtWidgets.QMainWindow):
    
    def __init__(self, dictPoints, windowPointsOpen, listingToGenerate, filePath):
        
        super(UI_PopUpDoublonsNoPts, self).__init__()
        # Charger le ui
        uic.loadUi(os.getcwd()+"\\interface\\PopUpDoublonsNoPts.ui", self)
        
        # Afficher la fenêtre
        self.show()
        
        # Init des variables de la fenêtre précédente
        self.dictPoints = dictPoints
        self.count = 0  # variable qui s'incrémente à "suivant"
        self.windowPointsOpen = windowPointsOpen
        self.listingToGenerate = listingToGenerate
        self.filePath = filePath
        
        # détection des pts proches
        self.detectDuplicatePtsNames()
        
        # connexion au bouton next et previous
        self.buttonNext.clicked.connect(self.nextDoublon)
        self.buttonPrevious.clicked.connect(self.previousDoublon)
        
    def detectDuplicatePtsNames(self):
        """
        ECRIRE DOCSTRING
        
        Returns
        -------
        None.

        """
        
        # Récupérer tous les no de points dans une liste
        listePtsName = []
        for point in self.dictPoints['points']['point']:

            try: # si pas convertible en float, ne pas le traiter
                listePtsName.append(point['pointName'])
            except:
                pass
            
        
        # extraire les no de pts qui apparaissent 2 fois ou plus
        listeNoPtsDuplicate = extract_duplicates(listePtsName)
        
        # Liste qui contient tous les listes des points à display
        self.listeAllPointsToDisplay = []
        for noPtDupli in listeNoPtsDuplicate:
            
            groupeDoublons = []
            for point in self.dictPoints['points']['point']:
                
                if noPtDupli == point['pointName']:
                    groupeDoublons.append(point)
            
            self.listeAllPointsToDisplay.append(groupeDoublons)
    
        
        # générer le premier tableau
        self.generateTable()
        
        # générer un listing à coté du fichier des points
        if self.listingToGenerate: 
            self.generateListing()
        
        
        
    def nextDoublon(self):
        
        # Passer à la liste suivante
        self.count += 1
        self.generateTable()
        
    
    def previousDoublon(self):
        
        # Passer à la liste précédente
        self.count -= 1
        self.generateTable()
        
    def generateTable(self):
        
        
        # Si c'est le dernier tableau à afficher, ferme la fenêtre avec un bouton terminé
        if self.count == len(self.listeAllPointsToDisplay)-1:
            # Changer le texte en "terminé" et ferme la fenêtre
            self.buttonNext.setText('Terminé')
        else:
            self.buttonNext.setText('Suivant')
            
        # Désactiver le bouton précédent si premier tableau
        if self.count == 0:
            self.buttonPrevious.setEnabled(False)
        else:
            self.buttonPrevious.setEnabled(True)
            
            
        # après le clic sur "terminé", fermer le popup
        if self.count >= len(self.listeAllPointsToDisplay):
            
            # fermer la fenêtre 
            self.close()
            
            return None
        
        # générer le tableau
        self.tableDoublonsNoPts.setRowCount(len(self.listeAllPointsToDisplay[self.count]))
        # prendre la count-ieme liste de points à afficher 
        for row, ptData in enumerate(self.listeAllPointsToDisplay[self.count]):
            
            
            H = ptData['H'] # Possible qu'il n'y ai pas d'alitude (=None)
            if ptData['H'] == None:
                H = ''
            
            # Thème et nature si existant
            if 'themeMO' in ptData.keys():
                theme = ptData['themeMO'] if ptData['themeMO'] is not None else ''
                self.tableDoublonsNoPts.setItem(row, 4, QtWidgets.QTableWidgetItem(theme))
            if 'natureMO' in ptData.keys():
                nature = ptData['natureMO'] if ptData['natureMO'] is not None else ''
                self.tableDoublonsNoPts.setItem(row, 5, QtWidgets.QTableWidgetItem(nature))
                
            # On set les item dans la Table
            self.tableDoublonsNoPts.setItem(row, 0, QtWidgets.QTableWidgetItem(ptData['pointName']))
            self.tableDoublonsNoPts.setItem(row, 1, QtWidgets.QTableWidgetItem(ptData['E']))
            self.tableDoublonsNoPts.setItem(row, 2, QtWidgets.QTableWidgetItem(ptData['N']))
            self.tableDoublonsNoPts.setItem(row, 3, QtWidgets.QTableWidgetItem(H))
    
        
    def removeRow(self, tableWidget):
        """
        Fonction permettant de supprimer une ligne selectionée.
        """
        currentRow = tableWidget.currentRow()
        if tableWidget.rowCount() > 0: # Uniquement si il y'a au moins une row 
            tableWidget.removeRow(currentRow)
            
            # Get la data complète du point à supp.
            ptDataToDelete = self.listeAllPointsToDisplay[self.count][currentRow]
            
            # Delete de la liste à display pour ne pas le réafficher si suivant, puis précédent
            del self.listeAllPointsToDisplay[self.count][currentRow]
            
            # supprimer le point de la liste
            self.dictPoints['points']['point'].remove(ptDataToDelete)

            # recréer une fenêtre qui va refresh et MAJ sans le pt supp.
            self.windowPointsOpen.importPoints(self.dictPoints)

    
    def contextMenuEvent(self, event):
        '''
        Redéfinition de la fonction pour le menu contextuel au clic droit sur une QTable.
        Ajouter ou supprimer une row.        
        '''
        # print('MOUSE GLOBAL:', self.centralwidget.mapToGlobal(event.pos()))
        clicGlobal = self.centralwidget.mapToGlobal(event.pos())
        
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.centralwidget.mapToGlobal(self.tableDoublonsNoPts.geometry().topLeft()) # -> QPoint
        topLeftLocal = self.tableDoublonsNoPts.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableDoublonsNoPts.geometry().contains(clicGlobal-trans) :

            for i in self.tableDoublonsNoPts.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction('Supprimer la ligne selectionnée')
            action = menu.exec_(QtGui.QCursor.pos())
                
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableDoublonsNoPts)
                
                

    def generateListing(self):
        """
        Fonction qui permet de générer un listing simple des doublons.

        Returns
        -------
        None.

        """

        # arranger le nom de fichier du listing
        strListingFilePath = ''
        for elem in self.filePath.split('/')[:-1]:
            strListingFilePath += '/'+elem
        strListingFilePath += '/listingDuplicatesOfPointNames.csv'
        strListingFilePath = strListingFilePath[1:] # enlever le premier /
        
        # écrire le fichier (écrase si déjà un)
        with open(strListingFilePath,'w') as f:
            
            # en-tête
            f.write('LISTING OF POINTS WITH DUPLICATE NAME\n')
            f.write('No;E;N;\n') 
            f.write('---\n')
        
            for listePts in self.listeAllPointsToDisplay:
            
                
                for ptData in listePts:
                
                    # écrire le point
                    f.write(ptData['pointName']+';'+ptData['E']+';'+ptData['N']+'\n')
                 
                # séparer les groupes de doublons
                f.write('---\n')
        
        print('\n--- LISTING OF POINTS WITH DUPLICATE NAME EXPORTED AS',strListingFilePath)
                
                
        
        
    
    
        
        
        
            
            
        
                
            
            

                
            
            

        
        
        


        



