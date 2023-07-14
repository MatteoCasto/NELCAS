# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:24:36 2022

@author: Matteo Casto, INSIT
"""

from lxml import etree
import math
import numpy as np
import xmltodict
import sys
import libUtils.geometrieUtils as geometrieUtils
import libUtils.rechercheUtils as rechercheUtils
import libUtils.conversionUtils as conversionUtils
import os
import copy




def checkXmlXsd(nomXsd, nomXml) :
    
    """
    Checker pour valider un fichier xml par rapport à un fichier modèle XSD

    Parameters
    ----------
    nomXsd : string
        Nom avec l'extension du modèle de donnée'
    nomXml : string
        Nom avec l'extension du fichier xml'

    Returns
    -------
    result : bool
        Retourne si le fichier est compatible ou non.
    log : str
        Retourne le log de cette fonction.

    """
    
    # Initialisation du LOG
    log = "CODE 100 : STRUCTURE VALIDATION {:s} WITH DATAMODEL {:s}\n".format(nomXml.split('\\')[-1], nomXsd.split('\\')[-1])
    log+= (len(log)-1)*"-" + "\n"

    # Parse le fichier xsd
    xmlschema_doc = etree.parse(nomXsd)
    # Création du sxhéma xml
    xmlschema = etree.XMLSchema(xmlschema_doc)
    # Parse le fichier xml 
    xml_doc = etree.parse(nomXml)
    # Check la validation
    result = xmlschema.validate(xml_doc)
    # Erreur log (de etree)
    if result == False :
        # Test echoué, log de etree
        log += ">>> ERROR 100.1 : ETREE LIBRARY AUTO-ERROR MESSAGE:\n\n"
        log += str(xmlschema.error_log) + "\n\n"
    else: # résultat positif
        log += ">>> checked\n\n"
    

    print(log)
    return result, log




def structureListeInDict(dictionnaire, typeDict):
    
    """
    Ce fonction a pour but de mettre sous forme de liste certains éléments issus d'un dictionnaires (de fichier XML)
    Elle fonctionne notamment si il n'y a qu'un seul éléments où plusieurs sont possbiles, car xml2dict ne la met 
    pas en forme automatiquement sous forme de liste (de longueur 1).
    Exemple: groupeDistanceParDefaut --> [groupeDistanceParDefaut] 
    
    Parameters
    ----------
    dictionnaire : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    typeDict : string
        Type de dictionnaire à modifier. -> "parameters" ou "network"
    
    Returns
    -------
    dictionnaire : dictionnaire
        Retourne le fichier avec les listes par type de groupe
    
    """
    
    if typeDict == 'parameters':
    
        # Récupérer la balise des groupes
        groupes = dictionnaire['parameters']['groups']
        
        for key,value in groupes.items():
            
            
            for key2, value2 in value.items():
                if type(value2) == dict:
                    dictionnaire['parameters']['groups'][key][key2] = [value2]

    
        # Uniquement si altimétrie concernée, sinon planimétrie déjà 2pts minimum régit par le XSD
        
        if dictionnaire['parameters']['computationOptions']['calculationDimension'] == "1D" or dictionnaire['parameters']['computationOptions']['calculationDimension'] == "2D+1":
            
            try : # si pas de balise pointsFixesAlti (sera détectée en ERREUR 5.2)
                # Récupérer la balise des points fixes alti
                PFalti = dictionnaire['parameters']['altimetricControlPoints']
    
                for key,value in PFalti.items():           
                    if type(value) == dict: # Si un seul point fixe alti.
                        dictionnaire['parameters']['altimetricControlPoints'][key] = [value]
                        
            except: # ne pas appliquer la transformation en liste
                pass
            
         
        return dictionnaire 
        
        
    if typeDict == 'network':
        
        # Liste des balises présentes
        listeBalises = dictionnaire['network'].keys()
        for balise in listeBalises:
            
            #### ------ POLAIRE
            if balise == 'polar':
                # Check que ça soit pas un dictionnaire 
                stations = dictionnaire['network']['polar']['station']
                if type(stations) == dict:
                    dictionnaire['network']['polar']['station'] = [stations]
                
                # Mesures en en liste
                for sta in dictionnaire['network']['polar']['station']:
                    sta['stationData']['measure'] = sta['stationData']['measure'] if type(sta['stationData']['measure']) == list else [sta['stationData']['measure']]
                        
            #### ------ GNSS
            if balise == 'gnss':
                # Check que ça soit pas un dictionnaire 
                sessions = dictionnaire['network']['gnss']['session']
                if type(sessions) == dict:
                    dictionnaire['network']['gnss']['session'] = [sessions]
                    
            #### ------ SYSTEMES LOCAUX
            if balise == 'localSystems':
                # Check si c'est bien une liste
                systemesLocaux = dictionnaire['network']['localSystems']['localSystem']
                if type(systemesLocaux) == dict:
                    dictionnaire['network']['localSystems']['localSystem'] = [systemesLocaux]
                    
            #### ------ COTES
            if balise == 'simpleMeasures':
                # Check que ça soit pas un dictionnaire 
                cotes = dictionnaire['network']['simpleMeasures']['simpleMeasure']
                if type(cotes) == dict:
                    dictionnaire['network']['simpleMeasures']['simpleMeasure'] = [cotes]
                    
            #### ------ CONTRAINTES
            if balise == 'constraints':
                # Check que ça soit pas un dictionnaire 
                contraintes = dictionnaire['network']['constraints']['constraint']
                if type(contraintes) == dict:
                    dictionnaire['network']['constraints']['constraint'] = [contraintes]
                
        return dictionnaire
                
                
                
            
            
def checkDoublonsPoints(dictPoints):
    
    """
    Checker sémantique qui contrôle simplement qu'il n'y est pas de doublons dans les numéros de points.
    
    Parameters
    ----------
    dictPoints : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    
    Returns
    -------
    checkDoublonsPoints : bool
        Retourne si le fichier est ok ou non sur ces éléments sémantiques.
    log : str
        Retourne le log de cette fonction.
    
    """
    
    # Initialisation du LOG
    log = "CODE 200 : DUPLICATE POINTS\n"
    log+= (len(log)-1)*"-" + "\n"
    
    # Initialisation
    checkDoublonsPoints = True
    listeNoPoint = []
    
    # Parcourir les points
    listePoints = dictPoints['points']['point']
    for point in listePoints:
        
        # si le point n'y est pas, ajout du numéro
        if point['pointName'] not in listeNoPoint:
            listeNoPoint.append(point['pointName'])
            
        else: # le point y est déjà
            checkDoublonsPoints = False
            log += ">>> ERROR 200.1 : DUPLICATE POINT : {:s}\n".format(point['pointName'])

    if checkDoublonsPoints: # contrôle postitif
        log += ">>> checked\n\n"
    else:
        log+="\n" # retour à la ligne
    print(log)
    return checkDoublonsPoints, log    
            
        
        
        

    

def checkThemeNatureInCanevas(dictCanevas):
    
    """
    NON UTILISE POUR LE MOMENT
    Checker sémantique pour contrôler si chaque point visés/station a le même thème/nature si il est concernés plusieurs fois.
    Fonction à utiliser AVANT le calcul des coordonnées approchées.
    Reporte les éventuels problèmes dans la console/log.
    ATTENTION: la fonction considère la première apparition comme faisant foi, les autres seront considérées fausses. 
    
    Parameters
    ----------
    dictCanevas : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    
    Returns
    -------
    checkThemeNatureInCanevas : bool
        Retourne si le fichier est ok ou non sur ces éléments sémantiques.
    
    """
    
    checkThemeNatureInCanevas = True # Initialisation 
    
    # Liste de tous les points concernés dans le dict. Canevas (station et points)
    dictNoPointsCanevas = {}
    
    
    # --- POLAIRE
    
    if "polare" in dictCanevas['network'].keys():
    
        # Liste de toutes les objets station
        listeStations = dictCanevas['network']['polar']['station']
        
        for station in listeStations:
                
            # --- No de stations
            # Ajouter uniquement si le noSta n'y est pas déjà
            if station['stationName'] not in dictNoPointsCanevas.keys():
                # Récupération du No de point et son thème/nature
                dictNoPointsCanevas.update({station['stationName']: [station['themeMO'], station['natureMO']]})
            
            else: # Si le noSta y est déjà, contrôle du thème/nature avec le point déjà inséré
                if station['themeMO'] != dictNoPointsCanevas[station['stationName']][0] or station['natureMO'] != dictNoPointsCanevas[station['stationName']][1]:
                    print('ERREUR THEME/NATURE :','sta:',station['stationName'], 'thème/nature:',station['themeMO'],station['natureMO'])
                    checkThemeNatureInCanevas = False
    
                    
            # --- No de points visés
            listeObservations = station['stationData']['measure']
            for observation in listeObservations:
                
                # Ajouter uniquement si le noPt n'y est pas déjà
                if observation['pointName'] not in dictNoPointsCanevas.keys():
                    # Récupération du No de point et son thème/nature
                    dictNoPointsCanevas.update({observation['pointName']: [observation['themeMO'], observation['natureMO']]})
    
                else: # Si le noPt y est déjà, contrôle du thème/nature avec le point déjà inséré
                    if observation['themeMO'] != dictNoPointsCanevas[observation['pointName']][0] or observation['natureMO'] != dictNoPointsCanevas[observation['pointName']][1]:
                        print('ERREUR THEME/NATURE :','sta:',station['stationName'],'vers pt:',observation['pointName'], 'thème/nature:',observation['themeMO'],observation['natureMO'])
                        checkThemeNatureInCanevas = False
                    
                    
    # --- GNSS
    
    if 'gnss' in dictCanevas['network'].keys():
        
        # Liste de toutes les objets session
        listeSessions = dictCanevas['network']['gnss']['session']
        for session in listeSessions:
            
            # Parcourir la session et get les No de pts visés dans les obs.
            listeObservations = session['measure']
            
            for observation in listeObservations:
                
                # Ajouter uniquement si le noPt n'y est pas déjà
                if observation['pointName'] not in dictNoPointsCanevas.keys():
                    # Récupération du No de point et son thème/nature
                    dictNoPointsCanevas.update({observation['pointName']: [observation['themeMO'], observation['natureMO']]})
    
                else: # Si le noPt y est déjà, contrôle du thème/nature avec le point déjà inséré
                    if observation['themeMO'] != dictNoPointsCanevas[observation['pointName']][0] or observation['natureMO'] != dictNoPointsCanevas[observation['pointName']][1]:
                        print('ERREUR THEME/NATURE :','session:',session['sessionName'],'pt:',observation['pointName'], 'thème/nature:',observation['themeMO'],observation['natureMO'])
                        checkThemeNatureInCanevas = False
            

    return checkThemeNatureInCanevas





def checkCanevasInPoints(dictCanevas, dictPoints):
    
    """
    Checker sémantique pour contrôler si chaque point visés/station se trouve dans les points.
    Reporte les éventuels problèmes dans la console/log.
    
    Parameters
    ----------
    dictCanevas : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    dictPoints : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    
    Returns
    -------
    resControle : bool
        Retourne si le fichier est ok ou non sur ces éléments sémantiques.
    log : str
        Retourne le log de cette fonction.
    
    """
    
    # Initialisation du LOG
    log = "CODE 201 : POINTS FROM NETWORK FILE FOUND IN POINTS FILE\n"
    log+= (len(log)-1)*"-" + "\n"
    
    resControle = True # initialisation 
            
     #---------------
#### # --- POINTS ---
     #---------------
    
    # Dico de tous les no de points (key) du dicionnaire des points
    dictNoPts = {}
    
    # Liste de tous les objets points
    listePoints = dictPoints['points']['point']
    
    for point in listePoints:
        
        # Récupération du No de point et son thème/nature
        dictNoPts.update({point['pointName']: []}) # Remplir ici si on veut faire des check sur des thèmes ou autres
        
        
     #----------------
#### # --- CANEVAS ---
     #----------------
     
    # Si il n'y a pas de balises principales -> résultat = None
    if len(dictCanevas['network'].keys()) < 1:
       resControle = None 
    
    
    #### ------ POLAIRE
    
    # Vérifier qu'il y a bien un levé polaire
    if 'polar' in dictCanevas['network'].keys():
        
        # Liste de toutes les objets station
        listeStations = dictCanevas['network']['polar']['station']
        
        for station in listeStations:
            
            # Checker la présence du noSta dans les No du dictPoints   
            if station['stationName'] not in dictNoPts.keys():
                # Print du message d'erreur
                log += ">>> ERROR 201.1 : POLAR STATION MISSING : {:s}\n".format(station['stationName'])
                resControle = False
            
            # Parcourir le stationnement et get les No de pts visés dans les obs.
            listeObservations = station['stationData']['measure']
            for observation in listeObservations:
                
                # Checker la présence du noPtVisé dans les No du dictPoints
                if observation['pointName'] not in dictNoPts.keys(): 
                    
                    # Print du message d'erreur
                    log += ">>> ERROR 201.2 : POLAR TARGET MISSING : from station : {:s} to target : {:s}\n".format(station['stationName'], observation['pointName'])
                    resControle = False
                  

    #### ------ GNSS
    
    # Vérifier qu'il y a bien un levé GNSS
    if 'gnss' in dictCanevas['network'].keys():
    
        # Liste de toutes les objets session
        listeSessions = dictCanevas['network']['gnss']['session']
        for session in listeSessions:
            
            # Parcourir la session et get les No de pts visés dans les obs.
            listeObservations = session['measure']
            for observation in listeObservations:
    
                # Checker la présence du No dans les No du dictPoints
                if observation['pointName'] not in dictNoPts.keys():
                    
                    # Print du message d'erreur
                    log += ">>> ERROR 201.3 : GNSS SESSION TARGET MISSING : session: {:s} , target: {:s}\n".format(session['sessionName'], observation['pointName'])
                    resControle = False
                    
                                
           
    #### ------ SYSTEMES LOCAUX
    
    # Vérifier qu'il y a bien la balise des systèmes locaux
    if 'localSystems' in dictCanevas['network'].keys():
        
        listeSystemesLocaux = dictCanevas['network']['localSystems']['localSystem']
        for systemeLocal in listeSystemesLocaux:
            
            # Parcourir le système local et get les No de pts visés dans les obs.
            listeObservations = systemeLocal['measure']
            for observation in listeObservations:
                
                # Checker la présence du No dans les No du dictPoints
                if observation['pointName'] not in dictNoPts.keys():
                    
                    # Print du message d'erreur
                    log += ">>> ERROR 201.4 : LOCAL SYSTEM TARGET MISSING : local system: {:s} , target: {:s}\n".format(systemeLocal['localSystemName'], observation['pointName'])
                    resControle = False
            
  
            
    #### ------ COTES
    
    # Vérifier qu'il y a bien un levé GNSS
    if 'simpleMeasures' in dictCanevas['network'].keys():
    
        listeCotes = dictCanevas['network']['simpleMeasures']['simpleMeasure']
        for cote in listeCotes:
    
            # Checker la présence des No dans les No du dictPoints
            if cote['measure']['pointName1'] not in dictNoPts.keys() :
                # Print du message d'erreur
                log += ">>> ERROR 201.5 : POIN1 MISSING IN SIMPLE MEASURE : point1 : {:s} to point2 : {:s}\n".format(cote['measure']['pointName1'], cote['measure']['pointName2'])
                resControle = False
            if cote['measure']['pointName2'] not in dictNoPts.keys():
                # Print du message d'erreur
                log += ">>> ERROR 201.6 : POIN2 MISSING IN SIMPLE MEASURE : point1 : {:s} to point2 : {:s}\n".format(cote['measure']['pointName1'], cote['measure']['pointName2'])
                resControle = False        
    
    

    #### ------ CONTRAINTES  
    
    # Vérifier qu'il y a bien la balise des contraintes
    if 'constraints' in dictCanevas['network'].keys():
        
        listeContraintes = dictCanevas['network']['constraints']['constraint']
        for contrainte in listeContraintes:
            
            # Checker la présence des No dans les No du dictPoints + print des messages d'erreur
            listeRolesPts = [] 
            for point in contrainte['point']:
                if point['pointName'] not in dictNoPts.keys() and point['pointTypeInConstraint'] == "A":
                    log += ">>> ERROR 201.7 : POINT NAME A MISSING IN CONSTRAINT : {:s}\n".format(point['pointName'])
                    resControle = False
                if point['pointName'] not in dictNoPts.keys() and point['pointTypeInConstraint'] == "B":
                    log += ">>> ERROR 201.8 : POINT NAME B MISSING IN CONSTRAINT : {:s}\n".format(point['pointName'])
                    resControle = False
                if point['pointName'] not in dictNoPts.keys() and point['pointTypeInConstraint'] == "P":
                    log += ">>> ERROR 201.9 : POINT NAME P MISSING IN CONSTRAINT : {:s}\n".format(point['pointName'])
                    resControle = False
                    
                listeRolesPts.append(point['pointTypeInConstraint'])
            
            # Check si Il y'a bien A, B et P une fois de chaque
            if "A" not in listeRolesPts :
                log += ">>> ERROR 201.10 : POINT TYPE A MISSING IN A CONSTRAINT\n"
                resControle = False
            if "B" not in listeRolesPts :
                log += ">>> ERROR 201.10 : POINT TYPE B MISSING IN A CONSTRAINT\n"
                resControle = False
            if "P" not in listeRolesPts :
                log += ">>> ERROR 201.11 : POINT TYPE P MISSING IN A CONSTRAINT\n"
                resControle = False
            
            
                    
                    
                    
                
            
            
            
    if resControle: # Si le contrôle est positif
        log += ">>> checked\n\n"
    else:
        log+="\n" # retour à la ligne   
    print(log)
    return resControle, log








def checkGroupesCanevasInParam(dictCanevas, dictParametres):
    
    """
    Checker sémantique pour vérifier que les nom de groupe saisis dans le canevas sont inscrits dans le fichier
    des paramètres.
    Permet également de détecter si les paramètres inconnus à calculer sont possibles (ex.: si pas le LH, alors 
    impossible de calculer des paramètres alti.)
    
    Parameters
    ----------
    dictCanevas : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    dictParametres : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    
    Returns
    -------
    checkGroupesCanevasInParam : bool
        Retourne si le fichier est ok ou non sur ces éléments sémantiques.
    log : str
        Retourne le log de cette fonction.
    
    """
    
    # Initialisation du LOG
    log = "CODE 202 : GROUP FROM NETWORK FILE FOUND IN PARAMETERS FILE\n"
    log+= (len(log)-1)*"-" + "\n"
    
    checkGroupesCanevasInParam = True # Initialisation du résultat True
    
    # Initialisation des groupes utiles (ceux rééelement utilisés, set de valeurs uniques)
    nomsGroupesUtilises = set()
    
    #### ------ POLAIRE ( 3 types de groupes)
    
    # Vérifier qu'il y a bien un levé polaire
    if 'polar' in dictCanevas['network'].keys():
        
        # Récupérer les noms de tous les types groupes pour levé polaire dans les paramètres de calcul
        listeNomsGroupesDistance = []
        listeNomsGroupesDirection = []
        listeNomsGroupesCentrage = []
        try:
            for groupeDist in dictParametres['parameters']['groups']['distanceGroups']['distanceGroup']:
                listeNomsGroupesDistance.append(groupeDist['distanceGroupName'])
            for groupeDir in dictParametres['parameters']['groups']['directionGroups']['directionGroup']:
                listeNomsGroupesDirection.append(groupeDir['directionGroupName'])
            for groupeCent in dictParametres['parameters']['groups']['centringGroups']['centringGroup']:
                listeNomsGroupesCentrage.append(groupeCent['centringGroupName'])
        except: # si pas de groupes dans les param.
            pass
        
        # rendre les valeurs uniques en "set"
        listeNomsGroupesDistance = set(listeNomsGroupesDistance)
        listeNomsGroupesDirection = set(listeNomsGroupesDirection)
        listeNomsGroupesCentrage = set(listeNomsGroupesCentrage)
        
        # Parcourir les stations
        listeStations = dictCanevas['network']['polar']['station']
        for station in listeStations:
            
            # Récupération des noms de groupes pour chaque station
            groupeDistance, groupeDirection, groupeCentrage = station['stationData']['distanceGroup'], station['stationData']['directionGroup'], station['stationData']['centringGroup']
            
            # Ajout au set de tous les noms de groupes 
            nomsGroupesUtilises.add(groupeDistance)
            nomsGroupesUtilises.add(groupeDirection)
            nomsGroupesUtilises.add(groupeCentrage)
            
            # Check de la présence dans la liste des groupes saisis dans les param
            if groupeDistance not in listeNomsGroupesDistance :
                # Print du message d'erreur si le nom de groupe n'est pas dans le XML des paramètres
                checkGroupesCanevasInParam = False
                log += ">>> ERROR 202.1 : DISTANCE GROUP MISSING : station: {:s}, with group: {:s}\n".format(station['stationName'], groupeDistance)
            if groupeDirection not in listeNomsGroupesDirection :
                # Print du message d'erreur si le nom de groupe n'est pas dans le XML des paramètres
                checkGroupesCanevasInParam = False
                log += ">>> ERROR 202.2 : DIRECTION GROUP MISSING : station: {:s}, with group: {:s}\n".format(station['stationName'], groupeDirection)
            if groupeCentrage not in listeNomsGroupesCentrage :
                # Print du message d'erreur si le nom de groupe n'est pas dans le XML des paramètres
                checkGroupesCanevasInParam = False
                log += ">>> ERROR 202.3 : CENTRING GROUP MISSING : station: {:s}, with group: {:s}\n".format(station['stationName'], groupeCentrage)
            
            
            
    #### ------ GNSS
    
    # Vérifier qu'il y a bien un relevé de session GNSS
    if 'gnss' in dictCanevas['network'].keys():
        
        # Récupérer les noms de tous les types groupes pour GNSS dans les paramètres de calcul
        listeNomsGroupesGNSS = []
        try:
            for groupe in dictParametres['parameters']['groups']['gnssGroups']['gnssGroup']:
                listeNomsGroupesGNSS.append(groupe['gnssGroupName'])
        except: # si aucun groupe GNSS dans les paramètres
            pass
            
        # rendre les valeurs uniques en "set"
        listeNomsGroupesGNSS = set(listeNomsGroupesGNSS)
        
        # Parcourir les sessions
        listeSessions = dictCanevas['network']['gnss']['session']
        for session in listeSessions:
            
            # Types d'obs. dans la session
            typesObs = []
            for observation in session['measure']:
                if "LY" in observation.keys() and "LX" in observation.keys() :
                    typesObs.append("LY")
                    typesObs.append("LX")
                if "LH" in observation.keys() :
                    typesObs.append("LH")
            typesObs = set(typesObs)

            
            # Récupération des noms de groupes pour chaque station
            groupeGNSS = session['gnssGroup']
            
            # Ajout au set de tous les noms de groupes 
            nomsGroupesUtilises.add(groupeGNSS)
            
            # Check de la présence dans la liste des groupes
            if groupeGNSS not in listeNomsGroupesGNSS :
                
                # Print du message d'erreur si le nom de groupe n'est pas dans le XML des paramètres
                checkGroupesCanevasInParam = False
                log += ">>> ERROR 202.4 : GNSS GROUP MISSING : session: {:s}, avec groupe: {:s}\n".format(session['sessionName'], groupeGNSS)
            
            try:
                # Check si une inconnues n'est pas calculable (Ex.: si "true" en param. alti. alors que pas de LH)
                for groupe in dictParametres['parameters']['groups']['gnssGroups']['gnssGroup']:
                    if groupeGNSS == groupe['gnssGroupName']:
                        if "LY" not in typesObs or "LY" not in typesObs: # si LY ou LX PAS dans les types, ne peut pas avoir une inc. plani
                            # Msg erreur pour plani
                            if groupe['unknownParameters']['Etranslation'] == "true":
                                checkGroupesCanevasInParam = False
                                log += ">>> ERROR 202.5 : GROUP GNSS : session: {:s}, with group : {:s}, CANNOT HAVE PLANIMETRIC UNKNOWNS\n".format(session['sessionName'], groupeGNSS)
                            if groupe['unknownParameters']['Ntranslation'] == "true":
                                checkGroupesCanevasInParam = False
                                log += ">>> ERROR 202.5 : GROUP GNSS : session: {:s}, with group : {:s}, CANNOT HAVE PLANIMETRIC UNKNOWNS\n".format(session['sessionName'], groupeGNSS)
                            if groupe['unknownParameters']['horizRotation'] == "true":
                                checkGroupesCanevasInParam = False
                                log += ">>> ERROR 202.5 : GROUP GNSS : session: {:s}, with group : {:s}, CANNOT HAVE PLANIMETRIC UNKNOWNS\n".format(session['sessionName'], groupeGNSS)
                            if groupe['unknownParameters']['horizScaleFactor'] == "true":
                                checkGroupesCanevasInParam = False
                                log += ">>> ERROR 202.5 : GROUP GNSS : session: {:s}, with group : {:s}, CANNOT HAVE PLANIMETRIC UNKNOWNS\n".format(session['sessionName'], groupeGNSS)
                        if "LH" not in typesObs : # si LY ou LX PAS dans les types, ne peut pas avoir une inc. plani
                            # Msg erreur pour plani
                            if groupe['unknownParameters']['Htranslation'] == "true":
                                checkGroupesCanevasInParam = False
                                log += ">>> ERROR 202.6 : GROUP GNSS : session: {:s}, with group : {:s}, CANNOT HAVE ALTIMETRIC UNKNOWNS\n".format(session['sessionName'], groupeGNSS)
            except:
                pass
                                    
                


    #### ------ SYSTEMES LOCAUX

    # Vérifier qu'il y a bien la balise des systèmes locaux
    if 'localSystems' in dictCanevas['network'].keys():
        
        # Récupérer les noms de tous les types groupes pour les cotes dans les paramètres de calcul
        listeNomsGroupesSystemeLocal = []
        try:
            for groupe in dictParametres['parameters']['groups']['localSystemGroups']['localSystemGroup']:
                listeNomsGroupesSystemeLocal.append(groupe['localSystemGroupName'])
        except: # si pas de groupe
            pass
        listeNomsGroupesSystemeLocal = set(listeNomsGroupesSystemeLocal) # rendre les valeurs uniques
        
        # Parcourir les systèmes locaux
        listeSystemesLocaux = dictCanevas['network']['localSystems']['localSystem']
        for systemeLocal in listeSystemesLocaux:
            
            # Types d'obs. du système local
            typesObs = []
            for observation in systemeLocal['measure']:
                if "LY" in observation.keys() and "LX" in observation.keys() :
                    typesObs.append("LY")
                    typesObs.append("LX")
                if "LH" in observation.keys():
                    typesObs.append("LH")
            typesObs = set(typesObs)
            
            # Récupérer les noms de groupes pour chaque système local
            groupeSystemeLocal = systemeLocal['localSystemGroup']
            
            # Ajout au set de tous les noms de groupes 
            nomsGroupesUtilises.add(groupeSystemeLocal)
            
            # Check de la présence dans la liste des groupes
            if groupeSystemeLocal not in listeNomsGroupesSystemeLocal:
                # Print du message d'erreur si le nom du groupe n'est pas dans le XML des paramètres
                checkGroupesCanevasInParam = False
                log += ">>> ERROR 202.7 : LOCAL SYSTEM GROUP MISSING : local system: {:s}, with group: {:s}\n".format(systemeLocal['localSystemName'], groupeSystemeLocal)
            
            try:
                # Check si une inconnues n'est pas calculable (Ex.: si "true" en param. alti. alors que pas de LH)
                for groupe in dictParametres['parameters']['groups']['localSystemGroups']['localSystemGroup']:
                    if groupeSystemeLocal == groupe['localSystemGroupName']:
                        if "LY" not in typesObs or "LY" not in typesObs: # si LY ou LX PAS dans les types, ne peut pas avoir une inc. plani
                            # Msg erreur pour plani
                            if groupe['unknownParameters']['horizScaleFactor'] == "true":
                                checkGroupesCanevasInParam = False
                                log += ">>> ERROR 202.8 : LOCAL SYSTEM GROUP : local system: {:s}, with group: {:s}, CANNOT HAVE PLANIMETRIC UNKNOWNS\n".format(systemeLocal['localSystemName'], groupeSystemeLocal)
            except:
                pass
                


    #### ------ COTES
    
    # Vérifier qu'il y a bien un relevé de cotes
    if 'simpleMeasures' in dictCanevas['network'].keys():
        
        # Récupérer les noms de tous les types groupes pour les cotes dans les paramètres de calcul
        listeNomsGroupesCote = []
        try:
            for groupe in dictParametres['parameters']['groups']['simpleMeasureGroups']['simpleMeasureGroup']:
                listeNomsGroupesCote.append(groupe['simpleMeasureGroupName'])
        except:
            pass
        listeNomsGroupesCote = set(listeNomsGroupesCote) # rendre les valeurs uniques
        
        # Parcourir les cotes
        listeCotes = dictCanevas['network']['simpleMeasures']['simpleMeasure']
        for cote in listeCotes:
            
            # Récupération les noms de groupes pour chaque cote
            groupeCote = cote['simpleMeasureGroup']
            
            # Ajout au set de tous les noms de groupes 
            nomsGroupesUtilises.add(groupeCote)
            
            # Check de la présence dans la liste des groupes
            if groupeCote not in listeNomsGroupesCote :
                # Print du message d'erreur si le nom du groupe n'est pas dans le XML des paramètres
                checkGroupesCanevasInParam = False
                log += ">>> ERROR 202.10 : SIMPLE MEASURE GROUP MISSING : point1: {:s} to point2: {:s}, with group: {:s}\n".format(cote['measure']['pointName1'], cote['measure']['pointName2'], groupeCote )
    

    if checkGroupesCanevasInParam: # Si le contrôle est positif
        log += ">>> checked\n\n"
    else:
        log+="\n" # retour à la ligne   .
        
        
        
    #### Suppression des groupes inutilisés
    dictParametres = deleteUselessGroupsFromParameters(dictParametres, list(nomsGroupesUtilises))
    
    print(log)    
    return checkGroupesCanevasInParam, log, dictParametres




def deleteUselessGroupsFromParameters(dictParametres, nomsGroupesUtilises):
    
    """
    Suppression des groupes inutilisés (p.ex. si fichier paramètre repris par défaut et non-épuré). 
    N'écrase pas le fichier XML des paramètres en input (simplement le dictionnaire pour éviter les conflits)
    
    Parameters
    ----------
    dictParametres : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    nomsGroupesUtilises : set
        Contient les noms de tous les groupes rééllement utilisés dans les obs.
    
    Returns
    -------
    dictParametresOut : dict
        Paramètres épurés
    
    """
    
    # Copie pour écraser
    dictParametresOut = copy.deepcopy(dictParametres)
    
    
    # Tester si les groupes dans les paramètres sont pas utilisé -> suppression
    # Pour chaque type de groupe
    
    if 'distanceGroups' in dictParametres['parameters']['groups'].keys():
        for groupeDist in dictParametres['parameters']['groups']['distanceGroups']['distanceGroup']:
            if groupeDist['distanceGroupName'] not in nomsGroupesUtilises:
                dictParametresOut['parameters']['groups']['distanceGroups']['distanceGroup'].remove(groupeDist)
    
    if 'directionGroups' in dictParametres['parameters']['groups'].keys():
        for groupeDir in dictParametres['parameters']['groups']['directionGroups']['directionGroup']:
            if groupeDir['directionGroupName'] not in nomsGroupesUtilises:       
                dictParametresOut['parameters']['groups']['directionGroups']['directionGroup'].remove(groupeDir)
        
    if 'centringGroups' in dictParametres['parameters']['groups'].keys():
        for groupeCent in dictParametres['parameters']['groups']['centringGroups']['centringGroup']:
            if groupeCent['centringGroupName'] not in nomsGroupesUtilises: 
                dictParametresOut['parameters']['groups']['centringGroups']['centringGroup'].remove(groupeCent)
        
    if 'gnssGroups' in dictParametres['parameters']['groups'].keys(): 
        for groupeGNSS in dictParametres['parameters']['groups']['gnssGroups']['gnssGroup']:
            if groupeGNSS['gnssGroupName'] not in nomsGroupesUtilises:
                dictParametresOut['parameters']['groups']['gnssGroups']['gnssGroup'].remove(groupeGNSS)
                
    if 'localSystemGroups' in dictParametres['parameters']['groups'].keys():
        for groupeSysLoc in dictParametres['parameters']['groups']['localSystemGroups']['localSystemGroup']:
            if groupeSysLoc['localSystemGroupName'] not in nomsGroupesUtilises:
                dictParametresOut['parameters']['groups']['localSystemGroups']['localSystemGroup'].remove(groupeSysLoc)
        
    if 'simpleMeasureGroups' in dictParametres['parameters']['groups'].keys():
        for groupeCote in dictParametres['parameters']['groups']['simpleMeasureGroups']['simpleMeasureGroup']:
            if groupeCote['simpleMeasureGroupName'] not in nomsGroupesUtilises:
                dictParametresOut['parameters']['groups']['simpleMeasureGroups']['simpleMeasureGroup'].remove(groupeCote)
                
    
    # Retourner pour redéfinition
    return dictParametresOut


def checkDatumInPoints(dictParametres, dictPoints):
    
    """
    Checker sémantique pour vérifier que les points fixes planimétriques et altimétriques se trouvent bien dans le dictPoint.
    
    Parameters
    ----------
    dictCanevas : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    dictParametres : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    
    Returns
    -------
    checkGroupesCanevasInParam : bool
        Retourne si le fichier est ok ou non sur ces éléments sémantiques.
    log : str
        Retourne le log de cette fonction.
    
    """
    
    # Initialisation du LOG
    log = "CODE 203 : CONTROL POINTS (DATUM) FROM PARAMETERS FILE FOUND IN POINTS FILE\n"
    log+= (len(log)-1)*"-" + "\n"
    
    checkDatumInPoints = True # Initialisation
    
    # Dimension de calcul
    dimensionCalcul = dictParametres['parameters']['computationOptions']['calculationDimension']
    
    # Selon dimension, ici planimétrie
    if dimensionCalcul == "2D" or dimensionCalcul == "2D+1":
        
        # Check qu'il y ait bien la balise des PF plani
        if 'planimetricControlPoints'  in dictParametres['parameters'].keys():
        
            # Parcourir la liste des PF plani
            listePointsFixesPlani = dictParametres['parameters']['planimetricControlPoints']['point']
            for point in listePointsFixesPlani:
                
                # rechercher le point dans le dictPoint, si il arrive pas, le point n'y est pas
                presencePoint = rechercheUtils.rechercheNoPt(dictPoints, point['pointName'])
                if presencePoint == None: # si échec du test, msg erreur
                    checkDatumInPoints = False
                    log += ">>> ERROR 203.3 : PLANIMETRIC CONTROL POINT MISSING : {:s}\n".format(point['pointName'])
                    
                    
        else: # Si il manque la balise des PF plani
            checkDatumInPoints = False
            log += "ERROR 203.1 : ELEMENT <pointsFixesPlani> MISSING IN PARAMETERS FILE\n"
            

    # Selon dimension, ici altimétrie
    if dimensionCalcul == "1D" or dimensionCalcul == "2D+1":
        
        # Check qu'il y ait bien la balise des PF alti
        if 'altimetricControlPoints' in dictParametres['parameters'].keys():
        
            # Parcourir la liste des PF alti
            listePointsFixesAlti = dictParametres['parameters']['altimetricControlPoints']['point']
            for point in listePointsFixesAlti:
                
                # rechercher le point dans le dictPoint, si il arrive pas, le point n'y est pas
                presencePoint = rechercheUtils.rechercheNoPt(dictPoints, point['pointName'])
                if presencePoint == None: # si échec du test, msg erreur
                    checkDatumInPoints = False
                    log += ">>> ERROR 203.4 : ALTIMETRIC CONTROL POINT MISSING : {:s}\n".format(point['pointName'])
                    
                # si le point existe, check si il y'a bien une altitude H, sinon échec du ctrl et msg erreur
                else: 
                    if presencePoint['H'] == None:
                        checkDatumInPoints = False
                        log += ">>> ERROR 203.5 : ALTIMETRIC CONTROL POINT IS MISSING AN ALTITUDE H : {:s}\n".format(point['pointName'])
    
        else: # Si il manque la balise des PF alti
            checkDatumInPoints = False
            log += ">>> ERROR 203.2 : ELEMENT <pointsFixesAlti> MISSING IN PARAMETERS FILE\n"
    
    
    if checkDatumInPoints: # Si le contrôle est positif
        log += ">>> checked\n\n"
    else:
        log+="\n" # retour à la ligne   
    print(log)
    return checkDatumInPoints, log






def checkGeometrieGNSS(dictCanevas, dictPoints):
    
    """
    Checker géométrique pour vérifier si les mesures GNSS globales sont à moins de 50cm des coordonnées approchées du point concerné.
    Cela permet d'écarter les grosses incohérance avant la compensation.
    Reporte les éventuels problèmes dans la console/log.
    A utiliser après validation canevasInPoints.
    
    Parameters
    ----------
    dictCanevas : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    dictPoint : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    
    Returns
    -------
    checkGNSSCoord : bool
        Retourne si le fichier est ok ou non sur ces éléments géométriques.
    log : str
        Retourne le log de cette fonction.
    
    """
    
    # Initialisation du LOG
    log = "CODE 300 : GEOMETRIC CHECK OF GNSS GLOBAL SURVEY WITH POINTS FILE COORDINATES\n"
    log+= (len(log)-1)*"-" + "\n"
    
    checkGNSSCoord = True # Initialisation
    
    
    # Vérifier qu'il y a bien un relevé de session GNSS 
    if 'gnss' in dictCanevas['network'].keys():
    
        
        # Liste de toutes les objets session
        listeSessions = dictCanevas['network']['gnss']['session']
        for session in listeSessions:
            
            # Parcourir le stationnement et get les No de pts visés dans les obs.
            listeObservations = session['measure']
        
            for observation in listeObservations:
                
                # faire le contrôle seulement si il y'a des observations 2D
                if "LY" in observation.keys() and "LX" in observation.keys() :
                    
                    # si une des LY, LX (ou les deux) est écarté, ne pas le checker
                    ecarteLY, ecarteLX = observation['LY']['discarded'], observation['LX']['discarded']
                    
                    # Contrôle grossier des coordonnées à ~0.5cm 
                    point = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                    Ep, Np =  float(point['E']), float(point['N'])
                    LY, LX = float(observation['LY']['value']), float(observation['LX']['value'])
                    
                    if abs(Ep-LY) > 0.5 and ecarteLY in ['false', None]: # uniquement si non-écarté
                        checkGNSSCoord = False
                        log += ">>> ERROR 300.1 : GEOMETRIC CONSTITENCY LY GNSS : session: {:s} on target: {:s}, diff.= {:0.3f}m\n".format(session['sessionName'], observation['pointName'], Ep-LY)
                    
                    if abs(Np-LX) > 0.5 and ecarteLX in ['false', None]: # uniquement si non-écarté
                        checkGNSSCoord = False
                        log += ">>> ERROR 300.2 : GEOMETRIC CONSTITENCY LX GNSS : session: {:s} on target: {:s}, delta= {:0.3f}m\n".format(session['sessionName'], observation['pointName'], Np-LX)
                        
                    # Try dans le cas où il n'y a pas d'altitude au point ou de LH
                    try : 
                        Hp = float(point['H'])
                        LH = float(observation['LH']['value'])
                        ecarteLH = observation['LH']['discarded']
                        if abs(Hp-LH) > 0.5 and ecarteLH in ['false', None]: # uniquement si non-écarté
                            checkGNSSCoord = False
                            log += ">>> ERROR 300.3 : GEOMETRIC CONSTITENCY LH GNSS : session: {:s} on target: {:s}, delta= {:0.3f}m\n".format(session['sessionName'], observation['pointName'], Hp-LH)
                    except:
                        pass
                           
    
        if checkGNSSCoord: # Si le contrôle est positif
            log += ">>> checked\n\n"
        else:
            log+="\n" # retour à la ligne 
    
    else: # pas de relevé GNSS = contrôle validé
        log += ">>> checked (no GNSS sessions)\n\n"
      
    print(log)
    return checkGNSSCoord, log
        




def checkGeometrieDistancesPolaire(dictCanevas, dictPoints):
    
    """
    Checker géométrique pour vérifier si les mesures de distances (dans plan proj. et corrigées des déplacements) issues d'un levé polaire sont correctes à 0.5m près (par rapport aux coordonnées approchées).
    Fonctionne uniquement si DS n'est pas écarté.
    Cela permet d'écarter les grosses incohérance avant la compensation.
    Reporte les éventuels problèmes dans la console/log.
    A utiliser après validation canevasInPoints.
    
    Parameters
    ----------
    dictCanevas : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    dictPoint : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    
    Returns
    -------
    checkDistCoord : bool
        Retourne si le fichier est ok ou non sur ces éléments géométriques.
    log : str
        Retourne le log de cette fonction.
    
    """
    
    # Initialisation du LOG
    log = "CODE 301 : GEOMETRIC CHECK OF DISTANCES IN MAP PROJECTION WITH POINTS FILE COORDINATES\n"
    log+= (len(log)-1)*"-" + "\n"
    
    checkDistCoord = True # Initialisation
    
    
    # Vérifier qu'il y a bien un levé polaire
    if 'polar' in dictCanevas['network'].keys():
        
        # Liste de toutes les objets station
        listeStations = dictCanevas['network']['polar']['station']
        
        for station in listeStations:
            
            # Parcourir le stationnement et get le noSta
            listeObservations = station['stationData']['measure']
            noSta = station['stationName']
            
            # Pour chaque observation
            for observation in listeObservations:
                
                # Si DS est ecarté, ne fait pas ce check. (si ZD est écarté mais pas DP, on check DP quand même)
                ecarteDS = observation['DS']['discarded']
                if ecarteDS in ['false', None]:
                
                    # Chercher les coordonnées approchées de noSta et noPt dans dictPoints
                    noPt = observation['pointName']
                    pointSta = rechercheUtils.rechercheNoPt(dictPoints, noSta)
                    pointVis = rechercheUtils.rechercheNoPt(dictPoints, noPt)
                    
                    # Récupérer les coordonnées et réduire la distance dans le plan proj. avec correction dm1/dm2
                    Esta, Nsta = float(pointSta['E']), float(pointSta['N'])
                    Evis, Nvis = float(pointVis['E']), float(pointVis['N'])
                    DS, RI, ZD, dm1, dm2 = observation['DS']['value'], observation['RI']['value'], observation['ZD']['value'], observation['dm1']['value'], observation['dm2']['value']
                    DP = geometrieUtils.reductionDistancePlanProj(float(DS), float(ZD), float(Nsta), 500.0) # valeur Hab moy. générique (ordre de grandeur = 1m -> ok)
                    
                    # si vides: dm1 et dm2= 0.0
                    if dm1 == None : 
                        dm1 = 0.0
                    if dm2 == None :
                        dm2 = 0.0
                    
                    # Correction des déplacements
                    RIcorr, DPcorr = geometrieUtils.corrAvecDepl(float(RI), DP, float(dm1), float(dm2))
                    # Dist. issues des coordonnées approchées
                    DPapproch = math.sqrt((Esta-Evis)**2+(Nsta-Nvis)**2)
                    
                    # Comparaison avec dist. issue des coordonnées approchées
                    if abs(DPapproch-DPcorr) > 0.5 :
                        checkDistCoord = False
                        log += ">>> ERROR 301.1 : GEOMETRIC CONSTITENCY OF DISTANCE IN MAP PROJECTION : station: {:s} to target {:s}, with incl.dist={:0.3f}m, delta.={:0.3f}m\n".format(noSta, observation['pointName'], float(DS), DPapproch-DPcorr)
              
                
        if checkDistCoord: # Si le contrôle est positif
            log += ">>> checked\n\n"     
        else:
            log+="\n" # retour à la ligne 
            
    else: # pas de levé polaire = contrôle validé
        log += ">>> checked (no polar survey)\n\n" 
        
    print(log)
    return checkDistCoord, log


def checkGeometrieDirectionsPolaire(dictCanevas, dictPoints):
    
    """
    Checker géométrique pour vérifier si les mesures de direction (corrigées des déplacements) issues d'un levé polaire sont correctes grossièrement
    (par rapport aux coordonnées approchées). L'écart-type pour compraison est calculé à chaque observation (si la première est fausse, alors toutes seront impactées)
    Fonctionne uniquement si RI n'est pas écarté.
    Cela permet d'écarter les grosses incohérance avant la compensation.
    Reporte les éventuels problèmes dans la console/log.
    A utiliser après validation canevasInPoints.
    
    Parameters
    ----------
    dictCanevas : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    dictPoint : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    
    Returns
    -------
    checkDirCoord : bool
        Retourne si le fichier est ok ou non sur ces éléments géométriques.
    log : str
        Retourne le log de cette fonction.
    
    """
    
    # Initialisation du LOG
    log = "CODE 302 : GEOMETRIC CHECK OF DIRECTIONS WITH POINTS FILE COORDINATES\n"
    log+= (len(log)-1)*"-" + "\n"
    
    checkDirCoord = True # Initialisation
    
    # Vérifier qu'il y a bien un levé polaire
    if 'polar' in dictCanevas['network'].keys():
        
        # Liste de toutes les objets station
        listeStations = dictCanevas['network']['polar']['station']
        
        for station in listeStations:
            
            # Parcourir le stationnement et get le noSta
            listeObservations = station['stationData']['measure']
            noSta = station['stationName']
            listeIncOriParVisee = [] # liste des inc. ori par visée pour en tirer la moyenne pour ensuite comparer
            listeObsNonEcartees = [] # Liste des RI corrigés de dm1 et dm2 pour comparaison ensuite (dans une autre boucle)
            
            # Pour chaque observation, calcul de l'inc. ori. pour obtenir la moyenne
            for observation in listeObservations:
                
                # Si RI est ecarté, ne fait pas ce check. 
                ecarteRI = observation['RI']['discarded']
                if ecarteRI in ['false', None]:
                    
                    # Chercher les coordonnées approchées de noSta et noPt dans dictPoints
                    noPt = observation['pointName']
                    pointSta = rechercheUtils.rechercheNoPt(dictPoints, noSta)
                    pointVis = rechercheUtils.rechercheNoPt(dictPoints, noPt)
                    
                    # Récupérer les coordonnées et réduire la distance dans le plan proj. avec correction dm1/dm2
                    Esta, Nsta = float(pointSta['E']), float(pointSta['N'])
                    Evis, Nvis = float(pointVis['E']), float(pointVis['N'])
                    DS, RI, ZD, dm1, dm2 = observation['DS']['value'], observation['RI']['value'], observation['ZD']['value'], observation['dm1']['value'], observation['dm2']['value']
                    DP = geometrieUtils.reductionDistancePlanProj(float(DS), float(ZD), float(Nsta), 500.0) # valeur Hab moy. générique (ordre de grandeur = 1m -> ok)
                    distCoord = ((Esta-Evis)**2 + (Nsta - Nvis)**2)**0.5
                    
                    # si vides: dm1 et dm2 = 0.0
                    if dm1 == None : 
                        dm1 = 0.0
                    if dm2 == None :
                        dm2 = 0.0
                    
                    # Correction des déplacements
                    RIcorr, DPcorr = geometrieUtils.corrAvecDepl(float(RI), DP, float(dm1), float(dm2))
                    
                    # Calcul de l'inconnue d'ori. pour chaque visée et stockage pour validation
                    incOri = geometrieUtils.incOriFromCoord(Esta ,Nsta, Evis, Nvis, RIcorr)
                    # Si l'inconnue ori. est dans le 3e cadran (proche de 400.0), lui soustaire 400.0
                    if incOri > 300.0 and incOri < 400.0:
                        incOri -= 400.0
                    # on met à jour les listes pour le calcul des écarts à la moyenne
                    listeIncOriParVisee.append([incOri, distCoord])
                    listeObsNonEcartees.append(observation)
                    
            
            # Calcul de la médiane (robuste) de l'inc. ori. de la station
            moyIncOri = np.median(list(list(zip(*listeIncOriParVisee))[0]))
            
            # On reparcours les obs. de la station pour calculer les écarts à la moyenne
            for i, observation in enumerate(listeObsNonEcartees):
                
                # écart à la moyenne par obs. et écart latéral avec la distance sur les coord.
                ecartAlaMoy, distCoord = moyIncOri - listeIncOriParVisee[i][0] , listeIncOriParVisee[i][1]
                viLat = np.sin(ecartAlaMoy*np.pi/200.0) * distCoord
                
                # test si écart à la moyenne > 1 grade
                if abs(viLat) > 0.5:
                    # échec du test et msg erreur
                    checkDirCoord = False
                    log += ">>> ERROR 302.1 : GEOMETRIC CONSTITENCY OF DIRECTION : station: {:s} to target {:s}, with RI={:0.4f}g, delta orient.unkn.={:0.4f}g, lat.={:0.3f}m\n".format(noSta, observation['pointName'], float(observation['RI']['value']), ecartAlaMoy, viLat)
              
                
        if checkDirCoord: # Si le contrôle est positif
            log += ">>> checked\n\n"    
        else:
            log+="\n" # retour à la ligne

    else: # pas de levé polaire = contrôle validé
        log += ">>> checked (no polar survey)\n\n" 
        
    print(log)
    return checkDirCoord, log
    
    
    
    


def checkGeometrieSystemesLocaux(dictCanevas, dictPoints):
    
    """
    Checker géométrique pour vérifier si les distances entre le premier point (à ne pas écarter) et le reste des systèmes locaux sont à 0.5 m près (par rapport aux coordonnées approchées).
    Cela permet d'écarter les grosses incohérance avant la compensation.
    Calcule également le E et N global du premier point pour stabiliser le calcul des translations.
    Reporte les éventuels problèmes dans la console/log.
    A utiliser après validation canevasInPoints.
    
    Parameters
    ----------
    dictCanevas : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    dictPoint : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    
    Returns
    -------
    checkGeomSystemesLocaux : bool
        Retourne si le fichier est ok ou non sur ces éléments géométriques.
    log : str
        Retourne le log de cette fonction.
    
    """
    
    # Initialisation du LOG
    log = "CODE 303 : GEOMETRIC CHECK OF DISTANCES BETWEEN POINTS IN A LOCAL SYSTEM WITH POINTS FILE COORDINATES\n"
    log+= (len(log)-1)*"-" + "\n"
    
    checkGeometrieSystemesLocaux = True # Initialisation
    
    # Vérifier qu'il y a bien au moins un système local
    if 'localSystems' in dictCanevas['network'].keys():
        
        # Parcourir tous les sys. locaux XML
        listeSystemesLocaux = dictCanevas['network']['localSystems']['localSystem']
        for systemeLocal in listeSystemesLocaux:
            
            # Distance entre le premier point et tous les autres à contrôler
            premierPointYX = systemeLocal['measure'][0]
            premierPointEN = rechercheUtils.rechercheNoPt(dictPoints, premierPointYX['pointName'])
            
            
            # Parcourir les autres points dès le 2e jusq'au dernier compris
            for observation in systemeLocal['measure'][1:]:
                
                # faire le contrôle seulement si il y'a des observations 2D
                if "LY" in observation.keys() and "LX" in observation.keys() :
                
                    # Si LY ou LX est ecarté, ne fait pas ce check. (le premier point est gardé pour comparaison dans tous les cas)
                    ecarteLY, ecarteLX = observation['LY']['discarded'], observation['LX']['discarded']
                    if ecarteLY in ['false', None]  and ecarteLX in ['false', None]:
                        
                        # Récupération des éléments yx et EN
                        pointYX = observation
                        pointEN = rechercheUtils.rechercheNoPt(dictPoints, pointYX['pointName'])
                        
                        # Calcul des distances YX et EN par rapport au premier point
                        distYX = math.sqrt( (float(pointYX['LY']['value'])-float(premierPointYX['LY']['value']))**2  +  (float(pointYX['LX']['value'])-float(premierPointYX['LX']['value']))**2   )
                        distEN = math.sqrt( (float(pointEN['E'])-float(premierPointEN['E']))**2  +  (float(pointEN['N'])-float(premierPointEN['N']))**2   )
                        
                        # Si la différence > 0.5m, échec du contrôle et msg erreur
                        if abs(distEN-distYX) > 0.5 :
                            checkGeometrieSystemesLocaux = False 
                            log += ">>> ERROR 303.1 : GEOMETRIC CONSTITENCY OF DISTANCE : local system: {:s} : between target {:s} and target {:s}, delta={:0.3f}m\n".format(systemeLocal['localSystemName'],premierPointYX['pointName'],pointYX['pointName'], distEN-distYX )
        
        if checkGeometrieSystemesLocaux: # Si le contrôle est positif
            log += ">>> checked\n\n"    
        else:
            log+="\n" # retour à la ligne
    
    else: # pas de systèmes locaux = contrôle validé
        log += ">>> checked (no local systems)\n\n" 
        
    print(log)
    return checkGeometrieSystemesLocaux, log
    




def checkGeometrieCotes(dictCanevas, dictPoints):
    
    """
    Checker géométrique pour vérifier si les cotes (dans plan proj.) à 0.5m près (par rapport aux coordonnées approchées).
    Fonctionne uniquement si DS n'est pas écarté.
    Cela permet d'écarter les grosses incohérance avant la compensation.
    Reporte les éventuels problèmes dans la console/log.
    A utiliser après validation canevasInPoints.
    
    Parameters
    ----------
    dictCanevas : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    dictPoint : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    
    Returns
    -------
    checkGeomCotes : bool
        Retourne si le fichier est ok ou non sur ces éléments géométriques.
    log : str
        Retourne le log de cette fonction.
    
    """
    
    # Initialisation du LOG
    log = "CODE 304 : GEOMETRIC CHECK OF SIMPLE MEASURE WITH POINTS FILE COORDINATES\n"
    log+= (len(log)-1)*"-" + "\n"
    
    checkGeomCotes = True # Initialisation
    
    # Vérifier qu'il y a bien des cotes
    if 'simpleMeasures' in dictCanevas['network'].keys():
    
        # Liste de toutes les objets cote
        listeCotes = dictCanevas['network']['simpleMeasures']['simpleMeasure']
        
        for cote in listeCotes:
            
            # faire le contrôle seulement si il y'a des observations 2D
            if "DP" in cote['measure'].keys():
            
                numeroPoint1, numeroPoint2, valCote = cote['measure']['pointName1'], cote['measure']['pointName2'], float(cote['measure']['DP']['value'])
                point1, point2  = rechercheUtils.rechercheNoPt(dictPoints, numeroPoint1), rechercheUtils.rechercheNoPt(dictPoints, numeroPoint2)
                 
                # Récupérer les E,N des points issus des coordonnées approchées
                E1pt, N1pt, E2pt, N2pt = float(point1['E']), float(point1['N']), float(point2['E']), float(point2['N'])
                distEntrePts = math.sqrt((E1pt-E2pt)**2+(N1pt-N2pt)**2)
                
                # Si DP écarté, ne pas prendre en compte
                ecarteDP = cote['measure']['DP']['discarded']
                if ecarteDP in ['false', None]:
                
                    # Différences > 0.5 m
                    if abs(distEntrePts-valCote) > 0.5 :
                        checkGeomCotes = False
                        log += ">>> ERROR 304.1 : GEOMETRIC CONSTITENCY OF SIMPLE MEASURE : point1 : {:s} to point2 {:s}, with DP={:0.3f}m, delta={:0.3f}m\n".format(numeroPoint1, numeroPoint2, float(valCote), distEntrePts-valCote)
                    
                    
        if checkGeomCotes: # Si le contrôle est positif
            log += ">>> checked\n\n"      
        else:
            log+="\n" # retour à la ligne 
            
    else: # pas de cotes = contrôle validé
        log += ">>> checked (no simple measures)\n\n" 
        
    print(log)
    return checkGeomCotes, log


def checkGeometrieContraintes(dictCanevas, dictPoints):
    """
    Checker géométrique pour vérifier si les contraintes (perpenduclaire et alignement) ne sont pas grossièrement fausses avec les
    coordonnées approchées.
    Fonctionne uniquement si la contrainte n'est pas écartée.
    Cela permet d'écarter les grosses incohérance avant la compensation.
    Reporte les éventuels problèmes dans la console/log.
    A utiliser après validation canevasInPoints.
    
    Parameters
    ----------
    dictCanevas : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    dictPoint : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    
    Returns
    -------
    checkGeomeContraintes : bool
        Retourne si le fichier est ok ou non sur ces éléments géométriques.
    log : str
        Retourne le log de cette fonction.
    
    """
    
    # Initialisation du LOG
    log = "CODE 305 : GEOMETRIC CHECK OF CONSTRAINTS WITH POINTS FILE COORDINATES\n"
    log+= (len(log)-1)*"-" + "\n"
    
    checkGeomeContraintes = True # Initialisation
    
    # Vérifier qu'il y a bien des cotes
    if 'constraints' in dictCanevas['network'].keys():
        
        for contrainte in dictCanevas['network']['constraints']['constraint']:
            

            if contrainte['discarded'] in ['false', None]:
                # Récupération des éléments selon le role de chacun des points concernés par la contrainte
                for pt in contrainte['point']:
                    if pt['pointTypeInConstraint'] == "A":
                        noPtA = pt['pointName']
                    if pt['pointTypeInConstraint'] == "B":
                        noPtB = pt['pointName']
                    if pt['pointTypeInConstraint'] == "P":
                        noPtP = pt['pointName']
                    
                pointA = rechercheUtils.rechercheNoPt(dictPoints, noPtA)
                pA = np.array([float(pointA['E']), float(pointA['N'])])
                pointB = rechercheUtils.rechercheNoPt(dictPoints, noPtB)
                pB = np.array([float(pointB['E']), float(pointB['N'])])
                pointP = rechercheUtils.rechercheNoPt(dictPoints, noPtP)
                pP = np.array([float(pointP['E']), float(pointP['N'])])
                
                typeContrainte = contrainte['constraintType']
                dm1 = contrainte['dm1']['value']
                if dm1 == None:
                    dm1 = 0.0
                else:
                    dm1 = float(dm1)

                if typeContrainte == 'alignment':
                    
                    # Calcul de la distance de P à la droite AB
                    distApprochee = np.linalg.norm(np.cross(pB-pA, pA-pP))/np.linalg.norm(pB-pA)
                    # Valeur absolue de la différence entre dm1 et la distance approchée
                    if abs(distApprochee-abs(dm1)) > 0.5: # faute sur supérieur à 0.5m 
                        delta = distApprochee-abs(dm1)
                        checkGeomeContraintes = False
                        log += ">>> ERROR 305.1 : GEOMETRIC CONSTITENCY OF ALIGN. CONSTRAINT : ptA: {:s}, ptB: {:s}, ptP: {:s} with distance to alignment (includes dm1)={:0.3f}m, delta={:0.3f}m\n".format(noPtA, noPtB, noPtP, distApprochee, delta)
                
                if typeContrainte == 'perpendicular':
                    # calcul de l'angle entre 2 vecteurs
                    v1, v2 = pA-pP, pP-pB
                    normev1, normev2 = np.linalg.norm(v1), np.linalg.norm(v2)

                    if normev1*normev2 > 0.001: # si v2 ou v1 est si petit qu'il génère des instabilité de calcul
                        thetaApproch = np.arccos(np.dot(v1,v2) / (normev1*normev2)) * 200.0/np.pi
                    else:
                        thetaApproch = 100.0
                    if abs(thetaApproch-100.0) > 5 and normev1 > 2.0 and normev2 > 2.0: # faute si supérieur à 5 grades et les normes v1 et v2 supérieur à 1m (si trop proche, l'angle n'est pas représentatif)
                        delta = abs(thetaApproch-100.0)
                        checkGeomeContraintes = False
                        log += ">>> ERROR 305.2 : GEOMETRIC CONSTITENCY OF PERP. CONSTRAINT : ptA: {:s}, ptB: {:s}, ptP: {:s} with angle between PA and PB = {:0.3f}g, delta={:0.3f}g\n".format(noPtA, noPtB, noPtP, thetaApproch, delta)
                        
        
        if checkGeomeContraintes: # Si le contrôle est positif
            log += ">>> checked\n\n"      
        else:
            log+="\n" # retour à la ligne 
    
    else: # pas de cotes = contrôle validé
        log += ">>> checked (no constraints)\n\n"

    print(log)
    return checkGeomeContraintes, log 
    
    
    
    
    
    
def denombrementElementsPlaniAlti(dictCanevas, dictPoints, dictParametres):
    
    """
    Fonction pour compter les éléments de détermination (non-écartés) de chaque point en planimétrie ET en altimétrie (indépendemment).
    Les attributs "elemsPlani" et "elemsAlti" sont ajouté au dictionnaire de chaque point pour entrer ensuite dans la compensation.
    Ces éléments permettront au moteur de calcul de selectionner les points à ajouter au vecteur des inconnues.
    Contrôle également que chaque point fixe possède des éléments de détermination (renvoie False si pas suffisant).
    Contrôle supplémentaire des éléments plani. sur les points communs des systèmes locaux (renvoie False sinon).
    
    Parameters
    ----------
    dictCanevas : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    dictPoints : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    dictParametres : dictionnaire
        Après lecture d'un fichier XML et validé avec XSD
    
    Returns
    -------
    denombrementElementsPlaniAlti : bool 
        Retourne False uniquement :
            - si il n'y a pas de point dans le dictPoint.
            - que un des PF n'a pas assez de détermination.
            - si un système local est indeterminé.
    log : str
        Retourne le log de cette fonction.
    
    """
    
    # Initialisation du LOG
    log = "CODE 400 : COUNTING AND CHECK OF PLANIMETRIC AND ALTIMETRIC ELEMENTS\n"
    log+= (len(log)-1)*"-" + "\n"
    
    denombrementElementsPlaniAlti = True # Initialisation
    
    # Dimension de calcul
    dimensionCalcul = dictParametres['parameters']['computationOptions']['calculationDimension']

    
    # dictPoint avec un compteur à 0 pour chaque point (pour y ajouter le nb d'éléments plani. et alti.)
    listePoints = dictPoints['points']['point']
    
    for point in listePoints:
        point.update({'planimetricElems': 0})
        point.update({'altimetricElems': 0})
    
    # Dénombrer le réseau et apposer les index (places dans les matrices)
    nbObsTotalesPlani = 0
    nbObsTotalesAlti = 0
    nbContraintes = 0
    nbInconnuesPlani = 0
    nbInconnuesAlti = 0
    

     #----------------
#### # --- CANEVAS ---
     #----------------
     
    # Si il n'y a pas de balises principales dans le canevas -> résultat = None
    if len(dictCanevas['network'].keys()) < 1:
       denombrementElementsPlaniAlti = False 
       log += ">>> ERROR 400.1 : DATA MISSING IN NETWORK FILE"
       
       
       
    #### ------ POLAIRE
    
    # Vérifier qu'il y a bien un levé polaire
    if 'polar' in dictCanevas['network'].keys():
        
        # Parcourir les groupes des paramètres et ajouter +1 au compteur à chaque inconnue suppl. plani ou alti.(true/false)
        for groupeDist in dictParametres['parameters']['groups']['distanceGroups']['distanceGroup']:
            
            # test et incrément au compteur
            if groupeDist['additionalUnknowns']['scaleFactor'] == "true":
                nbInconnuesPlani += 1
            if groupeDist['additionalUnknowns']['additionConstant'] == "true":
                nbInconnuesPlani += 1
                
        
        # Liste de toutes les objets station
        listeStations = dictCanevas['network']['polar']['station']
        for station in listeStations:
            
            # Ajouter +X au numéro de station (X étant le nombre d'élém. plani. ou alti. "donné" aux points visés de la station) -> au minim 3 élém (pour E,N,w)
            nbElemPlaniStation = 0
            nbElemAltiStation = 0
            
            # Inconnue d'orientation fait +1 inc. à chaque station
            nbInconnuesPlani += 1
            
            # Hauteur I (si non-présente, pas d'éléments alti.)
            hauteurI = station['stationData']['I']
            
            # Parcourir les observations 
            listeObservations = station['stationData']['measure']
            for observation in listeObservations:
                
                
                # Si DS ou RI écartés, ne pas ajouter au compteur
                ecarteDS, ecarteRI, ecarteZD = observation['DS']['discarded'], observation['RI']['discarded'], observation['ZD']['discarded']
                hauteurS = observation['S']['value']
                dm1, dm2 = observation['dm1']['value'], observation['dm2']['value']
                
                # recherche du point du dictionnaire en Deep copy
                point = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])

                # si RI et DS se sont pas écartés, +1 pour chaucn
                if ecarteDS in ['false', None] and ecarteZD in ['false', None]:
                    point['planimetricElems'] += 1
                    nbElemPlaniStation += 1
                    nbObsTotalesPlani += 1
                if ecarteRI in ['false', None]:
                    point['planimetricElems'] += 1
                    nbElemPlaniStation += 1
                    nbObsTotalesPlani += 1
                
                # Si vides: dm1 et dm2= 0.0
                if dm1 == None : 
                    dm1 = 0.0
                if dm2 == None :
                    dm2 = 0.0

                # Filtrage des elems alti
                if ecarteDS in ['false', None] and ecarteZD in ['false', None] and hauteurI != None and hauteurS != None and float(dm1) == 0.0 and float(dm1) == 0.0: 
                    point['altimetricElems'] += 1
                    nbElemAltiStation += 1
                    nbObsTotalesAlti += 1
                    
            # rechercher le point de la station dans le dictionnaire en Deep copy (et ajouter aux compteurs les éléments sur la station)
            pointStation = rechercheUtils.rechercheNoPt(dictPoints, station['stationName'])

            pointStation['planimetricElems'] += nbElemPlaniStation
            pointStation['altimetricElems'] += nbElemAltiStation


                
    
    
    #### ------ GNSS
    
    # Vérifier qu'il y a bien un levé de session GNSS
    if 'gnss' in dictCanevas['network'].keys():
        
        # Liste de toutes les objets session
        listeSessions = dictCanevas['network']['gnss']['session']
        for session in listeSessions:
            
            # Inconnues supplémentaires suivant le groupe
            for groupeGNSS in dictParametres['parameters']['groups']['gnssGroups']['gnssGroup']:
                # Chercher le groupe correspondant
                if groupeGNSS['gnssGroupName'] == session['gnssGroup']:
                    
                    if groupeGNSS['unknownParameters']['Etranslation'] == "true":
                        nbInconnuesPlani += 1 
                    if groupeGNSS['unknownParameters']['Ntranslation'] == "true":
                        nbInconnuesPlani += 1 
                    if groupeGNSS['unknownParameters']['horizRotation'] == "true":
                        nbInconnuesPlani += 1
                    if groupeGNSS['unknownParameters']['horizScaleFactor'] == "true":
                        nbInconnuesPlani += 1 
                    if groupeGNSS['unknownParameters']['Htranslation'] == "true":
                        nbInconnuesAlti += 1 

                    
            
            # Parcourir les observations 
            listeObservations = session['measure']
            for observation in listeObservations:
                
                # faire le contrôle seulement si il y'a des observations 2D
                if "LY" in observation.keys() and "LX" in observation.keys() :
                
                    # Si LY ou LX écartés, ne pas ajouter l'élément au compteur
                    ecarteLY, ecarteLX = observation['LY']['discarded'], observation['LX']['discarded']
                    
                    # recherche du point du dictionnaire en Deep copy
                    point = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                    
                    # si LY ou LX se sont pas écartés, +1 pour chaucn
                    if ecarteLY in ['false', None]:
                        point['planimetricElems'] += 1
                        nbObsTotalesPlani += 1
                    if ecarteLX in ['false', None]:
                        point['planimetricElems'] += 1
                        nbObsTotalesPlani += 1

                # faire le contrôle seulement si il y'a une obs. 1D
                if "LH" in observation.keys() :
                    
                    # si LH est n'est pas écarté, ajoute +1 en alti
                    ecarteLH = observation['LH']['discarded']
                    
                    if ecarteLH in ['false', None] :
                        point['altimetricElems'] += 1
                        nbObsTotalesAlti += 1
                        
                        
                        
        # CHECK POUR POINTS COMMUNS (nouvelle boucle pour avoir la dernière version des elemsPlani)
        # Liste de toutes les objets de systemeLocal

        for session in listeSessions:
            
            # Parcourir les observations 
            listeObservations = session['measure']
            listeCommuns = [] # check des elems plani des points communs
            for observation in listeObservations:
            
                # recherche du point du dictionnaire en Deep copy
                point = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                
    
                # Les points communs doivent avoir 4 elems plani pour au moins 2 points
                # Si LY ou LX écartés, ne pas ajouter l'élément au compteur
                ecarteLY, ecarteLX = observation['LY']['discarded'], observation['LX']['discarded']
                if point['planimetricElems'] >= 4 and ecarteLY in ['false', None] and ecarteLX in ['false', None]:
                    listeCommuns.append((observation['pointName'], point['planimetricElems']))
                    
            # Si il y a moins de 4 elems plani /  pour au moins 2 pts du système local, msg erreur
            if len(listeCommuns) < 2:
                log += ">>> ERROR 400.1 : GNSS SESSION : {:s} MISSING COMMON REFERENCE WITH THE REST OF THE NETWORK\n".format(session['sessionName'])
                denombrementElementsPlaniAlti = False # échec du contrôle
                
                    
                    
      
                

    
    #### ------ SYSTEMES LOCAUX
    
    # Vérifier qu'il y a bien un système local
    if 'localSystems' in dictCanevas['network'].keys():
        
        # Liste de toutes les objets de systemeLocal
        listeSystemesLocaux = dictCanevas['network']['localSystems']['localSystem']
        for systemeLocal in listeSystemesLocaux:
            
            # Inconnues supplémentaires suivant le groupe
            for groupeSysteme in dictParametres['parameters']['groups']['localSystemGroups']['localSystemGroup']:
                # Chercher le groupe correspondant
                if groupeSysteme['localSystemGroupName'] == systemeLocal['localSystemGroup']:
                    
                    # Types d'obs. du système local
                    typesObs = []
                    for observation in systemeLocal['measure']:
                        if "LY" in observation.keys() and "LX" in observation.keys() :
                            typesObs.append("LY")
                            typesObs.append("LX")
                        if "LH" in observation.keys() :
                            typesObs.append("LH")
                    typesObs = set(typesObs)
                    
                    # Selon le type obs. compte les inconnues par défaut
                    if "LY" in typesObs and "LX" in typesObs:
                        nbInconnuesPlani += 3
                    if "LH" in typesObs:
                        nbInconnuesAlti += 1
                    
                    # Test si true pour inc. suppl. sur les facteurs d'échelle
                    if groupeSysteme['unknownParameters']['horizScaleFactor'] == "true":
                        nbInconnuesPlani += 1 

            
            
            # Parcourir les observations 
            listeObservations = systemeLocal['measure']
            
            for observation in listeObservations:
                
                # faire le contrôle seulement si il y'a des observations 2D
                if "LY" in observation.keys() and "LX" in observation.keys() :
                
                    # Si LY ou LX écartés, ne pas ajouter l'élément au compteur
                    ecarteLY, ecarteLX = observation['LY']['discarded'], observation['LX']['discarded']
                    
                    # recherche du point du dictionnaire en Deep copy
                    point = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                    
                    # si LY ou LX se sont pas écartés, +1 pour chaucn
                    if ecarteLY in ['false', None]:
                        point['planimetricElems'] += 1
                        nbObsTotalesPlani += 1
                    if ecarteLX in ['false', None]:
                        point['planimetricElems'] += 1
                        nbObsTotalesPlani += 1

                # faire le contrôle seulement si il y'a une obs. 1D
                if "LH" in observation.keys() :
                    
                    # si LH est n'est pas écarté, ajoute +1 en alti
                    ecarteLH = observation['LH']['discarded']
                    
                    if ecarteLH in ['false', None] :
                        point['altimetricElems'] += 1
                        nbObsTotalesAlti += 1
    
        # CHECK POUR POINTS COMMUNS (nouvelle boucle pour avoir la dernière version des elemsPlani)
        # Liste de toutes les objets de systemeLocal

        for systemeLocal in listeSystemesLocaux:
            
            # Parcourir les observations 
            listeObservations = systemeLocal['measure']
            listeCommuns = [] # check des elems plani des points communs
            for observation in listeObservations:
            
                # recherche du point du dictionnaire en Deep copy
                point = rechercheUtils.rechercheNoPt(dictPoints, observation['pointName'])
                    
                # Les points communs doivent avoir 4 elems plani pour au moins 2 points
                # Si LY ou LX écartés, ne pas ajouter l'élément au compteur
                ecarteLY, ecarteLX = observation['LY']['discarded'], observation['LX']['discarded']
                if point['planimetricElems'] >= 4 and ecarteLY in ['false', None] and ecarteLX in ['false', None]:
                    listeCommuns.append((observation['pointName'], point['planimetricElems']))
                    
            # Si il y a moins de 4 elems plani /  pour au moins 2 pts du système local, msg erreur
            if len(listeCommuns) < 2:
                log += ">>> ERROR 400.2 : LOCAL SYSTEM : {:s} MISSING COMMON REFERENCE WITH THE REST OF THE NETWORK\n".format(systemeLocal['localSystemName'])
                denombrementElementsPlaniAlti = False # échec du contrôle
                
                
            
        
                        
                        
                        
    #### ------ COTES
    
    # Vérifier qu'il y a bien au minimum une cote
    if 'simpleMeasures' in dictCanevas['network'].keys():
        
        # Liste de toutes les objets cotes
        listeCotes = dictCanevas['network']['simpleMeasures']['simpleMeasure']
        for cote in listeCotes:
  
            # faire le contrôle seulement si il y'a DP
            if "DP" in cote['measure'].keys():
                    
                # Si DP écarté, ne pas ajouter au compteur
                ecarteDP = cote['measure']['DP']['discarded']
    
                # recherche des points du dictionnaire en Deep copy
                point1 = rechercheUtils.rechercheNoPt(dictPoints, cote['measure']['pointName1'])
                point2 = rechercheUtils.rechercheNoPt(dictPoints, cote['measure']['pointName2'])
                
                # si DP est pas écarté, +1 aux points 1 et 2
                if ecarteDP in ['false', None]:
                    point1['planimetricElems'] += 1 
                    point2['planimetricElems'] += 1
                    nbObsTotalesPlani += 1
                    
            # faire le contrôle seulement si il y'a DH
            if "DH" in cote['measure'].keys():
                    
                # Si DP écarté, ne pas ajouter au compteur
                ecarteDH = cote['measure']['DH']['discarded']
    
                # recherche des points du dictionnaire en Deep copy
                point1 = rechercheUtils.rechercheNoPt(dictPoints, cote['measure']['pointName1'])
                point2 = rechercheUtils.rechercheNoPt(dictPoints, cote['measure']['pointName2'])
                
                # si DP est pas écarté, +1 aux points 1 et 2
                if ecarteDH in ['false', None] :
                    point1['altimetricElems'] += 1
                    point2['altimetricElems'] += 1
                    nbObsTotalesAlti+= 1       
                
    
    
    
    
    
        
        
    #### ------ CONTRAINTES
    
    # Vérifier qu'il y a bien au minimum une contrainte
    if 'constraints' in dictCanevas['network'].keys():
        
        # Liste de toutes les objets contraintes
        listeContraintes = dictCanevas['network']['constraints']['constraint']
        for contrainte in listeContraintes:
            
            # Si la contrainte est écarté, ne pas ajouter au compteur
            ecarteContrainte = contrainte['discarded']
            
            # recherche du point P du dictionnaire points
            for pt in contrainte['point']:
                if pt['pointTypeInConstraint'] == "P":
                    pointP = rechercheUtils.rechercheNoPt(dictPoints, pt['pointName'])
            
            # si la contrainte n'est pas écartée, +1 au point P (pas pour A et B)
            if ecarteContrainte in ['false', None]:
                pointP['planimetricElems'] += 1
                nbContraintes += 1
                  
                      
                
    
                    
                
            
        
  
            
     #------------------------------
#### # --- POINTS NOUVEAUX       ---
     #------------------------------
     
    # Lister tous les points du dictPoint
    listePoints = dictPoints['points']['point']
    for point in listePoints:
        
        # Récupération des elements plani. et alti.
        elemsPlani, elemsAlti = point['planimetricElems'], point['altimetricElems']
        
        # Comptage des inconnues
        if elemsPlani >= 2 :
            nbInconnuesPlani += 2
        if elemsAlti >= 1 :
            nbInconnuesAlti += 1
            
            
            


     #--------------------------------------
#### # --- POINTS FIXES ET LIBRE-AJUSTEE ---    
     #--------------------------------------
         
    # pour libre ajusté
    typeCalcul = dictParametres['parameters']['computationOptions']['networkType'] 
    libreAjuste = True if typeCalcul=='stochastic' else False

    # Pour la partie planimétrique
    if dimensionCalcul == "2D" or dimensionCalcul == "2D+1" :
        
        # Dénombrement des éléments de PF, datum (à retrancher au nombre d'inconnues)
        datumPlani = 0
         
        # Listage des PF plani
        listePointsFixesPlani = dictParametres['parameters']['planimetricControlPoints']['point']
        
        
        
        # Parcourir les points
        for pointPlani in listePointsFixesPlani:
            
            # recherche du point du dictionnaire points
            point = rechercheUtils.rechercheNoPt(dictPoints, pointPlani['pointName'])
            # Nb de détermination plani. sur les PF
            if point['planimetricElems'] < 1: # si pas assez de détermination
                log += ">>> ERROR 400.3 : PLANIMETRIC CONTROL POINTS : {:s} MISSING DETERMINATION\n".format(pointPlani['pointName'])
                denombrementElementsPlaniAlti = False # échec du contrôle (pas assez de déterm. pour un des PF)
            
            else: # si assez de détermination sur PF
                # compteur pour datum à déduire du nombre d'inc. (2 datum / point)
                datumPlani += 2
                if libreAjuste:
                    nbInconnuesPlani += 2
                    nbObsTotalesPlani += 2
            
            
    # Pour la partie planimétrique
    if dimensionCalcul == "1D" or dimensionCalcul == "2D+1" :
    
        # Dénombrement des éléments de PF, datum (à retrancher au nombre d'inconnues)
        datumAlti = 0
        
        # Listage des PF alti
        listePointsFixesAlti = dictParametres['parameters']['altimetricControlPoints']['point']
        
        # Parcourir les points
        for pointAlti in listePointsFixesAlti:
            
            # recherche du point du dictionnaire points
            point = rechercheUtils.rechercheNoPt(dictPoints, pointAlti['pointName'])
            # Nb de détermination alti. sur les PF
            if point['altimetricElems'] < 1: # si pas assez de détermination
                log += ">>> ERROR 400.4 : ALTIMETRIC CONTROL POINTS : {:s} MISSING DETERMINATION\n".format(pointAlti['pointName'])
                denombrementElementsPlaniAlti = False # échec du contrôle (pas assez de déterm. pour un des PF)
            else: # Si assez de détermination alti.
                # compteur pour datum à déduire du nombre d'inc.
                datumAlti += 1
                if libreAjuste:
                    nbInconnuesAlti += 1
                    nbObsTotalesAlti += 1
                
    


         #---------------------
    #### # --- DENOMBREMENT ---
         #---------------------   
    
    if denombrementElementsPlaniAlti: # Si le contrôle est positif
    
            log += ">>> checked\n\n" 
            
            # Planimétrie
            if dimensionCalcul == "2D" or dimensionCalcul == "2D+1" :
                log += "PLANIMETRIC COUNTING :\n"
                log += "- - - - - - - - - - -  \n"
                log += "NUMBER OF OBSERVATION :  {:d}\n".format(nbObsTotalesPlani)
                log += "NUMBER OF UNKNOWNS :     {:d}\n".format(nbInconnuesPlani-datumPlani)
                log += "NUMBER OF CONSTRAINTS :  {:d}\n".format(nbContraintes)
                if libreAjuste :
                    log += "DATUM :                  STO\n"
                else:
                    log += "DATUM :                  {:d}\n".format(datumPlani)
                log += "OVERDETERMINATION :      {:d}\n\n".format(nbObsTotalesPlani-(nbInconnuesPlani-datumPlani)+nbContraintes)
                
            # Altimétrie
            if dimensionCalcul == "1D" or dimensionCalcul == "2D+1" :    
                log += "ALTIMETRIC COUNTING :\n"
                log += "- - - - - - - - - - -\n"
                log += "NUMBER OF OBSERVATIONS : {:d}\n".format(nbObsTotalesAlti)
                log += "NUMBER OF UNKNOWNS :     {:d}\n".format(nbInconnuesAlti-datumAlti)
                if libreAjuste :
                    log += "DATUM :                  STO\n"
                else:
                    log += "DATUM :                  {:d}\n".format(datumAlti)
                log += "OVERDETERMINATION :      {:d}\n\n".format(nbObsTotalesAlti-(nbInconnuesAlti-datumAlti))
                
    else: # si négatif
        log+="\n" # retour à la ligne 
        
    print(log)  
    return denombrementElementsPlaniAlti, log



    
    
    

class ControlesCoherence:
    
    
    def __init__(self, nomsFichiers):    
        """
        Constructeur de la classe "controlesCoherence" qui permet de procéder à tous les contrôles de cohérences sur le canevas,
        les points et les paramètres de calcul.

        Parameters
        ----------
        nomsFichiers: dict
            Dictionnaire contenant le nom des 6 fichiers XML et XSD.
                                                                      
        Returns
        -------
        None.

        """
        
        # fichier logTotal
        self.logTotal = '\nCONSTITENCY CONTROLS\n'
        self.logTotal+= '====================\n\n'
        
        
        # Initiliastion de la variable pour cette fonction de constructeur
        self.erreurInit = True
        
        
        
        
        # Création des variables (dictionnaires)
        try:
            self.nomFichierXMLCanevas = nomsFichiers['fichierXMLCanevas']
        except:
            self.logTotal += "ERROR 99.1 NETWORK XML FILE MISSING\n"
            print("ERROR 99.1 NETWORK XML FILE MISSING\n")
            self.erreurInit = False
            
        try:
            self.nomFichierXMLPoints = nomsFichiers['fichierXMLPoints']
        except:
            self.logTotal += "ERROR 99.2 POINTS XML FILE MISSING\n"
            print("ERROR 99.2 POINTS XML FILE MISSING\n")
            self.erreurInit = False
            
        try:
            self.nomFichierXMLParametres = nomsFichiers['fichierXMLParametres']
        except:
            self.logTotal += "ERROR 99.3 PARAMETERS XML FILE MISSING\n"
            print("ERROR 99.3 PARAMETERS XML FILE MISSING\n")
            self.erreurInit = False
            
        try:
            self.dictCanevas = conversionUtils.xml2dictionnaire(nomsFichiers['fichierXMLCanevas'])
            self.dictCanevas = structureListeInDict(self.dictCanevas, 'network') # structure en liste si éléments uniques
        except Exception as e:
            self.logTotal += "ERROR 99.4 OBSERVATIONS XML FILE ENCOUNTER A MAJOR ERROR IN STRUCTURE (<> not closed or empty file): ETREE LIBRARY AUTO-ERROR MESSAGE:\n{:s}\n".format(str(e))
            print("ERROR 99.4 OBSERVATIONS XML FILE ENCOUNTER A MAJOR ERROR IN STRUCTURE (<> not closed or empty file): ETREE LIBRARY AUTO-ERROR MESSAGE:\n{:s}\n".format(str(e)))
            self.erreurInit = False

        try:
            self.dictPoints = conversionUtils.xml2dictionnaire(nomsFichiers['fichierXMLPoints'])
            conversionUtils.reinitialiserPoints(self.dictPoints)
        except Exception as e:
            self.logTotal += "ERROR 99.5 POINTS XML FILE ENCOUNTER A MAJOR ERROR IN STRUCTURE (<> not closed or empty file): ETREE LIBRARY AUTO-ERROR MESSAGE:\n{:s}\n".format(str(e))
            print("ERROR 99.5 POINTS XML FILE ENCOUNTER A MAJOR ERROR IN STRUCTURE (<> not closed or empty file): ETREE LIBRARY AUTO-ERROR MESSAGE:\n{:s}\n".format(str(e)))
            self.erreurInit = False
            
        try:
            self.dictParametres = conversionUtils.xml2dictionnaire(nomsFichiers['fichierXMLParametres'])
            self.dictParametres = structureListeInDict(self.dictParametres, 'parameters')
        except Exception as e:
            self.logTotal += "ERROR 99.6 PARAMETERS XML FILE ENCOUNTER A MAJOR ERROR IN STRUCTURE (<> not closed or empty file): ETREE LIBRARY AUTO-ERROR MESSAGE:\n{:s}\n".format(str(e))
            print("ERROR 99.6 PARAMETERS XML FILE ENCOUNTER A MAJOR ERROR IN STRUCTURE (<> not closed or empty file): ETREE LIBRARY AUTO-ERROR MESSAGE:\n{:s}\n".format(str(e)))
            self.erreurInit = False
        
        try:
            self.nomFichierXSDCanevas = nomsFichiers['fichierXSDCanevas']
        except:
            self.logTotal += "ERROR 99.7 NETWORK XSD DATAMODEL MISSING\n"
            print("ERROR 99.7 NETWORK XSD DATAMODEL MISSING\n")
            self.erreurInit = False
            
        try:
            self.nomFichierXSDPoints = nomsFichiers['fichierXSDPoints']
        except:
            self.logTotal += "ERROR 99.8 POINTS XSD DATAMODEL MISSING\n"
            print("ERROR 99.8 POINTS XSD DATAMODEL MISSING\n")
            self.erreurInit = False
            
        try:
            self.nomFichierXSDParametres = nomsFichiers['fichierXSDParametres']
        except:
            self.logTotal += "ERROR 99.9 PARAMETERS XSD DATAMODEL MISSING\n"
            print("ERROR 99.9 PARAMETERS XSD DATAMODEL MISSING\n")
            self.erreurInit = False
            
        try:
            self.nomFichierLOG = nomsFichiers['dossierResultats'] + "\\coherenceChecks.log"
        except:
            self.logTotal += "ERROR 99.10 RESULT PATH MISSING\n"
            print("ERROR 99.10 RESULT PATH MISSING\n")
            self.erreurInit = False


    def checkTotal(self):
        
        """
        Lancer les contrôles des XML (parsés en dictionnaires).
                                                                      
        Returns
        -------
        True ou None
            Retourne True si le contrôle complet est réussi. None sinon.

        """
        
        
        # PREMIERE PARTIES A FAIRE DANS TOUS LES CAS
        
        
        if self.erreurInit :
            #### CHECK MODELES XSD
            # Vérifie que les XML soient conformes aux modèles XSD
            # try:
                self.checkXmlXsdCanevas, self.log1 = checkXmlXsd(self.nomFichierXSDCanevas,self.nomFichierXMLCanevas)
                self.checkXmlXsdPoints, self.log2 = checkXmlXsd(self.nomFichierXSDPoints,self.nomFichierXMLPoints)
                self.checkXmlXsdParametres, self.log3 = checkXmlXsd(self.nomFichierXSDParametres,self.nomFichierXMLParametres)
                self.logTotal += self.log1+self.log2+self.log3
                
                #### CHECK SEMANTIQUE
                # Les contrôles XML-XSD doivent être ok pour passer aux contrôles sémantiques et géométriques
                if self.checkXmlXsdCanevas and self.checkXmlXsdPoints and self.checkXmlXsdParametres :
                    
                    
                    # Vérifie qu'il n'y a pas de doublons dans les points
                    self.checkDoublonsPoints, self.log = checkDoublonsPoints(self.dictPoints)
                    self.logTotal += self.log
                    
                    # Vérfie que chaque point concerné du canevas se trouve dans les points
                    self.checkerCanevasInPoints, self.log = checkCanevasInPoints(self.dictCanevas, self.dictPoints)
                    self.logTotal += self.log
                    
                    # Vérifie que chaque groupes (modèle stochastiques et paramètres inconnus suppl.) du canevas se trouve dans les paramètres
                    self.checkGroupesCanevasInParam, self.log, self.dictParametres = checkGroupesCanevasInParam(self.dictCanevas, self.dictParametres)
                    self.logTotal += self.log
                    
                    # Vérifie que chaque point fixe plani et alti se trouve bien dans les points
                    self.checkDatumInPoints, self.log = checkDatumInPoints(self.dictParametres, self.dictPoints)
                    self.logTotal += self.log
        

                    # Les contrôles sémantiques doivent être ok dans tous les cas (coché ou non)
                    if self.checkDoublonsPoints and self.checkerCanevasInPoints and self.checkGroupesCanevasInParam and self.checkDatumInPoints:
                        
                        # option des ctrl de cohé. cochée ou non
                        self.processCtrlCoh = self.dictParametres['parameters']['computationOptions']['geometryPreChecks']
                        if self.processCtrlCoh == "true":
                            self.processCtrlCoh = True
                        else:
                            self.processCtrlCoh = False

                        
                        # Si cltr coh. coché, on fait les ctrl géométriques
                        if self.processCtrlCoh:
                        

                            #### CHECK GEOMETRIQUES
                        
                            # Contrôle géométriques des coordonnées GNSS avec les points (0.5m)
                            self.checkGeometrieGNSS, self.log = checkGeometrieGNSS(self.dictCanevas, self.dictPoints)
                            self.logTotal += self.log
                            
                            # Contrôle géométriques des distances issues de levés polaires avec les points (corrigées dm1/dm2 et réduite dans le plan proj.)
                            self.checkGeometrieDistances, self.log = checkGeometrieDistancesPolaire(self.dictCanevas, self.dictPoints)
                            self.logTotal += self.log
                            
                            # Contrôle géométrique des écarts à la moyenne pour les directions RI corrigées de dm1 et dm2
                            self.checkGeometrieDirections, self.log = checkGeometrieDirectionsPolaire(self.dictCanevas, self.dictPoints)
                            self.logTotal += self.log
                            
                            # Contrôle géométrique des systèmes locaux (comparaison des dist. yx et dist. EN)
                            self.checkGeometrieSystemesLocaux, self.log = checkGeometrieSystemesLocaux(self.dictCanevas, self.dictPoints)
                            self.logTotal += self.log
                            
                            # Contrôle géométriques des cotes les points (0.5m)
                            self.checkGeomCotes, self.log = checkGeometrieCotes(self.dictCanevas, self.dictPoints)
                            self.logTotal += self.log
                            
                            # Contrôle géométriques des cotes les points (0.5m)
                            self.checkGeomContraintes, self.log = checkGeometrieContraintes(self.dictCanevas, self.dictPoints)
                            self.logTotal += self.log
                            
                            
                            #### CHECK DENOMBREMENT
                            # Les contrôles géométriques doivent être remplis pour passer au dénombrement des éléments plani. et alti.
                            if self.checkGeometrieGNSS and self.checkGeometrieDistances and self.checkGeometrieDirections and self.checkGeometrieSystemesLocaux and self.checkGeomCotes and self.checkGeomContraintes:
                                return self.denombrement()
                            
                            else: # si les contrôles géométriques ne sont pas remplis
                                self.logTotal += "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
                                self.logTotal += "NEXT VALIDATION STEP ONLY WITH CODE 100 TO 300 SUCCESSFUL\n"
                                self.logTotal += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\\n"
                                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                                print('NEXT VALIDATION STEP ONLY WITH CODE 100 TO 300 SUCCESSFUL')
                                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                                

                        else : # Si pas coché, retourner le dénombrement (ctrl sémantiques OK)
                            return self.denombrement()
                                    
                        
                    else: # si les contrôles sémantiques ne sont pas remplis, ne passe pas au ctrl géom.
                                        self.logTotal += "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
                                        self.logTotal += "NEXT VALIDATION STEP ONLY WITH CODE 100 TO 200 SUCCESSFUL\n"
                                        self.logTotal += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\\n"
                                        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                                        print('NEXT VALIDATION STEP ONLY WITH CODE 100 TO 200 SUCCESSFUL')
                                        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    
                    
                else:# si les contrôles XML-XSD ne sont pas remplis, ne rien faire d'autres
                    self.logTotal += "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
                    self.logTotal += "NEXT VALIDATION STEP ONLY WITH CODE 100 SUCCESSFUL\n"
                    self.logTotal += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\\n"
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    print('NEXT VALIDATION STEP ONLY WITH CODE 100 SUCCESSFUL')
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                     
                        
                    
                    
                    
                    
                    
                    
                    
        
        
        
        
        
        
        
        
        
        
        # # Si on procède au contrôle (option)
            
        #     if self.erreurInit :
        #         #### CHECK MODELES XSD
        #         # Vérifie que les XML soient conformes aux modèles XSD
        #         # try:
        #             self.checkXmlXsdCanevas, self.log1 = checkXmlXsd(self.nomFichierXSDCanevas,self.nomFichierXMLCanevas)
        #             self.checkXmlXsdPoints, self.log2 = checkXmlXsd(self.nomFichierXSDPoints,self.nomFichierXMLPoints)
        #             self.checkXmlXsdParametres, self.log3 = checkXmlXsd(self.nomFichierXSDParametres,self.nomFichierXMLParametres)
        #             self.logTotal += self.log1+self.log2+self.log3
                    
        #             #### CHECK SEMANTIQUE
        #             # Les contrôles XML-XSD doivent être ok pour passer aux contrôles sémantiques et géométriques
        #             if self.checkXmlXsdCanevas and self.checkXmlXsdPoints and self.checkXmlXsdParametres :
                        
                        
        #                 # Vérifie qu'il n'y a pas de doublons dans les points
        #                 self.checkDoublonsPoints, self.log = checkDoublonsPoints(self.dictPoints)
        #                 self.logTotal += self.log
                        
        #                 # Vérfie que chaque point concerné du canevas se trouve dans les points
        #                 self.checkerCanevasInPoints, self.log = checkCanevasInPoints(self.dictCanevas, self.dictPoints)
        #                 self.logTotal += self.log
                        
        #                 # Vérifie que chaque groupes (modèle stochastiques et paramètres inconnus suppl.) du canevas se trouve dans les paramètres
        #                 self.checkGroupesCanevasInParam, self.log, self.dictParametres = checkGroupesCanevasInParam(self.dictCanevas, self.dictParametres)
        #                 self.logTotal += self.log
                        
        #                 # Vérifie que chaque point fixe plani et alti se trouve bien dans les points
        #                 self.checkDatumInPoints, self.log = checkDatumInPoints(self.dictParametres, self.dictPoints)
        #                 self.logTotal += self.log
                        
                        
        #                 #### CHECK GEOMETRIQUE
        #                 # Les contrôles sémantiques doivent être ok pour passer aux contrôles géométriques
        #                 if self.checkDoublonsPoints and self.checkerCanevasInPoints and self.checkGroupesCanevasInParam and self.checkDatumInPoints:

        #                     # Contrôle géométriques des coordonnées GNSS avec les points (0.5m)
        #                     self.checkGeometrieGNSS, self.log = checkGeometrieGNSS(self.dictCanevas, self.dictPoints)
        #                     self.logTotal += self.log
                            
        #                     # Contrôle géométriques des distances issues de levés polaires avec les points (corrigées dm1/dm2 et réduite dans le plan proj.)
        #                     self.checkGeometrieDistances, self.log = checkGeometrieDistancesPolaire(self.dictCanevas, self.dictPoints)
        #                     self.logTotal += self.log
                            
        #                     # Contrôle géométrique des écarts à la moyenne pour les directions RI corrigées de dm1 et dm2
        #                     self.checkGeometrieDirections, self.log = checkGeometrieDirectionsPolaire(self.dictCanevas, self.dictPoints)
        #                     self.logTotal += self.log
                            
        #                     # Contrôle géométrique des systèmes locaux (comparaison des dist. yx et dist. EN)
        #                     self.checkGeometrieSystemesLocaux, self.log = checkGeometrieSystemesLocaux(self.dictCanevas, self.dictPoints)
        #                     self.logTotal += self.log
                            
        #                     # Contrôle géométriques des cotes les points (0.5m)
        #                     self.checkGeomCotes, self.log = checkGeometrieCotes(self.dictCanevas, self.dictPoints)
        #                     self.logTotal += self.log
                            
        #                     # Contrôle géométriques des cotes les points (0.5m)
        #                     self.checkGeomContraintes, self.log = checkGeometrieContraintes(self.dictCanevas, self.dictPoints)
        #                     self.logTotal += self.log
                            
                            
        #                     #### CHECK DENOMBREMENT
        #                     # Les contrôles géométriques doivent être remplis pour passer au dénombrement des éléments plani. et alti.
        #                     if self.checkGeometrieGNSS and self.checkGeometrieDistances and self.checkGeometrieDirections and self.checkGeometrieSystemesLocaux and self.checkGeomCotes and self.checkGeomContraintes:

        #                         return self.denombrement()
                                
                                
        #                     else: # si les contrôles géométriques ne sont pas remplis
        #                         self.logTotal += "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        #                         self.logTotal += "NEXT VALIDATION STEP ONLY WITH CODE 100 TO 300 SUCCESSFUL\n"
        #                         self.logTotal += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\\n"
        #                         print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        #                         print('NEXT VALIDATION STEP ONLY WITH CODE 100 TO 300 SUCCESSFUL')
        #                         print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                                
        #                 else: # si les contrôles sémantiques ne sont pas remplis
        #                     self.logTotal += "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        #                     self.logTotal += "NEXT VALIDATION STEP ONLY WITH CODE 100 TO 200 SUCCESSFUL\n"
        #                     self.logTotal += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\\n"
        #                     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        #                     print('NEXT VALIDATION STEP ONLY WITH CODE 100 TO 200 SUCCESSFUL')
        #                     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                                 
        #             else: # si les contrôles XML-XSD ne sont pas remplis
        #                 self.logTotal += "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        #                 self.logTotal += "NEXT VALIDATION STEP ONLY WITH CODE 100 SUCCESSFUL\n"
        #                 self.logTotal += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\\n"
        #                 print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        #                 print('NEXT VALIDATION STEP ONLY WITH CODE 100 SUCCESSFUL')
        #                 print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        
                        
        #         # except: # Si il y'a une erreur globale fatale, ce message apparaît
        #             # self.logTotal += "ERROR 999.1 : PROBLEME MAJEUR INEXPLIQUE DANS LES CONTROLES DE COHERENCE, VERIFIEZ LES FICHIERS XML\n"
        #             # print("ERROR 999.1 : PROBLEME MAJEUR INEXPLIQUE DANS LES CONTROLES DE COHERENCE, VERIFIEZ LES FICHIERS XML\n")
            
 
        # else: # si ne pas procéder au contrôle, il faut calculer obligatoirement le dénombrement
   
        #     return self.denombrement()
            
 
    
 
    
 
    
    def exportLog(self):
        
        """
        Lancer l'export du fichier log avec tous les contrôles ou non (si échec).
                                                                      
        Returns
        -------
        None.

        """
        
        try:
            # Ouverture du fichier
            with open(self.nomFichierLOG, 'w') as f:
                
                # écrire le log
                f.writelines(self.logTotal)
        except:
            print("ERROR 500.1 : PROBLEME A L'EXPORT DU FICHIER LOG\n")
            sys.exit()
        
        
        
    def denombrement(self):
        
        # Dénombrer les éléments plani et alti. de chaque point avec le canevas

        self.denombrementElementsPlaniAlti, self.log = denombrementElementsPlaniAlti(self.dictCanevas, self.dictPoints, self.dictParametres)
        self.logTotal += self.log
        
        
        if self.denombrementElementsPlaniAlti : # Tous les tests sont OK
            
            self.logTotal += "********************************\n"
            self.logTotal += "* NETWORK READY FOR ADJUSTMENT *\n"
            self.logTotal += "********************************\n"
            print("********************************")
            print('* NETWORK READY FOR ADJUSTMENT *')
            print("********************************\n")
            
            return True
            

        else: # Si le dénombrement a échoué (voir dans quel cas dans les infos de la fonction)
            self.logTotal += "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
            self.logTotal += "COMPLETE VALIDATION ONLY WITH CODE 100 TO 400 SUCCESSFUL\n"
            self.logTotal += "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\\n"
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('COMPLETE VALIDATION ONLY WITH CODE 100 TO 400 SUCCESSFUL')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            
            
            
### MODIFIY TO FALSE HERE
   
            return False 
        
        
    def getDictPoints(self):
        
        return self.dictPoints
    
    def getDictCanevas(self):
        
        return self.dictCanevas
    
    def getDictParametres(self):
        
        return self.dictParametres
    
    
    
    
  

   
    
   
    

    




    
    





    







