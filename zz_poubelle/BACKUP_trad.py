def traductionFRA2ENG(dictCanevas):
    
    
    dictENGmeasurments = {'measurements':{}}
    dictENGpoints = {'points':{}}
    dictENGparameters = {'parameters':{}}
    
    # -------------
    #### CANEVAS
    # -------------
    
    for key in dictCanevas['canevas'].keys():
        
        # Balises principales
        if key == "polaire":
            dictENGmeasurments['measurements'].update({'polar':{}})
        if key == "GNSS":
            dictENGmeasurments['measurements'].update({'GNSS':{}})  
        if key == "systemesLocaux":
            dictENGmeasurments['measurements'].update({'localSystems':{}})  
        if key == "cotes":
            dictENGmeasurments['measurements'].update({'simpleMeasures':{}})     
        if key == "contraintes":
            dictENGmeasurments['measurements'].update({'constraints':{}})      
            
            
    #### POLAIRE
    
    if "polaire" in dictCanevas['canevas'].keys():
        
        dictENGmeasurments['measurements']['polar'].update({'station':[]}) # liste
        listeStation = dictCanevas['canevas']['polaire']['station']
        listeENGstation = []
        for station in listeStation:

            stationENG = {'stationName': station['numeroStation'],
                          'stationData': {'centringGroup':station['stationnement']['groupeCentrage'],
                                              'directionGroup':station['stationnement']['groupeDirection'],
                                              'distanceGroup':station['stationnement']['groupeDistance'],
                                              'I':station['stationnement']['I'],
                                              'measure':[]} # liste
                          }
            
            for observation in station['stationnement']['observation']:
                
                stationENG['stationData']['measure'].append(
                {
                    "pointName":observation['numeroPoint'],
                    "RI":{
                       "stdDev":{
                          "cc":observation['RI']['ecartType']['cc']
                       },
                       "value":observation['RI']['valeur'],
                       "discarded":observation['RI']['ecarte']
                    },
                    "DS":{
                       "stdDev":{
                          "mm":observation['DS']['ecartType']['mm'],
                          "ppm":observation['DS']['ecartType']['ppm']
                       },
                       "value":observation['DS']['valeur'],
                       "discarded":observation['DS']['ecarte']
                    },
                    "ZD":{
                       "stdDev":{
                          "cc":observation['ZD']['ecartType']['cc']
                       },
                       "value":observation['ZD']['valeur'],
                       "discarded":observation['ZD']['ecarte']
                    },
                    "S":{
                       "value":observation['S']['valeur']
                    },
                    "dm1":{
                       "value":observation['dm1']['valeur']
                    },
                    "dm2":{
                       "value":observation['dm2']['valeur']
                    }
                } )
                
            listeENGstation.append(stationENG)
            
        # Ajouter la liste des stations en ENG    
        dictENGmeasurments['measurements']['polar']['station'] =  listeENGstation
        
    
    #### GNSS
    if "GNSS" in dictCanevas['canevas'].keys():
        dictENGmeasurments['measurements']['gnss'].update({'session':[]}) # liste
        listeSession = dictCanevas['canevas']['GNSS']['session']
        listeENGsession = []
        
        for session in listeSession:
            
            sessionENG = {'gnssGroup':''}
            
            
            
            
            
            
        
        
    
    
    return dictENGmeasurments
    
    
    
    
dictCanevas = conversionUtils.xml2dictionnaire(nomsFichiers['fichierXMLCanevas'])
    dictENGCanevas  = conversionUtils.traductionFRA2ENG(dictCanevas)
    
    xmlCanevas = xmltodict.unparse(dictENGCanevas, pretty=True, encoding='utf-8')
    with open(dirPath+"\\canevasENG.xml", 'w') as f:
        f.write(xmlCanevas)