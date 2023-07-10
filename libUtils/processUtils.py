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
    
    def __init__(self, nomsFichiers, processCtrlCoh):
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
        self.processCtrlCoh = processCtrlCoh
        
    
    def run(self):
        """
        Fonction principale de lancement du calcul.
                                                                      
        Returns
        -------
        None.

        """
        
        self.ControlesCoherence = controlesCoherenceUtils.ControlesCoherence(self.nomsFichiers, self.processCtrlCoh)
        self.checkCoherence = self.ControlesCoherence.checkTotal()
        self.ControlesCoherence.exportLog()
        
        debugPlani,debugAlti = None,None
        calculDone = False

        if self.checkCoherence : # Uniquement si le contrôle est complet
        
            # récupération des dictionnaires après contrôle
            self.dictCanevas = self.ControlesCoherence.getDictCanevas()
            self.dictPoints = self.ControlesCoherence.getDictPoints()
            self.dictParametres = self.ControlesCoherence.getDictParametres()
            
            # création objet preProcess
            self.PreProcess = preTraitementsUtils.PreProcess(self.dictCanevas, self.dictPoints, self.dictParametres)
            
            # Lancement des pré-traitements
            self.checkPreProcess = self.PreProcess.preTraitements()
            self.checkPreProcessRot = self.PreProcess.rotationsApprochees()
            self.checkPreProcessCentroids = self.PreProcess.centroidesSystemesSessions()
            self.denombrement = self.PreProcess.getDenombrement()
            
            
            if self.checkPreProcess and self.checkPreProcessRot and self.checkPreProcessCentroids : # uniquement si les étapes précédentes validées
                
                # ESTIMATION
                self.Estimation = estimationUtils.Estimation(self.dictCanevas, self.dictPoints, self.dictParametres, self.denombrement, self.nomsFichiers['dossierResultats'])
                
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