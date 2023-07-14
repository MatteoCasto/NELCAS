# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 10:04:57 2023

@author: matteo.casto
"""


import numpy as np







def binary_matrix(matrice):
    matrice_transformee = np.where(matrice != 0, 1, 0)
    return matrice_transformee

def indices_colonnes_non_resolues(A):
    Q, R = np.linalg.qr(A)
    indices_non_resolus = np.where(np.abs(np.diag(R)) < 1e-16)[0]
    return list(indices_non_resolus), Q, R







class SolvabilityAnalysis():
    
    
    def __init__(self, M, b, listeIdCoord, limitdx, dictObs, dictPts, dictParam):
        """
        Init. variables

        Parameters
        ----------
        M : np.array
        b : np.array

        """
        
        self.M = M
        self.b = b
        self.listeIdCoord = listeIdCoord
        self.limitdx = limitdx
        self.dictObs, self.dictPts, self.dictParam = dictObs, dictPts, dictParam
        
        
        
    def findEmptyColumnsInM(self):
        """
        Function that analyses if there is any columns of the matrix 
        that contains only 0s. 

        Returns
        -------
        list(empty_columns) : list
            List that contains all index of columns that contains only 0s.

        """
        empty_columns = np.where(~self.M.any(axis=0))[0]
        
        return list(empty_columns)
    


    def findUnsolvableColumnsInM(self):
        """
        Function that analyse if some unknonws are not normally solvable with the M-matrix.
        It uses the QR decomposition the get the linae dependencies of rows.

        Returns
        -------
        indices_non_resolus : list of int
            Liste of inndex that are not normally solvable (infinite or no solution).

        """
        
        
        Q, R = np.linalg.qr(self.M)
        indices_non_resolus = np.where(np.abs(np.diag(R)) < 1e-16)[0]
        return list(indices_non_resolus)
    
    
    
    def finddxvaluesGreaterThan(self):
        """
        Function that analyses what is the index and values of dx after an iteration of
        a solvable system.
        It helps to find the unknons that don't converge to a solution 
        over the iterations.

        Returns
        -------
        dxSup : list of list
            List that contains [index, value] of dx greater than the convergence limit
            defined by user in parameters.

        """
        
        abs_dx = np.abs(self.dx)
        indices = np.where(abs_dx > self.limitdx)[0]
        # Garder uniquement les indices de coord
        indices = [index for index in indices if index in self.listeIdCoord] 
        values = self.dx[indices]
        dxSup = [[idx, val[0]] for idx, val in zip(indices, values)]
        return dxSup
    
    
    
    def searchIdUnk(self, idUnk):
        """
        Function that search in the total dataset where to find the id of the unknown.

        Parameters
        ----------
        idUnk : int
            input id of unknown to find.

        Returns
        -------
        idUnk : int
            input id of unknown.
        relatedTo : str
            exactly what is related to the idUnk (point, ori. unkn., session parameters, etc.)

        """
        
        #### IN COORDINATES
        
        for pt in self.dictPts['points']['point']:
            
            print(pt)
            # E
            if 'idUnkE' in pt.keys() and idUnk == int(pt['idUnkE']):
                print(pt)
                
        
        
        
        
        
        
        
        
        
        
        relatedTo = ''
        
        
        return idUnk, relatedTo
        
        
    
    
    
    
        
        
    
    def runAnalysis(self):
        
        # Etape 1 : analyse des colonnes vides
        self.emptyColumnsInM = self.findEmptyColumnsInM()
        
        # Etape 2 : colonnes non-résolvables avec QR
        self.unsolvedColsInM = self.findUnsolvableColumnsInM()
        
        # Etape 3 : analyse des accroissements DX
        try:
            self.dx = np.linalg.inv(self.M) @ self.b
            self.dxSup = self.finddxvaluesGreaterThan()
        except:
            self.dxSup = None
            print('singular')

    
        
        # print(self.emptyColumnsInM, self.unsolvedColsInM, self.dxSup)
        
        print('search')
        for idUnk in self.unsolvedColsInM:
            
            self.searchIdUnk(idUnk)
        
        
        
        
        
        
        
        
        
        
        







