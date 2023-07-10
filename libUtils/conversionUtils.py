# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 11:41:35 2022

@author: Matteo Casto, INSIT
"""

from xml.dom import minidom
from xml.etree import ElementTree as ET
import os
import libUtils.geometrieUtils as geometrieUtils
import libUtils.controlesCoherenceUtils as controlesCoherenceUtils
import xmltodict
import copy
import os


def xml2dictionnaire(path):
    
    """
    Parser un fichier XML en dictionnaire avec la librairie xmltodict

    Parameters
    ----------
    path : string
        Nom avec l'extension du fichier xml'. Ne pas oublier les doubles slash

    Returns
    -------
    dictRes : dictionnaire
        Retourne le dictionnaire issu de la lecture du fichier XML
    """
    
    with open(path) as f:
        dictRes = xmltodict.parse(f.read(), encoding='utf-8')
        
    return dictRes

def dictionnaire2xml(dictionnaire, path):
    
    """
    Parser un dictionnaire et l'écrit sous un format XML dans un fichier.

    Parameters
    ----------
    dictionnaire : dictionnaire
        dictionnaire à parser

    Returns
    -------
    None.
    
    """
    
    xml= xmltodict.unparse(dictionnaire, pretty=True, encoding='utf-8')
    with open(path, 'w') as f:
        f.write(xml)
    
    return None


def reinitialiserPoints(dictPoints):
    
    """
    Enlever tous les indicateurs pour repartir d'un fichier points où
    les indicateurs pourront être introduit.
    Cela permet de conserver toute autre balise du fichier XML 

    Parameters
    ----------
    dictPoints : dictionnaire
        dictionnaire des points

    Returns
    -------
    dictPoints.
    
    """
    
    
    listKeysToDelete = ['planimetricElems', 'altimetricElems', 'idUnkH', 'idUnkE', 'idUnkN',
                        'stdErrEllipse', 'externalReliabilityPlaniVector', 'deltaPlani', 
                        'altiStdError', 'externalReliabilityAlti', 'deltaAlti']
    
    dictCopy = copy.deepcopy(dictPoints)
    
    for i, point in enumerate(dictCopy['points']['point']):
        
        for key in point.keys():
            if key in listKeysToDelete:
                dictPoints['points']['point'][i].pop(key)
    
    return dictPoints
    
    





def canevas2xml(filePathll1, filePathOutput, dictPoints):
    
    """
    Transformation du fichier de résultats Homère ll1 en XML (canevas des mesures et contraintes)

    Parameters
    ----------
    filePathll1 : string (ne pas oublier les doubles backslash)
        Lien vers le fichier .ll1 
    filePathOutput : string (ne pas oublier les doubles backslash)
        Lien vers le fichier d'export XML
    dictPoints : dictionnaire 
        Dict. des points après la lecture du fichier XML des points .
        Ici, utile pour remplacer les natures des visées du canevas (admises correctes dans les points).
        
    Returns
    -------
    None.

    """
    
    # Initialisation du format XML
    doc = minidom.Document()
    canevas = doc.createElement('network')
    doc.appendChild(canevas) 
    
    # Lecture du fichier .ll1
    fichier = open(filePathll1,'r')
    line = fichier.readline()
    
    # variable qui devient True une fois entré dans la liste des mesures
    listeMesures = False
    GK = ''

    nSessionIncr = 0 # incérment pour les sessions GNSS 'Sx'
    noSys = 0 # incrément pour les noms de sys. locaux
    
    # Initialisation des balises (sans encore les ajouter au canevas, voir fin de la fonction)
    polaire = doc.createElement('polar')
    GNSS = doc.createElement('gnss')
    systemesLocaux = doc.createElement('localSystems')
    cotes = doc.createElement('simpleMeasures')
    contraintes = doc.createElement('constraints')


    # Boucle de lecture du fichier .ll1    
    while line:
        if len(line.strip())>0:
            if line[0] != "*":
                stringLine = line.rstrip() # enlever le \n en fin de ligne
                
                # on entre dans la liste des mesures -> listeMesures = True   
                if stringLine[0:17] == 'LISTE DES MESURES':
                    listeMesures = True
                
                # on sort de la liste des mesures -> listeMesures = False    
                if stringLine[0:21] == 'DEROULEMENT DU CALCUL':
                    listeMesures = False
                
                # on arrive dans la liste des mesures si listeMesures == True
                if listeMesures == True:
                    
                    # teste si le GK est bien 2 chiffres (ex. 51, 11, 71, etc.)
                    if stringLine[4].isdigit() and stringLine[5].isdigit():
                        GK = stringLine[4:6]
                        
                        
                    #-----------------------
  ####              # --- LEVES POLAIRES ---
                    #----------------------- 
                    
                    if (GK == '11' or GK == '51') and stringLine[6] == '!' and stringLine[2].isdigit():
                        
                        # check si on est sur la ligne de station
                        ligneSta = False 
                        
                        # pour les no, il faut veiller -> identique au no du calcul des PF
                        if stringLine[4:6] == GK: # première ligne de la séquence = noSta
                            noCmne, noPlan, no = stringLine[7:10], stringLine[11:15], stringLine[18:22]
                            lenPlan = len(noPlan.strip())
                            if lenPlan < 4: # Si pas un numéro de plan
                                reste = 4-lenPlan
                                noPlan = reste*' ' + noPlan.strip()
                            noSta = noCmne + noPlan + '    ' + no

                            ligneSta = True
                            
                            # Récupération des éléments de station
                            hauteurI = line[24:29].strip()
                            
                            # Initialisation de la balise du stationnement
                            station = doc.createElement('station')
                            polaire.appendChild(station)
                            
                            # Numéro de station
                            numeroStation = doc.createElement('stationName')
                            numeroStation.appendChild(doc.createTextNode(noSta))
                            station.appendChild(numeroStation)
                            
                            # Thème MO du stationnement (issus du dictPoints)
                            listePoints = dictPoints['points']['point']
                            theme, nature = '', ''
                            
                            for point in listePoints:
                                if point['pointName'] == noSta :
                                    theme, nature = point['themeMO'], point['natureMO']
                            themeMO, natureMO = doc.createElement('themeMO'), doc.createElement('natureMO')
                            themeMO.appendChild(doc.createTextNode(theme))
                            natureMO.appendChild(doc.createTextNode(nature))
                            station.appendChild(themeMO)
                            station.appendChild(natureMO)
                            
                            # Stationnement
                            stationnement = doc.createElement('stationData')
                            station.appendChild(stationnement)
                            
                            # Hauteur d'instrument I
                            I = doc.createElement('I')
                            I.appendChild(doc.createTextNode(hauteurI))
                            stationnement.appendChild(I)
                            
                            # Erreurs de centrage station manuelles
                            centSta = doc.createElement('stationCentring')
                            plani = doc.createElement('planiStdDev')
                            alti = doc.createElement('altiStdDev')
                            mmPlani = doc.createElement('mm')
                            mmAlti= doc.createElement('mm')
                            mmPlani.appendChild(doc.createTextNode(''))
                            mmAlti.appendChild(doc.createTextNode(''))
                            plani.appendChild(mmPlani)
                            alti.appendChild(mmAlti)
                            centSta.appendChild(plani)
                            centSta.appendChild(alti)
                            stationnement.appendChild(centSta)
                            
                            # Groupe distances (par défaut)
                            groupeDistance = doc.createElement('distanceGroup')
                            groupeDistance.appendChild(doc.createTextNode('groupeDistanceParDefaut'))
                            stationnement.appendChild(groupeDistance)
                            
                            # Groupe directions (par défaut)
                            groupeDirection = doc.createElement('directionGroup')
                            groupeDirection.appendChild(doc.createTextNode('groupeDirectionParDefaut'))
                            stationnement.appendChild(groupeDirection)
                            
                            # Groupe centrage (par défaut)
                            groupeCentrage = doc.createElement('centringGroup')
                            groupeCentrage.appendChild(doc.createTextNode('groupeCentrageParDefaut'))
                            stationnement.appendChild(groupeCentrage)
                            
                            
                            

                        # check pour bien se trouver sur une ligne de visée
                        ligneVis = True
                        if stringLine[60:69] == '         ':
                            ligneVis = False
                            
                        # continue seulement si on se trouve bien sur une ligne de visée
                        if ligneSta == False and ligneVis == True:
                            
                            # Numéro de point visé formaté 
                            noCmne, noPlan, no = stringLine[37:40], stringLine[41:45], stringLine[48:52]
                            lenPlan = len(noPlan.strip())
                            if lenPlan < 4: # Si un no de plan de - de 4 caractère (!= PFP2)
                                reste = 4-lenPlan
                                noPlan = reste*' ' + noPlan.strip()
                            noPt = noCmne + noPlan + '    ' + no 
                            
                            # Récupérations des éléments de l'observation
                            theme, nature, hz, dist, zenith = line[53].strip(), line[57].strip(), line[60:68].strip(), line[78:86].strip(), line[69:77].strip()
                            hauteurS, d1, d2 = line[103:109].strip(), line[87:94].strip(), line[95:102].strip()
                            
                            # Si le thème/nature est None, le remplacer par la valeure issue des point (admise correcte)
                            if theme == '' or nature == '':
                                listePoints = dictPoints['points']['point']
                                for point in listePoints:
                                    if point['pointName'] == noPt :
                                        theme, nature = point['themeMO'], point['natureMO']
                            
                            # Balise observation XML
                            observation = doc.createElement('measure')
                            stationnement.appendChild(observation)
                            
                            # Numéro de point
                            numeroPoint = doc.createElement('pointName')
                            numeroPoint.appendChild(doc.createTextNode(noPt))
                            observation.appendChild(numeroPoint)
                            
                            # Thème MO
                            themeMO = doc.createElement('themeMO')
                            themeMO.appendChild(doc.createTextNode(theme))
                            observation.appendChild(themeMO)
                            
                            # Nature MO
                            natureMO = doc.createElement('natureMO')
                            natureMO.appendChild(doc.createTextNode(nature))
                            observation.appendChild(natureMO)
                            
                            # Direction horizontale et son écart-type
                            RI = doc.createElement('RI')
                            ecartType = doc.createElement('stdDev')
                            cc = doc.createElement('cc')
                            cc.appendChild(doc.createTextNode(''))
                            ecartType.appendChild(cc)
                            valeur = doc.createElement('value')
                            valeur.appendChild(doc.createTextNode(hz))
                            RI.appendChild(ecartType)
                            RI.appendChild(valeur)
                            observation.appendChild(RI)
                            # écarté (bool) 
                            ecarte = doc.createElement('discarded')
                            ecarte.appendChild(doc.createTextNode('')) # ici False par défaut
                            RI.appendChild(ecarte)
                            
                            # Distance inclinée
                            DS = doc.createElement('DS')
                            ecartType = doc.createElement('stdDev') # L'utilisateur pourra la modifier manuellement
                            mm = doc.createElement('mm')
                            mm.appendChild(doc.createTextNode(''))
                            ppm = doc.createElement('ppm')
                            ppm.appendChild(doc.createTextNode(''))
                            valeur = doc.createElement('value')
                            valeur.appendChild(doc.createTextNode(dist))
                            ecartType.appendChild(mm)
                            ecartType.appendChild(ppm)
                            DS.appendChild(ecartType)
                            DS.appendChild(valeur)
                            observation.appendChild(DS)
                            # écarté (bool) 
                            ecarte = doc.createElement('discarded')
                            ecarte.appendChild(doc.createTextNode('')) # ici False par défaut
                            DS.appendChild(ecarte)
                            
                            # Angle zénithal
                            ZD = doc.createElement('ZD')
                            ecartType = doc.createElement('stdDev')
                            cc = doc.createElement('cc')
                            cc.appendChild(doc.createTextNode(''))
                            ecartType.appendChild(cc)
                            valeur = doc.createElement('value')
                            valeur.appendChild(doc.createTextNode(zenith))
                            ZD.appendChild(ecartType)
                            ZD.appendChild(valeur)
                            observation.appendChild(ZD)
                            # écarté (bool) 
                            ecarte = doc.createElement('discarded')
                            ecarte.appendChild(doc.createTextNode('')) # ici False par défaut
                            ZD.appendChild(ecarte)
                            
                            # Hauteur du signal 
                            S = doc.createElement('S')
                            valeur = doc.createElement('value')
                            valeur.appendChild(doc.createTextNode(hauteurS))
                            S.appendChild(valeur)
                            observation.appendChild(S)
                            
                            # Déplacement dm1 
                            dm1 = doc.createElement('dm1')
                            valeur = doc.createElement('value')
                            valeur.appendChild(doc.createTextNode(d1))
                            dm1.appendChild(valeur)
                            observation.appendChild(dm1)
                            
                            # Déplacement dm2 
                            dm2 = doc.createElement('dm2')
                            valeur = doc.createElement('value')
                            valeur.appendChild(doc.createTextNode(d2))
                            dm2.appendChild(valeur)
                            observation.appendChild(dm2)
                            
                            # centrage manuel point visée
                            centVis = doc.createElement('targetCentring')
                            plani = doc.createElement('planiStdDev')
                            alti = doc.createElement('altiStdDev')
                            mmPlani = doc.createElement('mm')
                            mmAlti= doc.createElement('mm')
                            mmPlani.appendChild(doc.createTextNode(''))
                            mmAlti.appendChild(doc.createTextNode(''))
                            plani.appendChild(mmPlani)
                            alti.appendChild(mmAlti)
                            centVis.appendChild(plani)
                            centVis.appendChild(alti)
                            observation.appendChild(centVis)
                            
                            

                            

                    #----------------------
  ####              # --- SESSIONS GNSS ---
                    #----------------------
                    
                    if GK == '71' and stringLine[60:71] != '           ' and stringLine[6] == '!' and stringLine[2].isdigit():
                        
                        # Numéro de point
                        noCmne, noPlan, no = stringLine[7:10], stringLine[11:15], stringLine[18:22]
                        lenPlan = len(noPlan.strip())
                        if lenPlan < 4: # Si pas un numéro de plan
                            reste = 4-lenPlan
                            noPlan = reste*' ' + noPlan.strip()
                        noPt = noCmne + noPlan + '    ' + no
                        ligneSta = True
                        
                        if stringLine[35:58] == '                       ': #première ligne, création session GNSS
                            
                            # Incrément pour Sxxx
                            nSessionIncr += 1
                            
                            # Initialisation de la balise de la session
                            Session = doc.createElement('session')
                            GNSS.appendChild(Session)
                            
                            # Nom de la session (ici incrémenté de S1 à Sxxx, mais nimporte quel str possible)
                            nomSession = doc.createElement('sessionName')
                            nomSession.appendChild(doc.createTextNode('S'+str(nSessionIncr)))
                            Session.appendChild(nomSession)
                            
                            # Groupe paramètres de sessions (par défaut)
                            groupeParam = doc.createElement('gnssGroup')
                            groupeParam.appendChild(doc.createTextNode('groupeGNSSParDefaut'))
                            Session.appendChild(groupeParam)
                        
                        else: # autres lignes de la séquence
                        
                            # Numéro de point visé formaté 
                            noCmne, noPlan, no = stringLine[37:40], stringLine[41:45], stringLine[48:52]
                            lenPlan = len(noPlan.strip())
                            if lenPlan < 4: # Si un no de plan de - de 4 caractère (!= PFP2)
                                reste = 4-lenPlan
                                noPlan = reste*' ' + noPlan.strip()
                            noPt = noCmne + noPlan + '    ' + no
                            
                            
                        # Récupération des éléments 
                        theme,nature = stringLine[53].strip(), stringLine[57].strip()
                        est, nord, alt = stringLine[60:72].strip(), stringLine[74:86].strip(), stringLine[93:101].strip() 
                        
                        # Si le thème/nature est None, le remplacer par la valeure issue des point (admise correcte)
                        if theme == '' or nature == '':
                            listePoints = dictPoints['points']['point']
                            for point in listePoints:
                                if point['pointName'] == noPt :
                                    theme, nature = point['themeMO'], point['natureMO']
                        
                        # Balise observation XML 
                        observation = doc.createElement('measure')
                        Session.appendChild(observation) 
                        
                        # Numéro de point
                        numeroPoint = doc.createElement('pointName')
                        numeroPoint.appendChild(doc.createTextNode(noPt))
                        observation.appendChild(numeroPoint)
                        
                        # Thème MO
                        themeMO = doc.createElement('themeMO')
                        themeMO.appendChild(doc.createTextNode(theme))
                        observation.appendChild(themeMO)
                        
                        # Nature MO
                        natureMO = doc.createElement('natureMO')
                        natureMO.appendChild(doc.createTextNode(nature))
                        observation.appendChild(natureMO)
                        
                        # Observation LY
                        LY = doc.createElement('LY')
                        ecartType = doc.createElement('stdDev')
                        mm = doc.createElement('mm')
                        mm.appendChild(doc.createTextNode(''))
                        ecartType.appendChild(mm)
                        valeur = doc.createElement('value')
                        valeur.appendChild(doc.createTextNode(est))
                        LY.appendChild(ecartType)
                        LY.appendChild(valeur)
                        observation.appendChild(LY)
                        # écarté (bool) 
                        ecarte = doc.createElement('discarded')
                        ecarte.appendChild(doc.createTextNode('')) # ici False par défaut
                        LY.appendChild(ecarte)
                        
                        # Observation LX
                        LX = doc.createElement('LX')
                        ecartType = doc.createElement('stdDev')
                        mm = doc.createElement('mm')
                        mm.appendChild(doc.createTextNode(''))
                        ecartType.appendChild(mm)
                        valeur = doc.createElement('value')
                        valeur.appendChild(doc.createTextNode(nord))
                        LX.appendChild(ecartType)
                        LX.appendChild(valeur)
                        observation.appendChild(LX)
                        # écarté (bool) 
                        ecarte = doc.createElement('discarded')
                        ecarte.appendChild(doc.createTextNode('')) # ici False par défaut
                        LX.appendChild(ecarte)
                        
                        # Observation LH
                        LH = doc.createElement('LH')
                        ecartType = doc.createElement('stdDev')
                        mm = doc.createElement('mm')
                        mm.appendChild(doc.createTextNode(''))
                        ecartType.appendChild(mm)
                        valeur = doc.createElement('value')
                        valeur.appendChild(doc.createTextNode(alt))
                        LH.appendChild(ecartType)
                        LH.appendChild(valeur)
                        observation.appendChild(LH)
                        # écarté (bool) 
                        ecarte = doc.createElement('discarded')
                        ecarte.appendChild(doc.createTextNode('')) # ici False par défaut
                        LH.appendChild(ecarte)
                    

                    
                    
                    #------------------------
  ####              # --- SYSTEMES LOCAUX ---
                    #------------------------
                    
                    #### ------ LEVE ORTHOGONAL ET DISTANCES CUMULEES
                    
                    if (GK == '24' or GK == '23') and stringLine[60:71] != '           ' and stringLine[6] == '!' and stringLine[2].isdigit():
                                                
                        # Numéro de point
                        noCmne, noPlan, no = stringLine[7:10], stringLine[11:15], stringLine[18:22]
                        lenPlan = len(noPlan.strip())
                        if lenPlan < 4: # Si pas un numéro de plan
                            reste = 4-lenPlan
                            noPlan = reste*' ' + noPlan.strip()
                        noPt = noCmne + noPlan + '    ' + no
                        ligneSta = True
                        
                        if stringLine[35:58] == '                       ': #première ligne, création du systeme local
                            
                            # Initialisation de la balise de la session
                            systemeLocal = doc.createElement('localSystem')
                            systemesLocaux.appendChild(systemeLocal)
                            
                            # Nom système local
                            nomSystemeLocal = doc.createElement('localSystemName')
                            nomSystemeLocal.appendChild(doc.createTextNode('sysLoc{:d}'.format(noSys)))
                            noSys += 1
                            systemeLocal.appendChild(nomSystemeLocal)
                            
                            # Groupe système local par défaut 
                            groupeSystemeLocal = doc.createElement('localSystemGroup')
                            groupeSystemeLocal.appendChild(doc.createTextNode('groupeSystemeLocalParDefaut'))
                            systemeLocal.appendChild(groupeSystemeLocal)
                            
                        else: # autres lignes de la séquence
                        
                            # Numéro de point visé formaté 
                            noCmne, noPlan, no = stringLine[37:40], stringLine[41:45], stringLine[48:52]
                            lenPlan = len(noPlan.strip())
                            if lenPlan < 4: # Si un no de plan de - de 4 caractère (!= PFP2)
                                reste = 4-lenPlan
                                noPlan = reste*' ' + noPlan.strip()
                            noPt = noCmne + noPlan + '    ' + no
                            
                        # Récupération des éléments de la première ligne du systeme local
                        theme,nature = stringLine[53].strip(), stringLine[57].strip()
                        y, x = str(-float(stringLine[60:72].strip())), stringLine[74:86].strip()  
                        
                        # Distances cumulées  (GK = 23) -> coord x = 0.000
                        if GK == '23': 
                            x = '0.000'
                        
                        # Si le thème/nature est None, le remplacer par la valeure issue des point (admise correcte)
                        if theme == '' or nature == '':
                            listePoints = dictPoints['points']['point']
                            for point in listePoints:
                                if point['pointName'] == noPt :
                                    theme, nature = point['themeMO'], point['natureMO']
                        
                        # Balise observation XML 
                        observation = doc.createElement('measure')
                        systemeLocal.appendChild(observation) 
                        
                        # Numéro de point
                        numeroPoint = doc.createElement('pointName')
                        numeroPoint.appendChild(doc.createTextNode(noPt))
                        observation.appendChild(numeroPoint)
                        
                        # Thème MO
                        themeMO = doc.createElement('themeMO')
                        themeMO.appendChild(doc.createTextNode(theme))
                        observation.appendChild(themeMO)
                        
                        # Nature MO
                        natureMO = doc.createElement('natureMO')
                        natureMO.appendChild(doc.createTextNode(nature))
                        observation.appendChild(natureMO)
                        
                        # Observation LY
                        LY = doc.createElement('LY')
                        ecartType = doc.createElement('stdDev')
                        mm = doc.createElement('mm')
                        mm.appendChild(doc.createTextNode(''))
                        ecartType.appendChild(mm)
                        valeur = doc.createElement('value')
                        valeur.appendChild(doc.createTextNode(y))
                        LY.appendChild(ecartType)
                        LY.appendChild(valeur)
                        observation.appendChild(LY)
                        # écarté (bool) 
                        ecarte = doc.createElement('discarded')
                        ecarte.appendChild(doc.createTextNode('')) # ici False par défaut
                        LY.appendChild(ecarte)
                        
                        # Observation LX
                        LX = doc.createElement('LX')
                        ecartType = doc.createElement('stdDev')
                        mm = doc.createElement('mm')
                        mm.appendChild(doc.createTextNode(''))
                        ecartType.appendChild(mm)
                        valeur = doc.createElement('value')
                        valeur.appendChild(doc.createTextNode(x))
                        LX.appendChild(ecartType)
                        LX.appendChild(valeur)
                        observation.appendChild(LX)
                        # écarté (bool) 
                        ecarte = doc.createElement('discarded')
                        ecarte.appendChild(doc.createTextNode('')) # ici False par défaut
                        LX.appendChild(ecarte)
                        
                
                    
                    #### ------ CHEMINEMENT ORTHOGONAL
                    
                    if GK == '27' and stringLine[6] == '!' and stringLine[2].isdigit():       
                        
                        noCmne, noPlan, no = stringLine[7:10], stringLine[11:15], stringLine[18:22]
                        lenPlan = len(noPlan.strip())
                        if lenPlan < 4: # Si pas un numéro de plan
                            reste = 4-lenPlan
                            noPlan = reste*' ' + noPlan.strip()
                        noPt = noCmne + noPlan + '    ' + no
                        premierPoint = True
                        
                        
                        #première ligne, création du systeme local
                        if stringLine[4:6] == GK and stringLine[35:58] == '                       ': 
                        
                            # Initialisation de la balise de la session
                            systemeLocal = doc.createElement('localSystem')
                            systemesLocaux.appendChild(systemeLocal)
                            
                            # Nom système local
                            nomSystemeLocal = doc.createElement('localSystemName')
                            nomSystemeLocal.appendChild(doc.createTextNode('sysLoc{:d}'.format(noSys)))
                            noSys += 1
                            systemeLocal.appendChild(nomSystemeLocal)
                            
                            # Groupe système local par défaut 
                            groupeSystemeLocal = doc.createElement('localSystemGroup')
                            groupeSystemeLocal.appendChild(doc.createTextNode('groupeSystemeLocalParDefaut'))
                            systemeLocal.appendChild(groupeSystemeLocal)
                            
                            # Création de la liste des yx
                            listeCotes = [0.0] # première cote = 0.0
                        
                        elif stringLine[35:58] != '                       ': # autres lignes de la séquence
                        
                            # Numéro de point visé formaté 
                            noCmne, noPlan, no = stringLine[37:40], stringLine[41:45], stringLine[48:52]
                            lenPlan = len(noPlan.strip())
                            if lenPlan < 4: # Si un no de plan de - de 4 caractère (!= PFP2)
                                reste = 4-lenPlan
                                noPlan = reste*' ' + noPlan.strip()
                            noPt = noCmne + noPlan + '    ' + no
                            premierPoint = False
                        
                        
                        # PASSAGE DE COTES SIGNEES EN SYSTEME LOCAL
                        
                        if premierPoint:  # le premier point à 0.0,0.0 comme coordonnées locales yx
                            
                            # Récupération des éléments de la première ligne du systeme local
                            theme,nature = stringLine[53].strip(), stringLine[57].strip()
                            y, x = '0.000', '0.000'
                        
                        else:  # les autres yx sont à générer à chaque fois avec la liste des cotes MAJ
                            cote = float(stringLine[60:72].strip())
                            i = len(listeCotes)   # get la longueur pour récupérer yx ensuite
                            listeCotes.append(cote)
                            listeYX = geometrieUtils.chOrtho2systemeLocal(listeCotes)
                            y, x = str(round(listeYX[i,0],3)), str(round(listeYX[i,1],3))

                        
                        # Tri pour ne pas garder les éventuelles lignes vides et écrire le XML d'un seul coup pour le premier point et les suivants
                        if noPt != '               ' and stringLine[8] != 'S' :
                            
                            # Récupérer le thème/nature
                            theme,nature = stringLine[53].strip(), stringLine[57].strip()
                            
                            # Si le thème/nature est None, le remplacer par la valeure issue des point (admise correcte)
                            if theme == '' or nature == '':
                                listePoints = dictPoints['points']['point']
                                for point in listePoints:
                                    if point['pointName'] == noPt :
                                        theme, nature = point['themeMO'], point['natureMO']
                            
                            # Balise observation XML 
                            observation = doc.createElement('measure')
                            systemeLocal.appendChild(observation) 
                            
                            # Numéro de point
                            numeroPoint = doc.createElement('pointName')
                            numeroPoint.appendChild(doc.createTextNode(noPt))
                            observation.appendChild(numeroPoint)
                            
                            # Thème MO
                            themeMO = doc.createElement('themeMO')
                            themeMO.appendChild(doc.createTextNode(theme))
                            observation.appendChild(themeMO)
                            
                            # Nature MO
                            natureMO = doc.createElement('natureMO')
                            natureMO.appendChild(doc.createTextNode(nature))
                            observation.appendChild(natureMO)
                            
                            # Observation LY
                            LY = doc.createElement('LY')
                            ecartType = doc.createElement('stdDev')
                            mm = doc.createElement('mm')
                            mm.appendChild(doc.createTextNode(''))
                            ecartType.appendChild(mm)
                            valeur = doc.createElement('value')
                            valeur.appendChild(doc.createTextNode(y))
                            LY.appendChild(ecartType)
                            LY.appendChild(valeur)
                            observation.appendChild(LY)
                            # écarté (bool) 
                            ecarte = doc.createElement('discarded')
                            ecarte.appendChild(doc.createTextNode('')) # ici False par défaut
                            LY.appendChild(ecarte)
                            
                            # Observation LX
                            LX = doc.createElement('LX')
                            ecartType = doc.createElement('stdDev')
                            mm = doc.createElement('mm')
                            mm.appendChild(doc.createTextNode(''))
                            ecartType.appendChild(mm)
                            valeur = doc.createElement('value')
                            valeur.appendChild(doc.createTextNode(x))
                            LX.appendChild(ecartType)
                            LX.appendChild(valeur)
                            observation.appendChild(LX)
                            # écarté (bool) 
                            ecarte = doc.createElement('discarded')
                            ecarte.appendChild(doc.createTextNode('')) # ici False par défaut
                            LX.appendChild(ecarte)
                            
                        
                        
                        
                    #--------------
  ####              # --- COTES ---
                    #--------------    

                    if GK == '28' and stringLine[6] == '!' and stringLine[2].isdigit():
                        
                        # Filtrer le point 1 (fichier ll1 particulier pour GK 28)
                        if (stringLine[4:6] == GK or stringLine[35:58] == '                       ') and stringLine[7:22] != '               ' and stringLine[8] != 'S':
                            # Numero du point 1 formaté 
                            noCmne, noPlan, no = stringLine[7:10], stringLine[11:15], stringLine[18:22]
                            lenPlan = len(noPlan.strip())
                            if lenPlan < 4: # Si pas un numéro de plan
                                reste = 4-lenPlan
                                noPlan = reste*' ' + noPlan.strip()
                            noPt1 = noCmne + noPlan + '    ' + no
                            
                            # Initialisation de la balise de la cote
                            cote = doc.createElement('simpleMeasure')
                            cotes.appendChild(cote)
                            
                            # nom du groupe de cote
                            groupeCote = doc.createElement('simpleMeasureGroup')
                            groupeCote.appendChild(doc.createTextNode('groupeCoteParDefaut'))
                            cote.appendChild(groupeCote)
                            
                            # Observation
                            observation = doc.createElement('measure')
                            cote.appendChild(observation)
                            
                            # Numéro du point 1
                            numeroPoint1 = doc.createElement('pointName1')
                            numeroPoint1.appendChild(doc.createTextNode(noPt1))
                            observation.appendChild(numeroPoint1)
                            
                            
                        # Filtrer le point 2
                        if stringLine[7:22] == '               ' and stringLine[35:58] != '                       ': 
                            # Numero du point 2 formaté 
                            noCmne, noPlan, no = stringLine[37:40], stringLine[41:45], stringLine[48:52]
                            lenPlan = len(noPlan.strip())
                            if lenPlan < 4: # Si un no de plan de - de 4 caractère (!= PFP2)
                                reste = 4-lenPlan
                                noPlan = reste*' ' + noPlan.strip()
                            noPt2 = noCmne + noPlan + '    ' + no
                            valCote = line[60:68].strip()
                            
                            # Numéro du point 2
                            numeroPoint2 = doc.createElement('pointName2')
                            numeroPoint2.appendChild(doc.createTextNode(noPt2))
                            observation.appendChild(numeroPoint2)
                            
                            # Distance horiz. dans le plan proj. DP
                            DP = doc.createElement('DP')
                            observation.appendChild(DP)
                            # écart-type
                            ecartType = doc.createElement('stdDev')
                            DP.appendChild(ecartType)
                            mm = doc.createElement('mm')
                            mm.appendChild(doc.createTextNode(''))
                            ecartType.appendChild(mm)
                            # valeur
                            valeur = doc.createElement('value')
                            valeur.appendChild(doc.createTextNode(valCote))
                            DP.appendChild(valeur)
                            # écarté (bool) 
                            ecarte = doc.createElement('discarded')
                            ecarte.appendChild(doc.createTextNode('')) # ici False par défaut
                            DP.appendChild(ecarte)
                            


                    #--------------------
  ####              # --- CONTRAINTES ---
                    #--------------------                       
                    
                    #### ------ ALIGNEMENT
                    
                    if GK == '25' and stringLine[6] == '!' and stringLine[2].isdigit():
                        
                        # pour le noVis, il faut veiller -> identique au noVis du calcul des PFP3
                        if stringLine[4:6] == GK: # première ligne de la séquence
                            noCmne, noPlan, no = stringLine[7:10], stringLine[11:15], stringLine[18:22]
                            lenPlan = len(noPlan.strip())
                            if lenPlan < 4: # Si pas un numéro de plan
                                reste = 4-lenPlan
                                noPlan = reste*' ' + noPlan.strip()
                            noPtA = noCmne + noPlan + '    ' + no
                        else: #autres lignes de la séquence
                            noCmne, noPlan, no = stringLine[37:40], stringLine[41:45], stringLine[48:52]
                            lenPlan = len(noPlan.strip())
                            if lenPlan < 4: # Si un no de plan de - de 4 caractère (!= PFP2)
                                reste = 4-lenPlan
                                noPlan = reste*' ' + noPlan.strip()
                            noPt = noCmne + noPlan + '    ' + no
                        
                        if stringLine[35:58] == '                       ': #première ligne, création contrainte

                            # Initialisation de la balise de la cote
                            contrainte = doc.createElement('constraint')
                            contraintes.appendChild(contrainte)
                            
                            # Type contrainte
                            typeContrainte = doc.createElement('constraintType')
                            typeContrainte.appendChild(doc.createTextNode('alignment'))
                            contrainte.appendChild(typeContrainte)
                            
                            # Balise du point A
                            ptContr = doc.createElement('point')
                            pointName = doc.createElement('pointName')
                            pointName.appendChild(doc.createTextNode(noPtA))
                            pointType = doc.createElement('pointTypeInConstraint')
                            pointType.appendChild(doc.createTextNode('A'))
                            ptContr.appendChild(pointName) 
                            ptContr.appendChild(pointType) 
                            contrainte.appendChild(ptContr)
                            
                        elif stringLine[35:36] == 'B': # point B
                    
                            # Balise du point B
                            ptContr = doc.createElement('point')
                            pointName = doc.createElement('pointName')
                            pointName.appendChild(doc.createTextNode(noPt))
                            pointType = doc.createElement('pointTypeInConstraint')
                            pointType.appendChild(doc.createTextNode('B'))
                            ptContr.appendChild(pointName) 
                            ptContr.appendChild(pointType) 
                            contrainte.appendChild(ptContr)
                            
                        elif stringLine[35:36] == ' ': # point P

                            # Balise du point P
                            ptContr = doc.createElement('point')
                            pointName = doc.createElement('pointName')
                            pointName.appendChild(doc.createTextNode(noPt))
                            pointType = doc.createElement('pointTypeInConstraint')
                            pointType.appendChild(doc.createTextNode('P'))
                            ptContr.appendChild(pointName) 
                            ptContr.appendChild(pointType) 
                            contrainte.appendChild(ptContr)
                            
                            # Autres balises de la contrainte
                            ecarte = doc.createElement('discarded')
                            ecarte.appendChild(doc.createTextNode('')) # ici False par défaut
                            contrainte.appendChild(ecarte)
                            # dm1 : décalage parralèlle
                            d1 = stringLine[87:94].strip()
                            dm1 = doc.createElement('dm1')
                            valeur = doc.createElement('value')
                            valeur.appendChild(doc.createTextNode(d1))
                            dm1.appendChild(valeur)
                            contrainte.appendChild(dm1)
                                                    
                            
                    #### ------ PERPENDICULAIRE
                    
                    if GK == '26' and stringLine[6] == '!' and stringLine[2].isdigit():
                        
                        # pour le noVis, il faut veiller -> identique au noVis du calcul des PFP3
                        if stringLine[4:6] == GK: # première ligne de la séquence
                            noCmne, noPlan, no = stringLine[7:10], stringLine[11:15], stringLine[18:22]
                            lenPlan = len(noPlan.strip())
                            if lenPlan < 4: # Si pas un numéro de plan
                                reste = 4-lenPlan
                                noPlan = reste*' ' + noPlan.strip()
                            noPt = noCmne + noPlan + '    ' + no
                        else: #autres lignes de la séquence
                            noCmne, noPlan, no = stringLine[37:40], stringLine[41:45], stringLine[48:52]
                            lenPlan = len(noPlan.strip())
                            if lenPlan < 4: # Si un no de plan de - de 4 caractère (!= PFP2)
                                reste = 4-lenPlan
                                noPlan = reste*' ' + noPlan.strip()
                            noPt = noCmne + noPlan + '    ' + no
                        
                        if stringLine[35:58] == '                       ': #première ligne, création contrainte

                            # Initialisation de la balise de la cote
                            contrainte = doc.createElement('constraint')
                            contraintes.appendChild(contrainte)
                            
                            # Type contrainte
                            typeContrainte = doc.createElement('constraintType')
                            typeContrainte.appendChild(doc.createTextNode('perpendicular'))
                            contrainte.appendChild(typeContrainte)
                            
                            # Balise du point A
                            ptContr = doc.createElement('point')
                            pointName = doc.createElement('pointName')
                            pointName.appendChild(doc.createTextNode(noPtA))
                            pointType = doc.createElement('pointTypeInConstraint')
                            pointType.appendChild(doc.createTextNode('A'))
                            ptContr.appendChild(pointName) 
                            ptContr.appendChild(pointType) 
                            contrainte.appendChild(ptContr)
                            
                        if stringLine[18:22] != '    ': # point B
                            
                            # Balise du point B
                            ptContr = doc.createElement('point')
                            pointName = doc.createElement('pointName')
                            pointName.appendChild(doc.createTextNode(noPt))
                            pointType = doc.createElement('pointTypeInConstraint')
                            pointType.appendChild(doc.createTextNode('B'))
                            ptContr.appendChild(pointName) 
                            ptContr.appendChild(pointType) 
                            contrainte.appendChild(ptContr)
                            
                        else: # point P
                            
                            # Balise du point P
                            ptContr = doc.createElement('point')
                            pointName = doc.createElement('pointName')
                            pointName.appendChild(doc.createTextNode(noPt))
                            pointType = doc.createElement('pointTypeInConstraint')
                            pointType.appendChild(doc.createTextNode('P'))
                            ptContr.appendChild(pointName) 
                            ptContr.appendChild(pointType) 
                            contrainte.appendChild(ptContr)
                            
                            # écarté (bool) 
                            ecarte = doc.createElement('discarded')
                            ecarte.appendChild(doc.createTextNode('')) # ici False par défaut
                            contrainte.appendChild(ecarte)
                            # dm1 (NON DEFINI ET A NE PAS UTILISER POUR LE MOMENT)
                            d1 = stringLine[87:94].strip()
                            dm1 = doc.createElement('dm1')
                            valeur = doc.createElement('value')
                            valeur.appendChild(doc.createTextNode(d1))
                            dm1.appendChild(valeur)
                            contrainte.appendChild(dm1)
                            


        line = fichier.readline()
        
    fichier.close()
    
    
      #----------------------------
####  # --- BALISES PRINCIPALES ---
      #----------------------------
    
    # Balises principales du XML (savoir si il y'en a pour éviter de les créer pour rien et faire rater les checks de cohérences)
    if polaire.hasChildNodes():
        canevas.appendChild(polaire)
    if GNSS.hasChildNodes():
        canevas.appendChild(GNSS)
    if systemesLocaux.hasChildNodes():
        canevas.appendChild(systemesLocaux)
    if cotes.hasChildNodes():
        canevas.appendChild(cotes)
    if contraintes.hasChildNodes():
        canevas.appendChild(contraintes)
    

      #---------------------
####  # --- FINALISATION ---
      #---------------------
      
    xml_str = doc.toprettyxml(indent = 4*" ")
    with open(filePathOutput, "w", encoding=('utf-8')) as f:
        f.write(xml_str) 
    
    
    return None



def points2xml(filePathll1, filePathOutput):
    
    """
    Transformation des coordonnées des points fixes et calculés par Homère via 
    le fichier résultat .ll1 en un fichier de coordonnée approchées XML

    Parameters
    ----------
    filePathll1 : string (ne pas oublier les doubles backslash)
        Lien vers le fichier ll1.
    filePathOutput : string (ne pas oublier les doubles backslash)
        Lien vers le fichier d'export XML

    Returns
    -------
    None.

    """
    
    # Initialisation du format XML des points
    doc = minidom.Document()
    points = doc.createElement('points')
    doc.appendChild(points)
    
    
    # Liste des No de point pour ne pas les ajouter à double
    listeNoPts = []
    
    zonePtsFixes = False
    zonePtsNouv = False
    with open(filePathll1,'r') as f:

        for line in f:
            
            line = line.rstrip() # enlever le \n en fin de ligne
            
            
            #---------------------
  ####      # --- POINTS FIXES ---  /!\ Ne sont dinstigués des autres uniquement dans le fichier paramètres
            #---------------------
            
            # parser uniquement dès cette indication (points fixes)
            if line[0:23] == 'POINTS DONNES CONFORMES':
                zonePtsFixes = True
                
            # si il y'a bien des coordonnées (= on se trouve sur une ligne de point)
            if zonePtsFixes and line[39:40] == '2': 
                
                # Conserver le No de cmne + plan jusqu'au prochains
                if line[1:4] != '   ':
                    noCmne = line[1:4]
                    noPlan = line[6:10]
                
                # récupérer les éléments du ll1
                noPt = noCmne + noPlan + '   ' + line[17:22] # formattage pour correspondre au string du Canevas
                theme = line[26:27]
                nature = line[31:32]
                E, N = line[39:51].strip(), line[52:64].strip()
                
                # Initialisation de la balise du point
                point = doc.createElement('point')
                if noPt not in listeNoPts: # éviter les doublons
                    points.appendChild(point)
                    listeNoPts.append(noPt)
                
                # Numéro
                numeroPoint = doc.createElement('pointName')
                numeroPoint.appendChild(doc.createTextNode(noPt))
                point.appendChild(numeroPoint)
                
                # Thème MO
                themeMO = doc.createElement('themeMO')
                themeMO.appendChild(doc.createTextNode(theme))
                point.appendChild(themeMO)
                
                # Nature MO
                natureMO = doc.createElement('natureMO')
                natureMO.appendChild(doc.createTextNode(nature))
                point.appendChild(natureMO)
                
                # Est
                Est = doc.createElement('E')
                Est.appendChild(doc.createTextNode(E))
                point.appendChild(Est)
                
                # Nord
                Nord = doc.createElement('N')
                Nord.appendChild(doc.createTextNode(N))
                point.appendChild(Nord)
                
                # H (pas besoin d'altitude approchée -> str vide)
                Ha = doc.createElement('H')
                Ha.appendChild(doc.createTextNode(''))
                point.appendChild(Ha)
                

            # Le parsing des points fixes se stoppe ici
            if line[0:17] == 'LISTE DES MESURES':
                zonePtsFixes = False
            
            

            #----------------------
  ####      # --- AUTRES POINTS ---  /!\ Ne sont dinstigués des pts fixes uniquement dans le fichier paramètres
            #----------------------      
        
            # parser uniquement dès cette indication (points nouv.)
            if line[0:25] == 'POINTS NOUVEAUX CONFORMES':
                zonePtsNouv = True
              
            # si il y'a bien des coordonnées (= on se trouve sur une ligne de point)
            if zonePtsNouv and line[27:28] == '2': 
                
                # Conserver le No de cmne + plan jusqu'au prochains
                if line[1:4] != '   ':
                    noCmne = line[1:4]
                    noPlan = line[5:9]
                    
                # récupérer les éléments du ll1
                noPt = noCmne + noPlan + '    ' + line[13:17] # formattage pour correspondre au string du Canevas
                theme = line[19:20]
                nature = line[22:23]
                E, N = line[27:38].strip(), line[39:50].strip()
                
                # Initialisation de la balise du point
                point = doc.createElement('point')
                if noPt not in listeNoPts: # éviter les doublons
                    points.appendChild(point)
                    listeNoPts.append(noPt)
                
                # Numéro
                numeroPoint = doc.createElement('pointName')
                numeroPoint.appendChild(doc.createTextNode(noPt))
                point.appendChild(numeroPoint)
                
                # Thème MO
                themeMO = doc.createElement('themeMO')
                themeMO.appendChild(doc.createTextNode(theme))
                point.appendChild(themeMO)
                
                # Nature MO
                natureMO = doc.createElement('natureMO')
                natureMO.appendChild(doc.createTextNode(nature))
                point.appendChild(natureMO)
                
                # Est
                Est = doc.createElement('E')
                Est.appendChild(doc.createTextNode(E))
                point.appendChild(Est)
                
                # Nord
                Nord = doc.createElement('N')
                Nord.appendChild(doc.createTextNode(N))
                point.appendChild(Nord)
                
                # H (pas besoin d'altitude approchée -> str vide)
                Ha = doc.createElement('H')
                Ha.appendChild(doc.createTextNode(''))
                point.appendChild(Ha)
                
                # Parfois la nature ou le thème est vide ou mal encol., -> affiche la ligne possédant une erreur dans le .ll1
                try:
                    int(theme) # doit être int
                except:
                    print("la nature n'est pas une entier à : \n", line)
                try:
                    int(nature) # doit être int
                except:
                    print("la nature n'est pas une entier à : \n", line)
                    
                    
                
            # Le parsing des points fixes se stoppe ici
            if line[0:40] == 'REFERENCES CROISEES (TOUTES LES MESURES)':
                zonePtsNouv = False
    

    
    
    # --- FINALISATION ET GENERATION DU FICHIER XML ---
    xml_str = doc.toprettyxml(indent = 4*" ")
    with open(filePathOutput, "w", encoding=('utf-8')) as f:
        f.write(xml_str) 
    
    
    return None



def LTOPKOO2xml(filePathKOO, filePathOutput):
    
    """
    Transformation du fichier de points .KOO de LTOP à XML.
    
    Parameters
    ----------
    filePathKOO : string (ne pas oublier les doubles backslash)
        Lien vers le fichier .ll1 
    filePathOutput : string (ne pas oublier les doubles backslash)
        Lien vers le fichier d'export XML
        
    Returns
    -------
    None.

    """
    dictPoints = {'points':{'point':[]}}
    with open(filePathKOO, 'r') as f:
        
        for line in f:
            line = line.rstrip() 
            
            if line[0:2] != '  ' and len(line[0:2]) > 0 and line[0:2] != '**' and line[0:2] != '$$': # Si 2 premiers caractères vides et la ligne pas vide
            
                # Récupération des éléments et ajout au dict des pts
                noPt, E, N, H = line[0:12].strip(), line[32:44].strip(), line[44:56].strip(), line[61:70].strip()
                pt = {'pointName':noPt,
                      'E':E,
                      'N':N,
                      'H':H}
                
                dictPoints['points']['point'].append(pt)
            
    # conversion dict to XML
    dictionnaire2xml(dictPoints, filePathOutput)
    
    print('\nLTOP KOO conversion to points XML successfully executed\n')
            


def LTOPMES2xml(filePathMES, filePathOutput):
    
    """
    
    
    !!! FONCTION A REFAIRE OU MODIFIER
    
    
    Transformation du fichier de mesure .MES de LTOP à XML.
    Parse d'abord le fichier LTOP pour trouver les points visés par sessions ou stations. 
    -> Ne prend pas en compte l'ordre des lignes, l'importance est le numéro du point.
    Si il manque un type de mesure, n'ajoute pas la visée (ex. si il manque LX et qu'il y a que LY et LH, n'ajoute aucune <measure>).

    Parameters
    ----------
    filePathMES : string (ne pas oublier les doubles backslash)
        Lien vers le fichier .ll1 
    filePathOutput : string (ne pas oublier les doubles backslash)
        Lien vers le fichier d'export XML
        
    Returns
    -------
    None.

    """

    #### LECTURE FICHEIR MES 
    
    # Initialisation
    listeLTOPsessions, listeLTOPstations = [], []
    
    # Lecture du fichier MES et pré-stockage des éléments de chaque station/session (avant la conversion XML, car LY/LX/LH peuvent être séparés)
    with open(filePathMES, 'r') as f:
        
        
        for line in f:
            line = line.rstrip() 
            
            if line[0:2] != '  ' and len(line[0:2]) > 0 and line[0:2] != '**' and line[0:2] != '$$': # Si 2 premiers caractères vides et la ligne pas vide
                indice = line[0:2]
                
                
            
                #### # --- LEVE POLAIRE
                
                if indice == 'ST' : # append et création de la session (la première est vide)
                    # nom
                    nomStation = line[2:14].strip()
                    I = line[46:53].strip()
                    
                    # Si la dernière station a le même nom, alors fusionne
                    if len(listeLTOPstations) > 0 and listeLTOPstations[-1]['stationName'] != nomStation:
                        listeLTOPstations.append({'stationName':nomStation,
                                                  'I': I,
                                                  'pointsVises':{}})
                    # Ecrire la première station
                    elif len(listeLTOPstations) == 0:
                        listeLTOPstations.append({'stationName':nomStation,
                                                  'I': I,
                                                  'pointsVises':{}})
                
                elif indice == 'RI' or indice == 'DS' or indice == 'HW' or indice =='ZD' or indice =='DP':
                    
                    # Ajout à la station courante (dernière de la liste)
                    pointName, stdDev, value = line[2:14].strip(), line[36:40].strip(), line[24:35].strip()
                    if indice=='ZD' or indice =='HW':
                        S = line[51:58].strip() # première occurence de S sur un point visé (car cité une fois pour chaque type d'obs. dans le MES, donc jusqu'à 3x par visée)
                    else: 
                        S = ''
                    # Si angle verticlal HW, le convertir en ZD (= 100.0-HW (avec signe))
                    if indice == 'HW':
                        indice = 'ZD'
                        value = "{:0.4f}".format(100.0-float(value.replace(' ','')))
                    # Si le no de point n'est pas dans la liste LTOP, crée une occurence
                    if pointName not in listeLTOPstations[-1]['pointsVises'].keys():
                        S = line[51:58].strip() 
                        listeLTOPstations[-1]['pointsVises'].update({pointName:{indice:[stdDev, value, S]}})
                    else:
                        listeLTOPstations[-1]['pointsVises'][pointName].update({indice:[stdDev, value, S]})
                    
            

            
                #### # --- SESSIONS GNSS 
                
                if indice == 'SL' : # append et création de la session (la première est vide)
                    
                    # nom
                    nomSession = line[2:14].strip()
                    listeLTOPsessions.append({'sessionName':nomSession,
                                              'pointsVises':{}})
                
                elif indice == 'LY' or indice == 'LX' or indice == 'LH':
                    
                    # Ajout à la session courante (dernière de la liste)
                    pointName, stdDev, value = line[2:14].strip(), line[36:40].strip(), line[24:35].strip()
                    # Si le no de point n'est pas dans la liste LTOP, crée une occurence
                    if pointName not in listeLTOPsessions[-1]['pointsVises'].keys():
                        listeLTOPsessions[-1]['pointsVises'].update({pointName:{indice:[stdDev, value]}})
                    else:
                        listeLTOPsessions[-1]['pointsVises'][pointName].update({indice:[stdDev, value]})
                        
                
    print(listeLTOPstations)

        
                        
    #### DONNES CONFORMES AU MODELE XSD          
        
    
    #### # --- LEVE POLAIRE 
    # Converti les occurences de sessions et station vers la structure XML
    allStations = {'polar':{'station':[]}}
    for station in listeLTOPstations:
        
        # En tête de station
        dictStation = {'stationName':station['stationName'],
                       'stationData':{'I':station['I'],
                                      'stationCentring':{'planiStdDev':{'mm':''},
                                                         'altiStdDev':{'mm':''}},
                                      'distanceGroup':'groupeDistanceParDefaut',
                                      'directionGroup':'groupeDirectionParDefaut',
                                      'centringGroup':'groupeCentrageParDefaut',
                                      'measure':[]
                                      }
                       }
        
        # points visés par session selon lecture du fichier LTOP
        for key,data in station['pointsVises'].items():
            
            # Initialiser à False, va se transformer en sous-dict de l'obs. si elle existe
            RI, DS, ZD, DP = False, False, False, False
            # Parcourir les types d'obs. lues dans le fichier LTOP
            if 'RI' in data.keys():
                RI = {'stdDev':{'cc':data['RI'][0]},
                      'value':data['RI'][1],
                      'discarded':''}
            if 'DS' in data.keys():
                DS = {'stdDev':{'mm':data['DS'][0],
                                'ppm':''},
                      'value':data['DS'][1],
                      'discarded':''}
            if 'ZD' in data.keys():
                ZD = {'stdDev':{'cc':data['ZD'][0]},
                      'value':data['ZD'][1],
                      'discarded':''}
            if 'DP' in data.keys():
                DP = {'stdDev':{'mm':data['DP'][0],
                                'ppm':''},
                      'value':data['DP'][1],
                      'discarded':''}
            
            
            
            # Aucune info de distance
            if not DP and not DS:
                DS = {'stdDev':{'mm':'9999',
                                'ppm':''},
                                'value':'9999',
                                'discarded':'true'}
            # si info de distance horiz. (DP devient DS)
            # ZD devient 100.0
            elif DP and not DS:
                DS = DP
                ZD = {'stdDev':{'cc':''},
                      'value':'100.0000',
                      'discarded':''}
                
            # Si pas de direction RI
            if not RI:
                RI = {'stdDev':{'cc':'9999'},
                      'value':'9999',
                      'discarded':'true'}
            
            
            # Si pas de ZD
            if not ZD:
                ZD = {'stdDev':{'cc':'9999'},
                      'value':'9999',
                      'discarded':'true'}
                
            
            print('\n\ndebug2')
            print(DP, DS, RI, ZD)
            # Ajouter la balise <measure>
            if DS and ZD and RI:
                
                    S = data['ZD'][2] # Le S du DS définit le S de la mesure (fusion du fichier LTOP, peut être vide '')
                    dictStation['stationData']['measure'].append({'pointName':key,
                                                    'RI':RI,
                                                    'DS':DS,
                                                    'ZD':ZD,
                                                    'S':{'value':S},
                                                    'dm1':{'value':''},
                                                    'dm2':{'value':''},
                                                    'targetCentring':{'planiStdDev':{'mm':''},
                                                                        'altiStdDev':{'mm':''}}
                                                    })
                    

                
                
                
                
                
                
                
                
                
                
                
            # # Ajoute la <measure> uniquement dès qu'il y'a les trois type d'obs. RI, DS et DP
            # if RI and DS and ZD:
                
            #     S = data['ZD'][2] # Le S du DS définit le S de la mesure (fusion du fichier LTOP, peut être vide '')
            #     dictStation['stationData']['measure'].append({'pointName':key,
            #                                     'RI':RI,
            #                                     'DS':DS,
            #                                     'ZD':ZD,
            #                                     'S':{'value':S},
            #                                     'dm1':{'value':''},
            #                                     'dm2':{'value':''},
            #                                     'targetCentring':{'planiStdDev':{'mm':''},
            #                                                        'altiStdDev':{'mm':''}}
            #                                     })
                
                
            
            # elif DP and RI and not ZD: # Si seulement RI et DP, on ajoute avec ZD = 100.0 et DS=DP
            #     dictStation['stationData']['measure'].append({'pointName':key,
            #                                     'RI':RI,
            #                                     'DS':DP,
            #                                     'ZD':{'stdDev':{'cc':''},
            #                                           'value':'100.0000',
            #                                           'discarded':''},
            #                                     'S':{'value':''},
            #                                     'dm1':{'value':''},
            #                                     'dm2':{'value':''},
            #                                     'targetCentring':{'planiStdDev':{'mm':''},
            #                                                        'altiStdDev':{'mm':''}}
            #                                     })
                
                
                
            
                
                
                
                
                
        
                
            
        # Ajout au dictionnaire total des station (si au moins 1 mesure valide, ex. si DH uniq. -> non ajoutée)
        # print(dictStation)
        if len(dictStation['stationData']['measure']) > 0:
            allStations['polar']['station'].append(dictStation)
    

                    
    #### # --- SESSIONS GNSS 
    # Converti les occurences de sessions et station vers la structure XML
    allSessions = {'gnss':{'session':[]}}
    for session in listeLTOPsessions:
        
        # En tête de session
        dictSession = {'sessionName':session['sessionName'],
                       'gnssGroup':'groupeGNSSParDefaut',
                       'measure':[]}
        
        # points visés par session selon lecture du fichier LTOP
        for key,data in session['pointsVises'].items():
            
            # Initialiser à False, va se transformer en sous-dict de l'obs. si elle existe
            LY, LX, LH = False, False, False
            # Parcourir les types d'obs. lues dans le fichier LTOP
            if 'LY' in data.keys():
                LY = {'stdDev':{'mm':data['LY'][0]},
                      'value':data['LY'][1],
                      'discarded':''}
            if 'LX' in data.keys():
                LX = {'stdDev':{'mm':data['LX'][0]},
                      'value':data['LX'][1],
                      'discarded':''}
            if 'LH' in data.keys():
                LH = {'stdDev':{'mm':data['LH'][0]},
                      'value':data['LH'][1],
                      'discarded':''}
            
            # Ajoute la <measure> uniquement si il y'a les trois type d'obs.
            if LY and LX and LH:
                dictSession['measure'].append({'pointName':key,
                                                'LY':LY,
                                                'LX':LX,
                                                'LH':LH,
                                                })
            
        # Ajout au dictionnaire total des sessions
        allSessions['gnss']['session'].append(dictSession)
        
    


                
    # Initialisation du dictionnaire final conforme au modèle XSD
    dictAll  = {'network':{}}    
    
    # Si au moins 1 station polaire
    if len(allStations['polar']['station']) > 0:
        dictAll['network'].update(allStations)
    
    # Si au moins 1 session GNSS
    if len(allSessions['gnss']['session']) > 0:
        dictAll['network'].update(allSessions)
    

    # conversion dict to XML
    dictionnaire2xml(dictAll, filePathOutput)
    
    # EN ORDRE au 14.11.2022
    # controlesCoherenceUtils.checkXmlXsd("C:\\01_ContraintesMsMo\\02_dev\\01_code\\modeleDonnees\\modeleCanevas.xsd", filePathOutput)
   

    
    # Message de fin d'éxécution
    print('\nLTOP MES conversion to observations XML successfully executed\n')
    return None




def pointsXMLtoCSV(filePathXML, filePathCSV):
    
    """
    Transformation des points issus d'un fichier XML conforme XSD à un fichier CSV.
    Cela prend en compte les balises ad-hoc du fichier XML et tous les indicateurs standards
    
    Parameters
    ----------
    filePathXML : string (ne pas oublier les doubles backslash)
        Lien vers le fichier XML des points.
    filePathCSV : string (ne pas oublier les doubles backslash)
        Lien vers le fichier d'export des points CSV.

    Returns
    -------
    None.

    """
    
    # dictionnaire des points
    dictPoints = xml2dictionnaire(filePathXML)
    
    listUsualKeys = ['planimetricElems', 'altimetricElems', 'idUnkH', 'idUnkE', 'idUnkN',
                     'stdErrEllipse', 'externalReliabilityPlaniVector', 'deltaPlani', 
                     'altiStdError', 'externalReliabilityAlti', 'deltaAlti',
                     'pointName', 'E', 'N', 'H']
    
    # Détecter les clés ad-hoc
    header1 = ['No','E [m]','N [m]','H [m]']
    header2 = ['id unknown E','id unknown N','id unknown N','StdErrPlani s-maj. axis a [m]','StdErrPlani s-min. axis b [m]','bear. a [g]','ext. reliab. NA [m]',' bear. NA [g]','id obs. resp. for NA','dE [m]','dN [m]','StdErrAlti semi axis c [m]','ext. reliab. NH [m]','id obs. resp. for NH','dH [m]']
    balisesAdHoc = []
    for point in dictPoints['points']['point']:
        for key in point.keys():
            # ajouter si pas déjà présent dans l'en-tête et pas dans les clés usuelles
            if key not in listUsualKeys and key not in header1:
                header1.append(key) # à ajouter au début des header (reconnaissance du pt, en général)
                balisesAdHoc.append(key)
        
    # Fusion des headers
    allHeader = header1 + header2
    
    
    
    
        
    
    # Parcourir les points encolonner les données avec un ;
    with open(filePathCSV, 'w') as f:
        
        # écrire les en-tête:
        for header in allHeader:
            f.write('{:s};'.format(header))
        f.write('\n')
        
        # f.write("""No;E [m];N [m];H [m];id unknown E;id unknown N;id unknown N;StdErrPlani s-maj. axis a [m];StdErrPlani s-min. axis b [m];bear. a [g];ext. reliab. NA [m]; bear. NA [g];id obs. resp. for NA;dE [m];dN [m];StdErrAlti semi axis c [m];ext. reliab. NH [m];id obs. resp. for NH;dH [m]; \n""")
        # Parcourir et écrire le fichier CSV
        for point in dictPoints['points']['point']:
            

            # Si H est vide ou non
            if point['H'] == None:
                H = ''
            else:
                H = point['H']
            
            
            #### ID DES INCONNUES
            try:
                idE = point['idUnkE']
            except:
                idE = ''
            try:
                idN = point['idUnkN']
            except:
                idN = ''
            try:
                idH = point['idUnkH']
            except:
                idH = ''
            
            
            #### PLANI EM ELLIPSES
            try:
                a = point['stdErrEllipse']['a']
            except:
                a = ''
            try:
                b = point['stdErrEllipse']['b']
            except:
                b = ''
            try:
                gisA = point['stdErrEllipse']['bearA']
            except:
                gisA = ''
                
            
            #### PLANI VECTEURS NA
            try:
                NA = point['externalReliabilityPlaniVector']['NA']
            except:
                NA = ''
            try:
                gisNA = point['externalReliabilityPlaniVector']['bearNA']
            except:
                gisNA = ''
            try:
                idObsRespNA = point['externalReliabilityPlaniVector']['idObsRespNA']
            except:
                idObsRespNA = ''
                
            #### PLANI DELTA
            try:
                dE = point['deltaPlani']['dE']
            except:
                dE = ''
            try:
                dN = point['deltaPlani']['dN']
            except:
                dN = ''
                
            #### ALTI EM ELLIPSES
            try:
                c = point['altiStdError']['c']
            except:
                c = ''
            
            #### ALTI VECTEURS NH
            try:
                NH = point['externalReliabilityAlti']['NH']
            except:
                NH = ''
            try:
                idObsRespNH = point['externalReliabilityAlti']['idObsRespNH']
            except:
                idObsRespNH = ''
            
            #### ALTI DELTA
            try:
                dH = point['deltaAlti']['dH']
            except:
                dH = ''
                
            
            #### création des lignes
            ligne1 = f'{point["pointName"]};{point["E"]};{point["N"]};{H};'
            
            #### AUTRES BALISES
            for balise in balisesAdHoc:
                
                # Si la balise est présente dans ce point, remplir la colonne
                if balise in point.keys():
                    # ne pas générer une erreur si 2 balises identiques dans le point
                    if type(point[balise]) != list: 
                        ligne1 += point[balise] + ';'
                    # prendre la val. de la première occurence de la balise
                    else:
                        ligne1 += point[balise][0] + ';' 
                else: # vide sinon (mais remplir pour éviter le décalage)
                    ligne1 += ''+';'
                
            # Suite des données 
            ligne2 = f'{idE};{idN};{idH};{a};{b};{gisA};{NA};{gisNA};{idObsRespNA};{dE};{dN};{c};{NH};{idObsRespNH};{dH}\n'
            
            # écrire la ligne totale
            f.write(ligne1+ligne2)
            
        print('\n--- POINTS XML CONVERSION TO CSV SUCCESSFULLY EXECUTED\n')
    return None




# def LTOP2xml(filePathMES, filePathOutput):
    
#     """
#     Transformation du fichier de mesure .MES de LTOP à XML (UNIQUEMENT SESSIONS GNSS POUR LE MOMENT).

#     Parameters
#     ----------
#     filePathMES : string (ne pas oublier les doubles backslash)
#         Lien vers le fichier .ll1 
#     filePathOutput : string (ne pas oublier les doubles backslash)
#         Lien vers le fichier d'export XML
        
#     Returns
#     -------
#     None.

#     """
    
#     # Initialisation
#     allSessions = {'gnss':{'session':[]}}
    
#     # Lecture du fichier MES
#     with open(filePathMES, 'r') as f:
        
#         dictSessionGNSS = {}
        
#         for line in f:
#             line = line.rstrip() 
            
#             #### # --- SESSIONS GNSS 
            
#             if line[0:2] == 'SL' : # append et création de la session (la première est vide)
                
#                 if len(dictSessionGNSS) > 0:
#                     allSessions['gnss']['session'].append(dictSessionGNSS)
                
#                 dictSessionGNSS = {
#                       "sessionName":line[0:15],
#                       "gnssGroup":"groupeGNSSParDefaut",
#                       "measure":[]
#                     }
            
#             typeObs = line[0:2]
            
#             # On ajoute uniquement si LY,LX et LH (et seulement si pas écarté avec 9999)
            
#             if typeObs == 'LY':
#                 dictObs = {'LY':line[24:35].strip()}
#             if typeObs == 'LX' and 'LY' in dictObs.keys():
#                 dictObs.update({'LX':line[24:35].strip()})
#             if typeObs == 'LH' and 'LY' in dictObs.keys() and 'LX' in dictObs.keys():
#                 dictObs.update({'LH':line[24:35].strip()})
                
#                 # Numéro de point 
#                 if line[2:6] == '1203':
#                     noPt = '400'+'1203'+'    '+line[6:9]+line[13] 
#                 else:
#                     noPt = '3'+line[2:8]+'    '+line[8:12]
#                 if line[36:40] != '9999':
#                     # création de l'observaation
#                     observation = {
#                               "pointName":noPt,
#                               "LY":{
#                                 "stdDev":{'mm':''},
#                                 "value":dictObs['LY'],
#                                 "discarded":"false",
#                               },
#                               "LX":{
#                                 "stdDev":{'mm':''},
#                                 "value":dictObs['LX'],
#                                 "discarded":"false",
#                               },
#                               "LH":{
#                                 "stdDev":{'mm':''},
#                                 "value":dictObs['LH'],
#                                 "discarded":"false",
#                               }
#                             }
                    
#                     dictSessionGNSS['measure'].append(observation)
                

    
#     dictionnaire2xml(allSessions, filePathOutput)
   

    
#     return None
    


def fusionFichiers(dirPath, filePathOutput, GNSS=False):
    
    """
    Fusion de tous fichiers d'un répertoire. 
    Uniquement les fichiers à fusionner doivent d'y trouver. 
    (Attention à la boucle infinie si le fichier de fusion s'y trouve) 

    Parameters
    ----------
    dirPath : string (ne pas oublier les doubles backslash)
        Lien vers le répértoir.
    filePathOutput : string (ne pas oublier les doubles backslash)
        Lien vers le répertoir de fusion.
    GNSS : optionel, bool 
        Si True, écrira un marqueur pour distinguer une session par fichier GCO

    Returns
    -------
    None.

    """
    
    listFiles = os.listdir(dirPath) 
    
    with open(filePathOutput, "w") as new_file:
        for name in listFiles:
            with open(dirPath + name,'r') as f:
                for line in f:
                    new_file.write(line)
                new_file.write('\n')
                
                # Un fichier GNSS = une session
                # écrire un marqueur pour séparer chaque sessions, si on fusionne des GCO de sessions GNSS
                if GNSS and name != listFiles[-1]: # ET ne pas avoir de '--' à la fin du dernier fichier GCO
                    new_file.write('--\n')
    
    return None

