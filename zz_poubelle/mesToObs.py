import numpy as np



def estPair(num):
    if num%2 == 0:
        return True
    else:
        return False


def chOrthoToLocal(chOrtho):
               
    sessionChOrtho = np.zeros(shape=(len(chOrtho),2))
    gisements = np.zeros(shape=(len(chOrtho),1))
    gisPrec = 0.0
    
    for i in range(0,len(chOrtho)):  
        
        cote = chOrtho[i]
        
        if i == 1:
            sessionChOrtho[i] = np.array([0,cote])
            
        if i != 0 and i != 1:
            
            yPrec = sessionChOrtho[i-1,0]
            xPrec = sessionChOrtho[i-1,1]
            gisPrec = gisements[i-1,0]
            if cote < 0: 
                gisNouv = gisPrec - 100.0
                yNouv = np.sin(gisNouv*np.pi/200.0)*abs(cote) + yPrec
                xNouv = np.cos(gisNouv*np.pi/200.0)*abs(cote) + xPrec
                sessionChOrtho[i,0] = yNouv
                sessionChOrtho[i,1] = xNouv
                gisements[i,0] = gisNouv
                
            if cote > 0:
                gisNouv = gisPrec + 100.0
                yNouv = np.sin(gisNouv*np.pi/200.0)*abs(cote) + yPrec
                xNouv = np.cos(gisNouv*np.pi/200.0)*abs(cote) + xPrec
                sessionChOrtho[i,0] = yNouv
                sessionChOrtho[i,1] = xNouv
                gisements[i,0] = gisNouv
            
    return sessionChOrtho     #np.array([[y,x],[y,x],...])   



def mesToObs(dictMesuresReduites, dictModeleStochastique):
    
    dictObs = {}
    idObs = 1000001
    idIncOri = 700000
    dictSupp = {}
    

    
    for idSta,data in dictMesuresReduites.items():
        
        typeLeve = data['typeLeve']
        indexCO = 0
        
        
        for mes in data['listeMes']:
            
            if mes['supp'] == True and mes['mesId']<2000000: # uniquement les mesures et pas les observations réduites avec l'id <2000000
                print('Mesure supprimée: {:<5s}idSta: {:<8s}ptDep: {:<15s}ptVis: {:<15s}valMes: {:s}'.format(mes['typeMes'],str(idSta),mes['noDep'],mes['noVis'],str(mes['valMes'])))
                dictSupp.update({mes['mesId']:{'typeMes':mes['typeMes'],
                                 'idSta':idSta,
                                 'noDep':mes['noDep'],
                                 'noVis':mes['noVis'],
                                 'valMes':mes['valMes']} })
                
            
            else:
                
                
                # STATIONS POLAIRES CORR ET REDUITES: garder uniq. les obs. corr. et réduites (nouvel mesId > 2'000'000)
                # OU SESSION GNSS
                typeMes = mes['typeMes']
                
                if  mes['mesId']>=2000000 or typeMes=='LY' or typeMes=='LX' or typeMes=='LOY' or typeMes=='LOX' or typeMes=='CO' or typeMes=='CC' or typeMes=='DC' : 
                    
                    # attribut d'observation
                    noDep = mes['noDep']
                    noVis = mes['noVis']
                    typeMes = mes['typeMes']
                    valObs = mes['valMes']
                    vientStaId = idSta
                    sigmaL = 0.0
                    sigmaCentDep = 0.0
                    sigmaCentVis = 0.0
                    
                    
                    
                    
                    
                    # --- LEDET ---
                    if typeLeve == 'STATION S/POINT LEDET':
                        sigmaCentDep = dictModeleStochastique['sCentStSpoint']
                        sigmaCentVis = dictModeleStochastique['sCentVisLEDET']
                        if typeMes == 'RI' : # directions
                            typeObs = 'RI'
                            sigmaL = dictModeleStochastique['sDirectionLEDET'] 
                            if mes['depl'] == True: # si il y a eu dlat et/ou dlon
                                sigmaL = dictModeleStochastique['sDirectionLEDETsiDlatDlon']
                            groupeStoch = 'dirLEDET'
                        if typeMes == 'DP' : # distances
                            typeObs = 'DP'
                            sigmaL = dictModeleStochastique['sDistanceLEDET']
                            if mes['depl'] == True: # si il y a eu dlat et/ou dlon
                                sigmaL = dictModeleStochastique['sDistanceLEDETsiDlatDlon']
                            groupeStoch = 'distLEDET'
                    
                    if typeLeve == 'STATION LIBRE LEDET':
                        sigmaCentDep = dictModeleStochastique['sCentStLibre']
                        sigmaCentVis = dictModeleStochastique['sCentVisLEDET']
                        if typeMes == 'RI' : # directions
                            typeObs = 'RI'
                            sigmaL = dictModeleStochastique['sDirectionLEDET'] 
                            if mes['depl'] == True: # si il y a eu dlat et/ou dlon
                                sigmaL = dictModeleStochastique['sDirectionLEDETsiDlatDlon']
                            groupeStoch = 'dirLEDET'
                        if typeMes == 'DP' : # distances
                            typeObs = 'DP'
                            sigmaL = dictModeleStochastique['sDistanceLEDET']
                            if mes['depl'] == True: # si il y a eu dlat et/ou dlon
                                sigmaL = dictModeleStochastique['sDistanceLEDETsiDlatDlon']
                            groupeStoch = 'distLEDET'
                                
                    if typeLeve == 'SESSION GNSS LEDET': 
                        sigmaCentDep = dictModeleStochastique['sCentVisLEDET']
                        sigmaCentVis = dictModeleStochastique['sCentVisLEDET']
                        if typeMes == 'LY' : # obs E
                            sigmaL = dictModeleStochastique['sSessionGNSS'] 
                            typeObs = 'LY'
                            groupeStoch = 'RTK'
                        if typeMes == 'LX' : # obs N
                            sigmaL = dictModeleStochastique['sSessionGNSS']
                            typeObs = 'LX'   
                            groupeStoch = 'RTK'
                            
                    if typeLeve == 'LEVE ORTHO': 
                        sigmaCentDep = 0.0
                        sigmaCentVis = 0.0
                        if typeMes == 'LOY' : # obs E
                            sigmaL = dictModeleStochastique['sCote'] 
                            typeObs = 'LY'
                            groupeStoch = 'COTE'
                        if typeMes == 'LOX' : # obs N
                            sigmaL = dictModeleStochastique['sCote']
                            typeObs = 'LX'    
                            groupeStoch = 'COTE'
                           
                    if typeLeve == 'COTE CTRL LEDET': 
                        sigmaCentDep = 0.0
                        sigmaCentVis = 0.0
                        if typeMes == 'CC' : # cote simple (non-signée) en DP
                            sigmaL = str(dictModeleStochastique['sCote']) + '+0.0' 
                            typeObs = 'DP'
                            groupeStoch = 'COTE'
                            
                    if typeLeve == 'CHEMINEMENT ORTHO' and mes['supp'] == False: 
                        sigmaCentDep = 0.0
                        sigmaCentVis = 0.0
                        if typeMes == 'CO' : # obs CO (toujours valeur unique et signée)
                            sigmaL = dictModeleStochastique['sCote'] 
                            listeCO = [] # pour entrée dans la fonction de ch. ortho à yx local
    
                            for idStaCO,dataSta in dictMesuresReduites.items():
                                if dataSta['typeLeve'] == 'CHEMINEMENT ORTHO':
                                    if idSta == idStaCO: # uniq. cette session de ch. ortho
                                        for mesu in dataSta['listeMes']:
                                            listeCO.append(mesu['valMes'])
                                            
    
                            yxLocal = chOrthoToLocal(listeCO) 
                            valObsLY = yxLocal[indexCO,0]
                            valObsLX = yxLocal[indexCO,1]
                            indexCO += 1
                            
                            # création du dict de l'obs. LY
                            dataObs = {'noDep': noVis,
                                       'noVis': noVis,
                                       'typeObs': 'LY',
                                       'valObs': round(valObsLY,4),
                                       'vientStaId': vientStaId,
                                       'groupeStoch':'COTE',
                                       'sigmaL': sigmaL,
                                       'sigmaCentDep': sigmaCentDep,
                                       'sigmaCentVis': sigmaCentVis }
                            dictObs.update({ idObs: dataObs })
                            idObs += 1
                            # création du dict de l'obs. LX
                            dataObs = {'noDep': noVis,
                                       'noVis': noVis,
                                       'typeObs': 'LX',
                                       'valObs': round(valObsLX,4),
                                       'vientStaId': vientStaId,
                                       'groupeStoch':'COTE',
                                       'sigmaL': sigmaL,
                                       'sigmaCentDep': sigmaCentDep,
                                       'sigmaCentVis': sigmaCentVis }
                            dictObs.update({ idObs: dataObs })
                            idObs += 1
                             
                    if typeLeve == 'PTS ALIGNES, DISTANCES CUMULEES LEDET' and mes['supp'] == False: 
                        sigmaCentDep = 0.0
                        sigmaCentVis = 0.0
                        if typeMes == 'DC' : # obs E
                            sigmaL = dictModeleStochastique['sCote'] 
                            typeObs = 'LY'
                            # création du dict de l'obs. LY
                            dataObs = {'noDep': noVis,
                                       'noVis': noVis,
                                       'typeObs': 'LY',
                                       'valObs': valObs,
                                       'vientStaId': vientStaId,
                                       'groupeStoch':'COTE',
                                       'sigmaL': sigmaL,
                                       'sigmaCentDep': sigmaCentDep,
                                       'sigmaCentVis': sigmaCentVis }
                            dictObs.update({ idObs: dataObs })
                            idObs += 1
                            # création du dict de l'obs. LX (LX=0 car aligné)
                            dataObs = {'noDep': noVis,
                                       'noVis': noVis,
                                       'typeObs': 'LX',
                                       'valObs': 0.0,
                                       'vientStaId': vientStaId,
                                       'groupeStoch':'COTE',
                                       'sigmaL': sigmaL,
                                       'sigmaCentDep': sigmaCentDep,
                                       'sigmaCentVis': sigmaCentVis }
                            dictObs.update({ idObs: dataObs })
                            idObs += 1
                            
    
                            
                            
                                
                    # --- PF ---
                    if typeLeve == 'STATION POLAIRE PF':
                        sigmaCentDep = dictModeleStochastique['sCentStSpoint']
                        sigmaCentVis = dictModeleStochastique['sCentVisPF']
                        if typeMes == 'RI' : # directions
                            typeObs = 'RI'
                            sigmaL = dictModeleStochastique['sDirectionPF'] 
                            if mes['depl'] == True: # si il y a eu dlat et/ou dlon
                                sigmaL = dictModeleStochastique['sDirectionLEDETsiDlatDlon']
                            groupeStoch = 'dirPF'
                        if typeMes == 'DP' : # distances
                            typeObs = 'DP'
                            sigmaL = dictModeleStochastique['sDistancePF']
                            if mes['depl'] == True: # si il y a eu dlat et/ou dlon
                                sigmaL = dictModeleStochastique['sDistanceLEDETsiDlatDlon']
                            groupeStoch = 'distPF'
    
                    if typeLeve == 'SESSION GNSS PF':
                        sigmaCentDep = dictModeleStochastique['sCentVisPF']
                        sigmaCentVis = dictModeleStochastique['sCentVisPF']
                        if typeMes == 'LY' : # obs session GNSS E
                            sigmaL = dictModeleStochastique['sSessionGNSS'] 
                            typeObs = 'LY'
                            groupeStoch = 'RTK'
                        if typeMes == 'LX' : # obs session GNSS N
                            sigmaL = dictModeleStochastique['sSessionGNSS']
                            typeObs = 'LX'
                            groupeStoch = 'RTK'
                        
                        
    
                     # Pour les dicos déjà créé au dessus (ch. ortho et pts alignés)
                    if typeLeve != 'CHEMINEMENT ORTHO' and typeLeve != 'PTS ALIGNES, DISTANCES CUMULEES LEDET' and mes['supp'] == False:
                        # création du dict de l'obs.
                        dataObs = {'noDep': noDep,
                                   'noVis': noVis,
                                   'typeObs': typeObs,
                                   'valObs': valObs,
                                   'vientStaId': vientStaId,
                                   'groupeStoch':groupeStoch,
                                   'sigmaL': sigmaL,
                                   'sigmaCentDep': sigmaCentDep,
                                   'sigmaCentVis': sigmaCentVis }
                    
                        # attribution de l'id de l'inconnue d'orientation (plusieurs stations sur le même pt)
                        if typeObs == 'RI' :
                            dataObs.update({ 'idIncOri': idIncOri})
                            
                        dictObs.update({ idObs: dataObs })
    
                        idObs += 1
                        
                    
                        
                
        idIncOri += 1 # change à chaque station physique (remise en station de l'instrument)
                
                
    print("--   Mesures converties en observations")         

    return dictObs, dictSupp