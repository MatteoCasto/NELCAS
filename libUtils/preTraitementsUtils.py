# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 08:57:20 2022

@author: Matteo Casto, INSIT
"""

import numpy as np
import libUtils.geometrieUtils as geometrieUtils
import libUtils.rechercheUtils as rechercheUtils
import copy
import time




def rotationsApprochees(dictCanevas, dictPoints):
    """
    Fonction permettant de calculer les rotation approchées des systèmes locaux (avec les points communs sur les coordonnées approchées).

    Parameters
    ----------
    dictCanevas : dictionnaire
        Après lecture d'un fichier XML et validé 
    dictPoints : dictionnaire
        Après lecture d'un fichier XML et validé     

    Returns
    -------
    None.

    """    
    
    
    # Uniquement si il y'a un système local
    if 'localSystems' in dictCanevas['network'].keys():
        
        # Parcourir les sessions
        for systeme in dictCanevas['network']['localSystems']['localSystem']:
            
            # Si rotation horiz. la déterminer de manière approch.
            if 'idIncRotationHoriz' in systeme['unknownParameters'].keys():
                               
                #### CALCUL VIA DETERM: PLANI SIMPLE
                
                # Récupéraiton des pts communs
                listePtsCommuns = []
                for observation in systeme['measure']:
                    
                    # récupérer chaque point dans le dictPoints
                    pointGlobal = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                    if pointGlobal['planimetricElems'] > 2: # = point commun avec le reste du réseau
                        listePtsCommuns.append(pointGlobal['pointName'])
                
                    
                # Calcul des gisements locaux et globaux
                for observation in systeme['measure']:
                    
                    if observation['pointName'] == listePtsCommuns[0]: # premier point commun
                        yLocal1, xLocal1 = observation['LY']['value'], observation['LX']['value']
                        pointGlobal1 = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                        yGlobal1, xGlobal1 = pointGlobal1['E'], pointGlobal1['N']
                    if observation['pointName'] == listePtsCommuns[-1]: # dernier point commun (le 2e en général)
                        yLocal2, xLocal2 = observation['LY']['value'], observation['LX']['value']
                        pointGlobal2 = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                        yGlobal2, xGlobal2 = pointGlobal2['E'], pointGlobal2['N']
                
                # Calcul de la rotation approchée par différence de gis.
                gisLocal = geometrieUtils.gisement(float(yLocal1),float(xLocal1),float(yLocal2),float(xLocal2))
                gisGlobal = geometrieUtils.gisement(float(yGlobal1),float(xGlobal1),float(yGlobal2),float(xGlobal2))
                rotationApprochee = gisGlobal - gisLocal
                systeme['unknownParameters'].update({'valIncRotationHoriz':rotationApprochee})
                
                        
    return None



def centroidesSystemesSessions(dictCanevas, dictPoints):
    """
    Fonction permettant de définir les centres de gravités (système global) des sessions GNSS et des systèmes locaux.
    
    Parameters
    ----------
    dictCanevas : dictionnaire
        Après lecture d'un fichier XML et validé 
    dictPoints : dictionnaire
        Après lecture d'un fichier XML et validé     

    Returns
    -------
    None.

    """  
    
    #### GNSS
    
    # Vérifier qu'il y a bien un relevé de session GNSS 
    if 'gnss' in dictCanevas['network'].keys():
    
        # Liste de toutes les objets session
        listeSessions = dictCanevas['network']['gnss']['session']
        for session in listeSessions:
            
            # Parcourir le stationnement et get les No de pts visés dans les obs.
            listeObservations = session['measure']
            idLastObs = len(listeObservations)-1 # récupérer l'index du dernier élément de la liste
            listeEglobal, listeNglobal = [], []
            listeYlocal, listeXlocal = [], []
        
            for i, observation in enumerate(listeObservations):
                
                # faire le contrôle seulement si il y'a des observations 2D
                if "LY" in observation.keys() and "LX" in observation.keys() :

                    # Contrôle grossier des coordonnées à ~0.5cm 
                    point = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                    Ep, Np =  float(point['E']), float(point['N'])
                    LY, LX = float(observation['LY']['value']), float(observation['LX']['value'])
                    listeEglobal.append(Ep)
                    listeNglobal.append(Np) 
                    listeYlocal.append(LY)
                    listeXlocal.append(LX)
                    
                    # Coordonnées du centroide E/N, pour stabilisatation du calcul (réduction au centre de gravité)
                    if i == idLastObs: # calcul de la moyenne au dernier point
                        session.update({'centroids':{}})
                        session['centroids'].update( {'meanE':round(np.mean(listeEglobal),4)} )
                        session['centroids'].update( {'meanN':round(np.mean(listeNglobal),4)} )
                        session['centroids'].update( {'meanY':round(np.mean(listeYlocal),4)} )
                        session['centroids'].update( {'meanX':round(np.mean(listeXlocal),4)} )

                        
                        
                        
    #### SYSTEMES LOCAUX    
                
    # Vérifier qu'il y a bien un relevé par système local
    if 'localSystems' in dictCanevas['network'].keys():
    
        # Liste de toutes les objets systeme
        listeSystemes = dictCanevas['network']['localSystems']['localSystem']
        for systeme in listeSystemes:
            
            # Parcourir le stationnement et get les No de pts visés dans les obs.
            listeObservations = systeme['measure']
            idLastObs = len(listeObservations)-1 # récupérer l'index du dernier élément de la liste
            listeEglobal, listeNglobal = [], []
            listeYlocal, listeXlocal = [], []
        
            for i, observation in enumerate(listeObservations):
                
                # faire le contrôle seulement si il y'a des observations 2D
                if "LY" in observation.keys() and "LX" in observation.keys() :

                    # Contrôle grossier des coordonnées à ~0.5cm 
                    point = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                    Ep, Np =  float(point['E']), float(point['N'])
                    LY, LX = float(observation['LY']['value']), float(observation['LX']['value'])
                    listeEglobal.append(Ep)
                    listeNglobal.append(Np) 
                    listeYlocal.append(LY)
                    listeXlocal.append(LX)
                    
                    # Coordonnées du centroide E/N, pour stabilisatation du calcul (réduction au centre de gravité)
                    if i == idLastObs: # calcul de la moyenne au dernier point
                        systeme.update({'centroids':{}})
                        systeme['centroids'].update( {'meanE':round(np.mean(listeEglobal),4)} )
                        systeme['centroids'].update( {'meanN':round(np.mean(listeNglobal),4)} )
                        systeme['centroids'].update( {'meanY':round(np.mean(listeYlocal),4)} )
                        systeme['centroids'].update( {'meanX':round(np.mean(listeXlocal),4)} )

    
    
            
    
    






def preTraitements(dictCanevas, dictPoints, dictParametres):
    
    """
    Fonction permettant de réduire les distances dans le plan de projection (DS->DP) et les corriger des déplacements dm1 et dm2. 
    Permet également de corriger les directions RI avec les déplacements.
    Les éléments DS et RI anciens sont remplacés par DP et RI après correction/réduction.
    Remplace également ZD par DH (obtenu avec ZD et DS).
    Appose les identifiant d'inconnues et d'observation (index des matrices).
    Calcule les écart-type rigoureux de chaque observation non-écartée (en unité de l'obs.).
    Les inconnues et observation issus d'un calcul libre-ajusté ne sont pas pris en compte dans le dict. dénombrement. (sera effectué dans Estimation)
    
    Parameters
    ----------
    dictCanevas : dictionnaire
        Après lecture d'un fichier XML et validé 
    dictPoints : dictionnaire
        Après lecture d'un fichier XML et validé 
    dictParametres : dictionnaire
        Après lecture d'un fichier XML et validé 
    
    Returns
    -------

    log : str
        Retourne le log de cette fonction.
    """

    
    
    # Initialisation des index "matrice" inconnues et observations (plani+alti) (incrément de 1M pour alti.)
    idObsPlani, idObsAlti = 0, 1000000
    idIncPlani, idIncAlti = 0, 1000000
    idConPlani = 0
    

   #-------------------
#### CALCUL DE Hmoy ---    
   #-------------------
        
    # Liste de tous les H disponibles
    listeAllH = []
    # liste des points
    listePoints = dictPoints['points']['point']
    for point in listePoints:
        
        # uniquement si H existe (pas vide)
        if point['H'] != None:
            listeAllH.append(float(point['H']))
            
    # Si au moins un H
    if len(listeAllH) >= 1:  
        Hmoy = np.mean(listeAllH)
    else: # si aucun H dans les points
        Hmoy = 600.0 # par défaut 600.0 m (altitude moyenne du plateau romand)
            

            
   #--------------------------------------------------------------------------------------------------------
#### CONSTANTES ADDITIONS ET FACT. ECHELLE ATTRIBUTION ID DANS GROUPE PARAM (GROUPE DISTANCE UNIQUEMENT) ---    
   #--------------------------------------------------------------------------------------------------------
   
    # Uniquement si un levé polaire est présent
    if 'polar' in dictCanevas['network'].keys(): 
        
        # Parcourir les groupes des paramètres et ajouter +1 au compteur à chaque inconnue suppl. plani ou alti.(true/false)
        for groupeDist in dictParametres['parameters']['groups']['distanceGroups']['distanceGroup']:
            
            # Saisir l'id (place dans la matrice) des inc. supplémentaires (concerne uniquement celles-ci, les GNSS et sys. locaux en ont par session)
            if groupeDist['additionalUnknowns']['scaleFactor'] == "true":
                groupeDist['additionalUnknowns'].update({'idIncFacteurEchelle':idIncPlani})
                groupeDist['additionalUnknowns'].update({'valIncFacteurEchelle':0.0})
                idIncPlani += 1
            if groupeDist['additionalUnknowns']['additionConstant'] == "true":
                groupeDist['additionalUnknowns'].update({'idIncConstanteAddition':idIncPlani})
                groupeDist['additionalUnknowns'].update({'valIncConstanteAddition':0.0})
                idIncPlani += 1
   
    
     
   #----------------------------------------------------
#### LEVES POLAIRE : REDUCTION ET ATTRIBUTION DES ID ---    
   #----------------------------------------------------
   
    # Uniquement si un levé polaire est présent
    if 'polar' in dictCanevas['network'].keys():
        
        # récupération du coef. de réfraction k
        k = float(dictParametres['parameters']['computationOptions']['refractionk'])
        sk = float(dictParametres['parameters']['computationOptions']['sigmaRefractionk'])
        
        
        # Liste de toutes les objets station
        listeStations = dictCanevas['network']['polar']['station']
        
        for iSta, station in enumerate(listeStations):
            
            # Parcourir le stationnement et get le noSta
            listeObservations = station['stationData']['measure']
            noSta = station['stationName']
            pointSta = rechercheUtils.rechercheNoPt(dictPoints, noSta)
            Nsta = pointSta['N'] # Nord de la station (pour distance au méridien)
            I = station['stationData']['I']
            
            # Saisir l'inconnue d'orientation et son id
            station['stationData'].update({'idIncOri':idIncPlani})
            station['stationData'].update({'valIncOri':0.0})
            idIncPlani += 1
            
            # groupe Distance
            nomGroupeDistance = station['stationData']['distanceGroup']
            groupeDistance = rechercheUtils.rechercheGroupeParNom(dictParametres, nomGroupeDistance)
            
            # groupe Direction
            nomGroupeDirection = station['stationData']['directionGroup']
            groupeDirection = rechercheUtils.rechercheGroupeParNom(dictParametres, nomGroupeDirection)
            
            # Centrage station
            nomGroupeCentrage= station['stationData']['centringGroup']
            groupeCentrage = rechercheUtils.rechercheGroupeParNom(dictParametres, nomGroupeCentrage)
            # si valeur manuelle vide -> par défaut
            if station['stationData']['stationCentring']['planiStdDev']['mm'] == None :
                mmStaPlaniParDef = float(groupeCentrage['stationCentring']['planiStdDev']['mm'])
            else: # si une valeur manuelle est entrée
                mmStaPlaniParDef = float(station['stationData']['stationCentring']['planiStdDev']['mm']) 
            if station['stationData']['stationCentring']['altiStdDev']['mm'] == None :
                mmStaAltiParDef = float(groupeCentrage['stationCentring']['altiStdDev']['mm'])
            else: # si une valeur manuelle est entrée
                mmStaAltiParDef = float(station['stationData']['stationCentring']['altiStdDev']['mm'])
            

            #### ^----- OBSERVATIONS POALIRES
            
            # Pour chaque observation
            for iObs, observation in enumerate(listeObservations):
                
                # deep copy de l'observation pour la modifier avec DP, RI et ZD mis à jour  
                newObservation = copy.deepcopy(observation)
                
                #Récupération des éléments
                # On réduit même si écarté (interviendra lors du remplissage des matrices dans l'estimation)
                RI, DS, ZD, dm1, dm2, S = observation['RI']['value'], observation['DS']['value'], observation['ZD']['value'], observation['dm1']['value'], observation['dm2']['value'], observation['S']['value']
                
                # Réduction plan proj. (sans déplacements)
                DP = geometrieUtils.reductionDistancePlanProj(float(DS), float(ZD), float(Nsta), Hmoy) # valeur Hab moy. générique (ordre de grandeur = 1m -> ok)
                
                
                #### ^----- ECART-TYPE PAR GROUPE ET INCONNUES SUPPLEMENTAIRES
                
                # si valeur manuelle vide -> par défaut
                if observation['DS']['stdDev']['mm'] == None :
                    mmParDef = float(groupeDistance['stdDev']['mm'])
                else: # si une valeur manuelle est entrée
                    mmParDef = float(observation['DS']['stdDev']['mm'])

                if observation['DS']['stdDev']['ppm'] == None :
                    ppmParDef = float(groupeDistance['stdDev']['ppm'])
                else: # si une valeur manuelle est entrée
                    ppmParDef = float(observation['DS']['stdDev']['ppm'])
                    
                # si valeur manuelle vide -> par défaut
                if observation['RI']['stdDev']['cc'] == None :
                    ccHorizParDef = float(groupeDirection['horizStdDev']['cc'])
                else: # si une valeur manuelle est entrée
                    ccHorizParDef = float(observation['RI']['stdDev']['cc'])
                if observation['ZD']['stdDev']['cc'] == None :
                    ccZenithParDef = float(groupeDirection['zenithStdDev']['cc'])
                else: # si une valeur manuelle est entrée
                    ccZenithParDef = float(observation['ZD']['stdDev']['cc'])
                    
                # si valeur de centrages du pt visé manuelles 
                if observation['targetCentring']['planiStdDev']['mm'] == None :
                    mmVisPlaniParDef = float(groupeCentrage['targetCentring']['planiStdDev']['mm'])
                    # Si vides: dm1 et dm2 = 0.0, dégrader la précision de centrage (ec-type manuel prime)
                    if dm1 != None or dm2 != None : 
                        mmVisPlaniParDef = np.sqrt(mmVisPlaniParDef**2 + 10.0**2)
                else: # si une valeur manuelle est entrée
                    mmVisPlaniParDef = float(observation['targetCentring']['planiStdDev']['mm']) 
                if observation['targetCentring']['altiStdDev']['mm'] == None :
                    mmVisAltiParDef = float(groupeCentrage['targetCentring']['altiStdDev']['mm'])
                else: # si une valeur manuelle est entrée
                    mmVisAltiParDef = float(observation['targetCentring']['altiStdDev']['mm']) 

                # si pas de dm saisi, = 0 (au lieu de None)
                if dm1 == None:
                    dm1 = 0.0
                if dm2 == None :
                    dm2 = 0.0

                # Correction des déplacements pour RI et DP
                RIcorr, DPcorr = geometrieUtils.corrAvecDepl(float(RI), DP, float(dm1), float(dm2))
                

                #### ^---------- RI to RIcorr
                RIcopy = newObservation['RI']
                newObservation.pop('RI') # remove RI
                RIcopy['stdDev'].pop('cc') # Suppression de la borne cc, pour une seule valeur d'écart-type en [g] 
                
                # Si RI est écarté
                if observation['RI']['discarded'] == "true":
                    RIcopy['discarded'] = "true"
                    RIcopy['value'] = None
                    RIcopy['stdDev'] = None
                    
                else: # si RI pas écarté, calculer RIcorr
                    RIcopy['value'] = round(RIcorr, 5) # arrondir à 5 décimales
                    RIcopy['stdDev'] = round(np.sqrt((ccHorizParDef/10000.0)**2 + ((mmStaPlaniParDef/1000.0)/float(DS)*200.0/np.pi)**2 + ((mmVisPlaniParDef/1000.0)/float(DS)*200.0/np.pi)**2),5)
                    RIcopy.update({'idObsPlani':idObsPlani})
                    idObsPlani += 1
                    
                newObservation.update({'RI':RIcopy})
                

                #### ^---------- (DS,ZD) to DPcorr
                DScopy = newObservation['DS']
                newObservation.pop('DS') # remove DS pour ajouter ensuite DP
                DScopy['stdDev'].pop('mm') # Suppression de la borne mm, pour une seule valeur d'écart-type en [m] 
                DScopy['stdDev'].pop('ppm') # Suppression de la borne mm, pour une seule valeur d'écart-type en [m] 
                
                # Uniquement si DS ou ZD pas écarté
                if observation['DS']['discarded'] == "true" or observation['ZD']['discarded'] == "true" :
                    DScopy['discarded'] = "true"
                    DScopy['stdDev'] = None
                    DScopy['value'] = round(DPcorr, 4) # arrondir à 4 décimales
                    
                    
                else : # si DS et ZD pas écartés, calculer DPcorr
                    DScopy['value'] = round(DPcorr, 4) # arrondir à 4 décimales
                    DScopy['stdDev'] = round(np.sqrt(  (mmParDef/1000.0 + ppmParDef*1e-6*float(DS))**2 + (mmStaPlaniParDef/1000.0)**2 + (mmVisPlaniParDef/1000.0)**2 ),4)
                    DScopy.update({'idObsPlani':idObsPlani})
                    idObsPlani += 1
                
                newObservation.update({'DP':DScopy})

                
                #### ^---------- (ZD,DS) to DH
                ZDcopy = newObservation['ZD']
                newObservation.pop('ZD') # remove ZD pour y ajouter ensuite DH (ZDcopy)
                ZDcopy['stdDev'].pop('cc') # Suppression de la borne cc, pour une valeur d'écart-type en [m]
                
                # Si déplacement ou pas de I ou pas de S ou DS écarté ou ZD écarté
                if abs(float(dm1)) > 0.0 or abs(float(dm2)) > 0.0 or S == None or I == None or observation['ZD']['discarded'] == "true" or observation['DS']['discarded'] == "true": 
                    ZDcopy['discarded'] = "true"
                    ZDcopy['stdDev'] = None
                    ZDcopy['value'] = None # arrondir à 4 décimales   

                else: # si une dénivelée peut être calculée
                    # Calcul de la dénivelée DH (ZD->DH)
                    DH = geometrieUtils.nivellementTrigoDH(float(ZD),float(DS),float(k),6378800.0, float(I), float(S))
                    ZDcopy['value'] = round(DH, 4) # arrondir à 4 décimales  np.cos(ZD*np.pi/200.0)**2 * (mmParDef/1000.0)**2  +   DS**2 * np.sin(ZD*np.pi/200.0)**2 * (ccZenithParDef/10000.0)**2
                    ZDcopy['stdDev'] = round(np.sqrt(     np.cos(float(ZD)*np.pi/200.0)**2 * (mmParDef/1000.0)**2  +   float(DS)**2 * np.sin(float(ZD)*np.pi/200.0)**2 * (ccZenithParDef/10000.0 * np.pi/200.0)**2   +    float(DS)**4/(4*6378800) * sk**2    + (mmStaAltiParDef/1000.0)**2 + (mmVisAltiParDef/1000.0)**2 ),4)
                    ZDcopy.update({'idObsAlti':idObsAlti})
                    idObsAlti += 1
                
                newObservation.update({'DH':ZDcopy})
                                
                # Mise à jour avec la nouvelle observation (avec DPcorr et RIcorr et DH au lieu de RI et DS et ZD)
                dictCanevas['network']['polar']['station'][iSta]['stationData']['measure'][iObs] = newObservation
                
                
       
   #------------------------------
#### GNSS : ATTRIBUTION DES ID ---    
   #------------------------------
       
    if 'gnss' in dictCanevas['network'].keys():
        
        # Parcourir les sessions
        for session in dictCanevas['network']['gnss']['session']:
            
            # Attribution des ID des inconnues en fonction du groupe
            groupeGNSS = rechercheUtils.rechercheGroupeParNom(dictParametres, session['gnssGroup'])
            ecartTypeHoriz, ecartTypeAlti = float(groupeGNSS['planiStdDev']['mm']), float(groupeGNSS['altiStdDev']['mm'])
            
            # Création d'un dictionnaire pour stocker les id
            session.update({'unknownParameters':{}})
            
            # Attribution pour chacun des param. inconnus
            if groupeGNSS['unknownParameters'] and groupeGNSS['unknownParameters']['Etranslation'] == "true":
                session['unknownParameters'].update({'idIncTranslationE': idIncPlani})
                session['unknownParameters'].update({'valIncTranslationE': 0.0})
                idIncPlani += 1
            if groupeGNSS['unknownParameters']['Ntranslation'] == "true":
                session['unknownParameters'].update({'idIncTranslationN': idIncPlani})
                session['unknownParameters'].update({'valIncTranslationN': 0.0})
                idIncPlani += 1
            if groupeGNSS['unknownParameters']['horizRotation'] == "true":
                session['unknownParameters'].update({'idIncRotationHoriz': idIncPlani})
                session['unknownParameters'].update({'valIncRotationHoriz': 0.0})
                idIncPlani += 1
            if groupeGNSS['unknownParameters']['horizScaleFactor'] == "true":
                session['unknownParameters'].update({'idIncFacteurEchelleHoriz': idIncPlani})
                session['unknownParameters'].update({'valIncFacteurEchelleHoriz': 1.0})
                idIncPlani += 1
            if groupeGNSS['unknownParameters']['Htranslation'] == "true":
                session['unknownParameters'].update({'idIncTranslationH': idIncAlti})
                session['unknownParameters'].update({'valIncTranslationH': 0.0})
                idIncAlti += 1

                
            #### ^------ OBSERVATIONS GNSS
            for observation in session['measure']:
                
                # Attribution des idObs plani et alti si non-écartés + calculer de sigma en [m]
                if "LY" in observation.keys() :
                    if observation['LY']['discarded'] in ['false', None]:
                        
                        if observation['LY']['stdDev']['mm'] == None: # si pas de sigma manuel
                            observation['LY']['stdDev'].pop('mm')
                            observation['LY']['stdDev'] = ecartTypeHoriz/1000.0 # en [m]
                        else: # si écart-type manuel
                            ecartTypeManuel = float(observation['LY']['stdDev']['mm'])
                            observation['LY']['stdDev'].pop('mm')
                            observation['LY']['stdDev'] = ecartTypeManuel/1000.0 # en [m]
                            
                        observation['LY'].update({'idObsPlani':idObsPlani})
                        idObsPlani += 1
                    else: # si écarté
                        observation['LY']['stdDev'].pop('mm')
                        observation['LY']['stdDev'] = None
                        
                        
                        
                if "LX" in observation.keys() :
                    if observation['LX']['discarded'] in ['false', None]:
                        
                        if observation['LX']['stdDev']['mm'] == None: # si pas de sigma manuel
                            observation['LX']['stdDev'].pop('mm')
                            observation['LX']['stdDev'] = ecartTypeHoriz/1000.0 # en [m]
                        else: # si écart-type manuel
                            ecartTypeManuel = float(observation['LX']['stdDev']['mm'])
                            observation['LX']['stdDev'].pop('mm')
                            observation['LX']['stdDev'] = ecartTypeManuel/1000.0 # en [m]
                        
                        observation['LX'].update({'idObsPlani':idObsPlani})
                        idObsPlani += 1
                    else: # si écarté
                        observation['LX']['stdDev'].pop('mm')
                        observation['LX']['stdDev'] = None
                        
                        
                if "LH" in observation.keys() :
                    if observation['LH']['discarded'] in ['false', None]:
                        
                        if observation['LH']['stdDev']['mm'] == None: # si pas de sigma manuel
                            observation['LH']['stdDev'].pop('mm')
                            observation['LH']['stdDev'] = ecartTypeAlti/1000.0 # en [m]
                        else: # si écart-type manuel
                            ecartTypeManuel = float(observation['LH']['stdDev']['mm'])
                            observation['LH']['stdDev'].pop('mm')
                            observation['LH']['stdDev'] = ecartTypeManuel/1000.0 # en [m]
                        
                        observation['LH'].update({'idObsAlti':idObsAlti})
                        idObsAlti += 1
                    else: # si écarté
                        observation['LH']['stdDev'].pop('mm')
                        observation['LH']['stdDev'] = None
             
                    
   #---------------------------------------
#### SYSTEMES LOC. : ATTRIBUTION DES ID ---    
   #---------------------------------------

    if 'localSystems' in dictCanevas['network'].keys():
        
        # Parcourir les systèmes
        for systemeLocal in dictCanevas['network']['localSystems']['localSystem']:
            
            # Attribution des ID des inconnues en fonction du groupe + écart-types par défaut selon param.
            groupeSystemeLocal = rechercheUtils.rechercheGroupeParNom(dictParametres, systemeLocal['localSystemGroup'])
            ecartTypeHoriz, ecartTypeAlti = float(groupeSystemeLocal['planiStdDev']['mm']), float(groupeSystemeLocal['altiStdDev']['mm'])

            # Création d'un dictionnaire pour stocker les id
            systemeLocal.update({'unknownParameters':{}})
            
            # Types d'obs. du système local
            typesObs = []
            for observation in systemeLocal['measure']:
                if "LY" in observation.keys() and "LX" in observation.keys() :
                    typesObs.append("LY")
                    typesObs.append("LX")
                if "LH" in observation.keys() :
                    typesObs.append("LH")
            typesObs = set(typesObs)
            
            # Ajout des inconnues par défaut selon les types d'obs.
            if "LY" in typesObs and "LX" in typesObs:
                systemeLocal['unknownParameters'].update({'idIncTranslationE': idIncPlani})
                systemeLocal['unknownParameters'].update({'valIncTranslationE': 0.0})
                idIncPlani += 1
                systemeLocal['unknownParameters'].update({'idIncTranslationN': idIncPlani})
                systemeLocal['unknownParameters'].update({'valIncTranslationN': 0.0}) 
                idIncPlani += 1
                systemeLocal['unknownParameters'].update({'idIncRotationHoriz': idIncPlani})
                # rotation approchée (valIncRotationHoriz ajouté dans la fonction rotationsApprochees)
                idIncPlani += 1
            if "LH" in typesObs:
                systemeLocal['unknownParameters'].update({'idIncTranslationH': idIncAlti})
                systemeLocal['unknownParameters'].update({'valIncTranslationH': 0.0}) 
                idIncAlti += 1
            
            

            # Attribution pour chacun des param. inconnus suppl.
            if groupeSystemeLocal['unknownParameters']['horizScaleFactor'] == "true":
                systemeLocal['unknownParameters'].update({'idIncFacteurEchelleHoriz': idIncPlani})
                systemeLocal['unknownParameters'].update({'valIncFacteurEchelleHoriz': 1.0}) 
                idIncPlani += 1

                
            #### ^------OBSERVATIONS SYSTEMES LOCAUX
            for observation in systemeLocal['measure']:
                
                # Attribution des idObs plani et alti si non-écartés + calculer de sigma en [m]
                if "LY" in observation.keys() :
                    if observation['LY']['discarded'] in ['false', None]:
                        
                        if observation['LY']['stdDev']['mm'] == None: # si pas de sigma manuel
                            observation['LY']['stdDev'].pop('mm')
                            observation['LY']['stdDev'] = ecartTypeHoriz/1000.0 # en [m]
                        else: # si écart-type manuel
                            ecartTypeManuel = float(observation['LY']['stdDev']['mm'])
                            observation['LY']['stdDev'].pop('mm')
                            observation['LY']['stdDev'] = ecartTypeManuel/1000.0 # en [m]
                            
                        observation['LY'].update({'idObsPlani':idObsPlani})
                        idObsPlani += 1
                    else: # si écarté
                        observation['LY']['stdDev'].pop('mm')
                        observation['LY']['stdDev'] = None
                        
                        
                        
                if "LX" in observation.keys() :
                    if observation['LX']['discarded'] in ['false', None]:
                        
                        if observation['LX']['stdDev']['mm'] == None: # si pas de sigma manuel
                            observation['LX']['stdDev'].pop('mm')
                            observation['LX']['stdDev'] = ecartTypeHoriz/1000.0 # en [m]
                        else: # si écart-type manuel
                            ecartTypeManuel = float(observation['LX']['stdDev']['mm'])
                            observation['LX']['stdDev'].pop('mm')
                            observation['LX']['stdDev'] = ecartTypeManuel/1000.0 # en [m]
                        
                        observation['LX'].update({'idObsPlani':idObsPlani})
                        idObsPlani += 1
                    else: # si écarté
                        observation['LX']['stdDev'].pop('mm')
                        observation['LX']['stdDev'] = None
                        
                        
                if "LH" in observation.keys() :
                    if observation['LH']['discarded'] in ['false', None]:
                        
                        if observation['LH']['stdDev']['mm'] == None: # si pas de sigma manuel
                            observation['LH']['stdDev'].pop('mm')
                            observation['LH']['stdDev'] = ecartTypeAlti/1000.0 # en [m]
                        else: # si écart-type manuel
                            ecartTypeManuel = float(observation['LH']['stdDev']['mm'])
                            observation['LH']['stdDev'].pop('mm')
                            observation['LH']['stdDev'] = ecartTypeManuel/1000.0 # en [m]
                        
                        observation['LH'].update({'idObsAlti':idObsAlti})
                        idObsAlti += 1
                    else: # si écarté
                        observation['LH']['stdDev'].pop('mm')
                        observation['LH']['stdDev'] = None
            

    #-------------------------------
 #### COTES : ATTRIBUTION DES ID ---    
    #-------------------------------   

    if 'simpleMeasures' in dictCanevas['network'].keys():
        
        # Parcourir les cotes
        for cote in dictCanevas['network']['simpleMeasures']['simpleMeasure']:
            
            #### ^------ OBSERVATION DE COTES DP OU DH
            
            
            # Groupe de cote pour calcul de l'écart-type par défaut
            groupeCote= rechercheUtils.rechercheGroupeParNom(dictParametres, cote['simpleMeasureGroup'])
            ecartTypeHoriz, ecartTypeAlti = float(groupeCote['planiStdDev']['mm']), float(groupeCote['altiStdDev']['mm'])

            
            # Si c'est une cote horiz. DP
            if "DP" in cote['measure'].keys():
                if cote['measure']['DP']['discarded'] in ['false', None]:
                    cote['measure']['DP'].update({'idObsPlani':idObsPlani})
                    idObsPlani += 1
                    
                    # écart-type manuel ou par défaut
                    if cote['measure']['DP']['stdDev']['mm'] == None: # si pas de sigma manuel
                        cote['measure']['DP']['stdDev'].pop('mm')
                        cote['measure']['DP']['stdDev'] = ecartTypeHoriz/1000.0 # en [m]
                    else: # si écart-type manuel
                        ecartTypeManuel = float(cote['measure']['DP']['stdDev']['mm'])
                        cote['measure']['DP']['stdDev'].pop('mm')
                        cote['measure']['DP']['stdDev'] = ecartTypeManuel/1000.0 # en [m]
                        
                else: # si écarté
                    cote['measure']['DP']['stdDev'].pop('mm')
                    cote['measure']['DP']['stdDev'] = None
                    
      
            # Si c'est une cote dénivelée. DH
            if "DH" in cote['measure'].keys():
                if cote['measure']['DH']['discarded'] in ['false', None]:
                    cote['measure']['DH'].update({'idObsAlti':idObsAlti})
                    idObsAlti += 1
                    
                    # écart-type manuel ou par défaut
                    if cote['measure']['DH']['stdDev']['mm'] == None: # si pas de sigma manuel
                        cote['measure']['DH']['stdDev'].pop('mm')
                        cote['measure']['DH']['stdDev'] = ecartTypeAlti/1000.0 # en [m]
                    else: # si écart-type manuel
                        ecartTypeManuel = float(cote['measure']['DP']['stdDev']['mm'])
                        cote['measure']['DH']['stdDev'].pop('mm')
                        cote['measure']['DH']['stdDev'] = ecartTypeManuel/1000.0 # en [m]
                        
                else: # si écarté
                    cote['measure']['DH']['stdDev'].pop('mm')
                    cote['measure']['DH']['stdDev'] = None
                    
               
                    
               
    #-------------------------------------
 #### CONTRAINTES : ATTRIBUTION DES ID ---    
    #-------------------------------------      

    if 'constraints' in dictCanevas['network'].keys():
        
        # Parcourir les contraintes
        for contrainte in dictCanevas['network']['constraints']['constraint']:
            
            # Attribution idConPlani si pas écartée
            if contrainte['discarded'] in ['false', None]:
                contrainte.update({'idConPlani':idConPlani})
                idConPlani += 1
    
            
    
    #--------------------------------
 #### POINTS : ATTRIBUTION DES ID ---    
    #-------------------------------- 
    
    
    # Liste des points fixes (ne pas attribuer de idInc)
    listeNoPfPlani = []
    listeNoPfAlti = []

    # Pour la partie planimétrique
    if dictParametres['parameters']['computationOptions']['calculationDimension'] == "2D" or dictParametres['parameters']['computationOptions']['calculationDimension'] == "2D+1" :
        listePointsFixesPlani = dictParametres['parameters']['planimetricControlPoints']['point']
        for PFplani in listePointsFixesPlani:
            listeNoPfPlani.append(PFplani['pointName'])
            
    # Pour la partie altimétrique
    if dictParametres['parameters']['computationOptions']['calculationDimension'] == "1D" or dictParametres['parameters']['computationOptions']['calculationDimension'] == "2D+1" :
        listePointsFixesAlti = dictParametres['parameters']['altimetricControlPoints']['point']
        for PFalti in listePointsFixesAlti:
            listeNoPfAlti.append(PFalti['pointName'])
            
    # Parcourir tous les points
    for point in dictPoints['points']['point']:
        
        # Attribution des idIncPlani/Alti aux pts ayant assez de détermination et si ils ne sont pas fixes
        if point['pointName'] not in listeNoPfPlani:
            if point['planimetricElems'] >= 2 :
                point.update({'idUnkE':idIncPlani})
                idIncPlani += 1
                point.update({'idUnkN':idIncPlani})
                idIncPlani += 1
                

                
        if point['pointName'] not in listeNoPfAlti:
            if point['altimetricElems'] >= 1 :
                point.update({'idUnkH':idIncAlti})
                idIncAlti += 1
                 
            
    # dictionnaire pour la future création des matrices
    denombrement = {'nbObsPlani':idObsPlani,
                    'nbIncPlani':idIncPlani,
                    'nbConPlani': idConPlani,
                    'surabondancePlani':idObsPlani-idIncPlani+idConPlani,
                    'nbObsAlti':idObsAlti-1000000,
                    'nbIncAlti':idIncAlti-1000000,
                    'surabondanceAlti':idObsAlti-idIncAlti}           


    return denombrement











class PreProcess:
    
    def __init__(self, dictCanevas, dictPoints, dictParametres):
        """
        Constructeur de la classe "preProcess".

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
        
        
    def preTraitements(self):
        """
        Fonction simple permettant de lancer la fonction de réduction et du calcul des dénivelées.
        
        Returns
        -------
        bool
            True si pré-traitement effectuée normalement. False sinon.
            
        """

        # try:
        self.denombrement = preTraitements(self.dictCanevas, self.dictPoints, self.dictParametres)
        return True
        # except:
            # print("ERROR 1000.1 : UNDEFINED PROBLEM WHEN PRE-PROCESSING DATA PRIOR TO AJUSTMENT")
            # return False
            
        
        
    def rotationsApprochees(self):
        """
        Fonction permettant de calculer les rotation approchées des systèmes locaux (avec les points communs sur les coordonnées approchées).

        Returns
        -------
        bool
            True si pré-traitement effectuée normalement. False sinon.

        """        
        
        try:
            rotationsApprochees(self.dictCanevas, self.dictPoints)
            return True
        except:
            print("ERROR 1100.1 : UNDEFINED PROBLEM IN APPROACHED ROTATIONS CALCULATIONS FOR LOCAL SYSTEMS PRIOR TO AJUSTMENT, CHECK COMMON POINTS")
            return False
    
    
    def centroidesSystemesSessions(self):
        """
        Fonction permettant de calculer les centroids des systemes locaux et sessions globales GNSS.

        Returns
        -------
        bool
            True si pré-traitement effectuée normalement. False sinon.

        """        
        
        try:
            centroidesSystemesSessions(self.dictCanevas, self.dictPoints)
            return True
        except:
            print("ERROR 1200.2 : UNDEFINED PROBLEM IN CENTROIDS CALCULATION FOR SESSIONS AND LOCAL SYSTEMS PRIOR TO AJUSTMENT")
            return False
    
        
        
        
    
    def getDenombrement(self):
        
        return self.denombrement