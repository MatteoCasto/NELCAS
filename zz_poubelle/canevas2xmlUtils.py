# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 16:05:13 2022

@author: Matteo Casto, INSIT
"""

from xml.dom import minidom
import xmltodict


def canevas2xml(filePathll1, filePathOutput):
    
    """
    Transformation du fichier de calcul ll1 en XML (canevas)

    Parameters
    ----------
    filePathll1 : string (ne pas oublier les doubles backslash)
        Lien vers le fichier .ll1 
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
    
    # Lecture du fichier .ll1
    fichier = open(filePathll1,'r')
    line = fichier.readline()
    
    # variable qui devient True une fois entré dans la liste des mesures
    listeMesures = False
    GK = ''

    # Balises principales du XML
    polaire = doc.createElement('polaire')
    canevas.appendChild(polaire)
    GNSS = doc.createElement('GNSS')
    canevas.appendChild(GNSS)
    nSessionIncr = 0 # incérment pour les sessions GNSS 'Sx'
    
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
                    # --- LEVES POLAIRES ---
                    #-----------------------
                        
                    
                    if GK == '11' or GK == '51':
                        
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
                            
                            # Balise observation XML
                            observation = doc.createElement('observation')
                            stationnement.appendChild(observation)
                            
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
                        
                        
                    #### A FINIR ICI PUIS CONTROLER AVEC LES CHECKER
                    
                    if GK == '71' and stringLine[60:71] != '           ':
                        
                        noCmne, noPlan, no = stringLine[7:10], stringLine[11:15], stringLine[18:22]
                        lenPlan = len(noPlan.strip())
                        if lenPlan < 4: # Si pas un numéro de plan
                            reste = 4-lenPlan
                            noPlan = reste*' ' + noPlan.strip()
                        noPt = noCmne + noPlan + '    ' + no
                        ligneSta = True
                        
                        if stringLine[35:58] == '                       ': #première ligne, création session GNSS
                            
                            # Récupération des éléments de la première ligne de session
                            theme,nature = stringLine[53].strip(), stringLine[57].strip()
                            est, nord, alt = stringLine[60:72].strip(), stringLine[74:86].strip(), stringLine[93:101].strip(), 
                            
                            # Incrément pour Sxxx
                            nSessionIncr += 1
                            
                            # Initialisation de la balise de la session
                            Session = doc.createElement('session')
                            GNSS.appendChild(Session)
                            
                            # Nom de la session (ici incrémenté de S1 à Sxxx, mais nimporte quel str possible)
                            nomSession = doc.createElement('nomSession')
                            nomSession.appendChild(doc.createTextNode('S'+str(nSessionIncr)))
                            Session.appendChild(nomSession)
                        
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
                        est, nord, alt = stringLine[60:72].strip(), stringLine[74:86].strip(), stringLine[93:101].strip(),   
                        
                        # Balise observation XML 
                        observation = doc.createElement('observation')
                        Session.appendChild(observation) 
                        
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
                        
                        # Observation LY
                        LY = doc.createElement('LY')
                        ecartType = doc.createElement('ecartType')
                        ecartType.appendChild(doc.createTextNode('')) # L'utilisateur pourra la modifier manuellement
                        valeur = doc.createElement('valeur')
                        valeur.appendChild(doc.createTextNode(est))
                        LY.appendChild(ecartType)
                        LY.appendChild(valeur)
                        observation.appendChild(LY)
                        
                        # Observation LX
                        LX = doc.createElement('LX')
                        ecartType = doc.createElement('ecartType')
                        ecartType.appendChild(doc.createTextNode('')) # L'utilisateur pourra la modifier manuellement
                        valeur = doc.createElement('valeur')
                        valeur.appendChild(doc.createTextNode(nord))
                        LX.appendChild(ecartType)
                        LX.appendChild(valeur)
                        observation.appendChild(LX)
                        
                        # Observation LH
                        LH = doc.createElement('LH')
                        ecartType = doc.createElement('ecartType')
                        ecartType.appendChild(doc.createTextNode('')) # L'utilisateur pourra la modifier manuellement
                        valeur = doc.createElement('valeur')
                        valeur.appendChild(doc.createTextNode(alt))
                        LH.appendChild(ecartType)
                        LH.appendChild(valeur)
                        observation.appendChild(LH)
                        
                        # 3 visées écartées (bool)
                        ecarte = doc.createElement('ecarte')
                        ecarte.appendChild(doc.createTextNode('False')) # ici False par défaut
                        observation.appendChild(ecarte)
                            
            
        line = fichier.readline()
        
    fichier.close()


    # --- FINALISATION ET GENERATION DU FICHIER XML ---
    xml_str = doc.toprettyxml(indent = 4*" ")
    with open(filePathOutput, "w", encoding=('utf-8')) as f:
        f.write(xml_str) 
    
    
    return None






