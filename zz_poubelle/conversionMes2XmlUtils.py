# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 11:27:34 2022

@author: Matteo Casto, INSIT
"""

import os
from xml.dom import minidom
import xmltodict



def fusionFichier(dirPath, filePathOutput, GNSS=False):
    
    """
    Fusion de tous fichiers GME d'un répertoire.
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





def hom2xml(filePathGME, filePathGCO, filePathOutput):
    
    """
    Transformation du fichier des observations de GME à XML

    Parameters
    ----------
    filePathGME : string (ne pas oublier les doubles backslash)
        Lien vers le fichier GME (uniquement levés polaires)
    filePathGCO : string (ne pas oublier les doubles backslash)
        Lien vers le fichier GCO (uniquement levés GNSS)
    filePathOutput : string (ne pas oublier les doubles backslash)
        Lien vers le fichier d'export XML

    Returns
    -------
    None.

    """
    
    # Initialisation du format XML
    doc = minidom.Document()
    canevas = doc.createElement('canevas')
    doc.appendChild(canevas)
    
    

    #-----------------------
    # --- LEVES POLAIRES ---
    #-----------------------
    
    polaire = doc.createElement('polaire')
    canevas.appendChild(polaire)
    
    newStation = False # newStation sert à distinguer chacune des stations
    with open(filePathGME,'r') as f:
        
        for line in f:
            line = line.strip()
            
            if len(line) > 0: # sauter les lignes vides
            
                indice = line[0:2]
                
                if indice == '10' and newStation == False : # no de stationnement
                
                    # Récupération des éléments de station
                    noSta, hauteurI = line[3:18], line[53:58].strip()
                    
                    # Initialisation de la balise du stationnement
                    station = doc.createElement('station')
                    polaire.appendChild(station)
                    
                    # Numéro de station
                    numeroStation = doc.createElement('numeroStation')
                    numeroStation.appendChild(doc.createTextNode(noSta))
                    station.appendChild(numeroStation)
                    
                    # Stationnement
                    stationnement = doc.createElement('stationnement')
                    station.appendChild(stationnement)
                    
                    # Hauteur d'instrument I
                    I = doc.createElement('I')
                    I.appendChild(doc.createTextNode(hauteurI))
                    stationnement.appendChild(I)
                    
                    # newStation sert à distinguer chacune des stations
                    newStation = True
                
                        
                # --- OBSERVATIONS TERRSETRES PAR STATIONNEMENT
                if indice == '11' or indice == '12':
                    newStation = False
                    
                    # Balise observation
                    observation = doc.createElement('observation')
                    stationnement.appendChild(observation)
                    
                    # Récupérations des éléments de l'observation
                    noPt, theme, nature, hz, dist, zenith = line[3:18], line[21:22].strip(), line[22:23].strip(), line[24:32].strip(), line[33:41].strip(), line[42:50].strip()
                    hauteurS, d1, d2 = line[51:58].strip(), line[59:66].strip(), line[67:74].strip()
    
                    # Si le thème est PF (=1), alors le plan dans le noPt devient 0:
                    if theme == '1' :
                        noPt = noPt[0:3] + '   0' + noPt[7:]
    
                    # Numéro de point
                    numeroPoint = doc.createElement('numeroPoint')
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
                    ecartType = doc.createElement('ecartType')
                    ecartType.appendChild(doc.createTextNode('')) # L'utilisateur pourra la modifier manuellement
                    valeur = doc.createElement('valeur')
                    valeur.appendChild(doc.createTextNode(hz))
                    RI.appendChild(ecartType)
                    RI.appendChild(valeur)
                    observation.appendChild(RI)
                    
                    # Distance inclinée
                    DS = doc.createElement('DS')
                    ecartType = doc.createElement('ecartType') # L'utilisateur pourra la modifier manuellement
                    mm = doc.createElement('mm')
                    mm.appendChild(doc.createTextNode(''))
                    ppm = doc.createElement('ppm')
                    ppm.appendChild(doc.createTextNode(''))
                    valeur = doc.createElement('valeur')
                    valeur.appendChild(doc.createTextNode(dist))
                    ecartType.appendChild(mm)
                    ecartType.appendChild(ppm)
                    DS.appendChild(ecartType)
                    DS.appendChild(valeur)
                    observation.appendChild(DS)
                    
                    # Angle zénithal
                    ZD = doc.createElement('ZD')
                    ecartType = doc.createElement('ecartType')
                    ecartType.appendChild(doc.createTextNode('')) # L'utilisateur pourra la modifier manuellement
                    valeur = doc.createElement('valeur')
                    valeur.appendChild(doc.createTextNode(zenith))
                    ZD.appendChild(ecartType)
                    ZD.appendChild(valeur)
                    observation.appendChild(ZD)
                    
                    # Hauteur du signal 
                    S = doc.createElement('S')
                    valeur = doc.createElement('valeur')
                    valeur.appendChild(doc.createTextNode(hauteurS))
                    S.appendChild(valeur)
                    observation.appendChild(S)
                    
                    # Déplacement dm1 
                    dm1 = doc.createElement('dm1')
                    valeur = doc.createElement('valeur')
                    valeur.appendChild(doc.createTextNode(d1))
                    dm1.appendChild(valeur)
                    observation.appendChild(dm1)
                    
                    # Déplacement dm2 
                    dm2 = doc.createElement('dm2')
                    valeur = doc.createElement('valeur')
                    valeur.appendChild(doc.createTextNode(d2))
                    dm2.appendChild(valeur)
                    observation.appendChild(dm2)
                    
                    # 3 visées écartées (bool)
                    ecarte = doc.createElement('ecarte')
                    ecarte.appendChild(doc.createTextNode('False')) # ici False par défaut
                    observation.appendChild(ecarte)
                    


    #----------------------
    # --- SESSIONS GNSS ---
    #----------------------
    
    GNSS = doc.createElement('GNSS')
    canevas.appendChild(GNSS)
    
    nSessionIncr = 1
    
    newSession = True
    with open(filePathGCO,'r') as f:
        
        for line in f:
            line = line.strip()
            
            if len(line) > 0: # sauter les lignes vides
            
                indice = line[0:2]
                
                # nouvelle session (séprarée par '--')
                if (indice == '--' or newSession == True) : 
                    
                    newSession = False
                    
                    # Initialisation de la balise de la mesure
                    Session = doc.createElement('session')
                    GNSS.appendChild(Session)
                    
                    # Nom de la session (ici incrémenté de S1 à Sxxx, mais nimporte quel str possible)
                    nomSession = doc.createElement('nomSession')
                    nomSession.appendChild(doc.createTextNode('S'+str(nSessionIncr)))
                    Session.appendChild(nomSession)
                    
                    nSessionIncr += 1
                    
                
                # Mesures LY, LX et LH de la session
                if indice == '01' and newSession == False : 
                    
                    # Balise observation
                    observation = doc.createElement('observation')
                    Session.appendChild(observation)
                
                    # Récupération des éléments de la ligne de mesure du GCO
                    noPt, theme, nature = line[3:10]+line[16:24], line[27:28], line[28:29]
                    E, N, H = line[34:46].strip(), line[47:59].strip(), line[60:69].strip()

                    # Numéro de station
                    numeroPoint = doc.createElement('numeroPoint')
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
                    
                    # LY
                    LY = doc.createElement('LY')
                    valeur = doc.createElement('valeur')
                    valeur.appendChild(doc.createTextNode(E))
                    ecartType = doc.createElement('ecartType')
                    ecartType.appendChild(doc.createTextNode(''))
                    LY.appendChild(ecartType)
                    LY.appendChild(valeur)
                    observation.appendChild(LY)
                    
                    # LX
                    LX = doc.createElement('LX')
                    valeur = doc.createElement('valeur')
                    valeur.appendChild(doc.createTextNode(N))
                    ecartType = doc.createElement('ecartType')
                    ecartType.appendChild(doc.createTextNode(''))
                    LX.appendChild(ecartType)
                    LX.appendChild(valeur)
                    observation.appendChild(LX)
                    
                    # LH
                    LH = doc.createElement('LH')
                    valeur = doc.createElement('valeur')
                    valeur.appendChild(doc.createTextNode(H))
                    ecartType = doc.createElement('ecartType')
                    ecartType.appendChild(doc.createTextNode(''))
                    LH.appendChild(ecartType)
                    LH.appendChild(valeur)
                    observation.appendChild(LH)
                    
                    # 3 mesures E,N,H écartées (bool)
                    ecarte = doc.createElement('ecarte')
                    ecarte.appendChild(doc.createTextNode('False')) # ici False par défaut
                    observation.appendChild(ecarte)
                    
                
                    newSession = False
                    

                
    # --- FINALISATION ET GENERATION DU FICHIER XML ---
    xml_str = doc.toprettyxml(indent = 4*" ")
    with open(filePathOutput, "w", encoding=('utf-8')) as f:
        f.write(xml_str) 
    
    
    # print('---   Conversion du fichier gme:', filePathGME, '\n effectuée avec succès dans le fichier destination :', filePathOutput)
                    
    return None





def xml2dictionnaire(path):
    
    """
    Parser d'un fichier XML en dictionnaire'

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
        dictRes = xmltodict.parse(f.read())
    
    print('---   Lecture du fichier xml:', path, '\n effectuée avec succès') 
    
    return dictRes
    












