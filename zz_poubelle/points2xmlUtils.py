# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 11:27:34 2022

@author: Matteo Casto, INSIT
"""

from xml.dom import minidom



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
    
    
    zonePtsFixes = False
    zonePtsNouv = False
    with open(filePathll1,'r') as f:

        for line in f:
            
            line = line.rstrip() # enlever le \n en fin de ligne
            
            
            #---------------------
            # --- POINTS FIXES ---  /!\ Ne sont dinstigués des autres uniquement dans le fichier paramètres
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
                points.appendChild(point)
                
                # Numéro
                numeroPoint = doc.createElement('numeroPoint')
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
            # --- AUTRES POINTS ---  /!\ Ne sont dinstigués des pts fixes uniquement dans le fichier paramètres
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
                points.appendChild(point)
                
                # Numéro
                numeroPoint = doc.createElement('numeroPoint')
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
    









    