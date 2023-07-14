# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 14:44:05 2022

@author: Matteo Casto, INSIT
"""

import libUtils.controlesCoherenceUtils as controlesCoherenceUtils
import libUtils.preTraitementsUtils as preTraitementsUtils
import libUtils.estimationUtils as estimationUtils
import libUtils.conversionUtils as conversionUtils








class Process:
    
    def __init__(self, nomsFichiers, progressBar=False):
        """
        Constructeur de la classe "Process".

        Parameters
        ----------
        nomsFichiers: dictionnaire
            Contenant tous les noms de fichiers nécéssaires (input et export)
                                                                      
        Returns
        -------
        None.

        """
        
        self.nomsFichiers = nomsFichiers
        self.progressBar = progressBar
    
    def updateProgressBar(self, n):
        """
        Fonction simple qui incrémente de nla progress bar pour un calcul via la UI.

        Parameters
        ----------
        n : int
            incrément.

        Returns
        -------
        None.

        """
        
        if self.progressBar: # Si le programme est appelé en ligne de commande, pas de progressBar
            self.progressBar.setValue(self.progressBar.value() + n)
    

        
    
    def run(self):
        """
        Fonction principale de lancement du calcul.
                                                                      
        Returns
        -------
        None.

        """
        
        
        
        self.ControlesCoherence = controlesCoherenceUtils.ControlesCoherence(self.nomsFichiers)
        self.checkCoherence = self.ControlesCoherence.checkTotal()
        
        
        
        self.ControlesCoherence.exportLog()
        
        debugPlani,debugAlti = None,None
        calculDone = False

        if self.checkCoherence : # Uniquement si le contrôle est complet
        
            # récupération des dictionnaires après contrôle
            self.dictCanevas = self.ControlesCoherence.getDictCanevas()
            self.dictPoints = self.ControlesCoherence.getDictPoints()
            self.dictParametres = self.ControlesCoherence.getDictParametres()
            
            self.updateProgressBar(5)
            
            # création objet preProcess
            self.PreProcess = preTraitementsUtils.PreProcess(self.dictCanevas, self.dictPoints, self.dictParametres)
            self.updateProgressBar(5)
            
            # Lancement des pré-traitements
            self.checkPreProcess = self.PreProcess.preTraitements()
            self.updateProgressBar(5)
            self.checkPreProcessRot = self.PreProcess.rotationsApprochees()
            self.updateProgressBar(5)
            self.checkPreProcessCentroids = self.PreProcess.centroidesSystemesSessions()
            self.updateProgressBar(5)
            self.denombrement = self.PreProcess.getDenombrement()
            self.updateProgressBar(5)
            
            
            if self.checkPreProcess and self.checkPreProcessRot and self.checkPreProcessCentroids : # uniquement si les étapes précédentes validées
                
                # ESTIMATION
                self.Estimation = estimationUtils.Estimation(self.dictCanevas, self.dictPoints, self.dictParametres, self.denombrement, self.nomsFichiers['dossierResultats'], self.progressBar)
                
                self.dimensionCalcul = self.dictParametres['parameters']['computationOptions']['calculationDimension']
                if  self.dimensionCalcul == "2D" or self.dimensionCalcul == "2D+1":
                    debugPlani = self.Estimation.compensation2D()
                
                if  self.dimensionCalcul == "1D" or self.dimensionCalcul == "2D+1":
                    debugAlti= self.Estimation.compensation1D()
                    
                # Export des résultats
                self.Estimation.exportsResultats()
                calculDone = True # Variable à exploiter pour ouvrir les résultats une fois le calcul terminé
                
                print()
                print("***************************************")
                print("* ADJUSTEMENT DONE, SEE RESULT FOLDER *")
                print("***************************************")
                print('\n\n\n\n')
        
        
        
        
        return calculDone