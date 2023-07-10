# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:13:26 2022

@author: Matteo Casto, INSIT
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import libUtils.conversionUtils as conversionUtils
import libUtils.controlesCoherenceUtils as controlesCoherenceUtils
import libUtils.rechercheUtils as rechercheUtils 
import libUtils.geometrieUtils as geometrieUtils

import os
import numpy as np
import matplotlib.pyplot as plt
import time
import copy


# ---   Réprétoir de base où se trouve les fichiers inpput et output (facillite la lecture)
dirPath = os.getcwd()



def gnssToPF(dictPoints, dictObs, viMax):
    """
    Function that process a median-based robust estimation with MN95/LV95 GNSS observations of coordinates
    in order to define reliable supplementary knowns points.

    Parameters
    ----------
    dictPoints : dictionnary
        Input points dictionary after a valid XSD checker.
    dictObs : dictionnary
        Input observations dictionary after a valid XSD checker.
    viMax : float
        Limit acceptable residuals [m].

    Returns
    -------
    None.

    """
    
    # Only if GNSS survey
    if 'gnss' in dictObs['network'].keys():
    
        
        # Dictionnaire rassemblant tous les points concernés par le levé GNSS
        dictPointsGnss = {}
        
    
        #### RECUPERATION DES OBS. GNSS PAR POINT
        
        # convert dicts in list si une seule session ou measure
        dictObs['network']['gnss']['session'] = dictObs['network']['gnss']['session'] if type(dictObs['network']['gnss']['session']) is list else [dictObs['network']['gnss']['session']]
        for session in dictObs['network']['gnss']['session']:
            
            # convert dicts in list si une seule session ou measure
            session['measure'] = session['measure'] if type(session['measure']) is list else [session['measure']]
            for measure in session['measure']:
                
                p = {'E':'', 'N':'', 'H':''}
                
                # [LYi, LXi]
                obs = [float(measure['LY']['value']), float(measure['LX']['value'])]
                
                # Uniquement pour avoir les points une seule fois
                if measure['pointName'] not in dictPointsGnss.keys():
                    dictPointsGnss.update({measure['pointName']:{'med':p}})
                    dictPointsGnss[measure['pointName']].update({'listeObs':[obs]})
                    
                else: # si point déjà existant
                    dictPointsGnss[measure['pointName']]['listeObs'].append(obs)
                
                
        #### CALCUL DES MEDIANES
        
        # Boucle qui va itérer jusqu'à que les obs. resp des grands vi soient écartée
        # et qu'il reste au min. 2 obs. GNSS pour rester dans le dictPointsGnss
        cont = True
        while cont:
            
            # par défaut, ne faire qu'une seule boucle
            cont = False
        
            for noPt, data in dictPointsGnss.items():
                
                listeObs = data['listeObs']
                # Récupérer uniquement les LY et LX (et trier) et calcul les médianes de chaque liste
                listObsLY, listObsLX  = list(list(zip(*listeObs))[0]),  list(list(zip(*listeObs))[1])
                medE, medN = np.median(listObsLY), np.median(listObsLX)
                
                # Calcul des vi sur la dist à la médiane (consituté de medE et medN)
                # print('\n----', noPt)
                for i in range(0, len(listeObs)):
                    
                    viDist = np.sqrt((medE - listObsLY[i])**2 + (medN - listObsLX[i])**2)
                    
                    if abs(viDist) > viMax and i < len(listeObs):
                        
                        # print(medE, medN ,viDist, i)
                        data['listeObs'].pop(i)
    
                        # Si on se trouve ici, on refait une itération while complète
                        cont = True
                    
                        
        #### MAJ DU DICT PTS AVEC LES NOUVEAUX PTS GNSS FIABLES
        
        # Après boucle while et convergence (plus de viDist > viMax)
        for  noPt, data in dictPointsGnss.items():
            listeObs = data['listeObs']
            # Si encore 2 obs. au moins, MAJ E, N et H
            if len(listeObs) >= 2:
                # Calcul final des médianes
                listObsLY, listObsLX  = list(list(zip(*listeObs))[0]),  list(list(zip(*listeObs))[1])
                medE, medN = np.median(listObsLY), np.median(listObsLX)
                
                # Stockage des médianes comme coordonnées de PF gnss finales dans le dictPoints
                point = rechercheUtils.rechercheNoPt(dictPoints, noPt)
                if point is  None: # Point encore non-existant -> l'ajouter comme pt connus (PF)
                    
                    p = {'pointName': noPt,
                         'E': round(medE,3),
                         'N': round(medN,3),
                         'H': '',
                         'comment':'approx. coord. come from robust GNSS estimation'}
                    
                    # Ajout final au dictPoint
                    dictPoints['points']['point'].append(p)
            
    
    return None



# @jit(target_backend='cuda')                         
# def func2(a):
#     for i in range(10000):
#         a[i]+= 1
        
        
        
        


def stationsToYX(dictObs, listeAllYX):
    """
    Fonction qui va calculer les stations polaires en systèmes locaux (avec  réductions/corrections de RI/DS).
    si aucun des deux n'est pas écarté.
    
    Parameters
    ----------
    dictObs : dictionnary
        Input observations dictionnaire after a valid XSD checker.
    listeAllYX : list
        List containing all local system of the network (incl. polar stations)

    Returns
    -------
    None.

    """
    
    # Only if polar survey
    if 'polar' in dictObs['network'].keys():
        
        # Parcourir toutes les stations
        for station in dictObs['network']['polar']['station']:
            
            listeAllYX.append({'nombrePtsCommuns':0,
                               'listePtsCommuns':[],
                               'name':'station as YX : '+station['stationName'],
                               'coordsYX':[[station['stationName'], 0.0,  0.0]] ,
                               'processed':False})
            
            # Parcourir les mes. de chaque station et réduire RI/DS en RIcorr et DPcorr
            for mes in station['stationData']['measure']:
                
                # Récupération des éléments de la visée
                noPt, RI, DS, ZD, dm1, dm2 = mes['pointName'], mes['RI']['value'], mes['DS']['value'], mes['ZD']['value'], mes['dm1']['value'], mes['dm2']['value'] 
                
                # continuer seulement si RI et DS pas écartés
                if mes['RI']['discarded'] != 'true' and mes['DS']['discarded'] != 'true' :
                    
                    # Réduction plan proj. (sans déplacements)
                    DP = geometrieUtils.reductionDistancePlanProj(float(DS), float(ZD), 1200000.0, 600.0) # valeur Hab et NSta générique (ordre de grandeur = 1m -> ok)
                    # si pas de dm saisi, = 0 (au lieu de None)
                    dm1 = float(dm1) if dm1 is not None else 0.0
                    dm2 = float(dm2) if dm2 is not None else 0.0
                    
                    # Correction des déplacements pour RI et DP
                    RIcorr, DPcorr = geometrieUtils.corrAvecDepl(float(RI)+150.0, DP, dm1, dm2)
                    
                    # 0.0 à la station et w=0.0 -> sys-local
                    y, x = DPcorr * np.sin(RIcorr*np.pi/200.0),  DPcorr * np.cos(RIcorr*np.pi/200.0)
                    
                    # Ajout à la liste du sysloc YXcourant (le dernier)
                    listeAllYX[-1]['coordsYX'].append([noPt,y,x])
                    
    return None


def localSystemsToYX(dictObs, listeAllYX):
    """
    Fonction qui va calculer les systèmes locaux sous la structure de listeAllYX.
    
    Parameters
    ----------
    dictObs : dictionnary
        Input observations dictionnaire after a valid XSD checker.
    listeAllYX : list
        List containing all local system of the network 

    Returns
    -------
    None.

    """
    
    # Only if there is a local system in observations
    if 'localSystems' in dictObs['network'].keys():
        
        # Parcourir les systèmes
        for system in dictObs['network']['localSystems']['localSystem']:
            
            listeAllYX.append({'nombrePtsCommuns':0,
                               'listePtsCommuns':[],
                               'name':'local sys. as YX : '+system['localSystemName'],
                               'coordsYX':[],
                               'processed':False})
            # Parcourir les mesures
            for mes in system['measure']:
                
                # Récupération des éléments de la visée
                noPt, LY, LX = mes['pointName'], float(mes['LY']['value']), float(mes['LX']['value'])
                
                # continuer seulement si LY et LX pas écartés
                if mes['LY']['discarded'] != 'true' and mes['LX']['discarded'] != 'true' :
                    
                    # Ajout à la liste du sysloc YXcourant (le dernier)
                    listeAllYX[-1]['coordsYX'].append([noPt,LY,LX])
                    
                    
    return None        
                    
                    
def gnssSessionsToYX(dictObs, listeAllYX):
    """
    Fonction qui va calculer les sessions GNSS sous la structure de listeAllYX.
    
    Parameters
    ----------
    dictObs : dictionnary
        Input observations dictionnary after a valid XSD checker.
    listeAllYX : list
        List containing all local system of the network (incl. GNSS sessions)
        
    Returns
    -------
    None.

    """
    
    # Only if there is a gnss survey in observations
    if 'gnss' in dictObs['network'].keys():
        
        # Parcourir les systèmes
        for session in dictObs['network']['gnss']['session']:
            
            listeAllYX.append({'nombrePtsCommuns':0,
                               'listePtsCommuns':[],
                               'name':'GNSS session as YX : '+session['sessionName'],
                               'coordsYX':[],
                               'processed':False})
            # Parcourir les mesures
            for mes in session['measure']:
                
                # Récupération des éléments de la visée
                noPt, LY, LX = mes['pointName'], float(mes['LY']['value']), float(mes['LX']['value'])
                
                # continuer seulement si LY et LX pas écartés
                if mes['LY']['discarded'] != 'true' and mes['LX']['discarded'] != 'true' :
                    
                    # Ajout à la liste du sysloc YXcourant (le dernier)
                    listeAllYX[-1]['coordsYX'].append([noPt,LY,LX])
                
    
    return None


def contraintToCalculate(dictObs, dictPoints):
    """
    Function that process to the calculation of points that are ONLY defined by a pair of contraints.
    At the moment, it can be either an intersection (2 alignments) or a perpendicular projection 
    of a point on a line (1 perpenciular and 1 alignment).

    Parameters
    ----------
    dictPoints : dictionnary
        Input points dictionary after a valid XSD checker.
    dictObs : dictionnary
        Input observations dictionary after a valid XSD checker.

    Returns
    -------
    None.

    """
    
    # only if there is some constraints
    if 'constraints' in dictObs['network'].keys():
        
            # Lister les nom de points déjà connus
            listePointName = knownPointsToListOfName(dictPoints)
            
            # Init du dict des contraintes par points restants à calculer
            dictContrPtPToCalculate = {}
            
            # Parcourir les contraintes et récupération des éléments par point P nouveaux (non-connus encore)
            for constraint in dictObs['network']['constraints']['constraint']:
                
                # Uniquement si pas écartée
                if constraint['discarded'] != 'true':
                    
                    typeContr = constraint['constraintType'] 
                    dm1 = constraint['dm1']['value']
                    
                    # Récupérer no A et B
                    for point in constraint['point']:
                        
                        if point['pointTypeInConstraint'] == 'A':
                            pointA = point['pointName']
                        if point['pointTypeInConstraint'] == 'B':
                            pointB = point['pointName']
                            
                    # Point P
                    for point in constraint['point']:  
                      
                      if point['pointTypeInConstraint'] == 'P':
                          
                          # Le point P n'esite pas et A et B doivent exister
                          if point['pointName'] not in listePointName and pointA in listePointName and pointB in listePointName:
                              
                             # Si pas encore dans le dict
                             if point['pointName'] not in dictContrPtPToCalculate.keys():
                                 dictContrPtPToCalculate.update({point['pointName']:{'listeContr':[{'A':pointA,
                                                                                                    'B':pointB,
                                                                                                    'type':typeContr,
                                                                                                    'dm1':dm1} ]}})
                             # Si déjà dans le dict, ajouter à la liste des contraintes de ce point
                             else:
                                 dictContrPtPToCalculate[point['pointName']]['listeContr'].append({'A':pointA,
                                                                                                 'B':pointB,
                                                                                                 'type':typeContr,
                                                                                                 'dm1':dm1})
                                 
                                 # Retourne la 1ere contrainte avec un pt P non-calculé et A et B connus
                                 # print(point['pointName'])
                                 return dictContrPtPToCalculate 
                             
                          else:
                             pass # Si P est pas trouvé, pass
                             
                        
                            




def constraintsToKnowPoints(dictContrPtPToCalculate, dictPoints):
    """
    Function that calculate the points calculated with at lest 2 geometric constraints.
    Currently it works with 2 alignement (intersection of 2 lines) or
    1 aligment and 1 perpendicular (projected point on line).

    Parameters
    ----------
    dictContrPtPToCalculate : dictionary output of the function contraintToCalculate
        Dictionnary of constraints related to the geometric definition of a point by a pair of constraints.
    dictPoints : dictionnary
        Input points dictionary after a valid XSD checker.
    
    Returns
    -------
    None.

    """
    
    # !!! ENVISAGER D'IMPLEMENTER D'AUTRES CAS   
                      
                                     
    #### Attribution des modes de calcul selon la configuration               

    # Parcourir chaque point concercné par une ou des contraintes (1 seule contrainte)
    for pointP, data in dictContrPtPToCalculate.items():
        
        
        if len(data['listeContr']) >= 2:
            
            nbAlign, nbPerp = 0, 0
            
            for contr in data['listeContr']:
                if contr['type'] == 'alignment':
                    nbAlign += 1
                if contr['type'] == 'perpendicular':
                    nbPerp += 1
            
            data.update({'nbAlign':nbAlign,
                         'nbPerp':nbPerp})
            
            
            
            #### ^---- Au moins 2 alignements
            if nbAlign >= 2:
                
                # Prendre les 2 premiers venues (rare qu'il y en ait plus que 2)
                found1 = False # Init
                for contr in data['listeContr']:
                    
                    # Première contrainte d'alignement (found1 == False)
                    if contr['type'] == 'alignment' and not found1 :
                        pA, pB = rechercheUtils.rechercheNoPt(dictPoints, contr['A']), rechercheUtils.rechercheNoPt(dictPoints, contr['B'])
                        Ea, Na, Eb, Nb = float(pA['E']), float(pA['N']), float(pB['E']), float(pB['N'])
                        
                        # Calcul dees coord. si OFFSET dm1
                        if contr['dm1'] != None:
                            
                            dm1 = float(contr['dm1'].replace(' ',''))
                            gisAB = geometrieUtils.gisement(Ea, Na, Eb, Nb)
                            
                            # Angle droit (gisement du décalage)
                            if dm1 > 0:
                                gisDm = gisAB + 100.0
                            elif dm1 < 0:
                                gisDm = gisAB - 100.0
                            # entre 0 et 400g
                            gisDm = np.mod(gisDm, 400.0)
                            
                            # print('line1 : ',pA['pointName'], pB['pointName'], gisDm, dm1)
                            
                            # Point A décalé (redéfinition par pt lancé)
                            Ea, Na = Ea + np.sin(gisDm*np.pi/200.0) * abs(dm1), Na + np.cos(gisDm*np.pi/200.0) * abs(dm1)
                            
                            # Point A décalé (redéfinition par pt lancé)
                            Eb, Nb = Eb + np.sin(gisDm*np.pi/200.0) * abs(dm1), Nb + np.cos(gisDm*np.pi/200.0) * abs(dm1)
                        
                        # génération de la ligne 1
                        L1 = geometrieUtils.line([Ea,Na], [Eb,Nb])
                        found1 = True 
                    
                    # Si la première contrainte alignmenet a déjà été trouvée, on récup.
                    # la 2e et on calcule l'intersection de 2 droites
                    elif found1: 
                        pA, pB = rechercheUtils.rechercheNoPt(dictPoints, contr['A']), rechercheUtils.rechercheNoPt(dictPoints, contr['B'])
                        Ea, Na, Eb, Nb = float(pA['E']), float(pA['N']), float(pB['E']), float(pB['N'])
                        
                        # Calcul dees coord. si OFFSET dm1
                        if contr['dm1'] != None:
                            
                            dm1 = float(contr['dm1'].replace(' ',''))
                            gisAB = geometrieUtils.gisement(Ea, Na, Eb, Nb)
                            
                            # Angle droit (gisement du décalage)
                            if dm1 > 0:
                                gisDm = gisAB + 100.0
                            elif dm1 < 0:
                                gisDm = gisAB - 100.0
                            # entre 0 et 400g
                            gisDm = np.mod(gisDm, 400.0)
                            
                            # print('line2 : ',pA['pointName'], pB['pointName'], gisDm , dm1)
                            
                            # Point A décalé (redéfinition par pt lancé)
                            Ea, Na = Ea + np.sin(gisDm*np.pi/200.0) * abs(dm1), Na + np.cos(gisDm*np.pi/200.0) * abs(dm1)
                            
                            # Point A décalé (redéfinition par pt lancé)
                            Eb, Nb = Eb + np.sin(gisDm*np.pi/200.0) * abs(dm1), Nb + np.cos(gisDm*np.pi/200.0) * abs(dm1)
                            
                            
                        # génération de la ligne 2
                        L2 = geometrieUtils.line([Ea,Na], [Eb,Nb])
                        
                        try: # erreur si 2 droites parallèles (sol. impossible)
                            Ep, Np = geometrieUtils.lineIntersection(L1,L2)
                            
                            # Ajout au dictPoints
                            dictPoints['points']['point'].append({'pointName':pointP,
                                                                 'E':round(Ep,3),
                                                                 'N':round(Np,3),
                                                                 'H':'',
                                                                 'comment': 'approx. coord. come from a 2-line intersection (constraints)'})
                        except:
                            print('Intersection at point P {:s} not found'.format(pointP))
                      
                            
            #### ^---- Au moins 1 alignement et 1 perpendiculaire (projection perpendiculaire)  
            if nbAlign >= 1 and nbPerp >=1:
                
                # Prendre les 2 premiers venues (1 al. ET 1 perp.)

                foundAlign, foundPerp  = False, False
                for contr in data['listeContr']:
                    
                    # Première contrainte d'alignement (found1 == False)
                    if ( contr['type'] == 'alignment' and not foundAlign ):
                        pA, pB = rechercheUtils.rechercheNoPt(dictPoints, contr['A']), rechercheUtils.rechercheNoPt(dictPoints, contr['B'])
                        foundAlign = True 
                        
                    if ( contr['type'] == 'perpendicular' and not foundPerp ):
                        
                        if contr['A'] not in [pA['pointName'], pB['pointName']]:
                            pC = rechercheUtils.rechercheNoPt(dictPoints, contr['A']) # Le point A de la perp. devient le point C à projeter sur la droite AB 
                            foundPerp = True
                        elif contr['B'] not in [pA['pointName'], pB['pointName']] :
                            pC = rechercheUtils.rechercheNoPt(dictPoints, contr['B']) # Le point B de la perp. devient le point C à projeter sur la droite AB 
                            foundPerp = True
                            
                        
                        
                    if foundAlign and foundPerp:
                        
                        # !!! Faire décalage aussi ici
                        
                        coordA = [float(pA['E']), float(pA['N'])]
                        coordB = [float(pB['E']), float(pB['N'])]
                        coordC = [float(pC['E']), float(pC['N'])]
                        coordP = geometrieUtils.projectPointOnLine(coordA, coordB, coordC)
                        # Ajout au dictPoints
                        dictPoints['points']['point'].append({'pointName':pointP,
                                                              'E':round(coordP[0],3),
                                                              'N':round(coordP[1],3),
                                                              'H':'',
                                                              'comment': 'approx. coord. come from a point projected (perp.) on a line (constraints)'})
                    
                         
   
    return None
    
    
    
    
    
    
    






def knownPointsToListOfName(dictPoints):
    """
    Rapide et simple fonction permettant d'extraire une liste des n° de points connus.

    Parameters
    ----------
    dictPoints : dictionnary
        Input points dictionnaire.

    Returns
    -------
    listePointName : list
        Liste de tous les points connus.

    """
    listePointName = []
    for point in dictPoints['points']['point']:
        if point['E'] is not None and point['N'] is not None : 
            listePointName.append(point['pointName'])
    return listePointName
    




def countingCommonPointsFromLocalSystemsWithKnownPoints(dictPoints, listeAllYX):
    """
    Fonction permettant de lister et compter les points communs entre les systèmes locaux YX avec les points déjà connus.

    Parameters
    ----------
    dictPoints : dictionnary
        Input points dictionnaire.
    listeAllYX : list
        List containing all local systems not already calculated of the network. (incl. polar stations)

    Returns
    -------
    None.

    """
    
    
    # Lister les nom de points déjà connus
    listePointName = knownPointsToListOfName(dictPoints)
    
    for sysloc in listeAllYX:
    
        # liste des numéros de points du système (position 0 des listes dans la liste 'coordsYX') 
        # en commun avec le reste des points déjà connus (listePointName).
        # Ajouter également la liste des points communs (facilite le helmert)
        listeNoPtOfSysLoc = list(list(zip(*sysloc['coordsYX']))[0])
        listeCommuns = list(set(listePointName).intersection(listeNoPtOfSysLoc))
        sysloc['nombrePtsCommuns'] = len(listeCommuns)
        sysloc['listePtsCommuns'] = listeCommuns
        sysloc['newPoints'] = len(listeNoPtOfSysLoc) - len(listeCommuns) # Nb de nouveaux pts
        # print(sysloc['newPoints'])
        
    return None





def sysLocWithHighestCommonPointsNumber(listeAllYX):
    """
    Fonction qui va retourner le système local avec le plus de points communs
    avec les points déjà connus et qui n'est pas déjà calculé (attribut "processed" == False)
    Permet ensuite de procéder à un helmert avec CE système.

    Parameters
    ----------
    listeAllYX : list
        List containing all local systems not already calculated of the network.

    Returns
    -------
    bestSysLoc : dictionnary
        Dict. of the local systems with the most commons points with the known points.

    """
    
    # Init avec 0
    highestNumber = 0
    indiceBestSysLoc = 0
    bestSysLoc = None
    for i, sysloc in enumerate(listeAllYX):
        
        # Test si plus grand que le précédent, remplacer et ainsi de suite (ne pas calculer les systèmes sans pts nouveaux)
        if sysloc['nombrePtsCommuns'] > highestNumber and not sysloc['processed'] and sysloc['newPoints'] >0:
            highestNumber = sysloc['nombrePtsCommuns']
            bestSysLoc = sysloc
            indiceBestSysLoc = i # Attribution de l'indice (pour supprimer ensuite ce sysloc de AllListYX
        
    return bestSysLoc, indiceBestSysLoc
            


def sysLocToKnownPoints(dictPoints, syslocToCalculate, listeAllYX, viLimite):
    """
    Fonction qui va transformer de manière robuste (médiane, rupture à 49.9%) le
    système local avec le plus de pt commun dans le reste des points connus.
    Va ajouter les points nouveaux au dict. des pts connus

    Parameters
    ----------
    dictPoints : dictionnary
        Input points dictionnaire.
    syslocToCalculate : dictionnary
        Dict. of the local systems with the most commons points with the known points.
    listeAllYX : list
        List containing all localSystems of the network.
    viMax : float
        Limit acceptable residuals [m].

    Returns
    -------
    None.

    """
    
    # Liste des points à ne pas transformer (résidus trop grands)
    listePtsNotOk = []
    

    # Init de la boucle
    cont = True
    
    while cont :
        
        cont = False
        
        # Lister les points communs et leurs coord. YX et EN
        pointsCommuns = {}
        listeEglobal, listeNglobal  = [], []
        listeYLocal, listeXLocal = [], []
        for noPtCommun in syslocToCalculate['listePtsCommuns']:
            
            # Rechercher ce point dans les no des points déjà connus
            pointGlobal = rechercheUtils.rechercheNoPt(dictPoints, noPtCommun)
            Eglobal, Nglobal =  float(pointGlobal['E']),  float(pointGlobal['N'])
            listeEglobal.append(Eglobal)
            listeNglobal.append(Nglobal)
            # Rechercher le point local dans le système YX
            for coord in syslocToCalculate['coordsYX']:
                if noPtCommun == coord[0]:
                    Ylocal, Xlocal =  coord[1], coord[2]
                    listeYLocal.append(Ylocal)
                    listeXLocal.append(Xlocal)
    
            pointsCommuns.update({noPtCommun:[Eglobal,Nglobal,Ylocal,Xlocal,0,0]}) # index 4 et 5 seront pour les résidus
        
        # Init  liste des résidus 
        liste_viDist = []
    
        # Calcul des centroides
        centroidEglobal, centroidNglobal = np.mean(listeEglobal), np.mean(listeNglobal)
        controidYlocal,  controidXlocal  = np.mean(listeYLocal), np.mean(listeXLocal)
        
        # Réduction des mesures aux centres de gravité (réatrobution des valeurs
        # et calcul des éléments des éléments de transformations
        listeAlpha, listeLamda = [], []
        for noPt, data in pointsCommuns.items():
            
            # Coords globales réduction au centre de gravité
            E_red, N_red = data[0] - centroidEglobal, data[1] - centroidNglobal 
            # Coords locales réduction au centre de gravité
            y_red, x_red = data[2] - controidYlocal, data[3] - controidXlocal 
            
            
            # Calcul des médianes de fact. échelle et de rotations
            gis_i_global  = geometrieUtils.gisement(0.0, 0.0, E_red, N_red)
            gis_i_local   = geometrieUtils.gisement(0.0, 0.0, y_red, x_red) 
            
            alpha_i = np.mod(gis_i_global - gis_i_local,400) # alpha (rotation) en grades et sens horaire
            if alpha_i >= 300 and alpha_i <= 400: # Attention au cadrans pour la moy. 
                alpha_i -= 400
                
            # !!! FIXE A 1
            lamda_i = 1.0 # facteur d'échelle fixé à 1
            
            listeAlpha.append(alpha_i)
            listeLamda.append(lamda_i)

            
        # -> Médianes (valeurs robuste pour écartement des valeurs fausses)
        # -> Moyennes (valeurs de transformation, plus précise)
        medAlpha, medLamda = np.median(listeAlpha), np.median(listeLamda)
        moyAlpha, moyLamda = np.mean(listeAlpha), np.mean(listeLamda)
        # print(listeAlpha)
        # print('moy. : ',np.mean(listeAlpha), np.mean(listeLamda))
        # print('med. :', medAlpha, medLamda)
        
        for noPt, data in pointsCommuns.items():
            
            # Coords locales réduction au centre de gravité
            y_red, x_red = data[2] - controidYlocal, data[3] - controidXlocal 
            R = np.array([[np.cos(medAlpha*np.pi/200.0)   , np.sin(medAlpha*np.pi/200.0)],
                          [-np.sin(medAlpha*np.pi/200.0)  ,  np.cos(medAlpha*np.pi/200.0)]])
            t = np.array([[centroidEglobal],
                          [centroidNglobal]])
            
            ptNouv = t + medLamda * R @ np.array([[y_red], 
                                       [x_red]]) 
            Enouv, Nnouv = ptNouv[0,0], ptNouv[1,0]
            
            # Calcul du résidus viDist sur la distance entre avant et après
            # Supprimer uniquement si 
            viDist = ((Enouv-data[0])**2 + (Nnouv-data[1])**2)**0.5
            liste_viDist.append([viDist,noPt])
            
            
        viDistMax = max(list(list(zip(*liste_viDist))[0]))
        
        # Supprimer le pt avec le plus grand vi de la liste des points communs
        for vi, noPt in liste_viDist:
            
            if round(vi,3) == round(viDistMax,3) and viDist > viLimite:
                syslocToCalculate['listePtsCommuns'].remove(noPt)
                listePtsNotOk.append(noPt)
                # print(liste_viDist)
                cont = True # refaire une boucle complète

                
        
        
    
    # Calcul des coordonnées des pts nouveaux et ajout aux PF
    for noPt, y, x in syslocToCalculate['coordsYX']:
        
        # Uniquement calcul pour les points nouveaux (non-communs) ou points communs à recalculer (faux)
        if noPt not in syslocToCalculate['listePtsCommuns'] and noPt not in listePtsNotOk:
           
            # Coords locales réduction au centre de gravité
            y_red, x_red = y - controidYlocal, x - controidXlocal 
            R = np.array([[np.cos(moyAlpha*np.pi/200.0)   , np.sin(moyAlpha*np.pi/200.0)],
                          [-np.sin(moyAlpha*np.pi/200.0)  ,  np.cos(moyAlpha*np.pi/200.0)]])
            t = np.array([[centroidEglobal],
                          [centroidNglobal]])
            
            ptNouv = t + moyLamda * R @ np.array([[y_red], 
                                       [x_red]]) 
            Enouv, Nnouv = ptNouv[0,0], ptNouv[1,0]
            
            # Si problème au calcul (coords = np.nan) ne pas ajouter le point
            if not np.isnan(Enouv) or not np.isnan(Nnouv):
            
                # Création ajout du pt aux pts connus
                p = {'pointName': noPt,
                     'E': round(Enouv,3),
                     'N': round(Nnouv,3),
                     'H': '',
                     'comment':'approx. coord. come from a robust helmert transformation'}
                
                # Ajout final au dictPoint
                dictPoints['points']['point'].append(p)
            
            
    
    # Set à True que le sysloc a été calculé
    for sysloc in listeAllYX:
        if sysloc == syslocToCalculate:
            sysloc['processed'] = True
            # écart type
            sigmaVi = round(np.mean(list(list(zip(*liste_viDist))[0]))*1000,1) # en mm
            sysloc.update({'sigmaVi':sigmaVi})
            sysloc.update({'outTolerance':str(listePtsNotOk)})
    
            
    return None






def generateLog(dictObs, dictPoints):
    """
    Function that generates a log as a String to export. It contains a summary of all the not calculated points
    and where we can find them in the observations.
    The log is also display in the console at the end of the function.

    Parameters
    ----------
    dictPoints : dictionnary
        Input points dictionary after a valid XSD checker.
    dictObs : dictionnary
        Input observations dictionary after a valid XSD checker.

    Returns
    -------
    log : String
        Log ready to be exported in a file.

    """
    
    
    listePtsConnus = knownPointsToListOfName(dictPoints)
    listePtsManquants = []
    log = '\nAPPROXIMATE COORDINATES OF POINTS NOT CALCULATED\n'
    log+= '================================================\n\n'
                      
    # !!! todo
    
    
    # Parcourir les levés polaires
    if 'polar' in dictObs['network'].keys():
        
        log += 'POLAR SURVEY\n'
        log += '------------\n'
    
        for station in dictObs['network']['polar']['station']:
            
            # Si la station n'est pas connue
            if station['stationName'] not in listePtsConnus :
            
                log += 'station: {:s}\n'.format(station['stationName'])
                listePtsManquants.append(station['stationName'])
            
            # Parcourir les mesures
            for mes in station['stationData']['measure']:
                
                noPt = mes['pointName']
                # Si la target n'est pas connue
                if noPt not in listePtsConnus :
                    
                    log += 'point: {:s}\tfrom station: {:s}\n'.format(noPt, station['stationName'])        
                    listePtsManquants.append(noPt)
    
    # Parcourir les levés GNSS
    if 'gnss' in dictObs['network'].keys():
        
        log += '\nGNSS\n'
        log += '----\n'
        
        for session in dictObs['network']['gnss']['session']:
            
            for mes in session['measure']:
                
                noPt = mes['pointName']
                # Si le pt n'est pas connu
                if noPt not in listePtsConnus :
                    
                    log += 'point: {:s}\tfrom session: {:s}\n'.format(noPt, session['sessionName'])   
                    listePtsManquants.append(noPt)
                        
    # Parcourir les levés GNSS
    if 'localSystems' in dictObs['network'].keys():
        
        log += '\nLOCAL SYSTEMS\n'
        log += '-------------\n'
        
        for sysloc in dictObs['network']['localSystems']['localSystem']:
            
            for mes in sysloc['measure']:
                
                noPt = mes['pointName']
                # Si le pt n'est pas connu
                if noPt not in listePtsConnus :
                    
                    log += 'point: {:s}\tfrom local system: {:s}\n'.format(noPt, sysloc['localSystemName'])   
                    listePtsManquants.append(noPt)
                           
    # Parcourir les mesures simples
    if 'simpleMeasures' in dictObs['network'].keys():          
        
        log += '\nSIMPLE MEASURES\n'
        log += '---------------\n'
        
        for mes in dictObs['network']['simpleMeasures']['simpleMeasure']:
            
            noPt1, noPt2 = mes['measure']['pointName1'], mes['measure']['pointName2']
            # Si le pt1 n'est pas connu
            if noPt1 not in listePtsConnus :
                log += 'point: {:s}\tlinked with point: {:s}\n'.format(noPt1, noPt2)   
                listePtsManquants.append(noPt1)
            # Si le pt2 n'est pas connu
            if noPt2 not in listePtsConnus:
                log += 'point: {:s}\tlinked with point: {:s}\n'.format(noPt2, noPt1)   
                listePtsManquants.append(noPt2)
                
        
    # Parcourir les mesures simples
    if 'constraints' in dictObs['network'].keys(): 
        
        log += '\nCONSTRAINTS\n'
        log += '-----------\n'
        
        for contr in dictObs['network']['constraints']['constraint']:
            
            # Parcourir les pts de la contrainte
            for point in contr['point']:
                
                # Récup des No de pts
                if point['pointTypeInConstraint'] == 'A':
                    noA = point['pointName']
                if point['pointTypeInConstraint'] == 'B':
                    noB = point['pointName'] 
                if point['pointTypeInConstraint'] == 'P':
                    noP = point['pointName'] 
                
            # Si le ptA n'est pas connu
            if noA not in listePtsConnus:
                log += 'point: {:s}\tlinked with points: {:s}\t{:s}\n'.format(noA, noB, noP)   
                listePtsManquants.append(noA)
            # Si le ptB n'est pas connu
            if noB not in listePtsConnus:
                log += 'point: {:s}\tlinked with points: {:s}\t{:s}\n'.format(noB, noA, noP)   
                listePtsManquants.append(noB)
            # Si le ptP n'est pas connu
            if noP not in listePtsConnus:
                log += 'point: {:s}\tlinked with points: {:s}\t{:s}\n'.format(noP, noA, noB)   
                listePtsManquants.append(noP)
                        
                
    # Résumé des pts non-calculés
    log += '\n\n===========================\n'
    log += 'MISSING COORDINATES SUMMARY\n'
    log += '===========================\n'
    
    # Rendre les valeurs uniques en via un set de la liste
    for no in set(listePtsManquants):
        log += no + '\n'
        
    log += '---------------------------\n'
    log += 'SUM MISSING    = {:d}\n'.format(len(set(listePtsManquants)))
    log += 'SUM KNOWN      = {:d}\n'.format(len(set(listePtsConnus)))
    log += '% OF MISSING   = {:0.1f}%\n'.format(len(set(listePtsManquants))/len(set(listePtsConnus)) * 100)
        
    
    
    print(log)
    return log



    

    
class ApproxCoordinates:
    
    def __init__(self, nomsFichiers):
        """
        Constructor function with XML conversion and structure checks

        Parameters
        ----------
        nomsFichiers : dictionnary
            Dict that contains all the file names necessary for this calculation.

        Returns
        -------
        None.

        """
        
        # Init des noms de fichiers
        self.nomsFichiers = nomsFichiers
        
        # Controles de cohérences sémantiques
        self.check1 =controlesCoherenceUtils.checkXmlXsd(self.nomsFichiers['fichierXSDPoints'], self.nomsFichiers['fichierXMLPoints'])
        self.check2 =controlesCoherenceUtils.checkXmlXsd(self.nomsFichiers['fichierXSDCanevas'], self.nomsFichiers['fichierXMLCanevas'])
        
        # Conversion XMl to dict
        self.dictPoints = conversionUtils.xml2dictionnaire(self.nomsFichiers['fichierXMLPoints'])
        self.dictObs = conversionUtils.xml2dictionnaire(self.nomsFichiers['fichierXMLCanevas'])
        # Mettre sous forme de liste
        controlesCoherenceUtils.structureListeInDict(self.dictObs, 'network')
        
        # Check doublons
        self.check3 = controlesCoherenceUtils.checkDoublonsPoints(self.dictPoints)
        
        # Résidus limite
        self.viLimite =self.nomsFichiers['residusLimite']
        
        
        # Init d'une liste des étapes de calcul
        self.listeEtape = []

        
        
    
    def run(self):
        """
        Main function that runs the process of calculation of the approximate coordinates.

        Returns
        -------
        None.

        """
        
        # First update
        self.updateListeEtapes('known points')
        
        # GNSS to PF
        gnssToPF(self.dictPoints, self.dictObs, self.viLimite)
        
        # Update after GNSS
        self.updateListeEtapes('robust GNSS')
        
        # Pour l'historique des étapes
        
        
        # Initialisation des systèmes locaux YX (stations, systèmes, etc.)
        self.listeAllYX = []
    
        # Convertir les stations en sys. local YX (avec réduction, correction, etc.)
        stationsToYX(self.dictObs, self.listeAllYX)
        
        # Ajout des systèmes locaux à la liste de tous les systèmes YX
        localSystemsToYX(self.dictObs, self.listeAllYX)
        
        # Ajout des sessions GNSS comme systèmes YX
        gnssSessionsToYX(self.dictObs, self.listeAllYX)
        
        print('---- local YX systems in calculation : ...')
        
        nbBoucles = len(self.listeAllYX)

        # CALCULS DES SYSTEMES LOCAUX YX (stations, sessions, sys.loc.)
        for i in range(0,nbBoucles):
            
            # Liste des points déjà connus
            self.listePtsConnus = knownPointsToListOfName(self.dictPoints)

            # Compte les points communs pour chaque réseau local avec les points déjà connus (dictPoints)
            countingCommonPointsFromLocalSystemsWithKnownPoints(self.dictPoints, self.listeAllYX)
            
            try:
                # Déterminer quel système local a le plus de pts communs
                self.syslocToCalculate, indiceBestSysLoc = sysLocWithHighestCommonPointsNumber(self.listeAllYX)
                
                # Si aucun systeme n'est encore à calculer, break la boucle
                if self.syslocToCalculate is None:
                    break
                # Logs divers de suivi
                nbToCalculate = len(self.syslocToCalculate['coordsYX']) - self.syslocToCalculate['nombrePtsCommuns']
                
                # Calculer helmert de ce système local avec les points communs aux points déjà connus (dictPoints)
                sysLocToKnownPoints(self.dictPoints, self.syslocToCalculate, self.listeAllYX, self.viLimite)
                
                # update la l'historique
                info = '{:s} \nσ : {:0.1f} mm \ncommon points : {:d} \nnew points : {:d} \nout of tolerance : {:s}'.format(
                    self.syslocToCalculate['name'],
                    self.syslocToCalculate['sigmaVi'],
                    self.syslocToCalculate['nombrePtsCommuns'],
                    nbToCalculate,
                    self.syslocToCalculate['outTolerance']
                        )
                # Pts communs séparés par un ;
                ptsCommuns = self.syslocToCalculate['listePtsCommuns']
                self.updateListeEtapes(info,ptsCommuns)
                
                # Logger en live dans la console 
                print('- sysloc', self.syslocToCalculate['name'])
                # print(info)
                
                # Suprrimer le sysloc de AllListAY (opti. pour éviter de parcourir à chaque fois la liste complète pour trouver le best)
                del self.listeAllYX[indiceBestSysLoc]
            
            except:
                print('- ERROR IN TRANSFORMATION OF LOCAL SYSTEM: {:s}'.format(self.syslocToCalculate['name']))
                
            
        
            
        
        # CALCUL DES CONTRAINTES par paires (alignement/alignement, alignement/perpendiculaire)
        if 'constraints' in self.dictObs['network'].keys():
            
            print('\n---- geometric constraints in calculation : ...')
            
            # Nb de boucles à réaliser (nb de contraintes divisé par 2 (couples de contraintes))
            nbBoucles = int(len(self.dictObs['network']['constraints']['constraint'])/2)
            for i in range(0,nbBoucles):
                

                # Récupération de la contrainte à calculer
                self.dictContrPtPToCalculate = contraintToCalculate(self.dictObs, self.dictPoints)
                
                # Si le programme a bien trouvé une contrainte à calculer
                if self.dictContrPtPToCalculate is not None:
                    
                    noP = list(self.dictContrPtPToCalculate.keys())[0]
                    
                    print('- constraint :', noP)
                
                    # Calcul de cette contrainte, puis itérations sur les autres contraintes dispo.
                    constraintsToKnowPoints(self.dictContrPtPToCalculate, self.dictPoints)
                    
                    #####
                    ##### A FAIRE : DELETE DES CONTRAINTES DEJA FAITES
                    #####
                    
                    # update lsite historique
                    self.updateListeEtapes('constraint\nnew point : {:s}'.format(noP))
                
                else: 
                    # print(i)
                    pass


    

    def exportPointsXML(self):
        """
        Function that export the calculated points after the algorithm according to the XSD structure.

        Returns
        -------
        None.

        """
        
        # Export des pts connus
        conversionUtils.dictionnaire2xml(self.dictPoints, self.nomsFichiers['dossierResultats'] + "\\knownPoints.xml")
        
        
    def updateListeEtapes(self, info, ptsCommuns=[]):
        """
        Function used to update the list containing all the steps of calculations (list of point's dictionnary).

        Parameters
        ----------
        info : String
            Text that will be displayed in the information of the current step in the user interface.
        ptsCommuns : list, optional
            List containing all point's name of the current step. It it useful to display the common points of a system or constraints with a
            specific symbology in user-interface.
            The default is [].

        Returns
        -------
        None.

        """
        
        # Faire une deep copy du dictPoints à un instant donné
        self.listeEtape.append([info,copy.deepcopy(self.dictPoints),ptsCommuns])   
        
    
    def getHistorique(self):
        """
        Function used to get the list containing all the steps of calculations (list of point's dictionnary).
        It is used from the user interface to get this list to be graphically displayed according to the steps.

        Returns
        -------
        listeEtape : list
            List of point's dictionnary for each step.

        """
        
        return self.listeEtape
    
    
    def exportPointsManquants(self):
        """
        Simple function that exports the log of not calculated points at the end of the algorithm.

        Returns
        -------
        None.

        """
        self.log = generateLog(self.dictObs, self.dictPoints)
        with open(self.nomsFichiers['dossierResultats'] + "\\missingPoints.log", 'w') as f:
            f.write(self.log)
            
            
            
            
        
    # !!! A FAIRE ICI -> Cas spéciaux (ex: directions sur un pt sans distances, intersection de distances, etc.)
        
        
        






















