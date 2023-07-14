# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 17:10:42 2022

@author: Matteo Casto, INSIT
"""

import libUtils.rechercheUtils as rechercheUtils
import libUtils.geometrieUtils as geometrieUtils
import libUtils.conversionUtils as conversionUtils
import libUtils.analyseSolvabiliteUtils as analyseSolvabiliteUtils
from scipy import sparse
from scipy.sparse import linalg
from scipy import linalg
import scipy
import numpy as np
import copy
import xmltodict
import time
import datetime
import matplotlib.pyplot as plt
from scipy.linalg.lapack import dtrtri
# import cupy




def updateProgressBar(progressBar, n):
    """
    Fonction simple qui incrémente de nla progress bar pour un calcul via la UI.

    Parameters
    ----------
    progressBar : objet 
        instance de l'objet progressBar PyQt5
    n : int
        incrément.

    Returns
    -------
    None.

    """
    
    if progressBar: # Si le programme est appelé en ligne de commande, pas de progressBar
        progressBar.setValue(progressBar.value() + n)



def find_problematic_rows(M):
    Q, R = linalg.qr(M)

    # Trouver les valeurs diagonales proches de zéro
    zero_tol = 1e-5  # Tolérance pour considérer une valeur diagonale comme nulle
    problematic_rows = np.where(np.abs(np.diag(R)) < zero_tol)[0]

    if problematic_rows.size > 0:
        print("Les lignes suivantes posent problème :")
        print(problematic_rows)
        return problematic_rows
    else:
        print("Aucune ligne de la matrice M ne pose problème.")
        return None
    
    
    
def find_non_invertible_columns(A):

    # Calcul de la matrice M = A^T @ A
    M = np.matmul(A.T, A)

    # Vérification de la non-inversibilité de M
    if np.linalg.matrix_rank(M) == M.shape[1]:
        return None

    # Récupération des colonnes de A qui engendrent la non-inversibilité de M
    non_invertible_columns = []
    for i in range(A.shape[1]):
        A_temp = np.delete(A, i, axis=1)  # Suppression de la colonne i de A
        if np.linalg.matrix_rank(A_temp) != A_temp.shape[1]:
            non_invertible_columns.append(i)

    return non_invertible_columns


def finEmptyRows(A):
    return np.where(np.sum(np.abs(A), axis=1)==0)[0]




def find_problematic_columns(M, A):
    Q, R = linalg.qr(M)

    # Trouver les valeurs diagonales proches de zéro
    zero_tol = 1e-5  # Tolérance pour considérer une valeur diagonale comme nulle
    problematic_rows = np.where(np.abs(np.diag(R)) < zero_tol)[0]

    if problematic_rows.size > 0:
        problematic_columns = np.where(np.abs(A.T @ Q[:, problematic_rows]) < zero_tol)[1]
        print("Les colonnes suivantes de A posent problème :")
        print(problematic_columns)
        return problematic_columns
    else:
        print("Aucune colonne de A ne pose problème.")
        return None










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




            
            


def estimation2D(dictCanevas, dictPoints, dictParametres, denombrement, dictResGlobaux, progressBar):
    
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
    # cupy._default_memory_pool.free_all_blocks() # libérer la mémoire GPU

    #### PARAMETRES GENERAUX
    nbrIterationMax = int(dictParametres['parameters']['computationOptions']['maxIterationNbr'])
    critereInterruption = float(dictParametres['parameters']['computationOptions']['interruptionCondition'])
    robuste = dictParametres['parameters']['computationOptions']['robust']
    robuste = True if robuste=="true" else False
    cRobuste = dictParametres['parameters']['computationOptions']['robustLimit']
    if cRobuste == None:
        dictParametres['parameters']['computationOptions']['robustLimit'] = 3.5 # par défaut
        cRobuste = 3.5
    else:
        cRobuste = float(cRobuste)
    typeCalcul = dictParametres['parameters']['computationOptions']['networkType'] # pour libre ajusté
    libreAjuste = True if typeCalcul=='stochastic' else False
    sigma0 = 1.0
    
    # Dénombrement
    nbObsPlani, nbIncPlani, nbConPlani = denombrement['nbObsPlani'], denombrement['nbIncPlani'], denombrement['nbConPlani']
    
    # Liste des index de coordonnées (pour calculer max(dx) uniq. sur les coordonnées)
    listeIdCoord = []
    logIterations = ''
    
    

    # ---------------
    #### LIBRE-AJUSTE
    # ---------------
    if libreAjuste:
        
        listeLA = []
        
        for PF in dictParametres['parameters']['planimetricControlPoints']['point']:
            
            ecartType = float(PF['planiStdDev']['mm']) / 1000.0 # en [m], code erreur à mettre si pas d'écart-type saisi
            PF['planiStdDev'] = ecartType # MAJ en m
            PF.update({'idObsEE':nbObsPlani}) # ajout de l'idObs
            nbObsPlani += 1
            PF.update({'idObsNN':nbObsPlani}) # ajout de l'idObs
            nbObsPlani += 1
            denombrement['nbObsPlani'] += 2
            denombrement['nbIncPlani'] += 2
            
            # Ajout des id d'inconnues
            point = rechercheUtils.rechercheNoPt(dictPoints, PF['pointName'])
            E,N = float(point['E']), float(point['N'])
            PF.update({'EE':E})
            PF.update({'NN':N})
            elemsPlani = point['planimetricElems']
            point['planimetricElems'] = elemsPlani+2
            point.update({'idUnkE':nbIncPlani}) 
            PF.update({'idUnkE':nbIncPlani})
            nbIncPlani += 1
            point.update({'idUnkN':nbIncPlani}) 
            PF.update({'idUnkN':nbIncPlani})
            nbIncPlani += 1
            
            listeLA.append(PF)
            


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
    
    
    updateProgressBar(progressBar, 5)
    
    
    # Boucle de calcul principale 
    cont = True
    iteration = 0
    
    
    while cont :
        
        
        #### ^----- OBSERVATION DE COORDONNEES
        
        if libreAjuste:
            
            for point in listeLA:
                
                idIncE, idIncN = point['idUnkE'], point['idUnkN']
                idObsEE, idObsNN = point['idObsEE'], point['idObsNN']
                obsEE, obsNN = point['EE'], point['NN']
                if iteration == 0:
                    x0[idIncE,0], x0[idIncN,0] = obsEE, obsNN
                    E0, N0 = obsEE, obsNN # en 1ere it
                    listeIdCoord.append(idIncE)
                    listeIdCoord.append(idIncN)
                else: # itérations suivantes, prendre la valeur de x0
                    E0, N0 = x0[idIncE,0], x0[idIncN,0]
                
                # Matrice A
                A[idObsEE,idIncE] = 1.0
                A[idObsNN,idIncN] = 1.0
                

                # Matrice dl (avec adaptations valeurs sur intervalle 0-400)
                f0 = E0
                obsEred = obsEE - f0
                dl[idObsEE,0] = obsEred
                f0 = N0
                obsNred = obsNN - f0
                dl[idObsNN,0] = obsNred
                
                # Matrice Kll
                Kll[idObsEE] = point['planiStdDev']**2
                Kll[idObsNN] = point['planiStdDev']**2
                        
            
            
            
            
        
        
        
    
        
        #### ^----- LEVES POLAIRES
        
        if 'polar' in dictCanevas['network'].keys():
            
            
            for station in dictCanevas['network']['polar']['station']:
                
                
                #### ^--------- INDEX ET VALEURS DES INCONNUES
                # index des paramètres inc. supplémentaire distances
                
                
                # FACTEUR ECHELLE
                groupeDistance = rechercheUtils.rechercheGroupeParNom(dictParametres, station['stationData']['distanceGroup'])
                if "idIncFacteurEchelle" in groupeDistance['additionalUnknowns'].keys():
                    
                    idIncFacteurEchelle = groupeDistance['additionalUnknowns']['idIncFacteurEchelle']
                    if iteration == 0:
                        m0 = groupeDistance['additionalUnknowns']['valIncFacteurEchelle']
                        x0[idIncFacteurEchelle,0] = m0
                    else: # itérations suivantes, prendre la valeur de x0
                        m0 = x0[idIncFacteurEchelle,0]
                        
                else: # Si pas à calculer
                    idIncFacteurEchelle = None
                    m0 = 0.0
                    
                    
                # CONSTANTE ADDITION
                if "idIncConstanteAddition" in groupeDistance['additionalUnknowns'].keys():
                    
                    idIncConstanteAddition = groupeDistance['additionalUnknowns']['idIncConstanteAddition']
                    if iteration == 0:
                        c0 = groupeDistance['additionalUnknowns']['valIncConstanteAddition']
                        x0[idIncConstanteAddition,0] = c0
                    else: # itérations suivantes, prendre la valeur de x0
                        c0 = x0[idIncConstanteAddition,0]
                        
                else: # Si pas à calculer
                    idIncConstanteAddition = None
                    c0 = 0.0
                    
                     
                # INCONNUE ORIENTATION
                idIncOri = station['stationData']['idIncOri']
                if iteration == 0:
                    w0 = station['stationData']['valIncOri']
                    x0[idIncOri,0] = w0
                else: # itérations suivantes, prendre la valeur de x0
                    w0 = x0[idIncOri,0]
                    
                
                # COORDONNEES DE STATION
                pointStation = rechercheUtils.rechercheNoPt(dictPoints, station['stationName'])
                if 'idUnkE' in pointStation.keys() and 'idUnkN' in pointStation.keys() :
                    
                    idIncStaE, idIncStaN = pointStation['idUnkE'], pointStation['idUnkN']
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
                
                for observation in station['stationData']['measure']:
                    
                    # COORDONNEES DU POINT VISE
                    pointVis = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                    if 'idUnkE' in pointVis.keys() and 'idUnkN' in pointVis.keys() :
                        
                        idIncVisE, idIncVisN = pointVis['idUnkE'], pointVis['idUnkN']
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
                        
                        
                        
                        
                        #### MODIF EN COURS ICI
                        # if idObsRI in [ 590 , 622,  648 , 649 , 650 ,
                        #                935 , 936, 1047, 1048, 1101 ,1102 ,
                        #                1164 ,1165 , 1166]:
                        #     print(station['stationName'])
                        
                        
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
                        obsRI = float(observation['RI']['value'])
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
                        Kll[idObsRI] = observation['RI']['stdDev']**2
                        
                
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
                        obsDP = float(observation['DP']['value'])
                        f0 = np.sqrt(DN**2+DE**2) -c0 -(m0*np.sqrt(DN**2+DE**2))
                        dl[idObsDP,0] = obsDP-f0
                        
                        # Matrice Kll
                        Kll[idObsDP] = observation['DP']['stdDev']**2
                        
                        
        
        
        
        #### ^----- GNSS
        
        if 'gnss' in dictCanevas['network'].keys():
        
            for session in dictCanevas['network']['gnss']['session']:

                
                #### ^--------- INDEX ET VALEURS DES INCONNUES
                
                paramInconnus = session['unknownParameters']
                
                
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
                
                for observation in session['measure']:
                    
                    # COORDONEES DU POINT VISE
                    pointVis = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                    if 'idUnkE' in pointVis.keys() and 'idUnkN' in pointVis.keys() :
                        
                        idIncVisE, idIncVisN = pointVis['idUnkE'], pointVis['idUnkN']
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
                    Evis, Nvis = Evis - session['centroids']['meanE'], Nvis - session['centroids']['meanN']
                    
                        
                    
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
                        obsLY = float(observation['LY']['value'])  - session['centroids']['meanY']
                        f0 = tE0 + lam0*np.cos(rot0*np.pi/200.0)*Evis - lam0*np.sin(rot0*np.pi/200.0)*Nvis
                        dl[idObsLY,0] = obsLY-f0
                        
                        # Matrice Kll
                        Kll[idObsLY] = observation['LY']['stdDev']**2
                        
                        
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
                        obsLX = float(observation['LX']['value'])  - session['centroids']['meanX']
                        f0 = tN0 + lam0*np.sin(rot0*np.pi/200.0)*Evis + lam0*np.cos(rot0*np.pi/200.0)*Nvis
                        dl[idObsLX,0] = obsLX-f0
                        
                        # Matrice Kll
                        Kll[idObsLX] = observation['LX']['stdDev']**2
                        
                        
            
                        
            
        #### ^----- SYSTEMES LOCAUX
        
        if 'localSystems' in dictCanevas['network'].keys():
        
            for systeme in dictCanevas['network']['localSystems']['localSystem']:
                
                #### ^--------- INDEX ET VALEURS DES INCONNUES
                
                paramInconnus = systeme['unknownParameters']
                
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
                
                for observation in systeme['measure']:
                    
                    # COORDONEES DU POINT VISE
                    pointVis = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                    if 'idUnkE' in pointVis.keys() and 'idUnkN' in pointVis.keys() :
                        
                        idIncVisE, idIncVisN = pointVis['idUnkE'], pointVis['idUnkN']
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
                    Evis, Nvis = Evis - systeme['centroids']['meanE'], Nvis - systeme['centroids']['meanN']
                    
                    
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
                        obsLY = float(observation['LY']['value']) - systeme['centroids']['meanY']
                        f0 = tE0 + lam0*np.cos(rot0*np.pi/200.0)*Evis - lam0*np.sin(rot0*np.pi/200.0)*Nvis 
                        dl[idObsLY,0] = obsLY-f0
                        
                        # Matrice Kll
                        Kll[idObsLY] = observation['LY']['stdDev']**2
                            
                        
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
                        obsLX = float(observation['LX']['value']) - systeme['centroids']['meanX']
                        f0 = tN0 + lam0*np.sin(rot0*np.pi/200.0)*Evis + lam0*np.cos(rot0*np.pi/200.0)*Nvis 
                        dl[idObsLX,0] = obsLX-f0
                        
                        # Matrice Kll
                        Kll[idObsLX] = observation['LX']['stdDev']**2
                    
            
               
            
            
        #### ^----- COTES
        
        
        if 'simpleMeasures' in dictCanevas['network'].keys():
            
            for cote in dictCanevas['network']['simpleMeasures']['simpleMeasure']:
                
                observation = cote['measure']
                
                #### ^--------- INDEX ET VALEURS DES INCONNUES
                
                # COORDONEES DU POINT VISE NO 1
                pointVis1 = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName1'])
                if 'idUnkE' in pointVis1.keys() and 'idUnkN' in pointVis1.keys() :
                    
                    idIncVisE1, idIncVisN1 = pointVis1['idUnkE'], pointVis1['idUnkN']
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
                pointVis2 = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName2'])
                if 'idUnkE' in pointVis2.keys() and 'idUnkN' in pointVis2.keys() :
                    
                    idIncVisE2, idIncVisN2 = pointVis2['idUnkE'], pointVis2['idUnkN']
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
                    obsDP = float(observation['DP']['value'])
                    f0 = np.sqrt(DN**2+DE**2) 
                    dl[idObsDP,0] = obsDP-f0
                    
                    # Matrice Kll
                    Kll[idObsDP] = observation['DP']['stdDev']**2
                        
    
        #### ^----- CONTRAINTES    
        
        if 'constraints' in dictCanevas['network'].keys():
            
            for contrainte in dictCanevas['network']['constraints']['constraint']:
                
                # Si non-écartée
                if contrainte['discarded'] in ['false', None]:
                    
                    # Points et index des inc. de coordonnées, rechercher les pts avec leur role respectifs ('pointTypeInConstraint')
                    for pt in contrainte['point']:
                        if pt['pointTypeInConstraint'] == "A":
                            noPtA = pt['pointName']
                        if pt['pointTypeInConstraint'] == "B":
                            noPtB = pt['pointName']
                        if pt['pointTypeInConstraint'] == "P":
                            noPtP = pt['pointName']
                    pointA = rechercheUtils.rechercheNoPt(dictPoints, noPtA)
                    pointB = rechercheUtils.rechercheNoPt(dictPoints, noPtB)
                    pointP = rechercheUtils.rechercheNoPt(dictPoints, noPtP)
                    
                    
                    # COORDONEES DU POINT VISE A
                    if 'idUnkE' in pointA.keys() and 'idUnkN' in pointA.keys() :
                        
                        idIncVisEA, idIncVisNA = pointA['idUnkE'], pointA['idUnkN']
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
                    if 'idUnkE' in pointB.keys() and 'idUnkN' in pointB.keys() :
                        
                        idIncVisEB, idIncVisNB = pointB['idUnkE'], pointB['idUnkN']
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
                    if 'idUnkE' in pointP.keys() and 'idUnkN' in pointP.keys() :
                        
                        idIncVisEP, idIncVisNP = pointP['idUnkE'], pointP['idUnkN']
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
                    dm1 = contrainte['dm1']['value']
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
                    if contrainte['constraintType'] == 'alignment':
                        
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
                    if contrainte['constraintType'] == 'perpendicular':
                        
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
                    
                    
                        
                    
        #### ESTIMATION

        # matrices compressées (sans perte) pour calculs rapides via SciPy
        if iteration == 0:
            xInitial = copy.deepcopy(x0)
        sparseP = sparse.diags(W * 1/((1/sigma0**2)*Kll))
        t = -cx0
        sparseC = sparse.csc_matrix(C, dtype=np.longdouble)
        sparseA = sparse.csc_matrix(A, dtype=np.longdouble)
        sparseAT = sparseA.transpose()
        sparseATP = sparseAT.dot(sparseP)
        sparseATPA = sparseATP.dot(sparseA)
        sparseM = sparse.bmat([[sparseATPA , sparseC.transpose()],
                               [sparseC    , sparseZcc          ]], format='csc')
        b = np.block([[sparseATP.dot(dl)],
                      [t]])
        
        
        
        # np.save('A.npy', A)
        
        #### ANALYSES DE SOLVABILITE
        P = np.diag(W * 1/((1/sigma0**2)*Kll))
        Zcc = np.zeros((nbConPlani,nbConPlani))
        M = np.block([[A.T@P@A      ,   C.T ],
                     [C          ,   Zcc ]])
        b = np.block([[A.T@P@dl],
                      [t]])
        
        
        #### ANALYSE DE SOLVABILITE
        
        listeIdCoord = list(set(listeIdCoord)) # Liste des dx qui concerne que les coordonnées
        AnalyseSolvabilite = analyseSolvabiliteUtils.SolvabilityAnalysis(M, b, listeIdCoord, critereInterruption,
                                                                         dictCanevas, dictPoints, dictParametres)
        AnalyseSolvabilite.runAnalysis()
        
        
        
        
        
        # Décomposition superLU et solve méthode avec membre de droite
        if iteration > 0: # pour la stabilité de calcul, si une iteration engendre une matrice singulière (dx trop petits pour être stables)
            try:
                MSPLU = sparse.linalg.splu(sparseM)
            except:
                print('!!! SINGULAR MATRIX, NETWORK NOT SOLVABLE 1 - CHECK DETERMINATIONS !!!')
                
        else:
            try:
                MSPLU = sparse.linalg.splu(sparseM)
            except:
                print('!!! SINGULAR MATRIX, NETWORK NOT SOLVABLE 2 - CHECK DETERMINATIONS !!!')
        
        try:
            dX = MSPLU.solve(b)
        except:
            print('!!! SINGULAR MATRIX, NETWORK NOT SOLVABLE 3 - CHECK DETERMINATIONS !!!')
        dx = np.array(dX[0:nbIncPlani],dtype=np.longdouble)
        x0 += dx # MAJ du vecteur des inconnues (pour itérations suivantes)
        
        
        
        
        
        
        #### CRITERES INTERRUPTION
        
        dxCoord = []
        for i in listeIdCoord:
            dxCoord.append(dx[i,0])

        # Maximum dx sur une coordonnée et compte
        dxCoordMax = np.max(np.abs(dxCoord))
        countDxMax = 0
        for dxi in dxCoord: # compte des dx > au critère interruption
            if abs(dxi) > critereInterruption:
                countDxMax += 1
        logIterations += "---- Iteration n°{:d} with max(dx) on a coordinate = {:0.3f} m ({:d} dx superior to {:0.3f} m)\n".format(iteration, dxCoordMax,countDxMax, critereInterruption )
        print( "---- Iteration n°{:d} with max(dx) on a coordinate = {:0.3f} m ({:d} dx superior to {:0.3f} m)".format(iteration, dxCoordMax,countDxMax, critereInterruption ))
        if iteration >= nbrIterationMax or abs(dxCoordMax) <= critereInterruption :
            if robuste and iteration > 1: # si c'est robuste, faire au moins 3 itérations
                cont = False
            elif not robuste:
                cont = False
            
        
        
        # incrément de la boucle princ.
        iteration += 1   
            
        
        
        #### CALCULS DES INDICATEURS
        
        # Calcul des wi à chaque itérations pour robuste
        if robuste:
            
            # vecteur des résidus v
            v = sparseA.dot(dx) - dl

            # cofacteurs des obs. Qll
            sparseQll = sparse.diags(1/(W * 1/((1/sigma0**2)*Kll)))
            diagQll = 1/(W * 1/((1/sigma0**2)*Kll))
            
            
            # COFACTEURS DES INCONNUES QXX
            print('Unknowns cofactors matrix...')
            timer1 = time.time()
            # try:
            #     Qxx_gpu = cupy.linalg.inv(cupy.array(sparseM.A, dtype=cupy.float32))[0:nbIncPlani,0:nbIncPlani]
            #     Qxx= Qxx_gpu.get()
            # except:
            #     print("WARNING 2900: UNABLE TO ALLOCATE NEEDED MEMORY TO GPU, -> USING CPU INSTEAD")
            Qxx = np.linalg.inv(np.array(sparseM.A, dtype=np.float32))[0:nbIncPlani,0:nbIncPlani]
    
            print('End unknowns cofactors matrix in {:0.1f}s'.format( time.time()-timer1))
            
            
            # COFACTEURS DES RESIDUS QVV
            print('Residuals cofactors matrix...')
            timer1 = time.time()
            # try:
            #     A_gpu = cupy.array(A)
            #     Qvv = sparseQll - (A_gpu @ Qxx_gpu @ A_gpu.T).get()
            #     # libération de la mémoire GPU
            #     del Qxx_gpu 
            #     del A_gpu
            # except:
            #     print("WARNING 2900: UNABLE TO ALLOCATE NEEDED MEMORY TO GPU, -> USING CPU INSTEAD")
            Qvv = sparseQll - sparseA @ Qxx @ sparseAT
            # cupy._default_memory_pool.free_all_blocks() 
            print('End residuals cofactors matrix in {:0.1f}s'.format( time.time()-timer1))
            
            # résidus normés wi
            for idObs, vi in enumerate(v[:,0]):
                qvvi = Qvv[idObs,idObs]
                if qvvi > 0.0:
                    w[idObs] = vi / (sigma0 * np.sqrt(qvvi))
                else:
                    w[idObs] = 0.0
                if abs(w[idObs]) > cRobuste:
                    W[idObs] = cRobuste/abs(w[idObs])
                    # print(W[idObs], idObs, cRobuste) # pour debug
                    
                    
    
    updateProgressBar(progressBar, 5)
    
    # delete A et C pour libérer RAM
    del A
    del C

    # Calcul pour L2 uniquement après convergence
    if not robuste :
        
        # vecteur des résidus v
        v = sparseA.dot(dx) - dl
        
        # cofacteurs des obs. Qll
        sparseQll = sparse.diags(1/(W * 1/((1/sigma0**2)*Kll)))
        diagQll = 1/(W * 1/((1/sigma0**2)*Kll))
        
        
        # COFACTEURS DES INCONNUES QXX
        print('Unknowns cofactors matrix...')
        timer1 = time.time()
        # try:
        #     Qxx_gpu = cupy.linalg.inv(cupy.array(sparseM.A, dtype=cupy.float32))[0:nbIncPlani,0:nbIncPlani]
        #     Qxx= Qxx_gpu.get()
        # except:
        #     print("WARNING 2900: UNABLE TO ALLOCATE NEEDED MEMORY TO GPU, -> USING CPU INSTEAD")
        Qxx = np.linalg.inv(np.array(sparseM.A, dtype=np.float32))[0:nbIncPlani,0:nbIncPlani]

        print('End unknowns cofactors matrix in {:0.1f}s'.format( time.time()-timer1))
        
        

        # COFACTEURS DES RESIDUS QVV
        print('Residuals cofactors matrix...')
        timer1 = time.time()
        # try:
        #     A_gpu = cupy.array(A)
        #     Qvv = sparseQll - (A_gpu @ Qxx_gpu @ A_gpu.T).get()
        #     # libération de la mémoire GPU
        #     del Qxx_gpu 
        #     del A_gpu
        # except:
        #     print("WARNING 2900: UNABLE TO ALLOCATE NEEDED MEMORY TO GPU, -> USING CPU INSTEAD")
        Qvv = sparseQll - sparseA @ Qxx @ sparseAT
        # cupy._default_memory_pool.free_all_blocks() 
        print('End residuals cofactors matrix in {:0.1f}s'.format( time.time()-timer1))
        
        # résidus normés wi
        for idObs, vi in enumerate(v[:,0]):
            qvvi = Qvv[idObs,idObs]
            if qvvi > 0.0:
                w[idObs] = vi / (sigma0 * np.sqrt(qvvi))
            else:
                w[idObs] = 0.0
                
        
        
    # s0 empirique
    s0 = np.sqrt((v.T@sparseP@v)/(nbObsPlani-nbIncPlani))[0,0]
    quotientGlobal = s0/sigma0
    
    # ...Suite des idicateurs 
    # Variance-covariance inconnues Kxx
    Kxx = s0**2*Qxx
    
      
            
    #### MAJ OBSERVATIONS ET INDICATEURS (+inc. sup. dist.)
    
    # Quotients de groupes
    dictQuotients = {}
    
    # Valeur de nablaLi théoriquement infinie (->stabilité de calcul)
    nablaLiInfini = 20.0
    
    # Si libre-ajusté, groupe des obs. de rattachement
    if libreAjuste:
        dictQuotients.update({'controlPointsGroup':{'vk':[], 'pk':[], 'zk':[]}})
    

    
    #### ^----- LEVES POLAIRES
    if 'polar' in dictCanevas['network'].keys():
        
        # Récupérer les noms de tous les types groupes pour levé polaire pour le calcul des quotients
        listeNomsGroupesDistance = []
        listeNomsGroupesDirection = []
        for groupeDist in dictParametres['parameters']['groups']['distanceGroups']['distanceGroup']:
            listeNomsGroupesDistance.append(groupeDist['distanceGroupName']) # pour calcul quotients
            
            # Inconnues supplémentaire des groupes de distance
            dictGroupeDist = {'distanceGroupName':groupeDist['distanceGroupName']}
            if groupeDist['additionalUnknowns']['scaleFactor'] == "true":
                idIncFacteurEchelle = groupeDist['additionalUnknowns']['idIncFacteurEchelle']
                valeur = x0[idIncFacteurEchelle,0]
                ecartType = np.sqrt(Kxx[idIncFacteurEchelle,idIncFacteurEchelle])
                groupeDist['additionalUnknowns']['valIncFacteurEchelle'] = round(1+valeur,7)
                groupeDist['additionalUnknowns'].update({'stdDevScaleFactor':round(ecartType,7)})
                
            if groupeDist['additionalUnknowns']['additionConstant'] == "true":
                idIncConstanteAddition = groupeDist['additionalUnknowns']['idIncConstanteAddition']
                valeur = x0[idIncConstanteAddition,0]
                ecartType = np.sqrt(Kxx[idIncConstanteAddition,idIncConstanteAddition])
                groupeDist['additionalUnknowns']['valIncConstanteAddition'] = round(valeur,4)
                groupeDist['additionalUnknowns'].update({'stdDevAdditionConstant':round(ecartType,4)})
                


         
        for groupeDir in dictParametres['parameters']['groups']['directionGroups']['directionGroup']:
            listeNomsGroupesDirection.append(groupeDir['directionGroupName'])
        
        # rendre les valeurs uniques en "set"
        listeNomsGroupesDistance = set(listeNomsGroupesDistance)
        listeNomsGroupesDirection = set(listeNomsGroupesDirection)
        for groupe in listeNomsGroupesDistance :
            dictQuotients.update({groupe:{'vk':[], 'pk':[], 'zk':[]}})
        for groupe in listeNomsGroupesDirection :
            dictQuotients.update({groupe:{'vk':[], 'pk':[], 'zk':[]}})


        for station in dictCanevas['network']['polar']['station']:
            
            # indicateurs et valeurs de l'inc. ori.
            stationnement = station['stationData']
            idIncOri = stationnement['idIncOri']
            stationnement['valIncOri'] = round(x0[idIncOri,0],5)
            EMincOri = np.sqrt(Kxx[idIncOri,idIncOri])
            stationnement.update({'EMincOri':round(EMincOri,5)})
            
            # Indicateurs sur les obs.
            for observation in stationnement['measure']:
                
                RI, DP = observation['RI'], observation['DP']
                
                # RI
                if 'idObsPlani' in RI.keys(): # si pas écarté
                    idObsRI = RI['idObsPlani']
                    vi = v[idObsRI,0]
                    zi = Qvv[idObsRI, idObsRI] / diagQll[idObsRI]
                    if zi > 0.0: # éviter les division par 0
                        nablaLi = 4.1 * np.sqrt(Kll[idObsRI]) / np.sqrt(zi)
                    else:
                        nablaLi = nablaLiInfini
                    nabla[idObsRI,0] = nablaLi
                    wi = w[idObsRI] / W[idObsRI]
                    if zi == 0.0: # éviter les divisions par 0
                        gi = np.nan
                    else:
                        gi = -vi/zi
                    viLat = np.sin(vi*np.pi/200.0) * DP['value']
                    RI.update({'vi':round(vi,5)})
                    RI.update({'wi':round(wi,2)})
                    RI.update({'zi':round(zi,2)})
                    RI.update({'nablaLi':round(nablaLi,5)})
                    RI.update({'gi':round(gi,5)})
                    RI.update({'viLat':round(viLat,5)})
                    RI.update({'dist':round(DP['value'],3)})
                    if robuste:
                        RI.update({'weightRobustFactor':round(W[idObsRI],2)})
                    
                    # pour quotients
                    dictQuotients[stationnement['directionGroup']]['vk'].append(vi)
                    dictQuotients[stationnement['directionGroup']]['pk'].append(1/diagQll[idObsRI])
                    dictQuotients[stationnement['directionGroup']]['zk'].append(zi)

                
                # DP
                if 'idObsPlani' in DP.keys(): # si pas écarté
                    idObsDP = DP['idObsPlani']
                    vi = v[idObsDP,0]
                    zi = Qvv[idObsDP, idObsDP] / diagQll[idObsDP]
                    if zi > 0.0:
                        nablaLi = 4.1 * np.sqrt(Kll[idObsDP]) / np.sqrt(zi)
                    else:
                        nablaLi = nablaLiInfini
                    nabla[idObsDP,0] = nablaLi
                    wi = w[idObsDP] / W[idObsDP]
                    if zi == 0.0: # éviter les divisions par 0
                        gi = np.nan
                    else:
                        gi = -vi/zi
                    DP.update({'vi':round(vi,4)})
                    DP.update({'wi':round(wi,2)})
                    DP.update({'zi':round(zi,2)})
                    DP.update({'nablaLi':round(nablaLi,4)})
                    DP.update({'gi':round(gi,4)})
                    if robuste:
                        DP.update({'weightRobustFactor':round(W[idObsDP],2)})
                    
                    # pour quotients
                    dictQuotients[stationnement['distanceGroup']]['vk'].append(vi)
                    dictQuotients[stationnement['distanceGroup']]['pk'].append(1/diagQll[idObsDP])
                    dictQuotients[stationnement['distanceGroup']]['zk'].append(zi)
                    
    
    #### ^----- GNSS
    if 'gnss' in dictCanevas['network'].keys():
        
        
        # Récupérer les noms de tous les types groupes pour levé polaire pour le calcul des quotients
        listeNomsGroupesGNSS = []
        for groupeGNSS in dictParametres['parameters']['groups']['gnssGroups']['gnssGroup']:
            listeNomsGroupesGNSS.append(groupeGNSS['gnssGroupName'])
        
        # rendre les valeurs uniques en "set"
        listeNomsGroupesGNSS = set(listeNomsGroupesGNSS)
        for groupe in listeNomsGroupesGNSS :
            dictQuotients.update({groupe:{'vk':[], 'pk':[], 'zk':[]}})

    
        for session in dictCanevas['network']['gnss']['session']:
       
            paramInconnus = session['unknownParameters']

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
            for observation in session['measure']:
                
                LY, LX = observation['LY'], observation['LX']
                
                # LY
                if 'idObsPlani' in LY.keys(): # si pas écarté
                    idObsLY = LY['idObsPlani']
                    vi = v[idObsLY,0]
                    zi = Qvv[idObsLY, idObsLY] / diagQll[idObsLY]
                    if zi > 0.0:
                        nablaLi = 4.1 * np.sqrt(Kll[idObsLY]) / np.sqrt(zi)
                    else:
                        nablaLi = nablaLiInfini
                    nabla[idObsLY,0] = nablaLi
                    wi = w[idObsLY] / W[idObsLY]
                    if zi == 0.0: # éviter les divisions par 0
                        gi = np.nan
                    else:
                        gi = -vi/zi
                    LY.update({'vi':round(vi,4)})
                    LY.update({'wi':round(wi,2)})
                    LY.update({'zi':round(zi,2)})
                    LY.update({'nablaLi':round(nablaLi,4)})
                    LY.update({'gi':round(gi,4)})
                    if robuste:
                        LY.update({'weightRobustFactor':round(W[idObsLY],2)})
                    
                    # pour quotients
                    dictQuotients[session['gnssGroup']]['vk'].append(vi)
                    dictQuotients[session['gnssGroup']]['pk'].append(1/diagQll[idObsLY])
                    dictQuotients[session['gnssGroup']]['zk'].append(zi)
                    
                # LX
                if 'idObsPlani' in LX.keys(): # si pas écarté
                    idObsLX = LX['idObsPlani']
                    vi = v[idObsLX,0]
                    zi = Qvv[idObsLX, idObsLX] / diagQll[idObsLX]
                    if zi > 0.0:
                        nablaLi = 4.1 * np.sqrt(Kll[idObsLX]) / np.sqrt(zi)
                    else:
                        nablaLi = nablaLiInfini
                    nabla[idObsLX,0] = nablaLi
                    wi = w[idObsLX] / W[idObsLX]
                    if zi == 0.0: # éviter les divisions par 0
                        gi = np.nan
                    else:
                        gi = -vi/zi
                    LX.update({'vi':round(vi,4)})
                    LX.update({'wi':round(wi,2)})
                    LX.update({'zi':round(zi,2)})
                    LX.update({'nablaLi':round(nablaLi,4)})
                    LX.update({'gi':round(gi,4)})
                    if robuste:
                        LX.update({'weightRobustFactor':round(W[idObsLX],2)})
                    
                    # pour quotients
                    dictQuotients[session['gnssGroup']]['vk'].append(vi)
                    dictQuotients[session['gnssGroup']]['pk'].append(1/diagQll[idObsLX])
                    dictQuotients[session['gnssGroup']]['zk'].append(zi)
                    
                    
                    
    #### ^----- SYSTEMES LOCAUX
    if 'localSystems' in dictCanevas['network'].keys():
        
        # Récupérer les noms de tous les types groupes pour levé polaire pour le calcul des quotients
        listeNomsGroupesSysteme = []
        for groupeSysteme in dictParametres['parameters']['groups']['localSystemGroups']['localSystemGroup']:
            listeNomsGroupesSysteme.append(groupeSysteme['localSystemGroupName'])
        
        # rendre les valeurs uniques en "set"
        listeNomsGroupesSysteme = set(listeNomsGroupesSysteme)
        for groupe in listeNomsGroupesSysteme :
            dictQuotients.update({groupe:{'vk':[], 'pk':[], 'zk':[]}})
            
            
    
        for systeme in dictCanevas['network']['localSystems']['localSystem']:
            
            paramInconnus = systeme['unknownParameters']
            
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
            for observation in systeme['measure']:
                
                LY, LX = observation['LY'], observation['LX']
                
                # LY
                if 'idObsPlani' in LY.keys(): # si pas écarté
                    idObsLY = LY['idObsPlani']
                    vi = v[idObsLY,0]
                    zi = Qvv[idObsLY, idObsLY] / diagQll[idObsLY]
                    if zi > 0.0:
                        nablaLi = 4.1 * np.sqrt(Kll[idObsLY]) / np.sqrt(zi)
                    else:
                        nablaLi = nablaLiInfini
                    nabla[idObsLY,0] = nablaLi # pour calcul futur de la fiab. externe
                    wi = w[idObsLY] /  W[idObsLY]
                    if zi == 0.0: # éviter les divisions par 0
                        gi = np.nan
                    else:
                        gi = -vi/zi
                    LY.update({'vi':round(vi,4)})
                    LY.update({'wi':round(wi,2)})
                    LY.update({'zi':round(zi,2)})
                    LY.update({'nablaLi':round(nablaLi,4)})
                    LY.update({'gi':round(gi,4)})
                    if robuste:
                        LY.update({'weightRobustFactor':round(W[idObsLY],2)})
                    
                    # pour quotients
                    dictQuotients[systeme['localSystemGroup']]['vk'].append(vi)
                    dictQuotients[systeme['localSystemGroup']]['pk'].append(1/diagQll[idObsLY])
                    dictQuotients[systeme['localSystemGroup']]['zk'].append(zi)
                    
                # LY
                if 'idObsPlani' in LX.keys(): # si pas écarté
                    idObsLX = LX['idObsPlani']
                    vi = v[idObsLX,0]
                    zi = Qvv[idObsLX, idObsLX] / diagQll[idObsLX]
                    if zi > 0.0:
                        nablaLi = 4.1 * np.sqrt(Kll[idObsLX]) / np.sqrt(zi)
                    else:
                        nablaLi = nablaLiInfini
                    nabla[idObsLX,0] = nablaLi
                    wi = w[idObsLX] /  W[idObsLX]
                    if zi == 0.0: # éviter les divisions par 0
                        gi = np.nan
                    else:
                        gi = -vi/zi
                    LX.update({'vi':round(vi,4)})
                    LX.update({'wi':round(wi,2)})
                    LX.update({'zi':round(zi,2)})
                    LX.update({'nablaLi':round(nablaLi,4)})
                    LX.update({'gi':round(gi,4)})
                    if robuste:
                        LX.update({'weightRobustFactor':round(W[idObsLX],2)})
                    
                    # pour quotients
                    dictQuotients[systeme['localSystemGroup']]['vk'].append(vi)
                    dictQuotients[systeme['localSystemGroup']]['pk'].append(1/diagQll[idObsLX])
                    dictQuotients[systeme['localSystemGroup']]['zk'].append(zi)
                    
                    
                   
                    
                
    #### ^----- COTES
    if 'simpleMeasures' in dictCanevas['network'].keys():
        
        # Récupérer les noms de tous les types groupes pour levé polaire pour le calcul des quotients
        listeNomsGroupesCotes = []
        for groupeCote in dictParametres['parameters']['groups']['simpleMeasureGroups']['simpleMeasureGroup']:
            listeNomsGroupesCotes.append(groupeCote['simpleMeasureGroupName'])
        
        # rendre les valeurs uniques en "set"
        listeNomsGroupesCotes = set(listeNomsGroupesCotes)
        for groupe in listeNomsGroupesCotes :
            dictQuotients.update({groupe:{'vk':[], 'pk':[], 'zk':[]}})
        
        for cote in dictCanevas['network']['simpleMeasures']['simpleMeasure']:
            
            DP = cote['measure']['DP']

            if 'idObsPlani' in DP.keys(): # si pas écarté
                idObsDP = DP['idObsPlani']
                vi = v[idObsDP,0]
                zi = Qvv[idObsDP, idObsDP] / diagQll[idObsDP]
                if zi > 0.0:
                    nablaLi = 4.1 * np.sqrt(Kll[idObsDP]) / np.sqrt(zi)
                else:
                    nablaLi = nablaLiInfini
                nabla[idObsDP,0] = nablaLi
                wi = w[idObsDP] /  W[idObsDP]
                if zi == 0.0: # éviter les divisions par 0
                    gi = np.inf
                else:
                    gi = -vi/zi
                DP.update({'vi':round(vi,4)})
                DP.update({'wi':round(wi,2)})
                DP.update({'zi':round(zi,2)})
                DP.update({'nablaLi':round(nablaLi,4)})
                DP.update({'gi':round(gi,4)})
                if robuste:
                    DP.update({'weightRobustFactor':round(W[idObsDP],2)})
                
                # pour quotients
                dictQuotients[cote['simpleMeasureGroup']]['vk'].append(vi)
                dictQuotients[cote['simpleMeasureGroup']]['pk'].append(1/diagQll[idObsDP])
                dictQuotients[cote['simpleMeasureGroup']]['zk'].append(zi)
        
        
    #### ^----- PTS RATTACHEMENT
    if libreAjuste:
        
        for point in listeLA:

            # EE
            idObsEE = point['idObsEE']
            vi = v[idObsEE,0]
            zi = Qvv[idObsEE, idObsEE] / diagQll[idObsEE]
            if zi > 0.0:
                nablaLi = 4.1 * np.sqrt(Kll[idObsEE]) / np.sqrt(zi)
            else:
                nablaLi = nablaLiInfini
            nabla[idObsEE,0] = nablaLi
            wi = w[idObsEE] / W[idObsEE]
            if zi == 0.0: # éviter les divisions par 0
                gi = np.inf
            else:
                gi = -vi/zi
            indicateursEE = {}
            indicateursEE.update({'vi':round(vi,4)})
            indicateursEE.update({'wi':round(wi,2)})
            indicateursEE.update({'zi':round(zi,2)})
            indicateursEE.update({'nablaLi':round(nablaLi,4)})
            indicateursEE.update({'gi':round(gi,4)})
            if robuste:
                indicateursEE.update({'weightRobustFactor':round(W[idObsEE],2)})
            point.update({'indicateursEE':indicateursEE})
            
            # pour quotients
            dictQuotients['controlPointsGroup']['vk'].append(vi)
            dictQuotients['controlPointsGroup']['pk'].append(1/diagQll[idObsEE])
            dictQuotients['controlPointsGroup']['zk'].append(zi)
            
            # NN
            idObsNN = point['idObsNN']
            vi = v[idObsNN,0]
            zi = Qvv[idObsNN, idObsNN] / diagQll[idObsNN]
            if zi > 0.0:
                nablaLi = 4.1 * np.sqrt(Kll[idObsNN]) / np.sqrt(zi)
            else:
                nablaLi = nablaLiInfini
            nabla[idObsNN,0] = nablaLi
            wi = w[idObsNN] / W[idObsNN]
            if zi == 0.0: # éviter les divisions par 0
                gi = np.inf
            else:
                gi = -vi/zi
            indicateursNN = {}
            indicateursNN.update({'vi':round(vi,4)})
            indicateursNN.update({'wi':round(wi,2)})
            indicateursNN.update({'zi':round(zi,2)})
            indicateursNN.update({'nablaLi':round(nablaLi,4)})
            indicateursNN.update({'gi':round(gi,4)})
            if robuste:
                indicateursEE.update({'weightRobustFactor':round(W[idObsNN],2)})
            point.update({'indicateursNN':indicateursNN})
            
            # FS (combiner viEE et viNN)
            point.update({'FS':round((indicateursEE['vi']**2 + indicateursNN['vi']**2)**0.5,4)})
            
            # pour quotients
            dictQuotients['controlPointsGroup']['vk'].append(vi)
            dictQuotients['controlPointsGroup']['pk'].append(1/diagQll[idObsNN])
            dictQuotients['controlPointsGroup']['zk'].append(zi)
            
    

    #### CALCUL DES QUOTIENTS
    
    del Qvv 
    
    updateProgressBar(progressBar, 5)
    
    for key,value in dictQuotients.items():
        # Uniquement si il y a bien des valeurs dans les groupes (utilisés)
        if len(value['vk']) > 0 and len(value['pk']) > 0 and len(value['zk']) > 0:
            
            vk,pk,zk = np.array([value['vk']]).T, np.diag(value['pk']), np.array([value['zk']]).T
            s0k = np.sqrt(vk.T @ pk @ vk / sum(zk))[0,0]
            quotient = s0k/sigma0
            value.update({'quotient':round(quotient,2)})
            # suppression des sous-vecteurs du groupe (meilleure lisibilité)
            value.pop('vk')
            value.pop('pk')
            value.pop('zk')
            



    #### MAJ POINTS ET INDICATEURS

    # Fiabilité etxerne NABLA et NABLAx
    print('External reliability calculations and matrixs...')
    timer1 = time.time()
    sparseNABLA = sparse.diags(nabla[:,0],dtype=np.float32)
    NABLAx = Qxx*sparseAT*sparseP*sparseNABLA
    print('End external reliability calculations and matrixs in {:0.1f}s'.format( time.time()-timer1))
    
    
    del Qxx
    
    updateProgressBar(progressBar, 5)
    
    for point in dictPoints['points']['point']:

        # Uniquement MAJ des points nouveaux
        if 'idUnkE' in point.keys() and 'idUnkN' in point.keys():
            
            idIncE, idIncN = point['idUnkE'], point['idUnkN'] # index des inconnues
            
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
            # u1 = [eigVec[0,1],eigVec[1,1]]
            # sans échelle, tout à 1sigma = 39%
            gisA = np.arctan2(eigVec[1,0],eigVec[1,1]) * 200.0 / np.pi
            if gisA < 0.0:
                gisA += 400.0
            # gisA = np.arccos(u1[0])*200.0/np.pi   formule non-utilisée (sens mathématique)
            ellipseEM = {'a':round(a,4),
                         'b':round(b,4),
                         'bearA':round(gisA,4)} 
            point.update({'stdErrEllipse':ellipseEM})
            
            # Fiabilité externe
            NE, NN = NABLAx[idIncE,:], NABLAx[idIncN,:]
            N = np.sqrt(NE**2+NN**2)
            NA = np.max(N)
            
            if NA > 10 :  # = fiabilité externe infinie
                NA = np.nan
                gisNA = np.nan
                idNA = np.nan
            else: # fiab. externe non-infinie 
                idNA = np.argmax(N)
                gisNA = np.mod(np.arctan2(NE[idNA],NN[idNA])*200.0/np.pi, 400.0)
                
            vecteurFiabExterne = {'NA':round(NA,4),
                                  'bearNA':round(gisNA,4),
                                  'idObsRespNA':idNA} 
            point.update({'externalReliabilityPlaniVector' :vecteurFiabExterne})
            
            # Calcul des diff. entre état initial et après compensation
            dE, dN = x0[idIncE,0] - xInitial[idIncE,0], x0[idIncN,0] - xInitial[idIncN,0]
            deltaCoord = {'dE':round(dE,4),
                          'dN':round(dN,4)}
            point.update({'deltaPlani':deltaCoord})
                
    
    
    #### CLASSEMENT DES WI MAX
    # Récupérer l'obs. des 5 premiers wiMax
    listeWiMaxPlani = []
    wiMaxId = np.flip(np.argsort(np.fabs(w)))
    i = 1
    count = 0
    # Lister tous les wi max>3.5 + 20 suivantss
    nbWiMaxToClassify = (np.fabs(w) > 3.5).sum() + 20
    for idObs in wiMaxId:
        if np.isnan(w[idObs]) == False and i < nbWiMaxToClassify:
            obsWiMax, parent = rechercheUtils.rechercheIdObs(dictCanevas, idObs)
            if obsWiMax != None: # Filtrer si Libre-ajuste
                for key, data in obsWiMax.items():
                    if (key == 'RI' or key == 'DP' or key == 'LY' or key == 'LX' ) and data['discarded'] in ['false', None]:
                        # Selectionner le bon idObs 
                        if data['idObsPlani'] == idObs: 
                            data.update({'obsType':key})
                            listeWiMaxPlani.append({'parent':parent,
                                               'pointName':obsWiMax['pointName'],
                                               'observation':data})
                            i += 1
                                                        
            
        # compter le nb sup à 3.5
        if np.isnan(w[idObs]) == False:
            if abs(w[idObs]) > 3.5 :
                count += 1
            
    
    
    # Remettre les quotients dans les groupes des paramètres
    for key,value in dictQuotients.items():
        #### !!!! MODIFICATION POUR METTRE LES QUOTIENTS DANS LES GROUPES
        for key1 in dictParametres['parameters']['groups'].keys():
            for key2 in dictParametres['parameters']['groups'][key1].keys():
                for groupe in dictParametres['parameters']['groups'][key1][key2]:
                    for key3 in copy.deepcopy(groupe).keys(): # Balise du nom d'un groupe
                        if 'Name' in key3 :
                            if groupe[key3] == key:
                                groupe.update({'stdDevQuotientFor2D':value['quotient']})

                                
                            
                                
                        
      
    
    #### RESULTATS GLOBAUX

    dictResGlobaux['globalResults'].update({'planimetry':{}})
    dictResGlobaux['globalResults']['planimetry'].update({'CalculationTime':"{:0.1f} s".format(time.time()-timer)})
    dictResGlobaux['globalResults']['planimetry'].update({'iterationsCount':"{:d}".format(iteration)})
    dictResGlobaux['globalResults']['planimetry'].update({'iterationsLog':"\n{:s}".format(logIterations)})
    
    # Quotients d'écart-type d'unité de poids par groupe (et global)
    dictResGlobaux['globalResults']['planimetry'].update({'globalStdDevQuotient':round(quotientGlobal,2)})
        
    # Dénombrement
    denombrementPlani = {'unknowns':denombrement['nbIncPlani'], 
                         'observations':denombrement['nbObsPlani'],
                         'constraints':denombrement['nbConPlani'],
                         'overdetermination':denombrement['surabondancePlani']}
    dictResGlobaux['globalResults']['planimetry'].update({'counting':denombrementPlani})
    
    # 5 observations avec leur wiMax
    dictResGlobaux['globalResults']['planimetry'].update({'nbWiSup3.5':count})
    dictResGlobaux['globalResults']['planimetry'].update({'biggestWi':{'wiMax':listeWiMaxPlani}})
    
    # décision de suppression et de tout figurer uniquement dans les paramètres
    # if libreAjuste:
    #     dictResGlobaux['globalResults']['planimetry'].update({'stochasticNetwork':{}})
    #     dictResGlobaux['globalResults']['planimetry']['stochasticNetwork'].update({'point':listeLA})
    
    
    # libérer la mémoire GPU
    # cupy._default_memory_pool.free_all_blocks() 
    
    return None











def estimation1D(dictCanevas, dictPoints, dictParametres, denombrement, dictResGlobaux, progressBar):
    
    timer = time.time()
    # libérer la mémoire GPU
    # cupy._default_memory_pool.free_all_blocks() 

    #### PARAMETRES GENERAUX
    nbrIterationMax = int(dictParametres['parameters']['computationOptions']['maxIterationNbr'])
    critereInterruption = float(dictParametres['parameters']['computationOptions']['interruptionCondition'])
    robuste = dictParametres['parameters']['computationOptions']['robust']
    robuste = True if robuste=="true" else False
    cRobuste = dictParametres['parameters']['computationOptions']['robustLimit']
    if cRobuste == None:
        dictParametres['parameters']['computationOptions']['robustLimit'] = 3.5 # par défaut
        cRobuste = 3.5
    else:
        cRobuste = float(cRobuste)
    typeCalcul = dictParametres['parameters']['computationOptions']['networkType'] # pour libre ajusté
    libreAjuste = True if typeCalcul=='stochastic' else False
    sigma0 = 1.0
    
    # Dénombrement
    nbObsAlti, nbIncAlti = denombrement['nbObsAlti'], denombrement['nbIncAlti']
    
    # Liste des index de coordonnées (pour calculer max(dx) uniq. sur les coordonnées)
    listeIdAlti = []
    logIterations = ''
    
    
    
    # ---------------
    #### LIBRE-AJUSTE
    # ---------------
    if libreAjuste:
        
        listeLA = []
        
        for PF in dictParametres['parameters']['altimetricControlPoints']['point']:
            
            ecartType = float(PF['altiStdDev']['mm']) / 1000.0 # en [m], code erreur à mettre si pas d'écart-type saisi
            PF['altiStdDev'] = ecartType # MAJ en m
            PF.update({'idObsHH':nbObsAlti+1000000}) # ajout de l'idObs
            nbObsAlti += 1
            denombrement['nbObsAlti'] += 1
            denombrement['nbIncAlti'] += 1

            # Ajout des id d'inconnues
            point = rechercheUtils.rechercheNoPt(dictPoints, PF['pointName'])
            HH = float(point['H'])
            PF.update({'HH':HH})
            elemsAlti = point['altimetricElems']
            point['altimetricElems'] = elemsAlti+2
            point.update({'idUnkH':nbIncAlti+1000000}) 
            PF.update({'idUnkH':nbIncAlti+1000000})
            nbIncAlti += 1
            
            listeLA.append(PF)
    
    
    
    
    
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
    for point in dictParametres['parameters']['altimetricControlPoints']['point']:
        listePFalti.append(point['pointName'])
        
        
    updateProgressBar(progressBar, 5)
    
    
    # -----------------------------------------
    #### REMPLISSAGE DES MATRICES ET ITERATIONS
    # -----------------------------------------
    
    # Boucle de calcul principale 
    cont = True
    iteration = 0
    
    while cont :
        
        
        
        #### ^----- OBSERVATION DE COORDONNEES
        
        if libreAjuste:
            
            for point in listeLA:
                
                idIncH = point['idUnkH'] - 1000000
                idObsHH = point['idObsHH'] - 1000000
                obsHH = point['HH']
                if iteration == 0:
                    x0[idIncH,0] = obsHH
                    H0 = obsHH # en 1ere it
                    listeIdAlti.append(idIncH)
                else: # itérations suivantes, prendre la valeur de x0
                    H0 = x0[idIncH,0]
                
                # Matrice A
                A[idObsHH,idIncH] = 1.0
                
                # Matrice dl (avec adaptations valeurs sur intervalle 0-400)
                f0 = H0
                obsHred = obsHH - f0
                dl[idObsHH,0] = obsHred

                # Matrice Kll
                Kll[idObsHH] = point['altiStdDev']**2
                

    
    
        #### ^----- LEVES POLAIRES
        
        if 'polar' in dictCanevas['network'].keys():
    
            for station in dictCanevas['network']['polar']['station']:
                
                
                # ALTITUDE DE STATION
                pointStation = rechercheUtils.rechercheNoPt(dictPoints, station['stationName'])
                if 'idUnkH' in pointStation.keys() :
                    
                    idIncStaH =  pointStation['idUnkH']-1000000
                    
                    # Prendre l'altitude si dispo. pour la première it.
                    if iteration == 0:
                        x0[idIncStaH,0] = float(pointStation['H']) if pointStation['H'] is not None else 0.0
                        Hsta = x0[idIncStaH,0]
                    else: # itérations suivantes, prendre la valeur de x0
                        Hsta = x0[idIncStaH,0]
                    
                    listeIdAlti.append(idIncStaH)
      
                elif pointStation['pointName'] in listePFalti: # si station sur pt fixe
                    idIncStaH = None
                    Hsta = float(pointStation['H'])
                else: # autres points non-définis en alti
                    idIncStaH = None
                  
                    
                #### ^--------- INDEX ET VALEURS DES OBS.
                
                for observation in station['stationData']['measure']:
                    
                    # ALTITUDE DU POINT VISE
                    pointVis = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                    if 'idUnkH' in pointVis.keys() :
                        
                        idIncVisH = pointVis['idUnkH'] - 1000000
                        
                        # Prendre l'altitude si dispo. pour la première it.
                        if iteration == 0:
                            x0[idIncVisH,0] = float(pointVis['H']) if pointVis['H'] is not None else 0.0
                            Hvis = x0[idIncVisH,0]
                        else: # itérations suivantes, prendre la valeur de x0
                            Hvis = x0[idIncVisH,0]
                        
                        listeIdAlti.append(idIncVisH)
                    
                    elif pointVis['pointName'] in listePFalti: # si station sur pt fixe
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
                        obsDH = float(observation['DH']['value'])
                        f0 = Hvis - Hsta
                        dl[idObsDH,0] = obsDH-f0
                        
                        # Matrice Kll
                        
                        Kll[idObsDH] = observation['DH']['stdDev']**2
                        
                        
                        
        #### ^----- GNSS
        
        if 'gnss' in dictCanevas['network'].keys():
        
            for session in dictCanevas['network']['gnss']['session']:
                
                #### ^--------- INDEX ET VALEURS DES INCONNUES
                
                paramInconnus = session['unknownParameters']
                    
                # TRANSLATION H
                if "idIncTranslationH" in paramInconnus.keys():
                    idIncTranslationH = paramInconnus['idIncTranslationH'] - 1000000
                    tH0 = paramInconnus['valIncTranslationH']
                    tH0 = x0[idIncTranslationH,0]
                else: # si fixe
                    idIncTranslationH = None
                    tH0 = 0.0
                    
                    
                    
                #### ^--------- INDEX ET VALEURS DES OBS. ET INC. COORD.
                
                for observation in session['measure']:
                
                    # ALTITUDE DU POINT VISE
                    pointVis = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                    if 'idUnkH' in pointVis.keys() :
                        
                        idIncVisH = pointVis['idUnkH'] - 1000000
                        listeIdAlti.append(idIncVisH)
                        
                        # Prendre l'altitude si dispo. pour la première it.
                        if iteration == 0:
                            x0[idIncVisH,0] = float(pointVis['H']) if pointVis['H'] is not None else 0.0
                            Hvis = x0[idIncVisH,0]
                        else: # itérations suivantes, prendre la valeur de x0
                            Hvis = x0[idIncVisH,0]
                        
                        # Hvis = x0[idIncVisH,0]
                    
                    elif pointVis['pointName'] in listePFalti: # si station sur pt fixe
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
                        obsLH = float(observation['LH']['value'])
                        f0 = Hvis + tH0
                        dl[idObsLH,0] = obsLH-f0
                        
                        # Matrice Kll
                        Kll[idObsLH] = observation['LH']['stdDev']**2
                    
                    
        

        #### ESTIMATION
       
        # matrices compressées (sans perte) pour calculs rapides via SciPy
        if iteration == 0:
            xInitial = copy.deepcopy(x0)
        sparseP = sparse.diags(W * 1/((1/sigma0**2)*Kll))
        sparseA = sparse.csc_matrix(A)
        sparseAT = sparseA.transpose()
        sparseATP = sparseAT.dot(sparseP)
        sparseATPA = sparseATP.dot(sparseA)
        b = sparseATP.dot(dl)

        # Décomposition superLU et solve méthode avec membre de droite
        if iteration > 0: # pour stabilité du calcul si première itération
            try:
                SPLU = sparse.linalg.splu(sparseATPA)
            except:
                print('!!! NETWORK NOT SOLVABLE - CHECK DETERMINATIONS !!!')
        else:
            try:
                SPLU = sparse.linalg.splu(sparseATPA)
            except:
                print('!!! NETWORK NOT SOLVABLE - CHECK DETERMINATIONS !!!')
            
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
        logIterations += "---- Iteration n°{:d} with max(dx) on an altitude = {:0.3f} m ({:d} dx superior to {:0.3f} m)\n".format(iteration, dxCoordMax,countDxMax, critereInterruption )
        print( "---- Iteration n°{:d} with max(dx) on an altitude = {:0.3f} m ({:d} dx superior to {:0.3f} m)".format(iteration, dxCoordMax,countDxMax, critereInterruption ))
        if iteration >= nbrIterationMax or dxCoordMax <= critereInterruption :
            if robuste and iteration > 1: # si c'est robuste, faire au moins 3 itérations
                cont = False
            elif not robuste:
                cont = False
            
        # incrément de la boucle princ.
        iteration += 1
            
        
        
    
        #### CALCULS DES INDICATEURS
        
        # Calcul des wi à chaque itérations pour robuste
        if robuste:
            # vecteur des résidus v
            v = sparseA.dot(dx) - dl
    
            # cofacteurs des obs. Qll
            sparseQll = sparse.diags(1/(W * 1/((1/sigma0**2)*Kll)))
            diagQll = 1/(W * 1/((1/sigma0**2)*Kll))
            
            # cofacteurs des inconnues Qxx
            print('Unknowns cofactors matrix...')
            timer1 = time.time()
 
            # if nbIncAlti> 5000:
            #     try:
            #         Qxx = cupy.linalg.inv(cupy.array(sparseATPA.A, dtype=cupy.float32)).get()
            #     except:
            #         print("WARNING 2900: UNABLE TO ALLOCATE NEEDED MEMORY TO GPU, -> USING CPU INSTEAD")
            #         Qxx = np.linalg.inv(np.array(sparseATPA.A, dtype=np.float32))
            # else:
            Qxx = np.linalg.inv(np.array(sparseATPA.A, dtype=np.float32))
            print('End unknowns cofactors matrix in {:0.1f}s'.format( time.time()-timer1))
            
            # cofacteurs des résidus Qvv
            print('Residuals cofactors matrix...')
            timer1 = time.time()
            Qvv = np.array(sparseQll - sparseA * Qxx * sparseAT, dtype=np.float32)
            print('End residuals cofactors matrix in {:0.1f}s'.format( time.time()-timer1))
            
            # résidus normés wi
            for idObs, vi in enumerate(v[:,0]):
                qvvi = Qvv[idObs,idObs]
                if qvvi > 0.0:
                    w[idObs] = vi / (sigma0 * np.sqrt(qvvi))
                else:
                    w[idObs] = 0.0
                if abs(w[idObs]) > cRobuste:
                    W[idObs] = cRobuste/abs(w[idObs])
        
  
    
    updateProgressBar(progressBar, 5)
    
    # Calcul pour L2 uniquement 
    if not robuste:
        
        # vecteur des résidus v
        v = sparseA.dot(dx) - dl
        
        # cofacteurs des obs. Qll
        sparseQll = sparse.diags(1/(W * 1/((1/sigma0**2)*Kll)))
        diagQll = 1/(W * 1/((1/sigma0**2)*Kll))
        
        # cofacteurs des inconnues Qxx
        print('Unknowns cofactors matrix...')
        timer1 = time.time()

        # try:
        #     Qxx_gpu = cupy.linalg.inv(cupy.array(sparseATPA.A, dtype=cupy.float32))
        #     Qxx = Qxx_gpu.get()
        # except:
        #     print("WARNING 3900: UNABLE TO ALLOCATE NEEDED MEMORY TO GPU, -> USING CPU INSTEAD")
        Qxx = np.linalg.inv(np.array(sparseATPA.A, dtype=np.float32))

        print('End unknowns cofactors matrix in {:0.1f}s'.format( time.time()-timer1))
        
        ## COFACTEURS DES RESIDUS QVV
        print('Residuals cofactors matrix...')
        timer1 = time.time()
        # try:
        #     A_gpu = cupy.array(A)
        #     Qvv = sparseQll - (A_gpu @ Qxx_gpu @ A_gpu.T).get()
        #     # libération de la mémoire GPU
        #     del Qxx_gpu 
        #     del A_gpu
        # except:
        #     print("WARNING 2900: UNABLE TO ALLOCATE NEEDED MEMORY TO GPU, -> USING CPU INSTEAD")
        Qvv = sparseQll - sparseA @ Qxx @ sparseAT
        # cupy._default_memory_pool.free_all_blocks() 
        print('End residuals cofactors matrix in {:0.1f}s'.format( time.time()-timer1))
        
        # résidus normés wi
        for idObs, vi in enumerate(v[:,0]):
            qvvi = Qvv[idObs,idObs]
            if qvvi > 0.0:
                w[idObs] = vi / (sigma0 * np.sqrt(qvvi))
            else:
                w[idObs] = 0.0
 
    # ...Suite des idicateurs pour L2 ET robuste
    # s0 empirique
    s0 = np.sqrt((v.T@sparseP@v)/(nbObsAlti-nbIncAlti))[0,0]
    quotientGlobal = s0/sigma0

    # Variance-covariance inconnues Kxx
    Kxx = s0**2*Qxx
    
    
    updateProgressBar(progressBar, 5)

    #### MAJ OBSERVATIONS ET INDICATEURS (+inc.)
    
    # Quotients de groupes
    dictQuotients = {}
    
    # Valeur de nablaLi théoriquement infinie (->stabilité de calcul)
    nablaLiInfini = 20.0
    
    # Si libre-ajusté, groupe des obs. de rattachement
    if libreAjuste:
        dictQuotients.update({'controlPointsGroup':{'vk':[], 'pk':[], 'zk':[]}})
    
    #### ^----- LEVES POLAIRES
    if 'polar' in dictCanevas['network'].keys():
        
        # Récupérer les noms de tous les groupes de directionj pour levé polaire pour le calcul des quotients
        listeNomsGroupesDirection = []
        for groupeDir in dictParametres['parameters']['groups']['directionGroups']['directionGroup']:
            listeNomsGroupesDirection.append(groupeDir['directionGroupName'])
        listeNomsGroupesDirection = set(listeNomsGroupesDirection)
        
        # Initialisation des éléments pour le calcul des quotients par groupe (groupes de direction)
        for groupe in listeNomsGroupesDirection :
            dictQuotients.update({groupe:{'vk':[], 'pk':[], 'zk':[]}})
            
        # Indicateurs sur les obs.
        for station in dictCanevas['network']['polar']['station']:    
            stationnement = station['stationData']
            
            for observation in stationnement['measure']:
                DH = observation['DH']
                
                if 'idObsAlti' in DH.keys(): # si pas écarté
                    idObsDH = DH['idObsAlti']-1000000
                    vi = v[idObsDH,0]
                    zi = Qvv[idObsDH, idObsDH] / diagQll[idObsDH]
                    if zi > 0.0: # éviter les division par 0
                        nablaLi = 4.1 * np.sqrt(Kll[idObsDH]) / np.sqrt(zi)
                    else:
                        nablaLi = nablaLiInfini
                    nabla[idObsDH,0] = nablaLi
                    wi = w[idObsDH] /  W[idObsDH]
                    if zi == 0.0: # éviter les divisions par 0
                        gi = np.inf
                    else:
                        gi = -vi/zi
                    DH.update({'vi':round(vi,4)})
                    DH.update({'wi':round(wi,2)})
                    DH.update({'zi':round(zi,2)})
                    DH.update({'nablaLi':round(nablaLi,4)})
                    DH.update({'gi':round(gi,4)})
                    if robuste:
                        DH.update({'weightRobustFactor':round(W[idObsDH],2)})
                    
                    # pour quotients directions 
                    dictQuotients[stationnement['directionGroup']]['vk'].append(vi)
                    dictQuotients[stationnement['directionGroup']]['pk'].append(1/diagQll[idObsDH])
                    dictQuotients[stationnement['directionGroup']]['zk'].append(zi)
                    

    
    #### ^----- GNSS
    if 'gnss' in dictCanevas['network'].keys():

        # Récupérer les noms de tous les types groupes pour levé polaire pour le calcul des quotients
        listeNomsGroupesGNSS = []
        for groupeGNSS in dictParametres['parameters']['groups']['gnssGroups']['gnssGroup']:
            listeNomsGroupesGNSS.append(groupeGNSS['gnssGroupName'])
        
        # rendre les valeurs uniques en "set"
        listeNomsGroupesGNSS = set(listeNomsGroupesGNSS)
        for groupe in listeNomsGroupesGNSS :
            dictQuotients.update({groupe:{'vk':[], 'pk':[], 'zk':[]}})
              
        # indicateurs sur les param. inconnus  
        for session in dictCanevas['network']['gnss']['session']:
       
            paramInconnus = session['unknownParameters']

            # TRANSLATION H
            if "idIncTranslationH" in paramInconnus.keys():   
                idIncTranslationH = paramInconnus['idIncTranslationH']-1000000
                paramInconnus['valIncTranslationH'] = round(x0[idIncTranslationH,0],4)
                EMtranslationH = np.sqrt(Kxx[idIncTranslationH,idIncTranslationH])
                paramInconnus.update({'EMtranslationH':round(EMtranslationH,4)})
            
            # Indicateurs sur les obs.
            for observation in session['measure']:
                LH = observation['LH']
                
                if 'idObsAlti' in LH.keys(): # si pas écarté
                    idObsLH = LH['idObsAlti']-1000000
                    vi = v[idObsLH,0]
                    zi = Qvv[idObsLH, idObsLH] / diagQll[idObsLH]
                    if zi > 0.0:
                        nablaLi = 4.1 * np.sqrt(Kll[idObsLH]) / np.sqrt(zi)
                    else:
                        nablaLi = nablaLiInfini
                    nabla[idObsLH,0] = nablaLi
                    wi = w[idObsLH] / W[idObsLH]
                    if zi == 0.0: # éviter les divisions par 0
                        gi = np.inf
                    else:
                        gi = -vi/zi
                    LH.update({'vi':round(vi,4)})
                    LH.update({'wi':round(wi,2)})
                    LH.update({'zi':round(zi,2)})
                    LH.update({'nablaLi':round(nablaLi,4)})
                    LH.update({'gi':round(gi,4)})
                    if robuste:
                        LH.update({'weightRobustFactor':round(W[idObsLH],2)})
                    
                    # pour quotients
                    dictQuotients[session['gnssGroup']]['vk'].append(vi)
                    dictQuotients[session['gnssGroup']]['pk'].append(1/diagQll[idObsLH])
                    dictQuotients[session['gnssGroup']]['zk'].append(zi)
          
     
          
    #### ^----- PTS RATTACHEMENT
    if libreAjuste:
        
        for point in listeLA:

            # HH
            idObsHH = point['idObsHH']-1000000
            vi = v[idObsHH,0]
            zi = Qvv[idObsHH, idObsHH] / diagQll[idObsHH]
            if zi > 0.0:
                nablaLi = 4.1 * np.sqrt(Kll[idObsHH]) / np.sqrt(zi)
            else:
                nablaLi = nablaLiInfini
            nabla[idObsHH,0] = nablaLi
            wi = w[idObsHH] / W[idObsHH]
            if zi == 0.0: # éviter les divisions par 0
                gi = np.inf
            else:
                gi = -vi/zi
            indicateursHH = {}
            indicateursHH.update({'vi':round(vi,4)})
            indicateursHH.update({'wi':round(wi,2)})
            indicateursHH.update({'zi':round(zi,2)})
            indicateursHH.update({'nablaLi':round(nablaLi,4)})
            indicateursHH.update({'gi':round(gi,4)})
            if robuste:
                indicateursHH.update({'weightRobustFactor':round(W[idObsHH],2)})
            point.update({'indicateursHH':indicateursHH})
            
            # pour quotients
            dictQuotients['controlPointsGroup']['vk'].append(vi)
            dictQuotients['controlPointsGroup']['pk'].append(1/diagQll[idObsHH])
            dictQuotients['controlPointsGroup']['zk'].append(zi)        
      
            
      

      
      
    #### CALCUL DES QUOTIENTS
    
    for key,value in dictQuotients.items():
        # Uniquement si il y a bien des valeurs dans les groupes (utilisés)
        if len(value['vk']) > 0 and len(value['pk']) > 0 and len(value['zk']) > 0:
            
            vk,pk,zk = np.array([value['vk']]).T, np.diag(value['pk']), np.array([value['zk']]).T
            s0k = np.sqrt(vk.T @ pk @ vk / sum(zk))[0,0]
            quotient = s0k/sigma0
            value.update({'quotient':round(quotient,2)})
            # suppression des sous-vecteurs du groupe (lisibilité)
            value.pop('vk')
            value.pop('pk')
            value.pop('zk')
            
    
    updateProgressBar(progressBar, 5)
    
    #### MAJ POINTS ET INDICATEURS
    
    # Fiabilité etxerne NABLA et NABLAx
    print('External reliability calculations and matrixs...')
    timer1 = time.time()
    sparseNABLA = sparse.diags(nabla[:,0],dtype=np.float32)
    NABLAx = Qxx*sparseAT*sparseP*sparseNABLA
    print('End external reliability calculations and matrixs in {:0.1f}s'.format( time.time()-timer1))
            
    for point in dictPoints['points']['point']:

        # Uniquement MAJ des points nouveaux
        if 'idUnkH' in point.keys():
            
            idIncH = point['idUnkH']-1000000 # index de l'inconnue H
            point['H'] = round(x0[idIncH,0],4)
            
            # Intervalle de confiance (équivalent ellipse en 1D) à 1 sigma
            intervalleEMH = np.sqrt(Kxx[idIncH,idIncH])
            intervalleEMH ={'c':round(intervalleEMH,4)}
            point.update({'altiStdError':intervalleEMH})
            
            # Fiabilité externe 
            N = NABLAx[idIncH,:]
            NH = np.max(N)
            if NH > 10 :  # => fiabilité externe considérée infinie
                NH = np.nan
                idNH = np.nan
            else: # fiab. externe non-infinie 
                idNH = np.argmax(N) + 1000000
            
            vecteurFiabExterne = {'NH':round(NH,4),
                                  'idObsRespNH':idNH} 
            point.update({'externalReliabilityAlti'  :vecteurFiabExterne})
            
            
            # Calcul des diff. entre état initial et après compensation
            dH = x0[idIncH,0] - xInitial[idIncH,0]
            deltaAlti = {'dH':round(dH,4)}
            point.update({'deltaAlti':deltaAlti})        
    
        
    updateProgressBar(progressBar, 5)
    
    #### CLASSEMENT DES WI MAX
    # Récupérer l'obs. des 5 premiers wiMax
    listeWiMaxAlti = []
    wiMaxId = np.flip(np.argsort(np.fabs(w)))
    i = 1
    count = 0
    # Lister tous les wi max>3.5 + 20 suivantss
    nbWiMaxToClassify = (np.fabs(w) > 3.5).sum() + 20
    for idObs in wiMaxId:
        if np.isnan(w[idObs]) == False and i < nbWiMaxToClassify:
            obsWiMax, parent = rechercheUtils.rechercheIdObs(dictCanevas, idObs+1000000)
            if obsWiMax != None: # Filtrer si Libre-ajuste
                for key, data in obsWiMax.items():
                    if (key == 'DH' or key == 'LH') and data['discarded'] in ['false', None]:
                        # Selectionner le bon idObs dans la mesure 
                        if data['idObsAlti'] == idObs+1000000: 
                            data.update({'obsType':key})
                            listeWiMaxAlti.append({'parent':parent,
                                               'pointName':obsWiMax['pointName'],
                                               'observation':data})
                            i += 1
        # compter le nb sup à 3.5
        if np.isnan(w[idObs]) == False:
            if abs(w[idObs]) > 3.5 :
                count += 1
                
                
            
   
    
    # Restructuration du dictionnaire des quotients (en liste sans identifiant dans les balises -> XML correct)
    # Remettre les quotients dans les groupes des paramètres
    for key,value in dictQuotients.items():
        #### !!!! MODIFICATION POUR METTRE LES QUOTIENTS DANS LES GROUPES
        for key1 in dictParametres['parameters']['groups'].keys():
            for key2 in dictParametres['parameters']['groups'][key1].keys():
                for groupe in dictParametres['parameters']['groups'][key1][key2]:
                    for key3 in copy.deepcopy(groupe).keys(): # Balise du nom d'un groupe
                        if 'Name' in key3 :
                            if groupe[key3] == key:
                                groupe.update({'stdDevQuotientFor1D':value['quotient']})
    
    #### RESULTATS GLOBAUX
    dictResGlobaux['globalResults'].update({'altimetry':{}})
    dictResGlobaux['globalResults']['altimetry'].update({'CalculationTime':"{:0.1f} s".format(time.time()-timer)})
    dictResGlobaux['globalResults']['altimetry'].update({'iterationsCount':"{:d}".format(iteration)})
    dictResGlobaux['globalResults']['altimetry'].update({'iterationsLog':"\n{:s}".format(logIterations)})
    
    # Quotients d'écart-type d'unité de poids par groupe (et global)
    dictResGlobaux['globalResults']['altimetry'].update({'globalStdDevQuotient':round(quotientGlobal,2)})
    
    # Dénombrement
    denombrementAlti = {'unknowns':denombrement['nbIncAlti'], 
                         'observations':denombrement['nbObsAlti'],
                         'overdetermination':denombrement['surabondanceAlti']}
    dictResGlobaux['globalResults']['altimetry'].update({'counting':denombrementAlti})
    
    # 5 observations avec leur wiMax
    dictResGlobaux['globalResults']['altimetry'].update({'nbWiSup3.5':count})
    dictResGlobaux['globalResults']['altimetry'].update({'biggestWi':{'wiMax':listeWiMaxAlti}})

    
    # décision de suppression et de tout figurer uniquement dans les paramètres
    # if libreAjuste:
    #     dictResGlobaux['globalResults']['altimetry'].update({'stochasticNetwork':{}})
    #     dictResGlobaux['globalResults']['altimetry']['stochasticNetwork'].update({'point':listeLA})    
 
            

    # libérer la mémoire GPU
    # cupy._default_memory_pool.free_all_blocks() 
    
    return None








class Estimation:
    
    def __init__(self, dictCanevas, dictPoints, dictParametres, denombrement, dirPathResultats, progressBar):
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
        self.progressBar = progressBar
        
        
        # En-tête des dictionnaires des résultats globaux
        self.dictResGlobaux = {}
        self.dictResGlobaux = {'globalResults':{}}
        self.dictResGlobaux['globalResults'].update({'date':datetime.datetime.now().strftime("%d.%m.%y")})
        self.dictResGlobaux['globalResults'].update({'time':datetime.datetime.now().strftime("%H:%M:%S")})

        
        
        
        
    def compensation2D (self):
        """
        Fonction qui lance l'estimation 2D.
             
        Returns
        -------
        None.

        """
        print("\nCODE 2000 : PLANIMETRIC ADJUSTEMENT")
        print("-----------------------------------\n")
        
        
        updateProgressBar(self.progressBar, 5)
        return estimation2D(self.dictCanevas, self.dictPoints, self.dictParametres, self.denombrement, self.dictResGlobaux, self.progressBar)
    
    
    def compensation1D (self):
        """
        Fonction qui lance l'estimation 1D.
             
        Returns
        -------
        None.

        """
        print("\n\nCODE 3000 : ALTIMETRIC ADJUSTEMENT")
        print("------------------------------------\n")
        
       
        updateProgressBar(self.progressBar, 5)
        return  estimation1D(self.dictCanevas, self.dictPoints, self.dictParametres, self.denombrement, self.dictResGlobaux, self.progressBar)
    
    
    
    def exportsResultats(self):
        """
        Fonction qui lance l'export des dictionnaires après compensation.
             
        Returns
        -------
        None.

        """
        conversionUtils.dictionnaire2xml(self.dictPoints, self.dirPathResultats+"\\pointsRes.xml")
        # conversionUtils.dictionnaire2xml(self.dictCanevas, self.dirPathResultats+"\\networkPostAdjustment.xml")
        # conversionUtils.dictionnaire2xml(self.dictResGlobaux, self.dirPathResultats+"\\globalResults.xml" )
        # Fusion des 3
        conversionUtils.dictionnaire2xml({'results':{**self.dictParametres, **self.dictResGlobaux , **self.dictPoints, **self.dictCanevas}}, self.dirPathResultats+"\\results.xml" )
        
        updateProgressBar(self.progressBar, 5)
            
        return None
        
        
        
        