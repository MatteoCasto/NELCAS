import sys
sys.path.append('C:\\HEIG-VD\\TB\\02_dev\\01_import\\')

import numpy as np
import copy







def reductionDistancePlanProj(distABincl, angleZenith, NabMoy, HabMoy):
    
    """
    Réduit une distance inclinée vers une distance dans le plan de projection

    Parameters
    ----------
    distABincl : float
        distance inclinnée brute [m]
        
    angleZenith : float
        angle zénithal de la visée [g]
        
    NabMoy : float
        coordonée Nord moyenne de la distance (format 1200000.000)
        
    HabMoy : float
        altitude NF02 moyenne de la distance (format 1000.000)

    Returns
    -------
    distRed : float
        distance réduite dans le plan de projection

    """
    
    distABhoriz = np.sin(angleZenith*np.pi/200.0)*distABincl
    distRed = distABhoriz + distABhoriz*((((NabMoy-1200000)**2)/(2*6378800**2)) - (HabMoy/6378800))
    
    return distRed


def corrAvecDepl(RI,DP,dlat,dlon):
   
    """
    Corrige une direction et une distance dans le plan de projection d'éventuels déplacement lat. et lon. 

    Parameters
    ----------
    RI : float
        direction sur le point aux. [g]
        
    DP : float
        distance au point aux. dans le plan de projection [m]
        
    dlat : float
        déplacement latéral, + si pt vrai à droite, - si gauche, [m]
        
    dlon : float
        déplacement latéral, + si pt vrai plus loins - si moins, [m]

    Returns
    -------
    RIcorr, DPcorr : float,float
        Direction [g] corrigée des dépl., Distance [g] dans le plan proj. corrigée des dépl.

    """
    DPlon = DP+dlon 
    DPcorr = (DPlon**2+dlat**2)**0.5
    RIcorr = RI + np.arctan(dlat/DPlon)*200.0/np.pi
    
    return RIcorr,DPcorr






def redCorrAllDistancesPlanProj(dictMesures, NabMoy, HabMoy):
    
    """
    Réduit les mesures de distances inclinées dans le plan de projection. Puis corrige des déplacements
    ces distances et les directions associées.

    Parameters
    ----------
    dictMesures : dictionnaire
        BDmes qui contient toutes les mesures
        
    NabMoy : float
        coordonée Nord moyenne de la zone (format 1200000.000)
        
    HabMoy : float
        altitude NF02 moyenne de la zone (format 1000.000)

    Returns
    -------
    RIcorr, DPcorr : float,float
        Direction [g] corrigée des dépl., Distance [g] dans le plan proj. corrigée des dépl.

    """

    # copie du dict pour l'output indépendant
    dictMesuresReduites = copy.deepcopy(dictMesures)
    pasAjout = False
    mesIdNouv = 2000001 # nouvel mesId pour DP corr et RI corr
    
    for staId,data in dictMesuresReduites.items():
        listeMes = data['listeMes']
        typeLeve = data['typeLeve']
        noSta = data['noSta']
        
        # continuer uniquement si il s'agit d'une station polaire (tout type)
        if typeLeve == 'STATION POLAIRE PF' or typeLeve == 'STATION S/POINT LEDET' or typeLeve == 'STATION LIBRE LEDET': 
        
            # parcourir la liste des entités de mesures par station
            dictValMesParNoVis = {} # dict du type {noVis:[['typeMes',valMes],['typeMes':valMes]]}
            for mes in listeMes:
                noVis = mes['noVis']
                dictValMesParNoVis.update({noVis:{}}) 
             
            for mes in listeMes:
                mesId = mes['mesId']
                noVis = mes['noVis']
                valMes = mes['valMes']
                typeMes = mes['typeMes']
                themePtVis = mes['themePtVis']
                naturePtVis = mes['naturePtVis']
                dm1 = mes['dm1']
                dm2 = mes['dm2']
                supp = mes['supp']
                dictValMesParNoVis[noVis].update({'mesId':mesId})
                dictValMesParNoVis[noVis].update({typeMes:valMes})
                dictValMesParNoVis[noVis].update({'themePtVis':themePtVis})
                dictValMesParNoVis[noVis].update({'naturePtVis':naturePtVis})
                dictValMesParNoVis[noVis].update({'dm1':dm1})
                dictValMesParNoVis[noVis].update({'dm2':dm2})
                dictValMesParNoVis[noVis].update({'supp':supp})
                
                
            DS = '' # portée de la variable
            HW = '' # portée de la variable
            ZD = '' # portée de la variable
            RI = '' # portée de la variable
            dataVis = ''
            
            for noVis,data in dictValMesParNoVis.items():
                corr = False # attribut pour savoir si il y a eu une déplacement sur une visée (dlat ou dlon)
                pasAjout = False
                
                # mesures RI sans distances, ni ZD, ni HW
                if 'RI' in data.keys() and 'DS' not in data.keys():
                    RI = data['RI']
                    # ajout de la mes RI à la liste des mesures (corr. des déplacements)
                    dataVis = {'mesId': mesIdNouv,
                               'noDep':noSta,
                               'noVis':noVis,
                               'typeMes':'RI',
                               'themePtVis': data['themePtVis'],
                               'naturePtVis':data['naturePtVis'],
                               'valMes':round(RI,5),
                               'depl':corr, # ajout de l'attribution depl True ou False si le RI a été corrigé de dlat ou dlon 
                               'supp':data['supp']}  
                    
                    listeMes.append(dataVis)
                    mesIdNouv += 1
                    
                    
                # mesures RI avec distances mais sans ZD, ni HW (donc pas de réduction = pas de distance)
                if 'RI' in data.keys() and 'ZD' not in data.keys() and 'HW' not in data.keys():
                    RI = data['RI']
                    # ajout de la mes RI à la liste des mesures (corr. des déplacements)
                    dataVis = {'mesId': mesIdNouv,
                               'noDep':noSta,
                               'noVis':noVis,
                               'typeMes':'RI',
                               'themePtVis': data['themePtVis'],
                               'naturePtVis':data['naturePtVis'],
                               'valMes':round(RI,5),
                               'depl':corr, # ajout de l'attribution depl True ou False si le RI a été corrigé de dlat ou dlon 
                               'supp':data['supp']} 
                    
                    listeMes.append(dataVis)
                    mesIdNouv += 1
                    
                

                
                
                if 'DS' in data.keys(): # traiter uniquement où il y a des distances inclinées DS
                    DS = data['DS']
                    DP = 0.0
                    
                    
                    # si aucun ZD ou HW pour réduire la distance
                    if 'HW' not in data.keys() and 'ZD' not in data.keys():
                        pasAjout = True
                        # print('Pas de HW ou ZD pour réduire la distance:',noSta,noVis)
                    

                    if 'HW' in data.keys():
                        HW = data['HW']
                        
                        # plan proj
                        DP = reductionDistancePlanProj(DS, 100.0-HW, NabMoy, HabMoy)
                        # correction des déplacements
                        if 'RI' in data.keys():
                            RI, DP = corrAvecDepl(data['RI'],DP,data['dm1'],data['dm2'])
                            # modification de l'attribut pour indiquer qu'un ou 2 déplacements ont été appliqués
                            if data['dm1'] != 0.0 or data['dm2'] != 0.0:
                                corr = True
                            # ajout de la mes RI à la liste des mesures (corr. des déplacements)
                            dataVis = {'mesId': mesIdNouv,
                                       'noDep':noSta,
                                       'noVis':noVis,
                                       'typeMes':'RI',
                                       'themePtVis': data['themePtVis'],
                                       'naturePtVis':data['naturePtVis'],
                                       'valMes':round(RI,5),
                                       'depl':corr, # ajout de l'attribution depl True ou False si le RI a été corrigé de dlat ou dlon 
                                       'supp':data['supp']}                          
                            
                            listeMes.append(dataVis)
                            mesIdNouv += 1

                    elif 'ZD' in data.keys():
                        ZD = data['ZD']
                        # plan proj
                        DP = reductionDistancePlanProj(DS, ZD, NabMoy, HabMoy)
                        # correction des déplacements
                        if 'RI' in data.keys():
                            RI, DP = corrAvecDepl(data['RI'],DP,data['dm1'],data['dm2'])
                            # modification de l'attribut pour indiquer qu'un ou 2 déplacements ont été appliqués
                            if data['dm1'] != 0.0 or data['dm2'] != 0.0:
                                corr = True
                            # ajout de la mes RI à la liste des mesures (corr. des déplacements)
                            dataVis = {'mesId': mesIdNouv,
                                       'noDep':noSta,
                                       'noVis':noVis,
                                       'typeMes':'RI',
                                       'themePtVis': data['themePtVis'],
                                       'naturePtVis':data['naturePtVis'],
                                       'valMes':round(RI,5),
                                       'depl':corr, # ajout de l'attribution depl True ou False si le DP a été corrigé de dlat ou dlon
                                       'supp':data['supp']} 
                            listeMes.append(dataVis)
                            mesIdNouv += 1
                    
                    
                    if pasAjout == False:

                        # ajout de la mes DP à la liste des mesures (corr. des déplacements et dans le plan proj)
                        dataVis = {'mesId': mesIdNouv,
                                   'noDep':noSta,
                                   'noVis':noVis,
                                   'typeMes':'DP',
                                   'themePtVis': data['themePtVis'],
                                   'naturePtVis':data['naturePtVis'],
                                   'valMes':round(DP,4),
                                   'depl':corr, # ajout de l'attribution depl True ou False si le DP a été corrigé de dlat ou dlon
                                   'supp':data['supp']} 
                        listeMes.append(dataVis)
                        mesIdNouv += 1
    

    print('--   Mesures corrigées et réduites')
    return dictMesuresReduites

        

        





    












