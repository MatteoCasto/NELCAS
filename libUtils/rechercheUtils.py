# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 10:32:31 2022

@author: Matteo Casto, INSIT
"""

def rechercheNoPt(dictPoints, noPt):
    
    """
    Fonction pour rechercher un no de point dans le dictPoint sans surcharger le code.

    Parameters
    ----------
    dictPoints : dictionnaire
        Dict. des points après validation de la fonction: 'xml2validate'
    noPt : string
        Numéro de point à rechercher

    Returns
    -------
    point : XMLelement
        Retourne le point commplet sous la forme d'un élément XML 
    """
    try:
        # Liste de tous les objets points
        listePoints = dictPoints['points']['point']
        
        for point in listePoints:
            if point['pointName'] == noPt: 
                pointXML = point
                return pointXML
    except:
        print(noPt, ": NOT FOUND IN POINTS")
        
        

        


def rechercheGroupeParNom(dictParametres, nomGroupe):
    
    """
    Simple fonction de recherche pour retrouver un groupe XML (avec tous ses éléments) par son nom (tous-types compris).
    Ne génère pas d'erreur puisque les groupes ont été contrôlés dans les contrôles de cohérences.
    
    Parameters
    ----------
    dictParametres : dictionnaire
        Contenant les paramètres issus du fichier XML après contrôles.
    nomGroupe : string
        Nom du groupe à rechercher.
    
    Returns
    -------
    groupe : dictionnaire
        Sous-dictionnaire du groupe correspondant (lié directement à dictParametres)
    
    """
    
    
    # Parcourir tous les groupes
    # distance
    try:
        for groupe in dictParametres['parameters']['groups']['distanceGroups']['distanceGroup']:
            if nomGroupe == groupe['distanceGroupName']:
                return groupe
    except:
        pass
    
    # direction
    try:
        for groupe in dictParametres['parameters']['groups']['directionGroups']['directionGroup']:
            if nomGroupe == groupe['directionGroupName']:
                return groupe
    except:
        pass
    
    # centrage
    try:
        for groupe in dictParametres['parameters']['groups']['centringGroups']['centringGroup']:
            if nomGroupe == groupe['centringGroupName']:
                return groupe
    except:
        pass
    
    # GNSS
    try:
        for groupe in dictParametres['parameters']['groups']['gnssGroups']['gnssGroup']:
            if nomGroupe == groupe['gnssGroupName']:
                return groupe
    except:
        pass
    
    # système Local
    try:
        for groupe in dictParametres['parameters']['groups']['localSystemGroups']['localSystemGroup']:
            if nomGroupe == groupe['localSystemGroupName']:
                return groupe
    except:
        pass
    
    # cote
    try:
        for groupe in dictParametres['parameters']['groups']['simpleMeasureGroups']['simpleMeasureGroup']:
            if nomGroupe == groupe['simpleMeasureGroupName']:
                return groupe
    except:
        pass

    print(nomGroupe, ": GROUP NOT FOUND IN PARAMETERS")
        




def rechercheIdObs(dictCanevas, idObs):
    
    """
    Fonction permettant de rapidement chercher un idObs parmis tous les types d'observation du canevas.
    Fonctionne pour la plani. et l'alti.(+1000000).
    
    Parameters
    ----------
    dictCanevas : dictionnaire
        Contenant le canevas issus du fichier XML après contrôles.
    idObs : integer
        index de l'observation à rechercher.
    
    Returns
    -------
    observation : dictionnaire
        Sous-dictionnaire de l'obs. correspondante
  
    """
    
    if 'polar' in dictCanevas['network']:
        
        for station in dictCanevas['network']['polar']['station']:  
            for observation in station['stationData']['measure']:
                
                if "RI" in observation.keys():
                    if "idObsPlani" in observation['RI'].keys():
                        if observation['RI']['idObsPlani'] == idObs:
                            return observation, 'station: '+station['stationName']
                        
                if "DP" in observation.keys():
                    if "idObsPlani" in observation['DP'].keys():
                        if observation['DP']['idObsPlani'] == idObs:
                            return observation, 'station: '+station['stationName']
                        
                if "DH" in observation.keys():
                    if "idObsAlti" in observation['DH'].keys():
                        if observation['DH']['idObsAlti'] == idObs:
                            return observation, 'station: '+station['stationName']
                        
    if 'gnss' in dictCanevas['network']:
        
        for session in dictCanevas['network']['gnss']['session']:
            for observation in session['measure']:
                
                if "LY" in observation.keys():
                    if "idObsPlani" in observation['LY'].keys():
                        if observation['LY']['idObsPlani'] == idObs:
                            return observation, 'gnssSession: '+session['sessionName']
                        
                if "LX" in observation.keys():
                    if "idObsPlani" in observation['LX'].keys():
                        if observation['LX']['idObsPlani'] == idObs:
                            return observation, 'gnssSession: '+session['sessionName']
                        
                if "LH" in observation.keys():
                    if "idObsAlti" in observation['LH'].keys():
                        if observation['LH']['idObsAlti'] == idObs:
                            return observation, 'gnssSession: '+session['sessionName']
                        
    if 'localSystems' in dictCanevas['network']:
        
        for systeme in dictCanevas['network']['localSystems']['localSystem']:
            for observation in systeme['measure']:
                
                if "LY" in observation.keys():
                    if "idObsPlani" in observation['LY'].keys():
                        if observation['LY']['idObsPlani'] == idObs:
                            return observation, 'localSystem: '+systeme['localSystemName']
                        
                if "LX" in observation.keys():
                    if "idObsPlani" in observation['LX'].keys():
                        if observation['LX']['idObsPlani'] == idObs:
                            return observation, 'localSystem: '+systeme['localSystemName']
                        
                if "LH" in observation.keys():
                    if "idObsAlti" in observation['LH'].keys():
                        if observation['LH']['idObsAlti'] == idObs:
                            return observation, 'localSystem: '+systeme['localSystemName']
                        
    if 'simpleMeasures' in dictCanevas['network']:
        
        for cote in dictCanevas['network']['simpleMeasures']['simpleMeasure']:
            observation = cote['measure']
            if "DP" in observation.keys():
                if "idObsPlani" in observation['DP'].keys():
                    if observation['DP']['idObsPlani'] == idObs:
                        observation.update({'pointName':observation['pointName2']})
                        return observation, 'simpleMes: '+observation['pointName1']
                    
            if "DH" in observation.keys():
                if "idObsAlti" in observation['DH'].keys():
                    if observation['DH']['idObsAlti'] == idObs:
                        observation.update({'pointName':observation['pointName2']})
                        return observation, 'simpleMes: '+observation['pointName1']
    
    return None, None
    
    