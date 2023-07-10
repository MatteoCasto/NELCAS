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
from interface import PopUpDoublonsCoords
from interface import PopUpDoublonsNoPts




class UI_PopUpDoublons(QtWidgets.QMainWindow):
    
    def __init__(self, dictPoints, windowPointsOpen, filepath):
        
        super(UI_PopUpDoublons, self).__init__()
        # Charger le ui
        uic.loadUi(os.getcwd()+"\\interface\\PopUpDoublons.ui", self)
        
        # Afficher la fenêtre
        self.show()
        
        # dictionnaire des points:
        self.dictPoints = dictPoints
        self.filepath = filepath
        
        # objet fenêtre des points ouverte
        self.windowPointsOpen = windowPointsOpen
        
        # connecter les boutons
        self.buttonRunDoublonsNoPts.clicked.connect(self.runDoublonsNoPts)
        self.buttonRunDoublonsCoo.clicked.connect(self.runDoublonsCoo)
        
    
    def runDoublonsNoPts(self):
        """
        Bouton s'activant au clic "lancer" pour les doublons de no de points.

        Returns
        -------
        None.

        """
        
        # Init la fenêtre de pop up sur les doublons de no de pts
        self.PopUpDoublonsNoPts = PopUpDoublonsNoPts.UI_PopUpDoublonsNoPts(self.dictPoints,
                                                                           self.windowPointsOpen,
                                                                           self.checkBoxListing.isChecked(),
                                                                           self.filepath)
        
    
        
        
        
    def runDoublonsCoo(self):
        """
        Bouton s'activant au clic "lancer" pour les doublons de coordonnées.

        Returns
        -------
        None : si la case tolérance n'est pas un float.

        """
        
        # Condition si float
        try:
            tol = float(self.inputTolerance.text()) 
        except:
            print('INCORRECT VALUE OF TOLERANCE')
            return None

        
        # Init la fenêtre de pop up sur les doublons de coordonnées
        self.PopUpDoublonsCoords = PopUpDoublonsCoords.UI_PopUpDoublonsCoords(self.dictPoints, 
                                                                              tol, 
                                                                              self.windowPointsOpen,
                                                                              self.checkBoxListing.isChecked(),
                                                                              self.filepath)
        
        # ferme ce pop-up 
        self.close()
        
        

        
        
        


        



