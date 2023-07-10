import os
from xml.dom import minidom


def fusionFichier(dirPath):
    
    listFiles = os.listdir(dirPath) 
    
    with open(dirPath + "fusionFiles.gme", "w") as new_file:
        for name in listFiles:
            with open(dirPath + name,'r') as f:
                for line in f:
                    new_file.write(line)
                new_file.write('\n')






def gme2xml(Filepath):
    
    doc = minidom.Document()
    canevas = doc.createElement('canevas')
    doc.appendChild(canevas)
    
    
    polaire = doc.createElement('polaire')
    canevas.appendChild(polaire)
    
    
    
    newStation = False
    with open(Filepath) as f:
        
        for line in f:
            line = line.strip()
            
            if len(line) > 0: # sauter les lignes vides
            
                indice = line[0:2]
                
                if indice == '10' and newStation == False : # no de stationnement
                    noSta, I = line[3:18], float(line[53:58])
                    
                    # initialisation de la balise du stationnement
                    station = doc.createElement('station')
                    polaire.appendChild(station)
                    
                    numeroStation = doc.createElement('numeroStation')
                    numeroStation.appendChild(doc.createTextNode(noSta))
                    
                    
                    
                    
                    
                    
                    station.appendChild(numeroStation)
                    
                    
                    
                    
                    
                    
                    
                    
                    newStation = True
                
                if indice == '11' or indice == '12':
                    newStation = False
                    
                    








    # --- FINALISATION ET GENERATION DU FICHIER ---
    xml_str = doc.toprettyxml(indent ="  ")
    with open('CanevasPolaire.xml', "w", encoding=('utf-8')) as f:
        f.write(xml_str) 
                    
                    



    
    return doc



# Fusion des fichiers de mesures des stations
# fusionFichier('C:\\01_ContraintesMsMo\\01_data\\02_MO-BelmontSurYverdon\\LeveDetail\\Diplome HEIG 2022\\Plan 1\\02_Calculs_Homere\\01_Leve_Theo\\')



dictCanevas = gme2xml('C:\\01_ContraintesMsMo\\01_data\\02_MO-BelmontSurYverdon\\LeveDetail\\Diplome HEIG 2022\\Plan 1\\02_Calculs_Homere\\01_Leve_Theo\\fusionFiles.gme')









