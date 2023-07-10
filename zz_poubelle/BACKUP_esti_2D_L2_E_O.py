# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 17:10:42 2022

@author: Matteo Casto, INSIT
"""

import libUtils.rechercheUtils as rechercheUtils
import libUtils.geometrieUtils as geometrieUtils
from scipy import sparse
from scipy.sparse import linalg
import numpy as np
import copy
import xmltodict
import time
import datetime
import matplotlib.pyplot as plt




def derivee_partielle(fonction,variables,x,dx):
    
    """
    Fonction permettant de calculer la dérivée partielle de n'importe quelle fonction à plusieurs variables.
    Principalement utilisée pour le remplissage des matrices jacobiennes A et C.
    
    Parameters
    ----------
    fonction: fonction
        nom de la fonction à dériver (variable).
    variables: dictionnaire
        contenant les variables et leurs valeurs.
    x : string
        nom de la variable selon laquelle dériver partiellement.
    dx : float
        incrément, en général 0.00001.
   
    Returns
    -------
    derivée partielle : float
        valeur de la dérivée partielle. 
    """
    
    variables_x_plus_dx = copy.deepcopy(variables)
    variables_x_plus_dx[x] += dx
    f_x_plus_dx = fonction(variables_x_plus_dx)
    f_x = fonction(variables)
    
    return (f_x_plus_dx - f_x)/dx




            
            
            
        
        
    
  


def estimation2D(dictCanevas, dictPoints, dictParametres, denombrement, dictResGlobaux):
    
    """
    Fonction de l'estimation 2D principale.
    
    Parameters
    ----------
    dictCanevas, dictPoints, dictParametres : dictionnaires
        dictionnaires input pré-traités.
    denombrement : dictionnaire.
        dictionnaire contenant le dénombrement du réseau (issu des prés-traitements).
    
    """
    
    timer = time.time()

    #### PARAMETRES GENERAUX
    nbrIterationMax = int(dictParametres['parametresCalcul']['optionsCalcul']['nbrIterationMax'])
    critereInterruption = float(dictParametres['parametresCalcul']['optionsCalcul']['critereInterruption'])
    robuste = dictParametres['parametresCalcul']['optionsCalcul']['robuste']
    robuste = True if robuste=="true" else False
    cRobuste = dictParametres['parametresCalcul']['optionsCalcul']['limiteRobuste']
    if cRobuste == None:
        dictParametres['parametresCalcul']['optionsCalcul']['limiteRobuste'] = 3.5 # par défaut
        cRobuste = 3.5
    else:
        cRobuste = float(cRobuste)
    sigma0 = 1.0
    
    # Dénombrement
    nbObsPlani, nbIncPlani, nbConPlani = denombrement['nbObsPlani'], denombrement['nbIncPlani'], denombrement['nbConPlani']
    
    # Liste des index de coordonnées (pour calculer max(dx) uniq. sur les coordonnées)
    listeIdCoord = []
    logIterations = ''
    
    
    #### INITIALISATION DES  MATRICES (scipy.sparses ou np.array)
    # A = sparse.csr_matrix((nbObsPlani, nbIncPlani)) # n x u
    A = np.zeros(shape=(nbObsPlani,nbIncPlani), dtype=np.float32) # n x u
    C = np.zeros(shape=(nbConPlani, nbIncPlani)) # c x u
    cx0 = np.zeros(shape=(nbConPlani,1)) # c x 1
    Kll = np.zeros(shape=(nbObsPlani)) # n x 1 (diagonale d'une matrice n x n)
    f0 = np.zeros(shape=(nbObsPlani,1)) # n x 1
    dl = np.zeros(shape=(nbObsPlani,1)) # n x 1
    x0 = np.zeros(shape=(nbIncPlani,1)) # u x 1
    w = np.zeros(shape=(nbObsPlani)) # n x 1 (diagonale d'une matrice n x n)
    W = np.ones(shape=(nbObsPlani))# n x 1 (diagonale d'une matrice n x n)
    sparseZcc = sparse.csc_matrix((nbConPlani,nbConPlani))
    nabla = np.zeros(shape=(nbObsPlani,1),dtype=np.float32)
    
    
    # -----------------------------------------
    #### REMPLISSAGE DES MATRICES ET ITERATIONS
    # -----------------------------------------
    
    # Boucle de calcul principale 
    cont = True
    iteration = 0
    
    
    while cont :
    
        
        #### ^----- LEVES POLAIRES
        
        if "polaire" in dictCanevas['canevas'].keys():
            
            
            for station in dictCanevas['canevas']['polaire']['station']:
                
                
                #### ^--------- INDEX ET VALEURS DES INCONNUES
                # index des paramètres inc. supplémentaire distances
                
                
                # FACTEUR ECHELLE
                groupeDistance = rechercheUtils.rechercheGroupeParNom(dictParametres, station['stationnement']['groupeDistance'])
                if "idIncFacteurEchelle" in groupeDistance['inconnuesSupplementaires'].keys():
                    
                    idIncFacteurEchelle = groupeDistance['inconnuesSupplementaires']['idIncFacteurEchelle']
                    if iteration == 0:
                        m0 = groupeDistance['inconnuesSupplementaires']['valIncFacteurEchelle']
                        x0[idIncFacteurEchelle,0] = m0
                    else: # itérations suivantes, prendre la valeur de x0
                        m0 = x0[idIncFacteurEchelle,0]
                        
                else: # Si pas à calculer
                    idIncFacteurEchelle = None
                    m0 = 0.0
                    
                    
                # CONSTANTE ADDITION
                if "idIncConstanteAddition" in groupeDistance['inconnuesSupplementaires'].keys():
                    
                    idIncConstanteAddition = groupeDistance['inconnuesSupplementaires']['idIncConstanteAddition']
                    if iteration == 0:
                        c0 = groupeDistance['inconnuesSupplementaires']['valIncConstanteAddition']
                        x0[idIncConstanteAddition,0] = c0
                    else: # itérations suivantes, prendre la valeur de x0
                        c0 = x0[idIncConstanteAddition,0]
                        
                else: # Si pas à calculer
                    idIncConstanteAddition = None
                    c0 = 0.0
                    
                     
                # INCONNUE ORIENTATION
                idIncOri = station['stationnement']['idIncOri']
                if iteration == 0:
                    w0 = station['stationnement']['valIncOri']
                    x0[idIncOri,0] = w0
                else: # itérations suivantes, prendre la valeur de x0
                    w0 = x0[idIncOri,0]
                    
                
                # COORDONNEES DE STATION
                pointStation = rechercheUtils.rechercheNoPt(dictPoints, station['numeroStation'])
                if "idIncE" in pointStation.keys() and "idIncN" in pointStation.keys() :
                    
                    idIncStaE, idIncStaN = pointStation['idIncE'], pointStation['idIncN']
                    if iteration == 0:
                        Esta, Nsta = float(pointStation['E']), float(pointStation['N'])
                        x0[idIncStaE,0], x0[idIncStaN,0] = Esta, Nsta 
                        listeIdCoord.append(idIncStaE)
                        listeIdCoord.append(idIncStaN)
                    else: # itérations suivantes, prendre la valeur de x0
                        Esta, Nsta = x0[idIncStaE,0], x0[idIncStaN,0]
                        
                else: # si station sur pt fixe
                    idIncStaE, idIncStaN = None, None 
                    Esta, Nsta = float(pointStation['E']), float(pointStation['N'])
                
                
                
                
                
                #### ^--------- INDEX ET VALEURS DES OBS.
                
                for observation in station['stationnement']['observation']:
                    
                    # COORDONNEES DU POINT VISE
                    pointVis = rechercheUtils.rechercheNoPt(dictPoints, observation['numeroPoint'])
                    if "idIncE" in pointVis.keys() and "idIncN" in pointVis.keys() :
                        
                        idIncVisE, idIncVisN = pointVis['idIncE'], pointVis['idIncN']
                        if iteration == 0:
                            Evis, Nvis = float(pointVis['E']), float(pointVis['N'])
                            x0[idIncVisE,0], x0[idIncVisN,0] = Evis, Nvis
                            listeIdCoord.append(idIncVisE)
                            listeIdCoord.append(idIncVisN)
                        else: # itérations suivantes, prendre la valeur de x0
                            Evis, Nvis = x0[idIncVisE,0], x0[idIncVisN,0]
                            
                    else: # si point visé est fixe
                        idIncVisE, idIncVisN = None, None 
                        Evis, Nvis = float(pointVis['E']), float(pointVis['N'])       
                            
                    
                    # INDEX OBSERVATIONS RI ET DP
                    if "idObsPlani" in observation['RI'].keys():
                        idObsRI = observation['RI']['idObsPlani']
                    else:
                        idObsRI = None
                    if "idObsPlani" in observation['DP'].keys():
                        idObsDP = observation['DP']['idObsPlani']
                    else:
                        idObsDP = None
                    
                    
                    
                                       
                    #### ^--------- MATRICE A, dl et Kll
                    
                    # delta coord dans les formules de dérivées partielles
                    DE, DN = Evis-Esta, Nvis-Nsta
                    D0 = DN**2+DE**2
                    
                    
                    # DIRECTION RI
                    if idObsRI != None:
                        
                        # Matrice A
                        if idIncStaE != None:
                            A[idObsRI,idIncStaE] = -DN/D0*200.0/np.pi
                        if idIncStaN != None:
                            A[idObsRI,idIncStaN] = DE/D0*200.0/np.pi
                        if idIncVisE != None:
                            A[idObsRI,idIncVisE] = DN/D0*200.0/np.pi
                        if idIncVisN != None:
                            A[idObsRI,idIncVisN] = -DE/D0*200.0/np.pi
                        A[idObsRI,idIncOri] = -1 # inc. ori toujours calculée
                    
                        # Matrice dl (avec adaptations valeurs sur intervalle 0-400)
                        obsRI = float(observation['RI']['valeur'])
                        if w0 < 0.0:
                            w0 = np.mod( np.arctan2(DE,DN)*200.0/np.pi - obsRI , 400.0)
                            x0[idIncOri,0] = w0
                        f0 = np.mod( np.arctan2(DE,DN)*200.0/np.pi - w0, 400.0)
                        obsRIred = obsRI - f0
                        if obsRIred < -200.0:
                            obsRIred += 400.0
                        if obsRIred > 200.0:
                            obsRIred -= 400.0    
                        dl[idObsRI,0] = obsRIred
                        
                        # Matrice Kll
                        Kll[idObsRI] = observation['RI']['ecartType']**2
                        
                
                    # DISTANCES DP
                    if idObsDP != None:
                        
                        # Matrice A
                        if idIncStaE != None:
                            A[idObsDP,idIncStaE] = -DE/np.sqrt(D0)
                        if idIncStaN != None:
                            A[idObsDP,idIncStaN] = -DN/np.sqrt(D0)
                        if idIncVisE != None:
                            A[idObsDP,idIncVisE] = DE/np.sqrt(D0)
                        if idIncVisN != None:
                            A[idObsDP,idIncVisN] = DN/np.sqrt(D0)
                        if idIncConstanteAddition != None:
                            A[idObsDP,idIncConstanteAddition] = -1 
                        if idIncFacteurEchelle != None:
                            A[idObsDP,idIncFacteurEchelle] = -np.sqrt(D0)
                            
                        # Matrice dl
                        obsDP = float(observation['DP']['valeur'])
                        f0 = np.sqrt(DN**2+DE**2) -c0 -(m0*np.sqrt(DN**2+DE**2))
                        dl[idObsDP,0] = obsDP-f0
                        
                        # Matrice Kll
                        Kll[idObsDP] = observation['DP']['ecartType']**2
                        
                        
        
        
        
        #### ^----- GNSS
        
        if "GNSS" in dictCanevas['canevas'].keys():
        
            for session in dictCanevas['canevas']['GNSS']['session']:
                
                #### ^--------- INDEX ET VALEURS DES INCONNUES
                
                paramInconnus = session['parametresInconnus']
                
                
                # TRANSLATION E
                if "idIncTranslationE" in paramInconnus.keys():
                    
                    idIncTranslationE = paramInconnus['idIncTranslationE']
                    if iteration == 0:
                        tE0 = paramInconnus['valIncTranslationE']
                        x0[idIncTranslationE,0] = tE0
                    else: # autres itérations, prendre la valeur de x0
                        tE0 = x0[idIncTranslationE,0]
                
                else: # si fixe
                    idIncTranslationE = None
                    tE0 = 0.0
                    
    
                # TRANSLATION N
                if "idIncTranslationN" in paramInconnus.keys():
                    
                    idIncTranslationN = paramInconnus['idIncTranslationN']
                    if iteration == 0:
                        tN0 = paramInconnus['valIncTranslationN']
                        x0[idIncTranslationN,0] = tN0
                    else: # autres itérations, prendre la valeur de x0
                        tN0 = x0[idIncTranslationN,0]
                        
                else: # si fixe
                    idIncTranslationN = None
                    tN0 = 0.0
                    
                    
                # ROTATION HORIZ
                if "idIncRotationHoriz" in paramInconnus.keys():
                    
                    idIncRotationHoriz = paramInconnus['idIncRotationHoriz']
                    if iteration == 0:
                        rot0 = paramInconnus['valIncRotationHoriz']
                        if rot0 < 0.0:
                            rot0 = np.mod(rot0, 400.0)
                            paramInconnus['valIncRotationHoriz'] = rot0
                        x0[idIncRotationHoriz,0] = rot0
                    else: # autres itérations, prendre la valeur de x0
                        rot0 = x0[idIncRotationHoriz,0]
                        
                else: # si fixe
                    idIncRotationHoriz = None
                    rot0 = 0.0
                
                
                # FACTEUR ECHELLE HORIZ
                if "idIncFacteurEchelleHoriz" in paramInconnus.keys():
                    
                    idIncFacteurEchelleHoriz = paramInconnus['idIncFacteurEchelleHoriz']
                    if iteration == 0:
                        lam0 = paramInconnus['valIncFacteurEchelleHoriz']
                        x0[idIncFacteurEchelleHoriz,0] = lam0
                    else: # autres itérations, prendre la valeur de x0
                        lam0 = x0[idIncFacteurEchelleHoriz,0]
                        
                else: # si fixe
                    idIncFacteurEchelleHoriz = None
                    lam0 = 1.0
                    
                
                
                #### ^--------- INDEX ET VALEURS DES OBS. ET INC. COORD.
                
                for observation in session['observation']:
                    
                    # COORDONEES DU POINT VISE
                    pointVis = rechercheUtils.rechercheNoPt(dictPoints, observation['numeroPoint'])
                    if "idIncE" in pointVis.keys() and "idIncN" in pointVis.keys() :
                        
                        idIncVisE, idIncVisN = pointVis['idIncE'], pointVis['idIncN']
                        if iteration == 0:
                            Evis, Nvis = float(pointVis['E']), float(pointVis['N'])
                            x0[idIncVisE,0], x0[idIncVisN,0] = Evis, Nvis
                            listeIdCoord.append(idIncVisE)
                            listeIdCoord.append(idIncVisN)
                        else: # itérations suivantes, prendre la valeur de x0
                            Evis, Nvis = x0[idIncVisE,0], x0[idIncVisN,0]
                            
                    else: # si point visé est fixe
                        idIncVisE, idIncVisN = None, None 
                        Evis, Nvis = float(pointVis['E']), float(pointVis['N'])       
                        
                        
                    # récupération des index RI et DP (si pas écarté)
                    if "idObsPlani" in observation['LY'].keys():
                        idObsLY = observation['LY']['idObsPlani']
                    else:
                        idObsLY = None
                    if "idObsPlani" in observation['LX'].keys():
                        idObsLX = observation['LX']['idObsPlani']
                    else:
                        idObsLX = None
                       
                    # Réduction aux coordonnées moyennes globales (correspondent au dernier point de la session pour être dans la zone)
                    # -> stabilité de calcul
                    Evis, Nvis = Evis - session['moyEglobal'], Nvis - session['moyNglobal']
                    
                        
                    
                    #### ^--------- MATRICE A, dl et Kll
                    
                    # LOCAL LY
                    if idObsLY != None:
                        
                        # Matrice A
                        if idIncVisE != None:
                            A[idObsLY,idIncVisE] = lam0*np.cos(rot0*np.pi/200.0)
                        if idIncVisN != None:
                            A[idObsLY,idIncVisN] = -lam0*np.sin(rot0*np.pi/200.0)
                        if idIncTranslationE != None:
                            A[idObsLY,idIncTranslationE] = 1.0
                        if idIncTranslationN != None:
                            A[idObsLY,idIncTranslationN] = 0.0
                        if idIncRotationHoriz != None:
                            A[idObsLY,idIncRotationHoriz] = -lam0*np.sin(rot0*np.pi/200.0)*Evis - lam0*np.cos(rot0*np.pi/200.0)*Nvis
                        if idIncFacteurEchelleHoriz != None:
                            A[idObsLY,idIncFacteurEchelleHoriz] = np.cos(rot0*np.pi/200.0)*Evis - np.sin(rot0*np.pi/200.0)*Nvis
                        
                        # Matrice dl
                        obsLY = float(observation['LY']['valeur'])  - session['moyEglobal']
                        f0 = tE0 + lam0*np.cos(rot0*np.pi/200.0)*Evis - lam0*np.sin(rot0*np.pi/200.0)*Nvis
                        dl[idObsLY,0] = obsLY-f0
                        
                        # Matrice Kll
                        Kll[idObsLY] = observation['LY']['ecartType']**2
                        
                        
                    # LOCAL LX
                    if idObsLX != None:    
                        
                        # Matrice A
                        if idIncVisE != None:
                            A[idObsLX,idIncVisE] = lam0*np.sin(rot0*np.pi/200.0)
                        if idIncVisN != None:
                            A[idObsLX,idIncVisN] = lam0*np.cos(rot0*np.pi/200.0)
                        if idIncTranslationE != None:
                            A[idObsLX,idIncTranslationE] = 0.0
                        if idIncTranslationN != None:
                            A[idObsLX,idIncTranslationN] = 1.0
                        if idIncRotationHoriz != None:
                            A[idObsLX,idIncRotationHoriz] = lam0*np.cos(rot0*np.pi/200.0)*Evis - lam0*np.sin(rot0*np.pi/200.0)*Nvis
                        if idIncFacteurEchelleHoriz != None:
                            A[idObsLX,idIncFacteurEchelleHoriz] = np.sin(rot0*np.pi/200.0)*Evis + np.cos(rot0*np.pi/200.0)*Nvis
                        
                        # Matrice dl
                        obsLX = float(observation['LX']['valeur'])  - session['moyNglobal']
                        f0 = tN0 + lam0*np.sin(rot0*np.pi/200.0)*Evis + lam0*np.cos(rot0*np.pi/200.0)*Nvis
                        dl[idObsLX,0] = obsLX-f0
                        
                        # Matrice Kll
                        Kll[idObsLX] = observation['LX']['ecartType']**2
                        
                        
            
                        
            
        #### ^----- SYSTEMES LOCAUX
        
        if "systemesLocaux" in dictCanevas['canevas'].keys():
        
            for systeme in dictCanevas['canevas']['systemesLocaux']['systemeLocal']:
                
                #### ^--------- INDEX ET VALEURS DES INCONNUES
                
                paramInconnus = systeme['parametresInconnus']
                
                # TRANSLATION E
                if "idIncTranslationE" in paramInconnus.keys():
                    
                    idIncTranslationE = paramInconnus['idIncTranslationE']
                    if iteration == 0:
                        tE0 = paramInconnus['valIncTranslationE']
                        x0[idIncTranslationE,0] = tE0 
                    else: # autres itérations, prendre la valeur de x0
                        tE0 = x0[idIncTranslationE,0] 
                
                else: # si fixe
                    idIncTranslationE = None
                    tE0 = 0.0
                      
                # TRANSLATION N
                if "idIncTranslationN" in paramInconnus.keys():
                    
                    idIncTranslationN = paramInconnus['idIncTranslationN']
                    if iteration == 0:
                        tN0 = paramInconnus['valIncTranslationN'] 
                        x0[idIncTranslationN,0] = tN0 
                    else: # autres itérations, prendre la valeur de x0
                        tN0 = x0[idIncTranslationN,0] 
                        
                else: # si fixe
                    idIncTranslationN = None
                    tN0 = 0.0
                    
                    
                # ROTATION HORIZ
                if "idIncRotationHoriz" in paramInconnus.keys():
                    
                    idIncRotationHoriz = paramInconnus['idIncRotationHoriz']
                    if iteration == 0:
                        rot0 = paramInconnus['valIncRotationHoriz']
                        x0[idIncRotationHoriz,0] = rot0
                    else: # autres itérations, prendre la valeur de x0
                        rot0 = x0[idIncRotationHoriz,0]
                        
                else: # si fixe
                    idIncRotationHoriz = None
                    rot0 = 0.0
                
                
                # FACTEUR ECHELLE HORIZ
                if "idIncFacteurEchelleHoriz" in paramInconnus.keys():
                    
                    idIncFacteurEchelleHoriz = paramInconnus['idIncFacteurEchelleHoriz']
                    if iteration == 0:
                        lam0 = paramInconnus['valIncFacteurEchelleHoriz']
                        x0[idIncFacteurEchelleHoriz,0] = lam0
                    else: # autres itérations, prendre la valeur de x0
                        lam0 = x0[idIncFacteurEchelleHoriz,0]
                        
                else: # si fixe
                    idIncFacteurEchelleHoriz = None
                    lam0 = 1.0


                    
                #### ^--------- INDEX ET VALEURS DES OBS. ET INC. COORD.
                
                for observation in systeme['observation']:
                    
                    # COORDONEES DU POINT VISE
                    pointVis = rechercheUtils.rechercheNoPt(dictPoints, observation['numeroPoint'])
                    if "idIncE" in pointVis.keys() and "idIncN" in pointVis.keys() :
                        
                        idIncVisE, idIncVisN = pointVis['idIncE'], pointVis['idIncN']
                        if iteration == 0:
                            Evis, Nvis = float(pointVis['E']), float(pointVis['N'])
                            x0[idIncVisE,0], x0[idIncVisN,0] = Evis, Nvis
                            listeIdCoord.append(idIncVisE)
                            listeIdCoord.append(idIncVisN)
                        else: # itérations suivantes, prendre la valeur de x0
                            Evis, Nvis = x0[idIncVisE,0], x0[idIncVisN,0]
                            
                            
                    else: # si point visé est fixe
                        idIncVisE, idIncVisN = None, None 
                        Evis, Nvis = float(pointVis['E']), float(pointVis['N'])  
                        
                        
                    # récupération des index RI et DP (si pas écarté)
                    if "idObsPlani" in observation['LY'].keys():
                        idObsLY = observation['LY']['idObsPlani']
                    else:
                        idObsLY = None
                    if "idObsPlani" in observation['LX'].keys():
                        idObsLX = observation['LX']['idObsPlani']
                    else:
                        idObsLX = None
                        
                    
                    # Réduction aux coordonnées moyennes globales (correspondent au dernier point de la session pour être dans la zone)
                    # -> stabilité de calcul
                    Evis, Nvis = Evis - systeme['moyEglobal'], Nvis - systeme['moyNglobal']
                    
                    
                    #### ^--------- MATRICE A, dl et Kll
                    
                    # LOCAL LY
                    if idObsLY != None:
                        
                        # Matrice A
                        if idIncVisE != None:
                            A[idObsLY,idIncVisE] = lam0*np.cos(rot0*np.pi/200.0)
                        if idIncVisN != None:
                            A[idObsLY,idIncVisN] = -lam0*np.sin(rot0*np.pi/200.0)
                        if idIncTranslationE != None:
                            A[idObsLY,idIncTranslationE] = 1.0
                        if idIncTranslationN != None:
                            A[idObsLY,idIncTranslationN] = 0.0
                        if idIncRotationHoriz != None:
                            A[idObsLY,idIncRotationHoriz] = -lam0*np.sin(rot0*np.pi/200.0)*Evis - lam0*np.cos(rot0*np.pi/200.0)*Nvis
                        if idIncFacteurEchelleHoriz != None:
                            A[idObsLY,idIncFacteurEchelleHoriz] = np.cos(rot0*np.pi/200.0)*Evis - np.sin(rot0*np.pi/200.0)*Nvis
                         
                        # Matrice dl
                        obsLY = float(observation['LY']['valeur']) 
                        f0 = tE0 + lam0*np.cos(rot0*np.pi/200.0)*Evis - lam0*np.sin(rot0*np.pi/200.0)*Nvis 
                        dl[idObsLY,0] = obsLY-f0
                        
                        # Matrice Kll
                        Kll[idObsLY] = observation['LY']['ecartType']**2
                            
                        
                    # LOCAL LX
                    if idObsLX != None:    
                        
                        # Matrice A
                        if idIncVisE != None:
                            A[idObsLX,idIncVisE] = lam0*np.sin(rot0*np.pi/200.0)
                        if idIncVisN != None:
                            A[idObsLX,idIncVisN] = lam0*np.cos(rot0*np.pi/200.0)
                        if idIncTranslationE != None:
                            A[idObsLX,idIncTranslationE] = 0.0
                        if idIncTranslationN != None:
                            A[idObsLX,idIncTranslationN] = 1.0
                        if idIncRotationHoriz != None:
                            A[idObsLX,idIncRotationHoriz] = lam0*np.cos(rot0*np.pi/200.0)*Evis - lam0*np.sin(rot0*np.pi/200.0)*Nvis
                        if idIncFacteurEchelleHoriz != None:
                            A[idObsLX,idIncFacteurEchelleHoriz] = np.sin(rot0*np.pi/200.0)*Evis + np.cos(rot0*np.pi/200.0)*Nvis
                        
                        # Matrice dl
                        obsLX = float(observation['LX']['valeur']) 
                        f0 = tN0 + lam0*np.sin(rot0*np.pi/200.0)*Evis + lam0*np.cos(rot0*np.pi/200.0)*Nvis 
                        dl[idObsLX,0] = obsLX-f0
                        
                        # Matrice Kll
                        Kll[idObsLX] = observation['LX']['ecartType']**2
                    
            
               
            
            
            #### ^----- COTES
            
            if "cotes" in dictCanevas['canevas'].keys():
                
                for cote in dictCanevas['canevas']['cotes']['cote']:
                    
                    observation = cote['observation']
                    
                    #### ^--------- INDEX ET VALEURS DES INCONNUES
                    
                    # COORDONEES DU POINT VISE NO 1
                    pointVis1 = rechercheUtils.rechercheNoPt(dictPoints, observation['numeroPoint1'])
                    if "idIncE" in pointVis1.keys() and "idIncN" in pointVis1.keys() :
                        
                        idIncVisE1, idIncVisN1 = pointVis1['idIncE'], pointVis1['idIncN']
                        if iteration == 0:
                            Evis1, Nvis1 = float(pointVis1['E']), float(pointVis1['N'])
                            x0[idIncVisE1,0], x0[idIncVisN1,0] = Evis1, Nvis1
                            listeIdCoord.append(idIncVisE1)
                            listeIdCoord.append(idIncVisN1)
                        else: # itérations suivantes, prendre la valeur de x0
                            Evis1, Nvis1 = x0[idIncVisE1,0], x0[idIncVisN1,0]
                            
                    else: # si point visé est fixe
                        idIncVisE1, idIncVisN1 = None, None 
                        Evis1, Nvis1 = float(pointVis1['E']), float(pointVis1['N'])  
                    
                    # COORDONEES DU POINT VISE NO 2
                    pointVis2 = rechercheUtils.rechercheNoPt(dictPoints, observation['numeroPoint2'])
                    if "idIncE" in pointVis2.keys() and "idIncN" in pointVis2.keys() :
                        
                        idIncVisE2, idIncVisN2 = pointVis2['idIncE'], pointVis2['idIncN']
                        if iteration == 0:
                            Evis2, Nvis2 = float(pointVis2['E']), float(pointVis2['N'])
                            x0[idIncVisE2,0], x0[idIncVisN2,0] = Evis2, Nvis2
                            listeIdCoord.append(idIncVisE2)
                            listeIdCoord.append(idIncVisN2)
                        else: # itérations suivantes, prendre la valeur de x0
                            Evis2, Nvis2 = x0[idIncVisE2,0], x0[idIncVisN2,0]
                            
                    else: # si point visé est fixe
                        idIncVisE2, idIncVisN2 = None, None 
                        Evis2, Nvis2 = float(pointVis2['E']), float(pointVis2['N'])  
                        
                    
                    # récupération des index DP (si pas écarté)
                    if "idObsPlani" in observation['DP'].keys():
                        idObsDP = observation['DP']['idObsPlani']
                    else:
                        idObsDP = None
                        
                
                    #### ^--------- MATRICE A, dl et Kll
                    
                    # delta coord dans les formules de dérivées partielles
                    DE, DN = Evis2-Evis1, Nvis2-Nvis1
                    D0 = DN**2+DE**2
                    
                    # DISTANCES DP
                    if idObsDP != None:
                        
                        # Matrice A
                        if idIncVisE1 != None:
                            A[idObsDP,idIncVisE1] = -DE/np.sqrt(D0)
                        if idIncVisN1 != None:
                            A[idObsDP,idIncVisN1] = -DN/np.sqrt(D0)
                        if idIncVisE2 != None:
                            A[idObsDP,idIncVisE2] = DE/np.sqrt(D0)
                        if idIncVisN2 != None:
                            A[idObsDP,idIncVisN2] = DN/np.sqrt(D0)
                            
                        # Matrice dl
                        obsDP = float(observation['DP']['valeur'])
                        f0 = np.sqrt(DN**2+DE**2) 
                        dl[idObsDP,0] = obsDP-f0
                        
                        # Matrice Kll
                        Kll[idObsDP] = observation['DP']['ecartType']**2
                        
                
                    
             
                    
        #### ^----- CONTRAINTES    
        
        if "contraintes" in dictCanevas['canevas'].keys():
            
            for contrainte in dictCanevas['canevas']['contraintes']['contrainte']:
                
                # Si non-écartée
                if contrainte['ecarte'] == "false":
                    
                    # Points et index des inc. de coordonnées
                    pointA = rechercheUtils.rechercheNoPt(dictPoints, contrainte['numeroPointA'])
                    pointB = rechercheUtils.rechercheNoPt(dictPoints, contrainte['numeroPointB'])
                    pointP = rechercheUtils.rechercheNoPt(dictPoints, contrainte['numeroPointP'])
                    
                    
                    # COORDONEES DU POINT VISE A
                    if "idIncE" in pointA.keys() and "idIncN" in pointA.keys() :
                        
                        idIncVisEA, idIncVisNA = pointA['idIncE'], pointA['idIncN']
                        if iteration == 0:
                            EvisA, NvisA = float(pointA['E']), float(pointA['N'])
                            x0[idIncVisEA,0], x0[idIncVisNA,0] = EvisA, NvisA
                            listeIdCoord.append(idIncVisEA)
                            listeIdCoord.append(idIncVisNA)
                        else: # itérations suivantes, prendre la valeur de x0
                            EvisA, NvisA = x0[idIncVisEA,0], x0[idIncVisNA,0]
                            
                    else: # si point visé est fixe
                        idIncVisEA, idIncVisNA = None, None 
                        EvisA, NvisA = float(pointA['E']), float(pointA['N'])  
                        
                    
                    # COORDONEES DU POINT VISE B
                    if "idIncE" in pointB.keys() and "idIncN" in pointB.keys() :
                        
                        idIncVisEB, idIncVisNB = pointB['idIncE'], pointB['idIncN']
                        if iteration == 0:
                            EvisB, NvisB = float(pointB['E']), float(pointB['N'])
                            x0[idIncVisEB,0], x0[idIncVisNB,0] = EvisB, NvisB
                            listeIdCoord.append(idIncVisEB)
                            listeIdCoord.append(idIncVisNB)
                        else: # itérations suivantes, prendre la valeur de x0
                            EvisB, NvisB = x0[idIncVisEB,0], x0[idIncVisNB,0]
                            
                    else: # si point visé est fixe
                        idIncVisEB, idIncVisNB = None, None 
                        EvisB, NvisB = float(pointB['E']), float(pointB['N'])  
                    
                    
                    # COORDONEES DU POINT VISE P
                    if "idIncE" in pointP.keys() and "idIncN" in pointP.keys() :
                        
                        idIncVisEP, idIncVisNP = pointP['idIncE'], pointP['idIncN']
                        if iteration == 0:
                            EvisP, NvisP = float(pointP['E']), float(pointP['N'])
                            x0[idIncVisEP,0], x0[idIncVisNP,0] = EvisP, NvisP
                            listeIdCoord.append(idIncVisEP)
                            listeIdCoord.append(idIncVisNP)
                        else: # itérations suivantes, prendre la valeur de x0
                            EvisP, NvisP = x0[idIncVisEP,0], x0[idIncVisNP,0]
                            
                    else: # si point visé est fixe
                        idIncVisEP, idIncVisNP = None, None 
                        EvisP, NvisP = float(pointP['E']), float(pointP['N'])  
                   
                    # déplacement parralèle dm1 pour les alignement
                    dm1 = contrainte['dm1']['valeur']
                    if dm1 == None:
                        dm1 = 0.0
                    else:
                        dm1 = float(dm1)
                        
                        
                    # Sous-dictionnaire simplifié de la contrainte
                    incContrainte = {}
                    incContrainte.update({'Ea':EvisA})
                    incContrainte.update({'Na':NvisA})
                    incContrainte.update({'Eb':EvisB})
                    incContrainte.update({'Nb':NvisB})
                    incContrainte.update({'Ep':EvisP})
                    incContrainte.update({'Np':NvisP})
                    incContrainte.update({'dm1':dm1})
                    
                    
                    #### ^--------- MATRICE C et cx0
                    
                    # Alignement
                    if contrainte['typeContrainte'] == "alignement":
                        
                        # Id de la contraintre et matrice cx0
                        idCon = contrainte['idConPlani']
                        cx0[idCon,0] = geometrieUtils.pointAligne(incContrainte)
                        
                        # Matrice C
                        if idIncVisEA != None:
                            C[idCon,idIncVisEA] = derivee_partielle(geometrieUtils.pointAligne, incContrainte, 'Ea', 0.000001)
                        if idIncVisNA != None:
                            C[idCon,idIncVisNA] = derivee_partielle(geometrieUtils.pointAligne, incContrainte, 'Na', 0.000001)
                        if idIncVisEB != None:
                            C[idCon,idIncVisEB] = derivee_partielle(geometrieUtils.pointAligne, incContrainte, 'Eb', 0.000001)
                        if idIncVisNB != None:
                            C[idCon,idIncVisNB] = derivee_partielle(geometrieUtils.pointAligne, incContrainte, 'Nb', 0.000001)
                        if idIncVisEP != None:    
                            C[idCon,idIncVisEP] = derivee_partielle(geometrieUtils.pointAligne, incContrainte, 'Ep', 0.000001)
                        if idIncVisNP != None:    
                            C[idCon,idIncVisNP] = derivee_partielle(geometrieUtils.pointAligne, incContrainte, 'Np', 0.000001)
                        
                        
                    
                    # Perpendiculaire
                    if contrainte['typeContrainte'] == "perpendiculaire":
                        
                        # Id de la contraintre et matrice cx0
                        idCon = contrainte['idConPlani']
                        cx0[idCon,0] = geometrieUtils.droitePerpendiculaire(incContrainte)
                    
                        # Matrice C
                        if idIncVisEA != None:
                            C[idCon,idIncVisEA] = derivee_partielle(geometrieUtils.droitePerpendiculaire, incContrainte, 'Ea', 0.000001)
                        if idIncVisNA != None:
                            C[idCon,idIncVisNA] = derivee_partielle(geometrieUtils.droitePerpendiculaire, incContrainte, 'Na', 0.000001)
                        if idIncVisEB != None:
                            C[idCon,idIncVisEB] = derivee_partielle(geometrieUtils.droitePerpendiculaire, incContrainte, 'Eb', 0.000001)
                        if idIncVisNB != None:
                            C[idCon,idIncVisNB] = derivee_partielle(geometrieUtils.droitePerpendiculaire, incContrainte, 'Nb', 0.000001)
                        if idIncVisEP != None:    
                            C[idCon,idIncVisEP] = derivee_partielle(geometrieUtils.droitePerpendiculaire, incContrainte, 'Ep', 0.000001)
                        if idIncVisNP != None:    
                            C[idCon,idIncVisNP] = derivee_partielle(geometrieUtils.droitePerpendiculaire, incContrainte, 'Np', 0.00001)
                    
                    
                        
                    
        #### ESTIMATION L2

        # matrices compressées (sans perte) pour calculs rapides via SciPy
        if iteration == 0:
            
            sparseP = sparse.diags(1/((1/sigma0**2)*Kll))
            xInitial = copy.deepcopy(x0)
        t = -cx0
        sparseC = sparse.csc_matrix(C, dtype=np.float32)
        sparseA = sparse.csc_matrix(A)
        sparseAT = sparseA.transpose()
        sparseATP = sparseAT.dot(sparseP)
        sparseATPA = sparseATP.dot(sparseA)
        sparseM = sparse.bmat([[sparseATPA , sparseC.transpose()],
                               [sparseC    , sparseZcc          ]], format='csc')
        b = np.block([[sparseATP.dot(dl)],
                      [t]])
        
        
        # Décomposition superLU et solve méthode avec membre de droite
        MSPLU = sparse.linalg.splu(sparseM)
        dX = MSPLU.solve(b)
        dx = dX[0:nbIncPlani]
        x0 += dx # MAJ du vecteur des inconnues (pour itérations suivantes)
        
        
        
        
        #### CRITERES INTERRUPTION
        listeIdCoord = list(set(listeIdCoord))
        dxCoord = []
        for i in listeIdCoord:
            dxCoord.append(dx[i,0])
            
            
        # Maximum dx sur une coordonnée et compte
        dxCoordMax = np.max(np.abs(dxCoord))
        countDxMax = 0
        for dxi in dxCoord: # compte des dx > au critère interruption
            if abs(dxi) > critereInterruption:
                countDxMax += 1
        logIterations += "Itération n°{:d} avec max(dx) sur une coordonnée = {:0.3f} m ({:d} dx supérieur à {:0.4f} m)\n".format(iteration, dxCoordMax,countDxMax, critereInterruption )
        print( "Itération n°{:d} avec max(dx) sur une coordonnée = {:0.4f} m ({:d} dx supérieur à {:0.4f} m)".format(iteration, dxCoordMax,countDxMax, critereInterruption ))
        if iteration >= nbrIterationMax or abs(dxCoordMax) <= critereInterruption :
            cont = False
        
        # incrément de la boucle princ.
        iteration += 1
            
            
        
        
    #### CALCULS DES INDICATEURS
    

    # vecteur des résidus v
    v = sparseA.dot(dx) - dl
    
    # s0 empirique
    s0 = np.sqrt((v.T@sparseP@v)/(nbObsPlani-nbIncPlani))[0,0]
    quotientGlobal = s0**2/sigma0**2
    
    # cofacteurs des obs. Qll
    sparseQll = sparse.diags((1/sigma0**2)*Kll)
    
    # cofacteurs des inconnues Qxx
    Qxx = np.array(np.linalg.inv(sparseM.toarray())[0:nbIncPlani,0:nbIncPlani], dtype=np.float32)
    
    # cofacteurs des résidus Qvv
    Qvv = np.array(sparseQll - sparseA * Qxx * sparseAT, dtype=np.float32)
    
    # résidus normés wi
    for idObs, vi in enumerate(v[:,0]):
        qvvi = Qvv[idObs,idObs]
        if qvvi > 0.0:
            w[idObs] = vi / (sigma0 * np.sqrt(qvvi))
        else:
            w[idObs] = 0.0
       
    
    # ...Suite des idicateurs 
    # Variance-covariance inconnues Kxx
    Kxx = s0**2*Qxx
    
    # Résidus normés max
    # Récupérer l'obs. des 5 premiers wiMax
    dictWiMax = {}
    wiMaxId = np.flip(np.argsort(np.fabs(w)))
    i = 1
    count = 0
    for idObs in wiMaxId:
        if np.isnan(w[idObs]) == False  and i < 6:
            obsWiMax = rechercheUtils.rechercheIdObs(dictCanevas, idObs)
            dictWiMax.update({'wiMax{:d}'.format(i):obsWiMax})
            i += 1
        # compter le nb sup à 3.5
        if np.isnan(w[idObs]) == False:
            if abs(w[idObs]) > 3.5 :
                count += 1

    # Fiabilité etxerne NABLA et NABLAx
    sparseNABLA = sparse.diags(nabla[:,0],dtype=np.float64)
    NABLAx = Qxx*sparseAT*sparseP*sparseNABLA
    
    
    
    

    
            
            
    #### MAJ OBSERVATIONS ET INDICATEURS (+inc.)
    
    # Quotients de groupes
    dictQuotients = {}
    
    # Noms des groupes distances utilisés (pour inc. suppl. c et m par groupe)
    dictIncSupplDistances = {}
    
    #### ^----- LEVES POLAIRES
    if "polaire" in dictCanevas['canevas'].keys():
        
        # Récupérer les noms de tous les types groupes pour levé polaire pour le calcul des quotients
        listeNomsGroupesDistance = []
        listeNomsGroupesDirection = []
        for groupeDist in dictParametres['parametresCalcul']['groupes']['groupesDistance']['groupeDistance']:
            listeNomsGroupesDistance.append(groupeDist['nomGroupeDistance'])
            
            
            # Inconnues supplémentaire des groupes de distance
            dictIncSupplDistances.update({groupeDist['nomGroupeDistance']:{}})
            if groupeDist['inconnuesSupplementaires']['facteurEchelle'] == "true":
                idIncFacteurEchelle = groupeDist['inconnuesSupplementaires']['idIncFacteurEchelle']
                valeur = x0[idIncFacteurEchelle,0]
                ecartType = np.sqrt(Kxx[idIncFacteurEchelle,idIncFacteurEchelle])
                dictIncSupplDistances[groupeDist['nomGroupeDistance']].update({'facteurEchelle':{'valeur':round(1+valeur,7)}})
                dictIncSupplDistances[groupeDist['nomGroupeDistance']]['facteurEchelle'].update({'ecartType':round(ecartType,8)})
                
            if groupeDist['inconnuesSupplementaires']['constanteAddition'] == "true":
                idIncConstanteAddition = groupeDist['inconnuesSupplementaires']['idIncConstanteAddition']
                valeur = x0[idIncConstanteAddition,0]
                ecartType = np.sqrt(Kxx[idIncConstanteAddition,idIncConstanteAddition])
                dictIncSupplDistances[groupeDist['nomGroupeDistance']].update({'constanteAddition':{'valeur':round(valeur,5)}})
                dictIncSupplDistances[groupeDist['nomGroupeDistance']]['constanteAddition'].update({'ecartType':round(ecartType,6)})
            
            
        for groupeDir in dictParametres['parametresCalcul']['groupes']['groupesDirection']['groupeDirection']:
            listeNomsGroupesDirection.append(groupeDir['nomGroupeDirection'])
        
        # rendre les valeurs uniques en "set"
        listeNomsGroupesDistance = set(listeNomsGroupesDistance)
        listeNomsGroupesDirection = set(listeNomsGroupesDirection)
        for groupe in listeNomsGroupesDistance :
            dictQuotients.update({groupe:{'vk':[], 'pk':[], 'zk':[]}})
        for groupe in listeNomsGroupesDirection :
            dictQuotients.update({groupe:{'vk':[], 'pk':[], 'zk':[]}})
    
    
    

        for station in dictCanevas['canevas']['polaire']['station']:
            
            # indicateurs et valeurs de l'inc. ori.
            stationnement = station['stationnement']
            idIncOri = stationnement['idIncOri']
            stationnement['valIncOri'] = round(x0[idIncOri,0],5)
            EMincOri = np.sqrt(Kxx[idIncOri,idIncOri])
            stationnement.update({'EMincOri':round(EMincOri,5)})
            
            # Indicateurs sur les obs.
            for observation in stationnement['observation']:
                
                RI, DP = observation['RI'], observation['DP']
                
                # RI
                if 'idObsPlani' in RI.keys(): # si pas écarté
                    idObsRI = RI['idObsPlani']
                    vi = v[idObsRI,0]
                    zi = Qvv[idObsRI, idObsRI] / ((1/sigma0**2)*Kll[idObsRI])
                    if zi > 0.0: # éviter les division par 0
                        nablaLi = 4.1 * np.sqrt(Kll[idObsRI]) / np.sqrt(zi)
                    else:
                        nablaLi = 1e6
                    nabla[idObsRI,0] = nablaLi
                    wi = w[idObsRI]
                    RI.update({'vi':round(vi,4)})
                    RI.update({'wi':round(wi,2)})
                    RI.update({'zi':round(zi,2)})
                    RI.update({'nablaLi':round(nablaLi,5)})
                    
                    # pour quotients
                    dictQuotients[stationnement['groupeDirection']]['vk'].append(vi)
                    dictQuotients[stationnement['groupeDirection']]['pk'].append(1/((1/sigma0**2)*Kll[idObsRI]))
                    dictQuotients[stationnement['groupeDirection']]['zk'].append(zi)

                
                # DP
                if 'idObsPlani' in DP.keys(): # si pas écarté
                    idObsDP = DP['idObsPlani']
                    vi = v[idObsDP,0]
                    zi = Qvv[idObsDP, idObsDP] / ((1/sigma0**2)*Kll[idObsDP])
                    if zi > 0.0:
                        nablaLi = 4.1 * np.sqrt(Kll[idObsDP]) / np.sqrt(zi)
                    else:
                        nablaLi = 1e6
                    nabla[idObsDP,0] = nablaLi
                    wi = w[idObsDP]
                    DP.update({'vi':round(vi,4)})
                    DP.update({'wi':round(wi,2)})
                    DP.update({'zi':round(zi,2)})
                    DP.update({'nablaLi':round(nablaLi,5)})
                    
                    # pour quotients
                    dictQuotients[stationnement['groupeDistance']]['vk'].append(vi)
                    dictQuotients[stationnement['groupeDistance']]['pk'].append(1/((1/sigma0**2)*Kll[idObsDP]))
                    dictQuotients[stationnement['groupeDistance']]['zk'].append(zi)
                    
    
    #### ^----- GNSS
    if "GNSS" in dictCanevas['canevas'].keys():
        
        
        # Récupérer les noms de tous les types groupes pour levé polaire pour le calcul des quotients
        listeNomsGroupesGNSS = []
        for groupeGNSS in dictParametres['parametresCalcul']['groupes']['groupesGNSS']['groupeGNSS']:
            listeNomsGroupesGNSS.append(groupeGNSS['nomGroupeGNSS'])
        
        # rendre les valeurs uniques en "set"
        listeNomsGroupesGNSS = set(listeNomsGroupesGNSS)
        for groupe in listeNomsGroupesGNSS :
            dictQuotients.update({groupe:{'vk':[], 'pk':[], 'zk':[]}})

    
        for session in dictCanevas['canevas']['GNSS']['session']:
       
            paramInconnus = session['parametresInconnus']

            # TRANSLATION E
            if "idIncTranslationE" in paramInconnus.keys():   
                idIncTranslationE = paramInconnus['idIncTranslationE']
                paramInconnus['valIncTranslationE'] = round(x0[idIncTranslationE,0],4)
                EMtranslationE = np.sqrt(Kxx[idIncTranslationE,idIncTranslationE])
                paramInconnus.update({'EMtranslationE':round(EMtranslationE,4)})
                
            # TRANSLATION N
            if "idIncTranslationN" in paramInconnus.keys():   
                idIncTranslationN = paramInconnus['idIncTranslationN']
                paramInconnus['valIncTranslationN'] = round(x0[idIncTranslationN,0],4)
                EMtranslationN = np.sqrt(Kxx[idIncTranslationN,idIncTranslationN])
                paramInconnus.update({'EMtranslationN':round(EMtranslationN,4)})
                
            # ROTATION Horiz
            if "idIncRotationHoriz" in paramInconnus.keys():   
                idIncRotationHoriz = paramInconnus['idIncRotationHoriz']
                paramInconnus['valIncRotationHoriz'] = round(x0[idIncRotationHoriz,0],5)
                EMrotationHoriz = np.sqrt(Kxx[idIncRotationHoriz,idIncRotationHoriz])
                paramInconnus.update({'EMrotationHoriz':round(EMrotationHoriz,5)})
                
            # FACTEUR ECHELLE
            if "idIncFacteurEchelleHoriz" in paramInconnus.keys():   
                idIncFacteurEchelleHoriz = paramInconnus['idIncFacteurEchelleHoriz']
                paramInconnus['valIncFacteurEchelleHoriz'] = round(x0[idIncFacteurEchelleHoriz,0],8)
                EMfacteurEchelleHoriz = np.sqrt(Kxx[idIncFacteurEchelleHoriz,idIncFacteurEchelleHoriz])
                paramInconnus.update({'EMfacteurEchelleHoriz':round(EMfacteurEchelleHoriz,5)})
                
            # Indicateurs sur les obs.
            for observation in session['observation']:
                
                LY, LX = observation['LY'], observation['LX']
                
                # LY
                if 'idObsPlani' in LY.keys(): # si pas écarté
                    idObsLY = LY['idObsPlani']
                    vi = v[idObsLY,0]
                    zi = Qvv[idObsLY, idObsLY] / ((1/sigma0**2)*Kll[idObsLY])
                    if zi > 0.0:
                        nablaLi = 4.1 * np.sqrt(Kll[idObsLY]) / np.sqrt(zi)
                    else:
                        nablaLi = 1e6
                    nabla[idObsLY,0] = nablaLi
                    wi = w[idObsLY]
                    LY.update({'vi':round(vi,4)})
                    LY.update({'wi':round(wi,2)})
                    LY.update({'zi':round(zi,2)})
                    LY.update({'nablaLi':round(nablaLi,5)})
                    
                    # pour quotients
                    dictQuotients[session['groupeGNSS']]['vk'].append(vi)
                    dictQuotients[session['groupeGNSS']]['pk'].append(1/((1/sigma0**2)*Kll[idObsLY]))
                    dictQuotients[session['groupeGNSS']]['zk'].append(zi)
                    
                # LY
                if 'idObsPlani' in LX.keys(): # si pas écarté
                    idObsLX = LX['idObsPlani']
                    vi = v[idObsLX,0]
                    zi = Qvv[idObsLX, idObsLX] / ((1/sigma0**2)*Kll[idObsLX])
                    if zi > 0.0:
                        nablaLi = 4.1 * np.sqrt(Kll[idObsLX]) / np.sqrt(zi)
                    else:
                        nablaLi = 1e6
                    nabla[idObsLX,0] = nablaLi
                    wi = w[idObsLX]
                    LX.update({'vi':round(vi,4)})
                    LX.update({'wi':round(wi,2)})
                    LX.update({'zi':round(zi,2)})
                    LX.update({'nablaLi':round(nablaLi,5)})
                    
                    # pour quotients
                    dictQuotients[session['groupeGNSS']]['vk'].append(vi)
                    dictQuotients[session['groupeGNSS']]['pk'].append(1/((1/sigma0**2)*Kll[idObsLX]))
                    dictQuotients[session['groupeGNSS']]['zk'].append(zi)
                    
                    
                    
    #### ^----- SYSTEMES LOCAUX
    if "systemesLocaux" in dictCanevas['canevas'].keys():
        
        # Récupérer les noms de tous les types groupes pour levé polaire pour le calcul des quotients
        listeNomsGroupesSysteme = []
        for groupeSysteme in dictParametres['parametresCalcul']['groupes']['groupesSystemeLocal']['groupeSystemeLocal']:
            listeNomsGroupesSysteme.append(groupeSysteme['nomGroupeSystemeLocal'])
        
        # rendre les valeurs uniques en "set"
        listeNomsGroupesSysteme = set(listeNomsGroupesSysteme)
        for groupe in listeNomsGroupesSysteme :
            dictQuotients.update({groupe:{'vk':[], 'pk':[], 'zk':[]}})
            
            
    
        for systeme in dictCanevas['canevas']['systemesLocaux']['systemeLocal']:
            
            paramInconnus = systeme['parametresInconnus']
            
            # TRANSLATION E
            if "idIncTranslationE" in paramInconnus.keys():   
                idIncTranslationE = paramInconnus['idIncTranslationE']
                paramInconnus['valIncTranslationE'] = round(x0[idIncTranslationE,0],4)
                EMtranslationE = np.sqrt(Kxx[idIncTranslationE,idIncTranslationE])
                paramInconnus.update({'EMtranslationE':round(EMtranslationE,4)})
                
            # TRANSLATION N
            if "idIncTranslationN" in paramInconnus.keys():   
                idIncTranslationN = paramInconnus['idIncTranslationN']
                paramInconnus['valIncTranslationN'] = round(x0[idIncTranslationN,0],4)
                EMtranslationN = np.sqrt(Kxx[idIncTranslationN,idIncTranslationN])
                paramInconnus.update({'EMtranslationN':round(EMtranslationN,4)})
                
            # ROTATION Horiz
            if "idIncRotationHoriz" in paramInconnus.keys():   
                idIncRotationHoriz = paramInconnus['idIncRotationHoriz']
                paramInconnus['valIncRotationHoriz'] = round(x0[idIncRotationHoriz,0],5)
                EMrotationHoriz = np.sqrt(Kxx[idIncRotationHoriz,idIncRotationHoriz])
                paramInconnus.update({'EMrotationHoriz':round(EMrotationHoriz,5)})
                
            # FACTEUR ECHELLE
            if "idIncFacteurEchelleHoriz" in paramInconnus.keys():   
                idIncFacteurEchelleHoriz = paramInconnus['idIncFacteurEchelleHoriz']
                paramInconnus['valIncFacteurEchelleHoriz'] = round(x0[idIncFacteurEchelleHoriz,0],8)
                EMfacteurEchelleHoriz = np.sqrt(Kxx[idIncFacteurEchelleHoriz,idIncFacteurEchelleHoriz])
                paramInconnus.update({'EMfacteurEchelleHoriz':round(EMfacteurEchelleHoriz,5)})      
                

            # Indicateurs sur les obs.
            for observation in systeme['observation']:
                
                LY, LX = observation['LY'], observation['LX']
                
                # LY
                if 'idObsPlani' in LY.keys(): # si pas écarté
                    idObsLY = LY['idObsPlani']
                    vi = v[idObsLY,0]
                    zi = Qvv[idObsLY, idObsLY] / ((1/sigma0**2)*Kll[idObsLY])
                    if zi > 0.0:
                        nablaLi = 4.1 * np.sqrt(Kll[idObsLY]) / np.sqrt(zi)
                    else:
                        nablaLi = 1e6
                    nabla[idObsLY,0] = nablaLi
                    wi = w[idObsLY]
                    LY.update({'vi':round(vi,4)})
                    LY.update({'wi':round(wi,2)})
                    LY.update({'zi':round(zi,2)})
                    LY.update({'nablaLi':round(nablaLi,5)})
                    
                    # pour quotients
                    dictQuotients[systeme['groupeSystemeLocal']]['vk'].append(vi)
                    dictQuotients[systeme['groupeSystemeLocal']]['pk'].append(1/((1/sigma0**2)*Kll[idObsLY]))
                    dictQuotients[systeme['groupeSystemeLocal']]['zk'].append(zi)
                    
                # LY
                if 'idObsPlani' in LX.keys(): # si pas écarté
                    idObsLX = LX['idObsPlani']
                    vi = v[idObsLX,0]
                    zi = Qvv[idObsLX, idObsLX] / ((1/sigma0**2)*Kll[idObsLX])
                    if zi > 0.0:
                        nablaLi = 4.1 * np.sqrt(Kll[idObsLX]) / np.sqrt(zi)
                    else:
                        nablaLi = 1e6
                    nabla[idObsLX,0] = nablaLi
                    wi = w[idObsLX]
                    LX.update({'vi':round(vi,4)})
                    LX.update({'wi':round(wi,2)})
                    LX.update({'zi':round(zi,2)})
                    LX.update({'nablaLi':round(nablaLi,5)})
                    
                    # pour quotients
                    dictQuotients[systeme['groupeSystemeLocal']]['vk'].append(vi)
                    dictQuotients[systeme['groupeSystemeLocal']]['pk'].append(1/((1/sigma0**2)*Kll[idObsLX]))
                    dictQuotients[systeme['groupeSystemeLocal']]['zk'].append(zi)
                    
                    
                    
                    
                
    #### ^----- COTES
    if "cotes" in dictCanevas['canevas'].keys():
        
        # Récupérer les noms de tous les types groupes pour levé polaire pour le calcul des quotients
        listeNomsGroupesCotes = []
        for groupeCote in dictParametres['parametresCalcul']['groupes']['groupesCote']['groupeCote']:
            listeNomsGroupesCotes.append(groupeCote['nomGroupeCote'])
        
        # rendre les valeurs uniques en "set"
        listeNomsGroupesCotes = set(listeNomsGroupesCotes)
        for groupe in listeNomsGroupesCotes :
            dictQuotients.update({groupe:{'vk':[], 'pk':[], 'zk':[]}})
        
        for cote in dictCanevas['canevas']['cotes']['cote']:
            
            DP = cote['observation']['DP']

            if 'idObsPlani' in DP.keys(): # si pas écarté
                idObsDP = DP['idObsPlani']
                vi = v[idObsDP,0]
                zi = Qvv[idObsDP, idObsDP] / ((1/sigma0**2)*Kll[idObsDP])
                if zi > 0.0:
                    nablaLi = 4.1 * np.sqrt(Kll[idObsDP]) / np.sqrt(zi)
                else:
                    nablaLi = 1e6
                nabla[idObsDP,0] = nablaLi
                wi = w[idObsDP]
                DP.update({'vi':round(vi,4)})
                DP.update({'wi':round(wi,2)})
                DP.update({'zi':round(zi,2)})
                DP.update({'nablaLi':round(nablaLi,5)})
                
                # pour quotients
                dictQuotients[cote['groupeCote']]['vk'].append(vi)
                dictQuotients[cote['groupeCote']]['pk'].append(1/((1/sigma0**2)*Kll[idObsDP]))
                dictQuotients[cote['groupeCote']]['zk'].append(zi)
        
        

        
    #### CALCUL DES QUOTIENTS
    
    for key,value in dictQuotients.items():
        # Uniquement si il y a bien des valeurs dans les groupes (utilisés)
        if len(value['vk']) > 0 and len(value['pk']) > 0 and len(value['zk']) > 0:
            
            vk,pk,zk = np.array([value['vk']]).T, np.diag(value['pk']), np.array([value['zk']]).T
            s0k = np.sqrt(vk.T @ pk @ vk / sum(zk))[0,0]
            quotient = s0k**2/sigma0**2
            value.update({'quotient':round(quotient,2)})
            # suppression des sous-vecteurs du groupe (lisibilité)
            value.pop('vk')
            value.pop('pk')
            value.pop('zk')
            
            
            

    

    #### MAJ POINTS ET INDICATEURS
    
    for point in dictPoints['points']['point']:

        # Uniquement MAJ des points nouveaux
        if 'idIncE' in point.keys() and 'idIncN' in point.keys():
            
            idIncE, idIncN = point['idIncE'], point['idIncN'] # index des inconnues
            
            point['E'], point['N'] = round(x0[idIncE,0],4), round(x0[idIncN,0],4)
            
            # Sous-matrice kxxi contenant les variances et covariance des inconnues du pt nouveau
            kxxi = np.zeros(shape=(2,2))
            kxxi[0,0], kxxi[1,1] = Kxx[idIncE, idIncE], Kxx[idIncN, idIncN]
            kxxi[1,0],kxxi[0,1] = Kxx[idIncE, idIncN], Kxx[idIncN, idIncE]
            # Calcul des éléments d'ellipse
            eigVal,eigVec = np.linalg.eigh(kxxi)
            if eigVal[0] < 0.0 or eigVal[1] < 0.0:
                eigVal = np.fabs(eigVal)
            a = np.sqrt(eigVal[1])
            b = np.sqrt(eigVal[0])
            u1 = [eigVec[0,1],eigVec[1,1]]
            # sans échelle, tout à 1sigma = 39%
            gisA = np.arccos(u1[0])*200.0/np.pi
            ellipseEM = {'a':round(a,4),
                         'b':round(b,4),
                         'gisA':round(gisA,4)} 
            point.update({'ellipseEMplani':ellipseEM})
            
            # Fiabilité externe
            NE, NN = NABLAx[idIncE,:], NABLAx[idIncN,:]
            N = np.sqrt(NE**2+NN**2)
            NA = np.max(N)
            
            if NA > 1e3 :  # = fiabilité externe infinie
                NA = np.nan
                gisNA = np.nan
                idNA = np.nan
            else: # fiab. externe non-infinie 
                idNA = np.argmax(N)
                gisNA = np.mod(np.arctan2(NE[idNA],NN[idNA])*200.0/np.pi, 400.0)
                
            vecteurFiabExterne = {'NA':round(NA,4),
                                  'gisNA':round(gisNA,4),
                                  'idObsRespNA':idNA} 
            point.update({'vecteurFiabExternePlani':vecteurFiabExterne})
            
            # Calcul des diff. entre état initial et après compensation
            dE, dN = x0[idIncE,0] - xInitial[idIncE,0], x0[idIncN,0] - xInitial[idIncN,0]
            deltaCoord = {'dE':round(dE,4),
                          'dN':round(dN,4)}
            point.update({'deltaCoordPlani':deltaCoord})
                
         
    
    #### RESULTATS GLOBAUX

    dictResGlobaux['resultatsGlobaux'].update({'planimetrie':{}})
    dictResGlobaux['resultatsGlobaux']['planimetrie'].update({'tempsCalcul':"{:0.1f} s".format(time.time()-timer)})
    dictResGlobaux['resultatsGlobaux']['planimetrie'].update({'nbIterations':"{:d}".format(iteration)})
    dictResGlobaux['resultatsGlobaux']['planimetrie'].update({'logIterations':"\n{:s}".format(logIterations)})
    
    # Quotients d'écart-type d'unité de poids par groupe (et global)
    dictResGlobaux['resultatsGlobaux']['planimetrie'].update({'quotientsEcartTypeUnitePoids':{}})
    dictResGlobaux['resultatsGlobaux']['planimetrie']['quotientsEcartTypeUnitePoids'].update({'global':"{:0.2f}".format(quotientGlobal)})
    dictResGlobaux['resultatsGlobaux']['planimetrie']['quotientsEcartTypeUnitePoids'].update(dictQuotients)
    
    # Inconnues supplémentaires pour les groupes distance
    dictResGlobaux['resultatsGlobaux']['planimetrie'].update({'inconnuesSupplementairesGroupesDistances':dictIncSupplDistances})
    
    # Dénombrement
    dictResGlobaux['resultatsGlobaux']['planimetrie'].update({'denombrement':denombrement})
    
    # 5 observations avec leur wiMax
    dictResGlobaux['resultatsGlobaux']['planimetrie'].update({'nbWiSup3.5':count})
    dictResGlobaux['resultatsGlobaux']['planimetrie'].update({'wiMax':dictWiMax})
    
    
    return None











def estimation1D(dictCanevas, dictPoints, dictParametres, denombrement, dictResGlobaux):
    
    timer = time.time()

    #### PARAMETRES GENERAUX
    nbrIterationMax = int(dictParametres['parametresCalcul']['optionsCalcul']['nbrIterationMax'])
    critereInterruption = float(dictParametres['parametresCalcul']['optionsCalcul']['critereInterruption'])
    robuste = dictParametres['parametresCalcul']['optionsCalcul']['robuste']
    robuste = True if robuste=="true" else False
    cRobuste = dictParametres['parametresCalcul']['optionsCalcul']['limiteRobuste']
    if cRobuste == None:
        dictParametres['parametresCalcul']['optionsCalcul']['limiteRobuste'] = 3.5 # par défaut
        cRobuste = 3.5
    else:
        cRobuste = float(cRobuste)
    sigma0 = 1.0
    
    # Dénombrement
    nbObsAlti, nbIncAlti = denombrement['nbObsAlti']-1000000, denombrement['nbIncAlti']-1000000
    
    # Liste des index de coordonnées (pour calculer max(dx) uniq. sur les coordonnées)
    listeIdAlti = []
    logIterations = ''
    
    #### INITIALISATION DES  MATRICES (scipy.sparses ou np.array)
    # A = sparse.csr_matrix((nbObsPlani, nbIncPlani)) # n x u
    A = np.zeros(shape=(nbObsAlti,nbIncAlti), dtype=np.float32) # n x u
    Kll = np.zeros(shape=(nbObsAlti)) # n x 1 (diagonale d'une matrice n x n)
    f0 = np.zeros(shape=(nbObsAlti,1)) # n x 1
    dl = np.zeros(shape=(nbObsAlti,1)) # n x 1
    x0 = np.zeros(shape=(nbIncAlti,1)) # u x 1
    w = np.zeros(shape=(nbObsAlti)) # n x 1
    W = np.ones(shape=(nbObsAlti))# n x 1 (diagonale d'une matrice n x n)
    nabla = np.zeros(shape=(nbObsAlti,1),dtype=np.float32)
    
    # Liste des points fixes alti.
    listePFalti = []
    for point in dictParametres['parametresCalcul']['pointsFixesAlti']['point']:
        listePFalti.append(point['numeroPoint'])
    
    
    # -----------------------------------------
    #### REMPLISSAGE DES MATRICES ET ITERATIONS
    # -----------------------------------------
    
    # Boucle de calcul principale 
    cont = True
    iteration = 0
    
    while cont :
    
    
        #### ^----- LEVES POLAIRES
        
        if "polaire" in dictCanevas['canevas'].keys():
    
            for station in dictCanevas['canevas']['polaire']['station']:
                
                
                # ALTITUDE DE STATION
                pointStation = rechercheUtils.rechercheNoPt(dictPoints, station['numeroStation'])
                if "idIncH" in pointStation.keys() :
                    
                    idIncStaH =  pointStation['idIncH']-1000000
                    Hsta = x0[idIncStaH,0]
                    listeIdAlti.append(idIncStaH)
      
                elif pointStation['numeroPoint'] in listePFalti: # si station sur pt fixe
                    idIncStaH = None
                    Hsta = float(pointStation['H'])
                else: # autres points non-définis en alti
                    idIncStaH = None
                  
                    
                #### ^--------- INDEX ET VALEURS DES OBS.
                
                for observation in station['stationnement']['observation']:
                    
                    # ALTITUDE DU POINT VISE
                    pointVis = rechercheUtils.rechercheNoPt(dictPoints, observation['numeroPoint'])
                    if "idIncH" in pointVis.keys() :
                        
                        idIncVisH = pointVis['idIncH'] - 1000000
                        Hvis = x0[idIncVisH,0]
                        listeIdAlti.append(idIncVisH)
                    
                    elif pointVis['numeroPoint'] in listePFalti: # si station sur pt fixe
                        idIncVisH = None
                        Hvis = float(pointVis['H'])
                    else: # autres points non-définis en alti
                        idIncVisH = None
                        
                        
                    # INDEX OBSERVATIONS DH
                    if "idObsAlti" in observation['DH'].keys():
                        idObsDH = observation['DH']['idObsAlti'] - 1000000
                    else:
                        idObsDH = None
                    
                    
                    #### ^--------- MATRICE A, dl et Kll
                    
                    # DENIVELEE DH
                    if idObsDH != None:
                        
                        # Matrice A
                        if idIncStaH != None:
                            A[idObsDH,idIncStaH] = -1.0
                        if idIncVisH != None:
                            A[idObsDH,idIncVisH] = 1.0
                            
                        # Matrice dl
                        obsDH = float(observation['DH']['valeur'])
                        f0 = Hvis - Hsta
                        dl[idObsDH,0] = obsDH-f0
                        
                        # Matrice Kll
                        Kll[idObsDH] = observation['DH']['ecartType']**2
                        
                        
                        
        #### ^----- GNSS
        
        if "GNSS" in dictCanevas['canevas'].keys():
        
            for session in dictCanevas['canevas']['GNSS']['session']:
                
                #### ^--------- INDEX ET VALEURS DES INCONNUES
                
                paramInconnus = session['parametresInconnus']
                    
                # TRANSLATION H
                if "idIncTranslationH" in paramInconnus.keys():
                    idIncTranslationH = paramInconnus['idIncTranslationH'] - 1000000
                    tH0 = paramInconnus['valIncTranslationH']
                    tH0 = x0[idIncTranslationH,0]
                else: # si fixe
                    idIncTranslationH = None
                    tH0 = 0.0
                    
                    
                    
                #### ^--------- INDEX ET VALEURS DES OBS. ET INC. COORD.
                
                for observation in session['observation']:
                
                    # ALTITUDE DU POINT VISE
                    pointVis = rechercheUtils.rechercheNoPt(dictPoints, observation['numeroPoint'])
                    if "idIncH" in pointVis.keys() :
                        
                        idIncVisH = pointVis['idIncH'] - 1000000
                        listeIdAlti.append(idIncVisH)
                        Hvis = x0[idIncVisH,0]
                    
                    elif pointVis['numeroPoint'] in listePFalti: # si station sur pt fixe
                        idIncVisH = None
                        Hvis = float(pointVis['H'])
                    else: # autres points non-définis en alti
                        idIncVisH = None
                        
                        
                    # INDEX OBSERVATIONS LH
                    if "idObsAlti" in observation['LH'].keys():
                        idObsLH = observation['LH']['idObsAlti'] - 1000000
                    else:
                        idObsLH = None
                    
                    
                    #### ^--------- MATRICE A, dl et Kll
                    
                    # ALTITUDE LH DANS SESSION
                    if idObsLH != None:
                        
                        # Matrice A
                        if idIncVisH != None :
                            A[idObsLH,idIncVisH] = 1.0
                        if idIncTranslationH != None:
                            A[idObsLH,idIncTranslationH] = 1.0
                             
                        # Matrice dl
                        obsLH = float(observation['LH']['valeur'])
                        f0 = Hvis + tH0
                        dl[idObsLH,0] = obsLH-f0
                        
                        # Matrice Kll
                        Kll[idObsLH] = observation['LH']['ecartType']**2
                    
                    
        

        #### ESTIMATION L2
       
        # matrices compressées (sans perte) pour calculs rapides via SciPy
        if iteration == 0:
            sparseP = sparse.diags(1/((1/sigma0**2)*Kll))
            xInitial = copy.deepcopy(x0)
        sparseA = sparse.csc_matrix(A)
        sparseAT = sparseA.transpose()
        sparseATP = sparseAT.dot(sparseP)
        sparseATPA = sparseATP.dot(sparseA)
        b = sparseATP.dot(dl)

        # Décomposition superLU et solve méthode avec membre de droite
        SPLU = sparse.linalg.splu(sparseATPA)
        dx = SPLU.solve(b)
        x0 += dx # MAJ du vecteur des inconnues (pour itérations suivantes)   
        
        
        
        
        
        #### CRITERES INTERRUPTION
        listeIdAlti= list(set(listeIdAlti))
        dxAlti = []
        for i in listeIdAlti:
            dxAlti.append(dx[i,0])
            
            
        # Maximum dx sur une coordonnée et compte
        dxCoordMax = np.max(np.abs(dxAlti))
        countDxMax = 0
        for dxi in dxAlti: # compte des dx > au critère interruption
            if abs(dxi) > critereInterruption:
                countDxMax += 1
        logIterations += "Itération n°{:d} avec max(dx) sur une coordonnée = {:0.3f} m ({:d} dx supérieur à {:0.4f} m)\n".format(iteration, dxCoordMax,countDxMax, critereInterruption )
        print( "Itération n°{:d} avec max(dx) sur une coordonnée = {:0.4f} m ({:d} dx supérieur à {:0.4f} m)".format(iteration, dxCoordMax,countDxMax, critereInterruption ))
        if iteration >= nbrIterationMax or dxCoordMax <= critereInterruption :
            cont = False
            
        # incrément de la boucle princ.
        iteration += 1
            
        
        
    
    #### CALCULS DES INDICATEURS
    
    # vecteur des résidus v
    v = sparseA.dot(dx) - dl
    
    # cofacteurs des obs. Qll
    sparseQll = sparse.diags((1/sigma0**2)*Kll)
    
    # cofacteurs des inconnues Qxx
    Qxx = np.array(np.linalg.inv(sparseATPA.toarray()), dtype=np.float32)
    
    # cofacteurs des résidus Qvv
    Qvv = np.array(sparseQll - sparseA * Qxx * sparseAT, dtype=np.float32)
    
    # résidus normés wi
    for idObs, vi in enumerate(v[:,0]):
        qvvi = Qvv[idObs,idObs]
        if qvvi > 0.0:
            w[idObs] = vi / (sigma0 * np.sqrt(Qvv[idObs,idObs]))
        else:
            w[idObs] = 0.0
 
    # ...Suite des idicateurs pour L2 ET robuste
    # s0 empirique
    s0 = np.sqrt((v.T@sparseP@v)/(nbObsAlti-nbIncAlti))[0,0]
    quotientGlobal = s0**2/sigma0**2

    # Variance-covariance inconnues Kxx
    Kxx = s0**2*Qxx
    
    # Lister les résidus normés max
    # Récupérer l'obs. des 5 premiers wiMax
    dictWiMax = {}
    wiMaxId = np.flip(np.argsort(np.fabs(w)))
    i = 1
    count = 0
    for idObs in wiMaxId:
        if np.isnan(w[idObs]) == False  and i < 6:
            obsWiMax = rechercheUtils.rechercheIdObs(dictCanevas, idObs+1000000)
            dictWiMax.update({'wiMax{:d}'.format(i):obsWiMax})
            i += 1
        # compter le nb sup à 3.5
        if np.isnan(w[idObs]) == False:
            if abs(w[idObs]) > 3.5 :
                count += 1

    # Fiabilité etxerne NABLA et NABLAx
    sparseNABLA = sparse.diags(nabla[:,0],dtype=np.float64)
    NABLAx = Qxx*sparseAT*sparseP*sparseNABLA


    
    #### MAJ OBSERVATIONS ET INDICATEURS (+inc.)
    
    # Quotients de groupes
    dictQuotients = {}

    
    #### ^----- LEVES POLAIRES
    if "polaire" in dictCanevas['canevas'].keys():
        
        # Récupérer les noms de tous les groupes de directionj pour levé polaire pour le calcul des quotients
        listeNomsGroupesDirection = []
        for groupeDir in dictParametres['parametresCalcul']['groupes']['groupesDirection']['groupeDirection']:
            listeNomsGroupesDirection.append(groupeDir['nomGroupeDirection'])
        listeNomsGroupesDirection = set(listeNomsGroupesDirection)
        
        # Initialisation des éléments pour le calcul des quotients par groupe (groupes de direction)
        for groupe in listeNomsGroupesDirection :
            dictQuotients.update({groupe:{'vk':[], 'pk':[], 'zk':[]}})
            
        # Indicateurs sur les obs.
        for station in dictCanevas['canevas']['polaire']['station']:    
            stationnement = station['stationnement']
            
            for observation in stationnement['observation']:
                DH = observation['DH']
                
                if 'idObsAlti' in DH.keys(): # si pas écarté
                    idObsDH = DH['idObsAlti']-1000000
                    vi = v[idObsDH,0]
                    zi = Qvv[idObsDH, idObsDH] / ((1/sigma0**2)*Kll[idObsDH])
                    if zi > 0.0: # éviter les division par 0
                        nablaLi = 4.1 * np.sqrt(Kll[idObsDH]) / np.sqrt(zi)
                    else:
                        nablaLi = 1e6
                    nabla[idObsDH,0] = nablaLi
                    wi = w[idObsDH]
                    DH.update({'vi':round(vi,4)})
                    DH.update({'wi':round(wi,2)})
                    DH.update({'zi':round(zi,2)})
                    DH.update({'nablaLi':round(nablaLi,5)})
                    
                    # pour quotients
                    dictQuotients[stationnement['groupeDirection']]['vk'].append(vi)
                    dictQuotients[stationnement['groupeDirection']]['pk'].append(1/((1/sigma0**2)*Kll[idObsDH]))
                    dictQuotients[stationnement['groupeDirection']]['zk'].append(zi)
                
    
    #### ^----- GNSS
    if "GNSS" in dictCanevas['canevas'].keys():

        # Récupérer les noms de tous les types groupes pour levé polaire pour le calcul des quotients
        listeNomsGroupesGNSS = []
        for groupeGNSS in dictParametres['parametresCalcul']['groupes']['groupesGNSS']['groupeGNSS']:
            listeNomsGroupesGNSS.append(groupeGNSS['nomGroupeGNSS'])
        
        # rendre les valeurs uniques en "set"
        listeNomsGroupesGNSS = set(listeNomsGroupesGNSS)
        for groupe in listeNomsGroupesGNSS :
            dictQuotients.update({groupe:{'vk':[], 'pk':[], 'zk':[]}})
              
        # indicateurs sur les param. inconnus  
        for session in dictCanevas['canevas']['GNSS']['session']:
       
            paramInconnus = session['parametresInconnus']

            # TRANSLATION H
            if "idIncTranslationH" in paramInconnus.keys():   
                idIncTranslationH = paramInconnus['idIncTranslationH']-1000000
                paramInconnus['valIncTranslationH'] = round(x0[idIncTranslationH,0],4)
                EMtranslationH = np.sqrt(Kxx[idIncTranslationH,idIncTranslationH])
                paramInconnus.update({'EMtranslationH':round(EMtranslationH,4)})
            
            # Indicateurs sur les obs.
            for observation in session['observation']:
                LH = observation['LH']
                
                if 'idObsAlti' in LH.keys(): # si pas écarté
                    idObsLH = LH['idObsAlti']-1000000
                    vi = v[idObsLH,0]
                    zi = Qvv[idObsLH, idObsLH] / ((1/sigma0**2)*Kll[idObsLH])
                    if zi > 0.0:
                        nablaLi = 4.1 * np.sqrt(Kll[idObsLH]) / np.sqrt(zi)
                    else:
                        nablaLi = 1e6
                    nabla[idObsLH,0] = nablaLi
                    wi = w[idObsLH]
                    LH.update({'vi':round(vi,4)})
                    LH.update({'wi':round(wi,2)})
                    LH.update({'zi':round(zi,2)})
                    LH.update({'nablaLi':round(nablaLi,5)})
                    
                    # pour quotients
                    dictQuotients[session['groupeGNSS']]['vk'].append(vi)
                    dictQuotients[session['groupeGNSS']]['pk'].append(1/((1/sigma0**2)*Kll[idObsLH]))
                    dictQuotients[session['groupeGNSS']]['zk'].append(zi)
          
            
          
    #### CALCUL DES QUOTIENTS
    
    for key,value in dictQuotients.items():
        # Uniquement si il y a bien des valeurs dans les groupes (utilisés)
        if len(value['vk']) > 0 and len(value['pk']) > 0 and len(value['zk']) > 0:
            
            vk,pk,zk = np.array([value['vk']]).T, np.diag(value['pk']), np.array([value['zk']]).T
            s0k = np.sqrt(vk.T @ pk @ vk / sum(zk))[0,0]
            quotient = s0k**2/sigma0**2
            value.update({'quotient':round(quotient,2)})
            # suppression des sous-vecteurs du groupe (lisibilité)
            value.pop('vk')
            value.pop('pk')
            value.pop('zk')
            
            
      
                
    
    
    
    
    #### MAJ POINTS ET INDICATEURS
            
    for point in dictPoints['points']['point']:

        # Uniquement MAJ des points nouveaux
        if 'idIncH' in point.keys():
            
            idIncH = point['idIncH']-1000000 # index de l'inconnue H
            point['H'] = round(x0[idIncH,0],4)
            
            # Intervalle de confiance (équivalent ellipse en 1D) à 1 sigma
            intervalleEMH = np.sqrt(Kxx[idIncH,idIncH])
            intervalleEMH ={'c':round(intervalleEMH,4)}
            point.update({'EMalti':intervalleEMH})
            
            # Fiabilité externe 
            N = NABLAx[idIncH,:]
            NH = np.max(N)
            if NH > 1e3 :  # = fiabilité externe infinie
                NH = np.nan
                idNH = np.nan
            else: # fiab. externe non-infinie 
                idNH = np.argmax(N) + 1000000
            
            vecteurFiabExterne = {'NH':round(NH,4),
                                  'idObsRespNH':idNH} 
            point.update({'vecteurFiabExterneAlti':vecteurFiabExterne})
            
            
            # Calcul des diff. entre état initial et après compensation
            dH = x0[idIncH,0] - xInitial[idIncH,0]
            deltaAlti = {'dH':round(dH,4)}
            point.update({'deltaAlti':deltaAlti})        
       
            
    #### RESULTATS GLOBAUX

    dictResGlobaux['resultatsGlobaux'].update({'altimetrie':{}})
    dictResGlobaux['resultatsGlobaux']['altimetrie'].update({'tempsCalcul':"{:0.1f} s".format(time.time()-timer)})
    dictResGlobaux['resultatsGlobaux']['altimetrie'].update({'nbIterations':"{:d}".format(iteration)})
    dictResGlobaux['resultatsGlobaux']['altimetrie'].update({'logIterations':"\n{:s}".format(logIterations)})
    
    # Quotients d'écart-type d'unité de poids par groupe (et global)
    dictResGlobaux['resultatsGlobaux']['altimetrie'].update({'quotientsEcartTypeUnitePoids':{}})
    dictResGlobaux['resultatsGlobaux']['altimetrie']['quotientsEcartTypeUnitePoids'].update({'global':"{:0.2f}".format(quotientGlobal)})
    dictResGlobaux['resultatsGlobaux']['altimetrie']['quotientsEcartTypeUnitePoids'].update(dictQuotients)
    
    # Dénombrement
    dictResGlobaux['resultatsGlobaux']['altimetrie'].update({'denombrement':denombrement})
    
    # 5 observations avec leur wiMax
    dictResGlobaux['resultatsGlobaux']['altimetrie'].update({'nbWiSup3.5':count})
    dictResGlobaux['resultatsGlobaux']['altimetrie'].update({'wiMax':dictWiMax})        
 
            
    return None








class Estimation:
    
    def __init__(self, dictCanevas, dictPoints, dictParametres, denombrement, dirPathResultats):
        """
        Constructeur de la classe "Estimation".

        Parameters
        ----------
        dictCanevas: dictionnaire
            Contenant le canevas après validation.
        dictPoints: dictionnaire
            Contenant les points après validation.
        dictParametres: dictionnaire
            Contenant les paramètres après validation.
                                                                      
        Returns
        -------
        None.

        """
        
        # Attribution des variables
        self.dictCanevas = dictCanevas
        self.dictPoints = dictPoints
        self.dictParametres = dictParametres
        self.denombrement = denombrement
        self.dirPathResultats = dirPathResultats
        
        # En-tête des dictionnaires des résultats globaux
        self.dictResGlobaux = {}
        self.dictResGlobaux = {'resultatsGlobaux':{}}
        self.dictResGlobaux['resultatsGlobaux'].update({'nomReseau':dictParametres['parametresCalcul']['nomReseau']})
        self.dictResGlobaux['resultatsGlobaux'].update({'date':datetime.datetime.now().strftime("%d.%m.%y")})
        self.dictResGlobaux['resultatsGlobaux'].update({'heure':datetime.datetime.now().strftime("%H:%M:%S")})
        self.dictResGlobaux['resultatsGlobaux'].update({'optionsCalcul':dictParametres['parametresCalcul']['optionsCalcul']})
        
        
        
        
        
    def compensation2D (self):
        """
        Fonction qui lance l'estimation 2D.
             
        Returns
        -------
        None.

        """
        
        print("\nCODE 2000 : COMPENSATION PLANIMETRIQUE")
        print("--------------------------------------\n")
        
        
        
        return estimation2D(self.dictCanevas, self.dictPoints, self.dictParametres, self.denombrement, self.dictResGlobaux)
    
    
    def compensation1D (self):
        """
        Fonction qui lance l'estimation 1D.
             
        Returns
        -------
        None.

        """
        
        print("\nCODE 3000 : COMPENSATION ALTIMETRIQUE")
        print("-------------------------------------\n")
        
       
        
        return  estimation1D(self.dictCanevas, self.dictPoints, self.dictParametres, self.denombrement, self.dictResGlobaux)
    
    
    
    def exportsResultats(self):
        """
        Fonction qui lance l'export des dictionnaires après compensation.
             
        Returns
        -------
        None.

        """
        
        self.xmlPoints = xmltodict.unparse(self.dictPoints, pretty=True, encoding='utf-8')
        with open(self.dirPathResultats+"\\pointsPostComp.xml", 'w') as f:
            f.write(self.xmlPoints)
            
        self.xmlCanevas = xmltodict.unparse(self.dictCanevas, pretty=True, encoding='utf-8')
        with open(self.dirPathResultats+"\\canevasPostComp.xml", 'w') as f:
            f.write(self.xmlCanevas)
            
        self.xmlRes = xmltodict.unparse(self.dictResGlobaux, pretty=True, encoding='utf-8')
        with open(self.dirPathResultats+"\\resultatsGlobaux.xml", 'w') as f:
            f.write(self.xmlRes)      
            
        return None
        
    
    
    

