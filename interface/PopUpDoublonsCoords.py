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


def regrouperTuples(indices):
    """
    Fonction utilisée dans la détection des pts ayant des coordonnées proches.
    Elle converti une liste de paire d'indice pour en retrouner une liste de tuples uniques.
    """
    regroupes = []
    for indice in indices:
        groupes_existants = []
        for groupe in regroupes:
            if any(val in groupe for val in indice):
                groupes_existants.append(groupe)
        if len(groupes_existants) == 0:
            regroupes.append(tuple(indice))
        else:
            groupe_fusionne = list(set().union(*groupes_existants, indice))
            for groupe in groupes_existants:
                regroupes.remove(groupe)
            regroupes.append(tuple(groupe_fusionne))

    return regroupes






class UI_PopUpDoublonsCoords(QtWidgets.QMainWindow):
    
    def __init__(self, dictPoints, tol, windowPointsOpen, listingToGenerate, filePath):
        
        super(UI_PopUpDoublonsCoords, self).__init__()
        # Charger le ui
        uic.loadUi(os.getcwd()+"\\interface\\PopUpDoublonsCoords.ui", self)
        
        # Afficher la fenêtre
        self.show()
        
        # Init des variables de la fenêtre précédente
        self.dictPoints = dictPoints
        self.tol = tol
        self.count = 0  # variable qui s'incrémente à "suivant"
        self.windowPointsOpen = windowPointsOpen
        self.listingToGenerate = listingToGenerate
        self.filePath = filePath
        
        # détection des pts proches
        self.detectClosePoints()
        
        # connexion au bouton next et previous
        self.buttonNext.clicked.connect(self.nextDoublon)
        self.buttonPrevious.clicked.connect(self.previousDoublon)
        
        # affichage de la tolérance dans le titre
        self.groupBox.setTitle('Doublons sur les coordonnées (tol. = '+str(round(self.tol,4))+' m)')
    
    
    def detectClosePoints(self):
        """
        Fonction qui analyse la proximité de chaque point avec tous les autres points sous 
        forme de numpy array pour une optimisation de la puissance de calcul.
        Génère, via des outils matriciels, les points prochent entre eux sous la forme de tuples
        pour les lancer dans une fonction d'affichage des points proches avec interface (fonction
        generateTable).
    
        Effectue la détection uniquement en 2D. La répartition altimétrique génère extrêment souvent
        des points identique dans cette dimension.
        
        Returns
        -------
        None.

        """
        
        # Récupérer le contenu du tableau en array numpy simplifié pour
        # cette fonction
        listePts = []
        listeCoo = []
        for point in self.dictPoints['points']['point']:

            try: # si pas convertible en float, ne pas le traiter
                listePts.append(point)
                listeCoo.append([float(point['E']), float(point['N'])])
            except:
                pass
        
        listeCoo = np.array(listeCoo)
        # Extraire les coordonnées Est et Nord
        est = listeCoo[:,0]
        nord = listeCoo[:,1]
        
        # Calculer les différences entre les coordonnées Est et Nord
        diff_est = est[:, np.newaxis] - est
        diff_nord = nord[:, np.newaxis] - nord
        
        # Calculer les distances entre les points
        distances = np.sqrt(diff_est**2 + diff_nord**2)
        # Créer une matrice booléenne indiquant les points proches
        points_proches = np.abs(distances) <= self.tol
        
        # Retourner les indices des points proches (en passant par matr. triangulaire)
        # indices_proches = np.where(np.triu(points_proches, k=1))
        points_proches =  np.triu(points_proches, k=1)
        indices_proches_array = np.argwhere(points_proches == True)
    
        # regrouper les tuples
        tuples_regroupes = regrouperTuples(indices_proches_array)
        
        # Liste qui contient tous les listes des points à display
        self.listeAllPointsToDisplay = []
        
        for indicePoints in tuples_regroupes:
            
            # Liste qui contient les infos des points pour un display
            listePointsToDisplay = []
            
            for indicePt in indicePoints:
                
                # Rechercher toutes les infos du pt
                ptData = listePts[indicePt]
                listePointsToDisplay.append(ptData)

                
            self.listeAllPointsToDisplay.append(listePointsToDisplay)
        
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
        self.tableDoublonsCoo.setRowCount(len(self.listeAllPointsToDisplay[self.count]))
        # prendre la count-ieme liste de points à afficher 
        for row, ptData in enumerate(self.listeAllPointsToDisplay[self.count]):
            
            
            H = ptData['H'] # Possible qu'il n'y ai pas d'alitude (=None)
            if ptData['H'] == None:
                H = ''
            
            # Thème et nature si existant
            if 'themeMO' in ptData.keys():
                theme = ptData['themeMO'] if ptData['themeMO'] is not None else ''
                self.tableDoublonsCoo.setItem(row, 4, QtWidgets.QTableWidgetItem(theme))
            if 'natureMO' in ptData.keys():
                nature = ptData['natureMO'] if ptData['natureMO'] is not None else ''
                self.tableDoublonsCoo.setItem(row, 5, QtWidgets.QTableWidgetItem(nature))
                
            # On set les item dans la Table
            self.tableDoublonsCoo.setItem(row, 0, QtWidgets.QTableWidgetItem(ptData['pointName']))
            self.tableDoublonsCoo.setItem(row, 1, QtWidgets.QTableWidgetItem(ptData['E']))
            self.tableDoublonsCoo.setItem(row, 2, QtWidgets.QTableWidgetItem(ptData['N']))
            self.tableDoublonsCoo.setItem(row, 3, QtWidgets.QTableWidgetItem(H))
    
        
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
        topLeftGlobal = self.centralwidget.mapToGlobal(self.tableDoublonsCoo.geometry().topLeft()) # -> QPoint
        topLeftLocal = self.tableDoublonsCoo.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableDoublonsCoo.geometry().contains(clicGlobal-trans) :

            for i in self.tableDoublonsCoo.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction('Supprimer la ligne selectionnée')
            action = menu.exec_(QtGui.QCursor.pos())
                
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableDoublonsCoo)
                
                

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
        strListingFilePath += '/listingDuplicatesOfCoordinates.csv'
        strListingFilePath = strListingFilePath[1:] # enlever le premier /
        
        # écrire le fichier (écrase si déjà un)
        with open(strListingFilePath,'w') as f:
            
            # en-tête
            f.write('LISTING OF POINTS WITH DUPLICATE COORDINATES\n')
            f.write('Input tolerance to consider duplicates = ' + str(round(self.tol,4))+' m\n')
            f.write('No;E;N;\n') 
            f.write('---\n')
        
            for listePts in self.listeAllPointsToDisplay:
            
                
                for ptData in listePts:
                
                    # écrire le point
                    f.write(ptData['pointName']+';'+ptData['E']+';'+ptData['N']+'\n')
                 
                # séparer les groupes de doublons
                f.write('---\n')
        
        print('\n--- LISTING OF POINTS WITH DUPLICATE COORDINATES EXPORTED AS',strListingFilePath )
                
                
        
        
    
    
        
        
        
            
            
        
                
            
            

                
            
            

        
        
        


        



