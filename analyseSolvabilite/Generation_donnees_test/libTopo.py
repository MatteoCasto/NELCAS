"""Librairie de calculs topometriques
HEIG-VD 2021
"""

import math
import matplotlib.pyplot as plt
import copy
from itertools import combinations,product
import numpy as np    


def dInclReelle2dHzReelle(dInclReelle_m,angle_zen_gon):
    """ Distance inclinee reelle => Distance horizontale reelle

    Parameters
    ----------
        dInclReelle_m : float
            Distance inclinee reelle [m]
        angle_zen_gon : float
            Angle zénithal [gon]
    
    Returns
    -------
        dHzReelle_m : float
            Distance horizontale reelle [m]
    """
    
    zen = angle_zen_gon*math.pi/200.0
    dHzReelle_m = dInclReelle_m*math.sin(zen)

    return dHzReelle_m

def dHzReelle2dInclReelle(dHzReelle_m,angle_zen_gon):
    """ Distance horizontale reelle => Distance inclinee reelle 

    Parameters
    ----------
        dHzReelle_m   : float
            Distance horizontale reelle [m]
        angle_zen_gon : float
            Angle zenithal [gon]
    
    Returns
    -------
        dInclReelle_m : float
            Distance inclinee reelle [m]
    """
    
    zen = angle_zen_gon*math.pi/200.0
    dInclReelle_m = dHzReelle_m/math.sin(zen)

    return dInclReelle_m

def dHzReelle2dPlanProj(dHzReelle_m,N_m,N0_m,H_m):
    """ Distance horizontale reelle => Distance plan de projection 

    Parameters
    ----------
        dHzReelle_m : float
            Distance horizontale reelle [m]
        N_m         : float
            Coordonnees Nord [m]
        N0_m        : float
            Coordonnees Nord du centre de projection [m]
        H_m         : float
            Altitude [m]
    
    Returns
    -------
        resultats : dict
            'dPlanProj_m' : float
                Distance dans le plan de projection [m]
            'corrH'       : float
                Correction de la reduction au niveau de la mer [m]
            'corrProj'    : float 
                Correction de la projection [m]        
            'corrTotale'  : float
                Correction totale [m]
            'ppmH'        : float
                Facteur d'ech. de la reduction au niveau de la mer [ppm]
            'ppmProj'     : float
                Facteur d'ech. de la projection [ppm]
            'ppmTotal'    : float
                Facteur d'ech. total [ppm]
    """

    R = 6380000.0
    corrH = -H_m/R*dHzReelle_m
    d0_m = dHzReelle_m + corrH
    corrProj = (N_m-N0_m)**2/(2*R**2)*d0_m   
    dPlanProj_m = d0_m + corrProj
    corrTotale = corrH + corrProj
    
    ppmH = (-H_m/R*1000.0)*1000.0
    ppmProj = ((N_m-N0_m)**2/(2*R**2)*1000.0)*1000.0
    ppmTotal = ppmH + ppmProj

    resultats = {}
    resultats.update({'dPlanProj_m':dPlanProj_m})
    resultats.update({'corrH':corrH})
    resultats.update({'corrProj':corrProj})
    resultats.update({'corrTotale':corrTotale})
    resultats.update({'ppmH':ppmH})
    resultats.update({'ppmProj':ppmProj})
    resultats.update({'ppmTotal':ppmTotal})
    
    return resultats

def dPlanProj2dHzReelle(dPlanProj_m,N_m,N0_m,H_m):
    """Distance plan de projection => Distance horizontale reelle

    Parameters
    ----------
        dPlanProj_m : float
            Distance dans le plan de projection [m]
        N_m         : float
            Coordonnees Nord [m]
        N0_m        : float
            Coordonnees Nord du centre de projection [m]
        H_m         : float
            Altitude [m]
    
    Returns
    -------
        resultats : dict
            'dHzReelle_m' : float
                Distance horizontale reelle [m]
            'corrH'       : float
                Correction de l'altitude' [m]
            'corrProj'    : float 
                Correction de la projection [m]        
            'corrTotale'  : float
                Correction totale [m]
            'ppmH'        : float
                Facteur d'ech. de l'altitude [ppm]
            'ppmProj'     : float
                Facteur d'ech. de la projection [ppm]
            'ppmTotal'    : float
                Facteur d'ech. total [ppm]
    """

    R = 6380000.0
    corrProj = -(N_m-N0_m)**2/(2*R**2)*dPlanProj_m
    d0_m = dPlanProj_m + corrProj    
    corrH = +H_m/R*d0_m
    dHzReelle_m =  d0_m + corrH
    corrTotale = corrH + corrProj
        
    ppmH = (H_m/R*1000.0)*1000.0
    ppmProj = -((N_m-N0_m)**2/(2*R**2)*1000.0)*1000.0
    ppmTotal = ppmH + ppmProj

    resultats = {}
    resultats.update({'dHzReelle_m':dHzReelle_m})
    resultats.update({'corrH':corrH})
    resultats.update({'corrProj':corrProj})
    resultats.update({'corrTotale':corrTotale})
    resultats.update({'ppmH':ppmH})
    resultats.update({'ppmProj':ppmProj})
    resultats.update({'ppmTotal':ppmTotal})
    
    return resultats

def gisementAB(EA_m,NA_m,EB_m,NB_m):
    """ Calcul d'un gisement entre A et B

    Parameters
    ----------
        EA_m : float
            coordonnee Est du point A [m]
        NA_m : float
            coordonnee Nord du point A [m]
        EB_m : float
            coordonnee Est du point B [m]
        NB_m : float
            coordonnee Nord du point B [m]
    
    Returns
    -------
        gisAB_gon : float
            gisement entre A et B [gon]
    """    
    
    
    DE = EB_m-EA_m
    DN = NB_m-NA_m
    gisAB_gon = math.atan2(DE,DN)*200.0/math.pi
    
    if gisAB_gon < 0.0:
        gisAB_gon += 400.0        
    
    return gisAB_gon

def distanceAB(EA_m,NA_m,EB_m,NB_m):
    
    """ Calcul d'une distance entre A et B

    Parameters
    ----------
        EA_m : float
            coordonnee Est du point A [m]
        NA_m : float
            coordonnee Nord du point A [m]
        EB_m : float
            coordonnee Est du point B [m]
        NB_m : float
            coordonnee Nord du point B [m]
    
    Returns
    -------
        dAB_m : float
            distance entre A et B [m]
    """        
    
    DE = EB_m-EA_m
    DN = NB_m-NA_m
    dAB_m = math.sqrt(DE**2+DN**2)
        
    return dAB_m

def gisement(dictPts,noA,noB):
    
    """ Calcul d'un gisement entre A et B

    Parameters
    ----------
        dictPts : dict
            dictionnaire de points
        noA : str
            numero du point A
        noB : str
            numero du point B
    
    Returns
    -------
        gisement : float
            gisement entre A et B [gon]
    """      

    EA = dictPts[noA]['E']
    NA = dictPts[noA]['N']
    EB = dictPts[noB]['E']
    NB = dictPts[noB]['N']

    gisement = gisementAB(EA,NA,EB,NB)    
   
    return gisement

def distance(dictPts,noA,noB):

    """ Calcul d'une distance entre A et B

    Parameters
    ----------
        dictPts : dict
            dictionnaire de points
        noA : str
            numero du point A
        noB : str
            numero du point B
    
    Returns
    -------
        distance : float
            distance entre A et B [gon]
    """      
   

    EA = dictPts[noA]['E']
    NA = dictPts[noA]['N']
    EB = dictPts[noB]['E']
    NB = dictPts[noB]['N']

    distance = distanceAB(EA,NA,EB,NB)    
   
    return distance

def importPoints(path):
    """ Import de points a partir d'un fichier

    Parameters
    ----------
        path : str
            fichier des points            

                format:
                    no -> E -> N -> (H)
    
    Returns
    -------
        points : dict

            'no' : str
                numero du point

            data : dict
                
                'E' : float
                    coordonnee Est [m]
                'N' : float
                    coordonnee Nord [m]
                'H' : float
                    Altitude [m]
    """    
    
    #creation du dictionnaire des points
    points = {}
    
    #ouverture du fichier texte
    fichier = open(path,'r')
    
    #lecture de la 1ere ligne
    line = fichier.readline()
    #boucle pour toutes les lignes
    while line:
        
        #si le 1er char n'est pas un commentaire
        if line[0] != '#':
            
            data = line.strip().split('\t')
            no = data[0]
            E = float(data[1])
            N = float(data[2])            
            donnees = {'E':E,'N':N}
            
            if len(data) >= 4:
                H = float(data[3])
                donnees.update({'H':H})
            
            points.update({no:donnees})
            
        line = fichier.readline()
    
    #fermeture du fichier texte    
    fichier.close()    
    
    return points

def exportPoints(path,dictPts):
    """ Export de points a partir d'un dictionnaire de points

    Parameters
    ----------
        path : str
            fichier d'export            

                format:
                    no -> E -> N -> (H)
                    
        dictPts : dict
            dictionnaire des points
    
    Returns
    -------
    
        rien
    
    """        
    
    #ouverture du fichier texte
    fichier = open(path,'w')

    #ecriture de la ligne d'entete    
    fichier.write("#no\tE[m]\tN[m]\tH[m]\n")
    
    #ecriture des points
    for key,data in dictPts.items():
        
        if 'H' in data.keys():
            fichier.write("{:s}\t{:0.4f}\t{:0.4f}\t{:0.4f}\n".format(key,
                                                                     data['E'],
                                                                     data['N'],
                                                                     data['H']))
        else:
            fichier.write("{:s}\t{:0.4f}\t{:0.4f}\n".format(key,
                                                            data['E'],
                                                            data['N']))

            
    #fermeture du fichier texte    
    fichier.close()

    

def importObservations(path):
    """ Import des observations a partir d'un fichier

    Parameters
    ----------
        path : str
            fichier des observtions
            
                format:
                    no Sta -> no Vis -> I -> S -> rhz -> zen -> (dincl)
    
    Returns
    -------
        observations : dict

            (noSta,noVis) : tuple
                
                noSta : str
                    numero du point de station
                noVis : str
                    numero du point vise

            data : dict
                
                'I' : float
                    hauteur d'instrument [m]
                'S' : float
                    hauteur du signal [m]
                'rhz' : float
                    direction horizontale [gon]
                'zen' : float
                    angle zenithal [gon]
                'dincl' : float
                    distance inclinee [m]
    """        
    
    #creation du dictionnaire des observations
    observations = {}
    
    #ouverture du fichier texte
    fichier = open(path,'r')

    #lecture de la 1ere ligne
    ligne = fichier.readline().strip()
    #boucle pour toutes les lignes
    while ligne:
        if ligne[0] != '#':
            data = ligne.split('\t')
            numero_sta = data[0]
            numero_vis = data[1]
            cleObs = (numero_sta,numero_vis)

            donnees = {}
            I = float(data[2])
            S = float(data[3])            
            donnees.update({'I':I})
            donnees.update({'S':S})

            if len(data)>4:
                rhz = float(data[4])            
                zen = float(data[5])            
                donnees.update({'rhz':rhz})
                donnees.update({'zen':zen})

            if len(data)>6:
                dincl = float(data[6])
                donnees.update({'dincl':dincl})

            observations.update({cleObs:donnees})

        ligne = fichier.readline().strip()
            
    fichier.close()
    
    return observations

def plotPoints(dictPts,symbole='o',taille_symbole=7.0,couleur='k'):
    """ plot d'un dictionnaire de points 

    Parameters
    ----------
        dictPts : dict
            dictionnaire des points            
        symbole : str
            symbole des points ('.','o','^',...)
        taille_symbole : float
            taille des symboles
        couleur : str
            couleur des points ('k','b','r',...)
    
    Returns
    -------
        rien
    """            

    for key,data in dictPts.items():

        plt.plot(data['E'],data['N'],marker=symbole,color=couleur,markersize=taille_symbole)
        plt.text(data['E'],data['N'],key,fontsize=14,color=couleur)    
    
    plt.axis('equal')
     
def plotObservations(dictPts,dictObs,couleur='k'):
    """ plot d'un dictionnaire des observations 

    Parameters
    ----------
        dictPts : dict
            dictionnaire des points
        dictObs : dict
            dictionnaire des observations
        couleur : str
            couleur des points ('k','b','r',...)
    
    Returns
    -------
        rien
    """      
    
    for key,data in dictObs.items():        

        noSta=key[0]
        noVis=key[1]
        
        if noSta in dictPts.keys() and noVis in dictPts.keys():
        
            E_sta = dictPts[noSta]['E']
            N_sta = dictPts[noSta]['N']
            E_vis = dictPts[noVis]['E']
            N_vis = dictPts[noVis]['N']
            
            E_c = E_sta + (E_vis-E_sta)*0.75
            N_c = N_sta + (N_vis-N_sta)*0.75
            
            plt.plot([E_sta,E_c],[N_sta,N_c],color=couleur)
            plt.plot([E_c,E_vis],[N_c,N_vis],color=couleur,linestyle='--')
            
            if 'dincl' in data.keys():
                
                E_d = E_sta + (E_vis-E_sta)*0.2
                N_d = N_sta + (N_vis-N_sta)*0.2
                E_e = E_sta + (E_vis-E_sta)*0.4
                N_e = N_sta + (N_vis-N_sta)*0.4
                
                plt.plot([E_d,E_e],[N_d,N_e],color=couleur,linewidth=3)
        
        else:
            print('Observations entre la station: {:s}, et le point visé {:s} => pas dessinées!!'.format(noSta,noVis))
        
    plt.axis('equal')

def pointLanceBase(EA_m,NA_m,wA_gon,rAP_gon,dAP_m):
    """ calcul d'un point lance (fonction de base)

    Parameters
    ----------
        EA_m : float
            coordonnee Est du point A [m]            
        NA_m : float
            coordonnee Nord du point A [m]
        wA_gon : float
            inconnue d'orientation de la station A [gon]
        rAP_gon : float
            direction hz sur P [gon]
        dAP_m : float
            distance dans le plan de projection entre A et P [m]
    
    Returns
    -------
        resultats : dict
        
            'EP_m' : float
                coordonnee Est du point P                
            'NP_m' : float
                coordonnee Nord du point P
    """ 
    
    wA = wA_gon*math.pi/200.0
    rAP = rAP_gon*math.pi/200.0
    
    EP_m = EA_m + dAP_m*math.sin(wA+rAP)
    NP_m = NA_m + dAP_m*math.cos(wA+rAP)    
    
    resultats = {}
    resultats.update({'EP_m':EP_m})
    resultats.update({'NP_m':NP_m})    

    return resultats

def pointLance(dictPts,dictObs,noSta,wSta,noVis,N0_m):
    """ calcul d'un point lance

    Parameters
    ----------
        dictPts : dict
            dictionnaire des points
        dictObs : dict
            dictionnaire des observations
        noSta : str
            numero de la station
        wSta : float
            inconnue d'orientation de la station [gon]
        noVis : str
            numero du point vise
        N0_m : float
            coordonnee Nord du centre de la projection cartographique
    
    Returns
    -------
        resultats : dict
        
            'ptVise' : dict
                point vise calcule                
            'noSta' : str
                numero de la station
            'noVis' : str
                numero du point vise                
            'wSta' : float
                inconnue d'orientation de la station [gon]                
            'obs' : dict
                observation utilisee
            'res_dHzReelle2dPlanProj' : dict
                resultat de l'appel a la  fonction res_dHzReelle2dPlanProj(...)                 
                
    """ 
    
    resultats = {}

    dHzReelle_m = dInclReelle2dHzReelle(dictObs[(noSta,noVis)]['dincl'],dictObs[(noSta,noVis)]['zen'])
    res_dHzReelle2dPlanProj = dHzReelle2dPlanProj(dHzReelle_m,dictPts[noSta]['N'],N0_m,dictPts[noSta]['H'])
    dAP_proj = res_dHzReelle2dPlanProj['dPlanProj_m']

    rhzAP = dictObs[(noSta,noVis)]['rhz']

    pt = pointLanceBase(dictPts[noSta]['E'],dictPts[noSta]['N'],
                        wSta,rhzAP,dAP_proj)
    
    ptVise = {}
    ptVise.update({noVis: {'E':pt['EP_m'],'N':pt['NP_m']} })

    resultats.update({'ptVise':ptVise})
    resultats.update({'noSta':noSta})
    resultats.update({'noVis':noVis})
    resultats.update({'wSta':wSta})    
    resultats.update({'obs':dictObs[(noSta,noVis)]})    
    resultats.update({'res_dHzReelle2dPlanProj':res_dHzReelle2dPlanProj})    

    return resultats

def printTitrePointLance(path):
    """ ecriture des lignes de titre de la fonction pointLance(...)

    Parameters
    ----------
        path : str
            fichier des resultats
    
    Returns
    -------
        rien
                
    """ 
        
    fichier = open(path,'a', encoding='utf-8')
    fichier.write('\n\n=========================================\n')
    fichier.write('POINTS LANCES\n')
    fichier.write('=========================================\n\n')
    
    fichier.write('{:6s} {:>6s} {:>7s} {:>7s} '.format('STA','VISE','I ','S '))
    fichier.write('{:>10s} {:>10s} {:>10s} {:>10s}'.format('rhz ','zen ','dincl ','dproj '))
    fichier.write('{:>10s} {:>12s} {:>12s}\n\n'.format('w0 ','E ','N '))

    fichier.write('{:6s} {:>6s} {:>7s} {:>7s}'.format('','','[m]','[m]')) 
    fichier.write('{:>10s} {:>10s} {:>10s} {:>10s} '.format('[gon]','[gon]','[m]','[m]'))
    fichier.write('{:>10s} {:>12s} {:>12s}\n\n'.format('[gon]','[m]','[m]'))
    
    fichier.close()    

def printPointLance(path,ptLance):
    """ ecriture des resultats de la fonction pointLance(...)

    Parameters
    ----------
        path : str
            fichier des resultats            
        ptLance : dict
            dictionnaire des resultats de la fonction pointLance(...)
    
    Returns
    -------
        rien
                
    """ 
        
    if ptLance == {}:
        return

    fichier = open(path,'a', encoding='utf-8')
    fichier.write('{:6s} {:>6s} {:>7.3f} {:>7.3f} '.format(ptLance['noSta'],
                                                           ptLance['noVis'],
                                                           ptLance['obs']['I'],
                                                           ptLance['obs']['S']))
    
    fichier.write('{:>10.4f} {:>10.4f} {:>10.4f} {:>10.4f} '.format(ptLance['obs']['rhz'],
                                                                    ptLance['obs']['zen'],
                                                                    ptLance['obs']['dincl'],
                                                                    ptLance['res_dHzReelle2dPlanProj']['dPlanProj_m']))
    
    fichier.write('{:>10.4f} {:>12.3f} {:>12.3f}\n'.format(ptLance['wSta'],
                                                           ptLance['ptVise'][ptLance['noVis']]['E'],
                                                           ptLance['ptVise'][ptLance['noVis']]['N']))

    fichier.close()

def elementsImplantationBase(EA_m,NA_m,HA_m,wA_gon,EP_m,NP_m,N0_m):
    """ calcul des elements d'implantation (fonction de base)

    Parameters
    ----------
    
        EA_m : float
            coordonnee Est du point de la station [m]
        NA_m : float
            coordonnee Nord du point de la station [m]
        HA_m : float
            altitude du point de la station [m]
        wA_gon : float
            inconnue d'orientation de la station [m]
        EP_m : float
            coordonnee Est du point P [m]
        NP_m : float
            coordonnee Nord du point P [m]
        N0_m : float
            coordonnee Nord du centre de la projection cartographique [m]
            
    Returns
    -------
        resultats : dict
        
            'gisAP_gon' : float
                gisement entre les points A et P
            'rhzAP_gon' : float
                direction horizontale entre les points A et P
            'dHzReelle_m' : float
                distance horizontale reelle entre les points A et P
            'res_dHzReelle_AP' : dict
                resultat de la fonction dPlanProj2dHzReelle(...)
                
    """ 
    
    gisAP = gisementAB(EA_m,NA_m,EP_m,NP_m)
    rhzAP = gisAP-wA_gon
    if rhzAP < 0.0:
        rhzAP += 400.0
        
    dAP_plan = distanceAB(EA_m,NA_m,EP_m,NP_m) 
    res_dHzReelle_AP = dPlanProj2dHzReelle(dAP_plan,NA_m,N0_m,HA_m)
    dHzAPReelle_m = res_dHzReelle_AP['dHzReelle_m']
        
    resultats = {}
    resultats.update({'gisAP_gon':gisAP})
    resultats.update({'rhzAP_gon':rhzAP})
    resultats.update({'dHzAPReelle_m':dHzAPReelle_m})    
    resultats.update({'res_dHzReelle_AP':res_dHzReelle_AP})

    return resultats  

def elementsImplantation(dictPts,noSta,wSta_gon,noVise,N0_m):
    """ calcul des elements d'implantation

    Parameters
    ----------
    
        dictPts : dict
            dictionnaire des points
        noSta : str
            numero du point de station
        wSta_gon : float
            inconnue d'orientation de la station [m]
        noVise : str
            numero du point vise
        N0_m : float
            coordonnee Nord du centre de la projection cartographique [m]
            
    Returns
    -------
        resultats : dict
        
            'gisAP_gon' : float
                gisement entre les points A et P
            'rhzAP_gon' : float
                direction horizontale entre les points A et P
            'dHzReelle_m' : float
                distance horizontale reelle entre les points A et P
            'res_dHzReelle_AP' : dict
                resultat de la fonction dPlanProj2dHzReelle(...)
                
    """ 
    
    resultats = {}
    
    if not ( noSta in dictPts.keys() ):
        print('\nLa station {:s} n est pas connue...\n'.format(noSta))
        return resultats
        
    if not( noVise in dictPts.keys() ):
        print('\nLe point à implanter {:s} n est pas connu...\n'.format(noVise))
        return resultats
    
    if not ( 'H' in dictPts[noSta].keys() ):    
        print('\nL altitude de la station {:s} n est pas connue (correction de la distance)...\n'.format(noSta))
        return resultats
        
    EA_m = dictPts[noSta]['E']
    NA_m = dictPts[noSta]['N']
    HA_m = dictPts[noSta]['H']

    EP_m = dictPts[noVise]['E']
    NP_m = dictPts[noVise]['N']
    
    wA_gon = wSta_gon

    elemImpl = elementsImplantationBase(EA_m,NA_m,HA_m,wA_gon,EP_m,NP_m,N0_m)    
    
    resultats.update({'elemImpl':elemImpl})
    resultats.update({'noSta':noSta})
    resultats.update({'ESta':EA_m})
    resultats.update({'NSta':NA_m})
    resultats.update({'HSta':HA_m})
    resultats.update({'wSta_gon':wSta_gon})
    resultats.update({'noVise':noVise})
    resultats.update({'EVise':EP_m})
    resultats.update({'NVise':NP_m})
    return resultats



def printTitreElementsImplantation(path):
    """ ecriture des lignes de titre de la fonction elementsImplantation(...)

    Parameters
    ----------
        path : str
            fichier des resultats
    
    Returns
    -------
        rien
                
    """
    
    fichier = open(path,'a', encoding='utf-8')
    
    fichier.write('\n\n=========================================\n')
    fichier.write('ELEMENTS D IMPLANTATION\n')
    fichier.write('=========================================\n\n')
    
    fichier.write('{:5s} {:>12s} {:>12s} {:>10s} '.format('STA','E STA ','N STA ','H STA '))
    fichier.write('{:>5s} {:>12s} {:>12s} {:>10s} '.format('VISE','E VISE ','N VISE ','W0 '))
    fichier.write('{:>10s} {:>10s} {:>10s}\n'.format('gis ST-P ','rhz ','dhz '))
    
    fichier.write('{:5s} {:>12s} {:>12s} {:>10s} '.format('','[m]','[m]','[m]'))
    fichier.write('{:>5s} {:>12s} {:>12s} {:>10s} '.format('','[m]','[m]','[gon]'))
    fichier.write('{:>10s} {:>10s} {:>10s}\n\n'.format('[gon]','[gon]','[m]'))
    
    fichier.close()
    
def printElementsImplantation(path,elemImpl):
    """ ecriture des resultats de la fonction elementsImplantation(...)

    Parameters
    ----------
        path : str
            fichier des resultats            
        elemImpl : dict
            dictionnaire des resultats de la fonction elementsImplantation(...)
    
    Returns
    -------
        rien
                
    """ 
    
    if elemImpl == {}:
        return

    fichier = open(path,'a', encoding='utf-8')
    

    fichier.write('{:5s} {:>12.3f} {:>12.3f} {:>10.3f} '
                  '{:>5s} {:>12.3f} {:>12.3f} {:>10.4f} '
                  '{:>10.4f} {:>10.4f} {:>10.4f}\n'.format(elemImpl['noSta'],elemImpl['ESta'],
                                                           elemImpl['NSta'],elemImpl['HSta'],
                                                           elemImpl['noVise'],elemImpl['EVise'],
                                                           elemImpl['NVise'],elemImpl['wSta_gon'],
                                                           elemImpl['elemImpl']['gisAP_gon'],
                                                           elemImpl['elemImpl']['rhzAP_gon'],
                                                           elemImpl['elemImpl']['dHzAPReelle_m']))
    
    fichier.close()

    
def creationNouveauFichierResultats(path):
    """ creation d'un nouveau fichier texte

    Parameters
    ----------
        path : str
            fichier des resultats            
    
    Returns
    -------
        rien
                
    """ 
    
    import datetime
    fichier = open(path,"w")
    fichier.write("Fichier resultats topo cree le " + 
                  datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + "\n")
    fichier.close()
    
    
def moyennePonderee(donnees):
    """ calcul d'une moyenne ponderee

    Parameters
    ----------
        donnees : list [donnee,donnee,...,donnee]
            liste des donnees

                donnee : dict
                    'li' : float
                        mesure li
                    'sigma_li' : float
                        ecart-type de li
    
    Returns
    -------
        resultats : dict
            resultats du calcul            

            'lm' : float
                moyenne ponderee
            'sm' : float
                ecart-type de la moyenne ponderee
            's0' : float
                ecart-type de l'unite de poids'
            donnees : list [donnee,donnee,...,donnee]
                liste des donnees
                    donnee : dict
                        'li' : float
                            mesure li
                        'sigma_li' : float
                            ecart-type de li
                        'pi' : float
                            poids de li
                        'vi' : float
                            residu de li
                        'wi' : float
                            residu norme de li
                
    """ 
    
    donnees = copy.deepcopy(donnees)
    
    #calcul des poids
    for donnee in donnees:
        pi = 1/donnee['sigma_li']**2
        donnee.update({'pi':pi})
    
    #calcul de la moyenne ponderee
    sum_pili = 0.0
    sum_pi = 0.0
    for donnee in donnees:
        sum_pili += donnee['pi']*donnee['li']
        sum_pi += donnee['pi']
    
    lm = sum_pili/sum_pi
    
    #calcul des residus
    for donnee in donnees:
        vi = lm - donnee['li']
        wi = vi/donnee['sigma_li']
        donnee.update({'vi':vi})
        donnee.update({'wi':wi})
    
    #calcul de s0    
    sum_pivivi = 0.0
    for donnee in donnees:
        sum_pivivi += donnee['pi']*donnee['vi']*donnee['vi']
        
    n = len(donnees)
    if n > 1:
        s0 = math.sqrt(sum_pivivi/(n-1))
    else:
        s0 = math.nan
    
    #calcul de sm
    sm = s0/math.sqrt(sum_pi)
        
    resultats = {}
    resultats.update({'lm':lm})
    resultats.update({'sm':sm})
    resultats.update({'s0':s0})
    resultats.update({'donnees':donnees})

    return resultats     


def printMoyennePonderee(path,moyPond):    
    """ ecriture des resultats de la fonction moyennePonderee(...)

    Parameters
    ----------
        path : str
            fichier des resultats            
        moyPond : dict
            dictionnaire des resultats de la fonction moyennePonderee(...)
    
    Returns
    -------
        rien
                
    """ 
    
    if moyPond == {}:
        return

    fichier = open(path,'a', encoding='utf-8')    
    
    fichier.write('\nMOYENNE PONDEREE\n')
    fichier.write('================\n\n')

    fichier.write('{:<3s} {:>10s} {:>10s} '
                  '{:>10s} {:>5s}\n\n'.format('no',
                                              'li ',
                                              'sigma_li',
                                              'vi ',
                                              'wi '))
    
    i=0
    for donnee in moyPond['donnees']:
        i+=1
        fichier.write('{:<3d} {:>+10.4f} {:>+10.4f} '
                      '{:>+10.4f} {:>+5.1f}\n'.format(i,
                                                      donnee['li'],
                                                      donnee['sigma_li'],
                                                      donnee['vi'],
                                                      donnee['wi']))
    
    fichier.write('\ns0 = {:0.2f} [-]\n'.format(moyPond['s0']))
    fichier.write('lm = {:0.4f} +/- {:0.4f}\n'.format(moyPond['lm'],moyPond['sm']))
    fichier.close()
    
    
    
def orientationStation(dictPts,dictObs,noSta,listOri,sigma_r_gon,sigma_c_m):
    """ calcul de l'orientation a la station

    Parameters
    ----------
    
        dictPts : dict
            dictionnaire des points
        dictObs : dict
            dictionnaire des observations
        noSta : str
            numero du point de station
        listOri : list
            liste des numeros des points d'orientation
        noVise : str
            numero du point vise
        sigma_r_gon : float
            ecart-type d'une direction horizontale [gon]
        sigma_c_m : float
            ecart-type de centrage [m]
            
    Returns
    -------
        resultats : dict
        
            'noSta' : str
                numero du point de station
            'sigma_r_gon' : float
                ecart-type d'une direction horizontale [gon]
            'sigma_c_m' : float
                ecart-type de centrage [m]
            'w0_gon' : float
                orientation a la station moyenne [gon]
            'sw0_gon' : float
                ecart-type empirique de l'orientation a la station moyenne [gon]
            'moyPond' : dict
                dictionnaire des resultats de la fonction moyennePonderee(...)
                
    """ 
    listwi = []

    for noOri in listOri:
        
        if noSta in dictPts.keys() and noOri in dictPts.keys() and (noSta, noOri) in dictObs.keys():
                
            #calcul de wi
            gis_Si = gisement(dictPts, noSta, noOri)
            rhz_i = dictObs[(noSta, noOri)]['rhz']
            wi = gis_Si - rhz_i
            if wi < 0.0:
                wi += 400.0
            
            #calcul de l'ecart-type de wi
            dSi = distance(dictPts, noSta, noOri)
            sigma_gis = sigma_c_m/dSi*200.0/math.pi
            sigma_wi = math.sqrt( sigma_gis**2 + sigma_r_gon**2 )
            
            listwi.append({'li':wi,'sigma_li':sigma_wi,'noOri':noOri,'dist':dSi})

        else:
            print("La station {:s} n'existe pas OU "
                  "le point d'orientation {:s} n'existe pas OU "
                  "l'observation sur l'orientation {:s} n'existe pas".format(noSta,
                                                                             noOri,
                                                                             noOri))
            

    #calcul de la moyenne ponderee
    if len(listwi)>0:
        moyPond = moyennePonderee(listwi) 
    else:
        resultats = {}
        return resultats

    #output
    resultats = {}
    resultats.update({'noSta':noSta})
    resultats.update({'sigma_r_gon':sigma_r_gon})
    resultats.update({'sigma_c_m':sigma_c_m})
    resultats.update({'w0_gon':moyPond['lm']})    
    resultats.update({'sw0_gon':moyPond['sm']})    
    resultats.update({'moyPond':moyPond})

    return resultats



def printOrientationStation(path,oriSta):
    """ ecriture des resultats de la fonction orientationStation(...)

    Parameters
    ----------
        path : str
            fichier des resultats            
        oriSta : dict
            dictionnaire des resultats de la fonction orientationStation(...)
    
    Returns
    -------
        rien
                
    """ 

    if oriSta == {}:
        return

    fichier = open(path,'a', encoding='utf-8')    

    
    fichier.write('\n\n=========================================\n')
    fichier.write('ORIENTATION A LA STATION\n')
    fichier.write('=========================================\n\n')

    fichier.write('\nSTATION : {:s}\n'.format(oriSta['noSta']))

    fichier.write('\n{:50s} : {:0.4f} [gon]\n'.format('Ecart-type a priori d une direction horizontale',
                                                      oriSta['sigma_r_gon']))

    fichier.write('{:50s} : {:0.4f} [m]\n\n'.format('Ecart-type a priori de centrage',
                                                    oriSta['sigma_c_m']))
    
    fichier.write('\nRESULTATS\n')
    fichier.write('--------------\n\n')

    fichier.write('{:5s} : {:10.4f} +/- {:8.4f} [gon]\n'.format('w0',
                                                                oriSta['w0_gon'],
                                                                oriSta['sw0_gon']))

    fichier.write('{:5s} : {:10.2f} [-]\n'.format('s0',
                                                  oriSta['moyPond']['s0']))
    
    fichier.write('\nPOINTS VISES\n')
    fichier.write('--------------\n\n')
    
    fichier.write('{:10s} {:>10s} {:>8s} '
                  '{:>8s} {:>8s} {:>8s} '
                  '{:>10s}\n'.format('PT VISE',
                                     '\u03C9i ',
                                     '\u03C3\u03C9i ',
                                     'v ',
                                     'w ',
                                     'vlat ',
                                     'dist '))
    
    fichier.write('{:10s} {:>10s} {:>8s} '
                  '{:>8s} {:>8s} {:>8s} '
                  '{:>10s}\n\n'.format('',
                                       '[gon]',
                                       '[cc]',
                                       '[cc]',
                                       '[-]',
                                       '[mm]',
                                       '[m]'))

            
    for ori in oriSta['moyPond']['donnees']:
        fichier.write('{:10s} {:10.4f} {:8.1f} '
                      '{:+8.1f} {:+8.1f} {:+8.1f} '
                      '{:10.3f}\n'.format(ori['noOri'],
                                          ori['li'],
                                          ori['sigma_li']*1e4,
                                          ori['vi']*1e4,
                                          ori['wi'],
                                          1e3*ori['vi']*math.pi/200.0*ori['dist'],
                                          ori['dist']))
    

    fichier.close()
    
    
    
    
def intersectionDirectionsBase(EA_m,NA_m,gis_AP_gon,EB_m,NB_m,gis_BP_gon):
    """ calcul d'une intersection de directions (fonction de base)

    Parameters
    ----------
    
        EA_m : float
            coordonnee Est du point de la station A [m]
        NA_m : float
            coordonnee Nord du point de la station A [m]
        gis_AP_gon : float
            gisement AP [gon]
        EB_m : float
            coordonnee Est du point de la station B [m]
        NB_m : float
            coordonnee Nord du point de la station B [m]
        gis_BP_gon : float
            gisement BP [gon]
            
    Returns
    -------
        resultats : dict
        
            'EP_m' : float
                coordonnee Est du point P [m]
            'NP_m' : float
                coordonnee Nord du point P [m]
            'dAP_m' : float
                distance AP [m]
            'dBP_m' : float
                distance BP [m]
                
    """ 

    resultats = {}
    
    #test si les directions sont paralleles
    if math.fabs(gis_AP_gon - gis_BP_gon) < 1e-5 or math.fabs(math.fabs(gis_AP_gon - gis_BP_gon)-200.0) < 1e-5 :        
        print('\nLes deux directions sont paralleles => pas d intersection.\n')
        resultats.update({'EP_m':math.nan})
        resultats.update({'NP_m':math.nan})    
        resultats.update({'dAP_m':math.nan})
        resultats.update({'dBP_m':math.nan})
        return resultats

    gis_AP = gis_AP_gon*math.pi/200.0
    gis_BP = gis_BP_gon*math.pi/200.0

    #test pour choisir la formule à appliquer
    if math.fabs(gis_BP_gon - 100.0) > 1e-6 and math.fabs(gis_BP_gon - 300.0) > 1e-6:
        
        NP_m = NA_m + ( (EB_m-EA_m) - (NB_m-NA_m)*math.tan(gis_BP) ) / ( math.tan(gis_AP) - math.tan(gis_BP) )
        EP_m = EB_m + (NP_m-NB_m)*math.tan(gis_BP)
        
    else:
        
        NP_m = NB_m + ( (EA_m-EB_m) - (NA_m-NB_m)*math.tan(gis_AP) ) / ( math.tan(gis_BP) - math.tan(gis_AP) )
        EP_m = EA_m + (NP_m-NA_m)*math.tan(gis_AP)
        
    
    dAP_m = distanceAB(EA_m,NA_m,EP_m,NP_m)
    dBP_m = distanceAB(EB_m,NB_m,EP_m,NP_m)
    
    resultats.update({'EP_m':EP_m})
    resultats.update({'NP_m':NP_m})    
    resultats.update({'dAP_m':dAP_m})
    resultats.update({'dBP_m':dBP_m})
    
    return resultats

def intersectionDirections(dictPts,dictObs,listSta,sigma_gis_gon,sigma_c_m,noVise):
    """ calcul d'un point par intersection de directions

    Parameters
    ----------
        dictPts : dict
            dictionnaire des points
        dictObs : dict
            dictionnaire des observations
        listSta : list [sta,sta,...,sta]
            liste des stations
                sta : dict
                    'noSta' : str
                        numero de la station
                    'w0' : float
                        inconnue d'orientation de la station
        
        sigma_gis_gon : float
            ecart-type du gisement [gon]
        sigma_c_m : float
            ecart-type du centrage [m]

        noVise : str
            numero du point vise a determiner
    
    Returns
    -------
        resultats : dict
        
            'noVis' : str
                numero du point vise                
            'EP_m' : float
                coordonnee Est du point P [m]                
            'NP_m' : float
                coordonnee Nord du point P [m]                
            'sEP_m' : float
                ecart-type de la coordonnee Est du point P [m]                
            'sNP_m' : float
                ecart-type de la coordonnee Nord du point P [m]                
            'ptVise' : dict
                point vise calcule                
            'stations' : list
                liste des stations
            'combinaisons' : list
                liste des combinaisons
            'sigma_gis_gon' : float
                ecart-type du gisement [gon]
            'sigma_c_m' : float
                ecart-type du centrage [m]
            'moyPond_EP' : dict
                dictionnaire des resultats de la fonction moyennePonderee(...)
                pour le calcul de EP
            'moyPond_NP' : dict
                dictionnaire des resultats de la fonction moyennePonderee(...)
                pour le calcul de NP
                                
    """ 
    
    resultats = {}

    #determination des combinaisons
    combinaisons = {}
    for i in range(0,len(listSta)-1):
        for j in range(i+1,len(listSta)):            
            combinaison = {}
            combinaison.update({'wA':listSta[i]['w0']})
            combinaison.update({'wB':listSta[j]['w0']})
            combinaisons.update({(listSta[i]['noSta'],listSta[j]['noSta']):combinaison})

    list_EP = []
    list_NP = []
 
    for key,data in combinaisons.items():
        
        #calcul du gisement AP
        noA = key[0]
        EA = dictPts[noA]['E']
        NA = dictPts[noA]['N']
        wA = data['wA']
        rhz_AP = dictObs[(noA,noVise)]['rhz']
        gis_AP = wA + rhz_AP
        if gis_AP > 400.0:
            gis_AP = gis_AP - 400.0
        
        #calcul du gisement BP
        noB = key[1]
        EB = dictPts[noB]['E']        
        NB = dictPts[noB]['N']        
        wB = data['wB']
        rhz_BP = dictObs[(noB,noVise)]['rhz']
        gis_BP = wB + rhz_BP
        if gis_BP > 400.0:
            gis_BP = gis_BP - 400.0
        
        #Calcul de l intersection de direction
        interDir = intersectionDirectionsBase(EA,NA,gis_AP,EB,NB,gis_BP)
        data.update({'interDir':interDir})
        
        #Calcul de l ecart-type de l'intersection
        sigma_gis = sigma_gis_gon*math.pi/200.0
        dAP = interDir['dAP_m']
        dBP = interDir['dBP_m']
        
        sigma_P = math.sqrt( ( (sigma_gis*dAP)**2 + (sigma_gis*dBP)**2 ) * 1/math.sin( gis_AP*math.pi/200.0 - gis_BP*math.pi/200.0 )**2 + 2*sigma_c_m**2)
        
        dictEP = {}
        dictEP.update({'li':interDir['EP_m']})
        dictEP.update({'sigma_li':sigma_P})
        dictEP.update({'combinaison':key})
        list_EP.append(dictEP)
        
        dictNP = {}
        dictNP.update({'li':interDir['NP_m']})
        dictNP.update({'sigma_li':sigma_P})
        dictNP.update({'combinaison':key})
        list_NP.append(dictNP)

    #calcul du point P par moyenne ponderee
    moyPond_EP = moyennePonderee(list_EP)
    moyPond_NP = moyennePonderee(list_NP)
                
    #liste des informations des stations
    stations = []
    for sta in listSta:
        station = {}
        station.update({'noSta':sta['noSta']})
        station.update({'w0':sta['w0']})
        station.update({'E':dictPts[sta['noSta']]['E']})
        station.update({'N':dictPts[sta['noSta']]['N']})
        station.update({'rhz_P':dictObs[(sta['noSta'],noVise)]['rhz']})
        stations.append(station)
    
    EP = moyPond_EP['lm']
    NP = moyPond_NP['lm']
    sEP = moyPond_EP['sm']
    sNP = moyPond_NP['sm']
    ptVise = {}
    ptVise.update({noVise:{'E':EP,'N':NP} })
    
    resultats.update({'noVise':noVise})
    resultats.update({'EP_m':EP})
    resultats.update({'NP_m':NP})
    resultats.update({'sEP_m':sEP})
    resultats.update({'sNP_m':sNP})
    resultats.update({'ptVise':ptVise})
    resultats.update({'stations':stations})
    resultats.update({'combinaisons':combinaisons})
    resultats.update({'sigma_gis_gon':sigma_gis_gon})
    resultats.update({'sigma_c_m':sigma_c_m})
    resultats.update({'moyPond_EP':moyPond_EP})
    resultats.update({'moyPond_NP':moyPond_NP})
 
    return resultats

def printIntersectionDirections(path,interDir):
    """ ecriture des resultats de la fonction intersectionDirections(...)

    Parameters
    ----------
        path : str
            fichier des resultats            
        interDir : dict
            dictionnaire des resultats de la fonction intersectionDirections(...)
    
    Returns
    -------
        rien
                
    """     
    
    if interDir == {}:
        return
    
    fichier = open(path,'a', encoding='utf-8')    

    fichier.write('\n\n=========================================\n')
    fichier.write('INTERSECTION DE DIRECTION\n')
    fichier.write('=========================================\n\n')
    
    fichier.write('PT VISE : {:s}\n'.format(interDir['noVise']))

    fichier.write('{:50s} : {:0.4f} [gon]\n'.format('Ecart-type a priori d un gisement',
                                                    interDir['sigma_gis_gon']))

    fichier.write('{:50s} : {:0.4f} [m]\n\n'.format('Ecart-type a priori de centrage',
                                                    interDir['sigma_c_m']))

    fichier.write('\nRESULTATS\n')
    fichier.write('--------------\n\n')

    fichier.write('{:5s} {:>15s} {:>9s} '
                  '{:>15s} {:>9s}\n'.format('NO',
                                          'EP ',
                                          '\u03C3EP ',
                                          'NP ',
                                          '\u03C3NP '))
    
    fichier.write('{:5s} {:>15s} {:>9s} '
                  '{:>15s} {:>9s}\n\n'.format('',
                                            '[m]',
                                            '[m]',
                                            '[m]',
                                            '[m]'))
    
    fichier.write('{:5s} {:15.4f} {:9.4f} '
                  '{:15.4f} {:9.4f}\n'.format(interDir['noVise'],
                                           interDir['EP_m'],
                                           interDir['sEP_m'],
                                           interDir['NP_m'],
                                           interDir['sNP_m']))

    fichier.write('\n{:5s} : {:10.2f} [-]\n'.format('s0 (EP)',
                                                  interDir['moyPond_EP']['s0']))
    
    fichier.write('{:5s} : {:10.2f} [-]\n'.format('s0 (NP)',
                                                interDir['moyPond_NP']['s0']))

    fichier.write('\nSTATIONS/MESURES\n')
    fichier.write('------------------\n\n')
    fichier.write('{:5s} {:>15s} {:>15s} '
                  '{:>10s} {:>10s} {:>10s}\n'.format('NO',
                                                   'E ',
                                                   'N ',
                                                   '\u03C90 ',
                                                   'r ST-P ',
                                                   'gis ST-P '))

    fichier.write('{:5s} {:>15s} {:>15s} '
                  '{:>10s} {:>10s} {:>10s}\n\n'.format('',
                                                     '[m]',
                                                     '[m]',
                                                     '[gon]',
                                                     '[gon]',
                                                     '[gon]'))


    for sta in interDir['stations']:
        fichier.write('{:5s} {:15.4f} {:15.4f} '
                      '{:10.4f} {:10.4f} {:10.4f}\n'.format(sta['noSta'],
                                                          sta['E'],
                                                          sta['N'],
                                                          sta['w0'],
                                                          sta['rhz_P'],
                                                          sta['w0']+sta['rhz_P']))

    
    fichier.write('\nCOMBINAISONS\n')
    fichier.write('--------------\n\n')

    fichier.write('{:5s} {:5s} {:>15s} '
                  '{:>15s} {:>8s} {:>8s} '
                  '{:>8s} {:>8s} {:>8s} '
                  '{:>8s}\n'.format('STA',
                                  'STB',
                                  'EP ',
                                  'NP ',
                                  '\u03C3EP ',
                                  '\u03C3NP ',
                                  'v EP',
                                  'v NP',
                                  'w EP',
                                  'w NP'))
    
    fichier.write('{:5s} {:5s} {:>15s} '
                  '{:>15s} {:>8s} {:>8s} '
                  '{:>8s} {:>8s} {:>8s} '
                  '{:>8s}\n\n'.format('',
                                    '',
                                    '[m]',
                                    '[m]',
                                    '[mm]',
                                    '[mm]',
                                    '[mm]',
                                    '[mm]',
                                    '[-]',
                                    '[-]'))

    for key,data in interDir['combinaisons'].items():

        comb = (key[0],key[1])
        
        resE = {}
        resN = {}
        for donnee in interDir['moyPond_EP']['donnees']:
            if donnee['combinaison'] == comb:                
                resE = donnee

        for donnee in interDir['moyPond_NP']['donnees']:
            if donnee['combinaison'] == comb:                
                resN = donnee
                
        fichier.write('{:5s} {:5s} {:15.4f} '
              '{:15.4f} {:8.1f} {:8.1f} '
              '{:+8.1f} {:+8.1f} {:+8.1f} '
              '{:+8.1f}\n'.format(key[0],
                                key[1],
                                resE['li'],
                                resN['li'],
                                resE['sigma_li']*1e3,
                                resN['sigma_li']*1e3,
                                resE['vi']*1e3,
                                resN['vi']*1e3,
                                resE['wi'],
                                resN['wi']))
        


def relevementBase(E_A_m,N_A_m,E_B_m,N_B_m,E_C_m,N_C_m,rPA_gon,rPB_gon,rPC_gon):
    """ calcul d'un relevement methode de Kneissl (fonction de base)

    Parameters
    ----------
    
        EA_m : float
            coordonnee Est du point vise A [m]
        NA_m : float
            coordonnee Nord du point vise A [m]
        EB_m : float
            coordonnee Est du point vise B [m]
        NB_m : float
            coordonnee Nord du point vise B [m]
        EC_m : float
            coordonnee Est du point vise C [m]
        NC_m : float
            coordonnee Nord du point vise C [m]
        rPA_gon : float
            direction hz sur le point A [gon]
        rPB_gon : float
            direction hz sur le point B [gon]
        rPC_gon : float
            direction hz sur le point C [gon]
            
            
    Returns
    -------
        resultats : dict
        
            'EP_m' : float
                coordonnee Est du point P [m]
            'NP_m' : float
                coordonnee Nord du point P [m]
            'dPA_m' : float
                distance PA [m]
            'dPB_m' : float
                distance PB [m]
            'dPC_m' : float
                distance PC [m]
            'rPA_gon' : float
                direction hz sur le point A [gon]
            'rPB_gon'' : float
                direction hz sur le point B [gon]
            'rPC_gon' : float
                direction hz sur le point C [gon]
                
    """ 
    
    resultats = {}
    
    alpha_B_gon = rPB_gon - rPA_gon
    alpha_C_gon = rPC_gon - rPA_gon

    alpha_B = alpha_B_gon * math.pi/200.0
    alpha_C = alpha_C_gon * math.pi/200.0
    
    a = 1.0/math.tan(alpha_B)
    b = 1.0/math.tan(alpha_C)
    
    K1 = (N_B_m-N_A_m) - a*(E_B_m-E_A_m)
    K2 = (E_B_m-E_A_m) + a*(N_B_m-N_A_m)
    K3 = (N_C_m-N_A_m) - b*(E_C_m-E_A_m)    
    K4 = (E_C_m-E_A_m) + b*(N_C_m-N_A_m)
   
    C = -(K1-K3)/(K2-K4)
    
    DN = (K1+C*K2)/(1+C**2)
    DE = C*DN
    
    EP = E_A_m + DE    
    NP = N_A_m + DN
    
    dPA_m = distanceAB(EP,NP,E_A_m,N_A_m)
    dPB_m = distanceAB(EP,NP,E_B_m,N_B_m)
    dPC_m = distanceAB(EP,NP,E_C_m,N_C_m)
    
    resultats.update({'EP_m':EP})
    resultats.update({'NP_m':NP})
    resultats.update({'dPA_m':dPA_m})    
    resultats.update({'dPB_m':dPB_m})    
    resultats.update({'dPC_m':dPC_m})    
    resultats.update({'rPA_gon':rPA_gon})    
    resultats.update({'rPB_gon':rPB_gon})    
    resultats.update({'rPC_gon':rPC_gon})    
    
    return resultats        

def relevement(dictPts,dictObs,noSta,listVise,sigma_r_gon,sigma_c_m):
    """ calcul d'un point par relevement

    Parameters
    ----------
        dictPts : dict
            dictionnaire des points
        dictObs : dict
            dictionnaire des observations
        noSta : str
            numero de la station
        listVise : list [vis,vis,...]
            liste des points vise
                vis : str
                    numero du point vise
        
        sigma_r_gon : float
            ecart-type d'une direction hz [gon]
        sigma_c_m : float
            ecart-type du centrage [m]
    
    Returns
    -------
        resultats : dict
        
            'noSta' : str
                numero du point de station                
            'EP_m' : float
                coordonnee Est de la station P [m]                
            'NP_m' : float
                coordonnee Nord de la station P [m]                
            'sEP_m' : float
                ecart-type de la coordonnee Est de la station P [m]                
            'sNP_m' : float
                ecart-type de la coordonnee Nord de la station P [m]                
            'ptSta' : dict
                point de station calcule
            'listVises' : list
                liste des points vises
            'combinaisons' : list
                liste des combinaisons
            'sigma_r_gon' : float
                ecart-type d'une direction hz [gon]
            'sigma_c_m' : float
                ecart-type du centrage [m]
            'moyPond_EP' : dict
                dictionnaire des resultats de la fonction moyennePonderee(...)
                pour le calcul de EP
            'moyPond_NP' : dict
                dictionnaire des resultats de la fonction moyennePonderee(...)
                pour le calcul de NP
                                
    """ 
    

    
    resultats = {}

    
    #determination des combinaisons
    combinaisons = []
    for i in range(0,len(listVise)-2):
        for j in range(i+1,len(listVise)-1):
            for k in range(j+1,len(listVise)):
                comb = (listVise[i],listVise[j],listVise[k])
                combinaisons.append(comb)
                
    #calcul des relevements
    
    donnees_EP = []
    donnees_NP = []
    
    for combinaison in combinaisons:
        
        noA = combinaison[0]
        noB = combinaison[1]
        noC = combinaison[2]
        
        E_A_m = dictPts[noA]['E']
        N_A_m = dictPts[noA]['N']
        E_B_m =  dictPts[noB]['E']
        N_B_m =  dictPts[noB]['N']
        E_C_m =  dictPts[noC]['E']
        N_C_m =  dictPts[noC]['N']
        rPA_gon = dictObs[(noSta,noA)]['rhz']
        rPB_gon = dictObs[(noSta,noB)]['rhz']
        rPC_gon = dictObs[(noSta,noC)]['rhz']
    
        relev = relevementBase(E_A_m, N_A_m,
                                E_B_m, N_B_m,
                                E_C_m, N_C_m,
                                rPA_gon, rPB_gon, rPC_gon)
        
        #calcul de l'ecart-type
        sigma_r = sigma_r_gon*math.pi/200.0
        dPA = relev['dPA_m']
        dPB = relev['dPB_m']
        dPC = relev['dPC_m']
        rA = rPA_gon*math.pi/200.0
        rB = rPB_gon*math.pi/200.0
        rC = rPC_gon*math.pi/200.0
        num = sigma_r * (dPA + dPB + dPC)
        denom = math.fabs( math.sin(rB-rA) + math.sin(rC-rB) + math.sin(rA-rC) )
        sigma_P = math.sqrt( (num/denom)**2 + 2*sigma_c_m**2 )
        
        donnee_EP = {'li':relev['EP_m'],'sigma_li':sigma_P,'combinaison':combinaison}
        donnee_NP = {'li':relev['NP_m'],'sigma_li':sigma_P,'combinaison':combinaison}
        
        donnees_EP.append(donnee_EP)
        donnees_NP.append(donnee_NP)
    
    #calcul des moyennes ponderees
    moyPond_EP = moyennePonderee(donnees_EP)
    moyPond_NP = moyennePonderee(donnees_NP)
    
    #resultats
    resultats.update({'noSta':noSta})
    resultats.update({'EP_m':moyPond_EP['lm']})
    resultats.update({'NP_m':moyPond_NP['lm']})
    resultats.update({'sEP_m':moyPond_EP['sm']})
    resultats.update({'sNP_m':moyPond_NP['sm']})
    sta = {noSta:{'E':moyPond_EP['lm'],'N':moyPond_NP['lm']}}
    resultats.update({'ptSta': sta })
    resultats.update({'combinaisons': combinaisons })
    resultats.update({'sigma_r_gon': sigma_r_gon })
    resultats.update({'sigma_c_m': sigma_c_m })
    resultats.update({'moyPond_EP': moyPond_EP })
    resultats.update({'moyPond_NP': moyPond_NP })
    
    listVises = []
    for vis in listVise:
        vise = {}
        vise.update({'noVise':vis})
        vise.update({'E':dictPts[vis]['E']})
        vise.update({'N':dictPts[vis]['N']})
        vise.update({'rhz':dictObs[(noSta,vis)]['rhz']})
        listVises.append(vise)
    
    resultats.update({'listVises':listVises})    
        
    return resultats
    

def printRelevement(path,relev):
    """ ecriture des resultats de la fonction relevement(...)

    Parameters
    ----------
        path : str
            fichier des resultats            
        relev : dict
            dictionnaire des resultats de la fonction relevement(...)
    
    Returns
    -------
        rien
                
    """     
    
    if relev == {}:
        return
    
    fichier = open(path,'a', encoding='utf-8')       
    if relev == {}:
        return

    
    fichier.write('\n\n=========================================\n')
    fichier.write('RELEVEMENT\n')
    fichier.write('=========================================\n\n')
    
    fichier.write('\nPT STATION : {:s}\n'.format(relev['noSta']))

    fichier.write('\n{:50s} : {:0.4f} [gon]\n'.format('Ecart-type a priori d une direction',
                                                      relev['sigma_r_gon']))
    
    fichier.write('{:50s} : {:0.4f} [m]\n\n'.format('Ecart-type a priori de centrage',
                                                    relev['sigma_c_m']))

    fichier.write('\nRESULTATS\n')
    fichier.write('--------------\n\n')

    fichier.write('{:5s} {:>15s} {:>9s} {:>15s} {:>9s}\n'.format('NO',
                                                                 'EP ',
                                                                 '\u03C3EP ',
                                                                 'NP ',
                                                                 '\u03C3NP '))
    
    fichier.write('{:5s} {:>15s} {:>9s} {:>15s} {:>9s}\n\n'.format('',
                                                                   '[m]',
                                                                   '[m]',
                                                                   '[m]',
                                                                   '[m]'))
    
    fichier.write('{:5s} {:15.4f} {:9.4f} {:15.4f} {:9.4f}\n'.format(relev['noSta'],
                                           relev['moyPond_EP']['lm'],
                                           relev['moyPond_EP']['sm'],
                                           relev['moyPond_NP']['lm'],
                                           relev['moyPond_NP']['sm']))

    fichier.write('\n{:5s} : {:10.2f} [-]\n'.format('s0 (EP)',
                                                    relev['moyPond_EP']['s0']))
    
    fichier.write('{:5s} : {:10.2f} [-]\n'.format('s0 (NP)',
                                                  relev['moyPond_NP']['s0']))

    fichier.write('\nSTATIONS/MESURES\n')
    fichier.write('------------------\n\n')
    fichier.write('{:5s} {:>15s} {:>15s} {:>10s}\n'.format('NO',
                                                           'E ',
                                                           'N ',
                                                           'rhz '))
    
    fichier.write('{:5s} {:>15s} {:>15s} {:>10s}\n\n'.format('',
                                                             '[m]',
                                                             '[m]',
                                                             '[gon]'))
    
    for vis in relev['listVises']:
        fichier.write('{:5s} {:15.4f} {:15.4f} {:10.4f}\n'.format(vis['noVise'],
                                                                  vis['E'],
                                                                  vis['N'],
                                                                  vis['rhz']))

    
    fichier.write('\nCOMBINAISONS\n')
    fichier.write('--------------\n\n')

    fichier.write('{:5s} {:5s} {:5s} '
                  '{:>15s} {:>15s} {:>8s} '
                  '{:>8s} {:>8s} {:>8s} '
                  '{:>8s} {:>8s}\n'.format('A','B','C',
                                           'EP ','NP ','\u03C3EP ',
                                           '\u03C3NP ','vEP','vNP',
                                           'wEP','wNP'))
    
    fichier.write('{:5s} {:5s} {:5s} '
                  '{:>15s} {:>15s} {:>8s} '
                  '{:>8s} {:>8s} {:>8s} '
                  '{:>8s} {:>8s}\n\n'.format('','','',
                                             '[m]','[m]','[mm]',
                                             '[mm]','[mm]','[mm]',
                                             '[-]','[-]'))

    for comb in relev['combinaisons']:

        resE = {}
        resN = {}
        for donnee in relev['moyPond_EP']['donnees']:
            if donnee['combinaison'] == comb:                
                resE = donnee

        for donnee in relev['moyPond_NP']['donnees']:
            if donnee['combinaison'] == comb:                
                resN = donnee
                
        fichier.write('{:5s} {:5s} {:5s} '
                      '{:15.4f} {:15.4f} {:8.1f} '
                      '{:8.1f} {:+8.1f} {:+8.1f} '
                      '{:+8.1f} {:+8.1f}\n'.format(comb[0],comb[1],comb[2],
                                                   resE['li'],resN['li'],resE['sigma_li']*1e3,
                                                   resN['sigma_li']*1e3,resE['vi']*1e3,resN['vi']*1e3,
                                                   resE['wi'],resN['wi']))
        
    
    fichier.close()
    
    
    
def excentrique(dictPts,dictObs,noSta,noCentre,listOri,sigma_r_gon,sigma_c_m,N0_m):
    """ calcul d'un excentrique

    Parameters
    ----------
        dictPts : dict
            dictionnaire des points
        dictObs : dict
            dictionnaire des observations
        noSta : str
            numero de la station excentrique
        noCentre : str
            numero du centre
        listOri : list [ori,ori,...]
            liste des points d'orientation
                ori : str
                    numero des points d'orientation        
        sigma_r_gon : float
            ecart-type d'une direction hz [gon]
        sigma_c_m : float
            ecart-type du centrage [m]
        N0_m : float
            Coordonnees Nord du centre de projection [m]
    
    Returns
    -------
        resultats : dict
        
            'noSta' : str
                numero du point de station                
            'noCentre' : str
                numero du point du centre                
            'EE_m' : float
                coordonnee Est de la station E [m]                
            'NE_m' : float
                coordonnee Nord de la station E [m]                
            'wSta_gon' : float
                inconnue d'orientation de la station [gon]                                
            'ptSta' : dict
                point de station calcule
            'sigma_r_gon' : float
                ecart-type d'une direction hz [gon]
            'sigma_c_m' : float
                ecart-type du centrage [m]
            'moyPond_phiCE' : dict
                dictionnaire des resultats de la fonction moyennePonderee(...)
                pour le calcul de phiCE
            'dHzReelle2dPlanProj' : dict   
                dictionnaire des resultats de la fonction dHzReelle2dPlanProj(...)
                pour le calcul de e
            'e' : float
                distance excentrique-centre dans le plan de projection [m]
    """     
    
    #calcul de la distance e
    dIncl = dictObs[(noSta,noCentre)]['dincl']
    zen = dictObs[(noSta,noCentre)]['zen']
    
    dHzReelle = dInclReelle2dHzReelle(dIncl, zen)
    res_dHzReelle2dPlanProj = dHzReelle2dPlanProj(dHzReelle,
                                                  dictPts[noCentre]['N'],
                                                  N0_m,
                                                  dictPts[noCentre]['H'])
    
    e = res_dHzReelle2dPlanProj['dPlanProj_m']
    
    #calcul de phiCE
    donnees_phiCE = []
    for noOri in listOri:
    
        phiCA = gisement(dictPts, noCentre, noOri )
        dCA = distance(dictPts, noCentre, noOri)
        rA = dictObs[(noSta,noOri)]['rhz']
        rC = dictObs[(noSta,noCentre)]['rhz']
        alpha = rA-rC
        delta = 200.0/math.pi*math.asin( e/dCA*math.sin(alpha*math.pi/200.0) )     
        phiCE = phiCA + (200.0 - alpha - delta)
        if phiCE < 0.0:
            phiCE += 400.0
        if phiCE > 400.0:
            phiCE -= 400.0
            
        sigma_li = math.sqrt( sigma_r_gon**2 + 2*((sigma_c_m/dCA)*200.0/math.pi)**2 )
        
        donnee_phiCE = {'li':phiCE,'sigma_li':sigma_li,'noOri':noOri}
        donnees_phiCE.append(donnee_phiCE)
    
    moyPond_phiCE = moyennePonderee(donnees_phiCE)
    phiCEm = moyPond_phiCE['lm']
    
    #calcul de E par point lance
    pt = pointLanceBase(dictPts[noCentre]['E'],
                    dictPts[noCentre]['N'],
                    phiCEm,0.0,e)
    
    #calcul de l'inconnue d'orientation   
    wSta = phiCEm + 200 - rC
    if wSta < 0.0:
        wSta += 400.0
    if wSta > 400.0:
        wSta -= 400.0
    
    
    #resultats
    resultats = {}
    resultats.update({'noSta':noSta})
    resultats.update({'noCentre':noCentre})
    resultats.update({'EE_m':pt['EP_m']})
    resultats.update({'NE_m':pt['NP_m']})
    resultats.update({'wSta_gon':wSta})
    resultats.update({'ptSta':{noSta:{'E':pt['EP_m'],'N':pt['NP_m']}}})    
    resultats.update({'sigma_r_gon':sigma_r_gon})
    resultats.update({'sigma_c_m':sigma_c_m})
    resultats.update({'moyPond_phiCE':moyPond_phiCE})
    resultats.update({'dHzReelle2dPlanProj':res_dHzReelle2dPlanProj})
    resultats.update({'e':e})
    return resultats    
    
    
  

def printExcentrique(path,exc):
    """ ecriture des resultats de la fonction excentrique(...)

    Parameters
    ----------
        path : str
            fichier des resultats            
        relev : dict
            dictionnaire des resultats de la fonction excentrique(...)
    
    Returns
    -------
        rien
                
    """     
    
    if exc == {}:
        return
    
    fichier = open(path,'a', encoding='utf-8')       
    if exc == {}:
        return

    
    fichier.write('\n\n=========================================\n')
    fichier.write('EXCENTRIQUE\n')
    fichier.write('=========================================\n\n')
    
    fichier.write('\nPT STATION : {:s}\n'.format(exc['noSta']))

    fichier.write('\n{:50s} : {:0.4f} [gon]\n'.format('Ecart-type a priori d une direction',exc['sigma_r_gon']))
    fichier.write('{:50s} : {:0.4f} [m]\n\n'.format('Ecart-type a priori de centrage',exc['sigma_c_m']))

    fichier.write('\nRESULTATS\n')
    fichier.write('--------------\n\n')

    fichier.write('{:5s} {:>15s} {:>15s} {:>9s}\n'.format('NO','E ','N ','wSta'))
    fichier.write('{:5s} {:>15s} {:>15s} {:>9s}\n\n'.format('','[m]','[m]','[gon]'))
    fichier.write('{:5s} {:15.4f} {:15.4f} {:9.4f}\n'.format(exc['noSta'],
                                           exc['ptSta'][exc['noSta']]['E'],
                                           exc['ptSta'][exc['noSta']]['N'],
                                           exc['wSta_gon']))

    fichier.write('\nDISTANCE CENTRE-EXCENTRE (e)\n')
    fichier.write('---------------------------------------\n\n')
    fichier.write('{:5s} {:5s} {:>15s}\n'.format('CENT.','EXC.','e '))
    fichier.write('{:5s} {:5s} {:>15s}\n\n'.format('','','[m]'))
    fichier.write('{:5s} {:5s} {:15.4f}\n'.format(exc['noSta'],exc['noCentre'],exc['e']))

    fichier.write('\nGISEMENTS CENTRE-EXCENTRE (phi CE)\n')
    fichier.write('---------------------------------------\n\n')
    
    fichier.write('{:5s} : {:10.2f} [-]\n\n'.format('s0 (phi CE)',exc['moyPond_phiCE']['s0']))
    
    fichier.write('{:5s} {:>15s} {:>8s} {:>8s} {:>8s}\n'.format('NO','phi ','\u03C3 phi','v phi','w phi'))
    fichier.write('{:5s} {:>15s} {:>8s} {:>8s} {:>8s}\n\n'.format('','[gon]','[cc]','[cc]','[-]'))
    for ori in exc['moyPond_phiCE']['donnees']:
        fichier.write('{:5s} {:15.4f} {:8.1f} {:8.1f} {:8.1f}\n'.format(ori['noOri'],ori['li'],ori['sigma_li']*1e4,ori['vi']*1e4,ori['wi']))

    fichier.close()

def bilaterationBase(EA_m,NA_m,EB_m,NB_m,dAP_m,dBP_m):
    """ calcul d'une bilateration (fonction de base)

    Parameters
    ----------
    
        EA_m : float
            coordonnee Est du point vise A [m]
        NA_m : float
            coordonnee Nord du point vise A [m]
        EB_m : float
            coordonnee Est du point vise B [m]
        NB_m : float
            coordonnee Nord du point vise B [m]
        dAP_m : float
            distance dans le plan de projection entre A et P [m]
        dBP_m : float
            distance dans le plan de projection entre B et P [m]
                        
    Returns
    -------
        resultats : dict
        
            'EP1_m' : float
                coordonnee Est du point P1 [m]
            'NP1_m' : float
                coordonnee Nord du point P1 [m]
            'EP2_m' : float
                coordonnee Est du point P2 [m]
            'NP2_m' : float
                coordonnee Nord du point P2 [m]
            'gamma' : float
                angle gamma [rad]
            'dAP_m' : float
                distance dans le plan de projection entre A et P [m]
            'dBP_m' : float
                distance dans le plan de projection entre B et P [m]
                
    """         
    
    resultats = {}

    dAB_m = distanceAB(EA_m,NA_m,EB_m,NB_m)
    arg_alpha = (dAP_m**2+dAB_m**2-dBP_m**2)/(2*dAP_m*dAB_m)
    arg_beta = (dBP_m**2+dAB_m**2-dAP_m**2)/(2*dBP_m*dAB_m)    

    if arg_alpha <= 1.0:
        alpha = math.acos(arg_alpha)*200.0/math.pi
    else:
        alpha = 0.0

    if arg_beta <= 1.0:
        beta = math.acos(arg_beta)*200.0/math.pi
    else:
        beta = 0.0
    
    phiAB = gisementAB(EA_m,NA_m,EB_m,NB_m)
    phiAP1 = phiAB+alpha
    phiAP2 = phiAB-alpha

        
    resPtLance1 = pointLanceBase(EA_m,NA_m,0.0,phiAP1,dAP_m)
    resPtLance2 = pointLanceBase(EA_m,NA_m,0.0,phiAP2,dAP_m)
    
    gamma = (alpha+beta)*math.pi/200.0
    
    resultats.update({'EP1_m':resPtLance1['EP_m']})
    resultats.update({'NP1_m':resPtLance1['NP_m']})    
    resultats.update({'EP2_m':resPtLance2['EP_m']})
    resultats.update({'NP2_m':resPtLance2['NP_m']})
    resultats.update({'gamma':gamma})
    resultats.update({'dAP_m':dAP_m})
    resultats.update({'dBP_m':dBP_m})
    
    return resultats        


def multilateration(dictPts,dictObs,noSta,listVise,sigma_d_m,sigma_c_m,N0_m):
    """ calcul d'une multilateration

    Parameters
    ----------
        dictPts : dict
            dictionnaire des points
        dictObs : dict
            dictionnaire des observations
        noSta : str
            numero de la station excentrique
        listVise : list [vis,vis,...]
            liste des points vise
                vis : str
                    numero du point vise
        sigma_d_m : float
            ecart-type d'une distance [m]
        sigma_c_m : float
            ecart-type du centrage [m]
        N0_m : float
            Coordonnees Nord du centre de projection [m]
    
    Returns
    -------
        resultats : dict
        
            'noSta' : str
                numero du point de station                
            'ptSta' : dict
                point de station calcule                
            'listVise' : list [vis,vis,...]
                liste des points vise
            'sigma_d_m' : float
                ecart-type d'une distance [m]
            'sigma_c_m' : float
                ecart-type du centrage [m]
            'moyPond_EP' : dict
                dictionnaire des resultats de la fonction moyennePonderee(...)
                pour le calcul de EP
            'moyPond_NP' : dict
                dictionnaire des resultats de la fonction moyennePonderee(...)
                pour le calcul de NP

    """         
            
    resultats = {}
    
    #création de la liste de toutes les combinaisons possibles
    combinaisons = list(combinations(listVise,2))

    bilaterations = []    
    for combinaison in combinaisons:
        
        A = combinaison[0]
        B = combinaison[1]
        
        EA = dictPts[A]['E']
        NA = dictPts[A]['N']
        EB = dictPts[B]['E']
        NB = dictPts[B]['N']

        #distance AP dans le plan de projection
        dHzReelle_m = dInclReelle2dHzReelle(dictObs[(noSta,A)]['dincl'],
                                            dictObs[(noSta,A)]['zen'])
        
        res_dHzReelle2dPlanProj = dHzReelle2dPlanProj(dHzReelle_m,dictPts[A]['N'],
                                                      N0_m,dictPts[A]['H'])
        
        dAP_PlanProj = res_dHzReelle2dPlanProj['dPlanProj_m']

        #distance BP dans le plan de projection
        dHzReelle_m = dInclReelle2dHzReelle(dictObs[(noSta,B)]['dincl'],
                                            dictObs[(noSta,B)]['zen'])
        
        res_dHzReelle2dPlanProj = dHzReelle2dPlanProj(dHzReelle_m,dictPts[B]['N'],
                                                      N0_m,dictPts[B]['H'])
        
        dBP_PlanProj = res_dHzReelle2dPlanProj['dPlanProj_m']
    
        bilateration = bilaterationBase(EA,NA,EB,NB,dAP_PlanProj,dBP_PlanProj)
        bilateration.update({'combinaison':combinaison})
        bilaterations.append(bilateration)

    if len(bilaterations)==0:
        print("\nMULTILATERATION ({:d} mesures)".format(len(listVise)))
        print("===============")
        return {}
                    
    #Si seulement 2 mesures sont disponibles => return les 2 points
    if len(bilaterations)==1:
        
        #Création du dictionnaire avec les 2 points d'intersection
        dictOut = {}
        pt1 = {}
        pt1.update({'E_m':bilateration['EP1_m']})
        pt1.update({'N_m':bilateration['NP1_m']})
        dictOut.update({noSta+'_1':pt1})        

        pt2 = {}
        pt2.update({'E_m':bilateration['EP2_m']})
        pt2.update({'N_m':bilateration['NP2_m']})
        dictOut.update({noSta+'_2':pt2})
        
        print("\nMULTILATERATION ({:d} mesures)".format(len(listVise)))
        print("===============")
        print("intersection 1: E1= {:0.3f} [m], N1= {:0.3f} [m]".format(pt1['E_m'],pt1['N_m']))
        print("intersection 2: E2= {:0.3f} [m], N2= {:0.3f} [m]".format(pt2['E_m'],pt2['N_m']))

        return dictOut
        
        
    #Si plus de 2 mesures sont disponibles => return la solution unique
    else:

        #Calcul du point unique en testant toutes les combinaisons possibles
        #Création de la liste de toutes les combinaisons par produit cartésien
        combinaisons_points=list(product(['P1','P2'],repeat=len(bilaterations)))    

        #Calcul de la moyenne pondérée et de l'écart-type de chaque combinaison
        #de points
        multilaterations = []
        for combinaison_points in combinaisons_points:
            
            #Calcul de la moyenne pondérée et de l'écart-type
            listEP = []
            listNP = []
            for i in range(0,len(bilaterations)):
                
                noP = combinaison_points[i]
                
                if noP == 'P1':
                    Ei = bilaterations[i]['EP1_m']            
                    Ni = bilaterations[i]['NP1_m']            
                else:
                    Ei = bilaterations[i]['EP2_m']            
                    Ni = bilaterations[i]['NP2_m']            
                
                gamma = bilaterations[i]['gamma']
                if math.fabs(math.sin(gamma)) > 0.0001:
                    sigma = math.sqrt((sigma_d_m**2 + 2*sigma_c_m**2) / (math.sin(gamma))**2)
                else:
                    sigma = 999999.9
                
                dictEP = {}
                dictEP.update({'li':Ei})
                dictEP.update({'sigma_li':sigma})
                listEP.append(dictEP)

                dictNP = {}
                dictNP.update({'li':Ni})
                dictNP.update({'sigma_li':sigma})
                listNP.append(dictNP)
                
            resEP = moyennePonderee(listEP)
            resNP = moyennePonderee(listNP)
            multilaterations.append([resEP,resNP])
        
        best_multilateration = None
        best_s0 = 9999999.9
        for multilateration in multilaterations:
            s0_E = multilateration[0]['s0']
            s0_N = multilateration[1]['s0']
            s0 = math.sqrt(s0_E**2+s0_N**2)
            if s0 < best_s0:
                best_s0 = s0
                best_multilateration = multilateration
        
        resultats.update({'listVise':listVise})
        resultats.update({'noSta':noSta})
        resultats.update({'sigma_d_m':sigma_d_m})
        resultats.update({'sigma_c_m':sigma_c_m})
        resultats.update({'moyPond_EP':best_multilateration[0]})        
        resultats.update({'moyPond_NP':best_multilateration[1]})        
        
        EP = best_multilateration[0]['lm']
        NP = best_multilateration[1]['lm']
        
        ptSta = {}
        ptSta.update({noSta:{'E':EP,'N':NP} })
        
        resultats.update({'ptSta':ptSta})
                
        return resultats
    
def calculParamTransfHelmert(dictPtsGlobal,dictPtsLocal,noPtsFixes):
    """ calcul des parametres d une transformation de Helmert

    Parameters
    ----------
        dictPtsGlobal : dict
            dictionnaire des points dans le systeme global
        dictPtsLocal : dict
            dictionnaire des points dans le systeme local
        noPtsFixes : list
            liste de points fixes

    Returns
    -------
        resultats : dict
        
            'dictPtsGlobal' : dict
                dictionnaire des points dans le systeme global
            'dictPtsLocal' : dict
                dictionnaire des points dans le systeme local
            'noPtsFixes' : list
                liste de points fixes
            'alpha_moyen' : float
                angle de rotation moyen [gon]
            'lamda_moyen' : float
                facteur d echelle moyen [gon]
            'EG' : float
                coordonnee Est du centre de gravite des points sys. global [m]
            'NG' : float
                coordonnee Nord du centre de gravite des points sys. global [m]
            'yG' : float
                coordonnee y du centre de gravite des points sys. local [m]
            'xG' : float
                coordonnee x du centre de gravite des points sys. local [m]
            'dictPtsGlobalTransf' : dict
                dictionnaire des points transformes dans le sys. global
                

    """         
    
    resultats = {}
    
    #calcul des centres de gravite
    somme_E = 0.0
    somme_N = 0.0
    somme_y = 0.0
    somme_x = 0.0
    nbr_pts = 0.0
    for no in noPtsFixes:
        
        Ei = dictPtsGlobal[no]['E']
        Ni = dictPtsGlobal[no]['N']
        
        yi = dictPtsLocal[no]['E']        
        xi = dictPtsLocal[no]['N']     
        
        somme_E += Ei
        somme_N += Ni
        somme_y += yi
        somme_x += xi
         
        nbr_pts += 1.0
    
    EG = somme_E/nbr_pts    
    NG = somme_N/nbr_pts    
    yG = somme_y/nbr_pts    
    xG = somme_x/nbr_pts
    
    #calcul de lambda et alpha moyen
    somme_lamda = 0.0
    somme_alpha = 0.0
    for no in noPtsFixes:
        
        Ei = dictPtsGlobal[no]['E']
        Ni = dictPtsGlobal[no]['N']
        
        yi = dictPtsLocal[no]['E']        
        xi = dictPtsLocal[no]['N']     
        
        dGi_global = distanceAB(EG, NG, Ei, Ni)        
        dGi_local = distanceAB(yG, xG, yi, xi)        
        
        gisGi_global = gisementAB(EG, NG, Ei, Ni)
        gisGi_local = gisementAB(yG, xG, yi, xi)
        
        lamda_i = dGi_global/dGi_local
        alpha_i = gisGi_global - gisGi_local
        if alpha_i < 0.0:
            alpha_i += 400.0
        
        somme_lamda += lamda_i
        somme_alpha += alpha_i
    
    lamda_moyen = somme_lamda/nbr_pts
    alpha_moyen = somme_alpha/nbr_pts
    alpha_moyen_rad = alpha_moyen*math.pi/200.0    
    
    #transformation des points local => global
    dictPtsGlobalTransf = {}
    for no in noPtsFixes:
        
        yi = dictPtsLocal[no]['E']        
        xi = dictPtsLocal[no]['N']     
        
        Ei = EG + lamda_moyen*math.cos(alpha_moyen_rad)*(yi-yG) + lamda_moyen*math.sin(alpha_moyen_rad)*(xi-xG)
        Ni = NG - lamda_moyen*math.sin(alpha_moyen_rad)*(yi-yG) + lamda_moyen*math.cos(alpha_moyen_rad)*(xi-xG)

        dictPtsGlobalTransf.update({no:{'E':Ei,
                                        'N':Ni}})        
     
    resultats.update({'dictPtsGlobal':dictPtsGlobal})
    resultats.update({'dictPtsLocal':dictPtsLocal})    
    resultats.update({'noPtsFixes':noPtsFixes})        
    resultats.update({'alpha_moyen':alpha_moyen})
    resultats.update({'lamda_moyen':lamda_moyen})
    resultats.update({'EG':EG})
    resultats.update({'NG':NG})
    resultats.update({'yG':yG})
    resultats.update({'xG':xG})
    resultats.update({'dictPtsGlobalTransf':dictPtsGlobalTransf})

    return resultats


def printCalculParamTransfHelmert(path,helm):
    """ ecriture des resultats de la fonction calculParamTransfHelmert(...)

    Parameters
    ----------
        path : str
            fichier des resultats            
        helm : dict
            dictionnaire des resultats de la fonction calculParamTransfHelmert(...)
    
    Returns
    -------
        rien
                
    """ 
    
    if helm == {}:
        return
    
    fichier = open(path,'a', encoding='utf-8')       
    
    fichier.write('\n\n=====================================================\n')
    fichier.write('CALCUL DES PARAMETRES DE LA TRANSFORMATION DE HELMERT\n')
    fichier.write('=====================================================\n\n')

    fichier.write('FORMULES DE LA TRANSFORMATION\n')
    fichier.write('--------------------------------\n\n')

    fichier.write('E = EG + lambda*[  cos(alpha)*(y-yG) + sin(alpha)*(x-xG) ]\n')
    fichier.write('N = NG + lambda*[- sin(alpha)*(y-yG) + cos(alpha)*(x-xG) ]\n\n')
    
    fichier.write('y = yG + 1/lambda*[ cos(alpha)*(E-EG) - sin(alpha)*(N-NG) ]\n')
    fichier.write('x = xG + 1/lambda*[ sin(alpha)*(E-EG) + cos(alpha)*(N-NG) ]\n\n')
    
    fichier.write('PARAMETRES DE LA TRANSFORMATION\n')
    fichier.write('----------------------------------\n\n')
    
    fichier.write('{:<6s} : {:12.3f} [m]\n'.format('EG',helm['EG']))
    fichier.write('{:<6s} : {:12.3f} [m]\n'.format('NG',helm['NG']))
    fichier.write('{:<6s} : {:12.3f} [m]\n'.format('yG',helm['yG']))
    fichier.write('{:<6s} : {:12.3f} [m]\n\n'.format('xG',helm['xG']))
    fichier.write('{:<6s} : {:12.4f} [gon]\n'.format('alpha',helm['alpha_moyen']))
    fichier.write('{:<6s} : {:12.6f} [-]\n'.format('lambda',helm['lamda_moyen']))
    
    fichier.write('\nPOINTS D AJUSTAGE / COORD. GLOBAL & LOCAL\n')
    fichier.write('-----------------------------------------\n\n')
    
    fichier.write('{:5s} {:>12s} {:>12s} {:>12s} {:>12s}\n'.format('NO','E ','N ','y ','x '))
    fichier.write('{:5s} {:>12s} {:>12s} {:>12s} {:>12s}\n\n'.format('','[m]','[m]','[m]','[m]'))
    
    for no in helm['noPtsFixes']:
        E = helm['dictPtsGlobal'][no]['E']
        N = helm['dictPtsGlobal'][no]['N']
        y = helm['dictPtsLocal'][no]['E']
        x = helm['dictPtsLocal'][no]['N']
        fichier.write('{:5s} {:12.3f} {:12.3f} {:12.3f} {:12.3f}\n'.format(no,E,N,y,x))

    fichier.write('\nPOINTS D AJUSTAGE / COORD. GLOBAL & GLOBAL TRANSF.\n')
    fichier.write('--------------------------------------------------\n\n')

    fichier.write('{:5s} {:>12s} {:>12s} {:>8s}  {:>12s} {:>12s} {:>8s}\n'.format('NO','E ','Et ','vE ','N ','Nt ','vN '))
    fichier.write('{:5s} {:>12s} {:>12s} {:>8s}  {:>12s} {:>12s} {:>8s}\n\n'.format('','[m]','[m]','[m]','[m]','[m]','[m]'))
    
    for no in helm['noPtsFixes']:
        E = helm['dictPtsGlobal'][no]['E']
        N = helm['dictPtsGlobal'][no]['N']
        Et = helm['dictPtsGlobalTransf'][no]['E']
        Nt = helm['dictPtsGlobalTransf'][no]['N']
        vE = E-Et
        vN = N-Nt
        fichier.write('{:5s} {:12.3f} {:12.3f} {:8.3f}  {:12.3f} {:12.3f} {:8.3f}\n'.format(no,E,Et,vE,N,Nt,vN))
 
    fichier.close()

def transfLocal2Global(helm,dictPtsLocal):
    """ transformation coord Local => Global

    Parameters
    ----------
        'helm' : dict
            dictionnaire des resultats de la fonction calculParamTransfHelmert(...)
        dictPtsLocal : dict
            dictionnaire des points dans le systeme local

    Returns
    -------
        resultats : dict
        
            'helm' : dict
                dictionnaire des resultats de la fonction calculParamTransfHelmert(...)
            'dictPtsLocal' : dict
                dictionnaire des points dans le systeme local
            'dictPtsGlobal' : dict
                dictionnaire des points dans le systeme global
                

    """         
    
    resultats = {}

    EG = helm['EG']
    NG = helm['NG']
    yG = helm['yG']
    xG = helm['xG']
    lamda_moyen = helm['lamda_moyen']
    alpha_moyen = helm['alpha_moyen']
    
    #Calcul des points dans le systeme global
    dictPtsGlobal = {}
    
    for no in dictPtsLocal.keys():
        
        y = dictPtsLocal[no]['E']
        x = dictPtsLocal[no]['N']
    
        vec_x = np.array([[y],
                          [x]])
        
        vec_XG = np.array([[EG],
                           [NG]])
            
        vec_xG = np.array([[yG],
                           [xG]])
            
        alpha = alpha_moyen*np.pi/200.0
        mat_R =  np.array([[ np.cos(alpha) , np.sin(alpha) ],
                           [-np.sin(alpha) , np.cos(alpha) ]])
        
        vec_X = vec_XG + lamda_moyen*mat_R@(vec_x-vec_xG)
        
        pt = {no:{'E':vec_X[0,0],'N':vec_X[1,0]}}
        dictPtsGlobal.update(pt)    
    
    
    resultats.update({'helm':helm})
    resultats.update({'dictPtsGlobal':dictPtsGlobal})
    resultats.update({'dictPtsLocal':dictPtsLocal})     
    
    return resultats

def printTransfLocal2Global(path,transfL2G):
    """ ecriture des resultats de la fonction transfLocal2Global(...)

    Parameters
    ----------
        path : str
            fichier des resultats            
        helm : dict
            dictionnaire des resultats de la fonction transfLocal2Global(...)
    
    Returns
    -------
        rien
                
    """ 
    
    if transfL2G == {}:
        return
    
    fichier = open(path,'a', encoding='utf-8') 

    
    fichier.write('\n\n=====================================================\n')
    fichier.write('TRANSFORMATION DE SIMILITUDE LOCAL => GLOBAL\n')
    fichier.write('=====================================================\n\n')

    fichier.write('FORMULES DE LA TRANSFORMATION\n')
    fichier.write('--------------------------------\n\n')

    fichier.write('E = EG + lambda*[  cos(alpha)*(y-yG) + sin(alpha)*(x-xG) ]\n')
    fichier.write('N = NG + lambda*[- sin(alpha)*(y-yG) + cos(alpha)*(x-xG) ]\n\n')
    
    fichier.write('PARAMETRES DE LA TRANSFORMATION\n')
    fichier.write('----------------------------------\n\n')
    
    fichier.write('{:<6s} : {:12.3f} [m]\n'.format('EG',transfL2G['helm']['EG']))
    fichier.write('{:<6s} : {:12.3f} [m]\n'.format('NG',transfL2G['helm']['NG']))
    fichier.write('{:<6s} : {:12.3f} [m]\n'.format('yG',transfL2G['helm']['yG']))
    fichier.write('{:<6s} : {:12.3f} [m]\n\n'.format('xG',transfL2G['helm']['xG']))
    fichier.write('{:<6s} : {:12.4f} [gon]\n'.format('alpha',transfL2G['helm']['alpha_moyen']))
    fichier.write('{:<6s} : {:12.6f} [-]\n'.format('lambda',transfL2G['helm']['lamda_moyen']))
    
    fichier.write('\nPOINTS TRANSFORMES\n')
    fichier.write('-----------------------------------------\n\n')
    
    fichier.write('{:5s} {:>12s} {:>12s} {:>12s} {:>12s}\n'.format('NO','y ','x ','E ','N '))
    fichier.write('{:5s} {:>12s} {:>12s} {:>12s} {:>12s}\n\n'.format('','[m]','[m]','[m]','[m]'))
    
    for no in transfL2G['dictPtsLocal'].keys():
        y = transfL2G['dictPtsLocal'][no]['E']
        x = transfL2G['dictPtsLocal'][no]['N']
        E = transfL2G['dictPtsGlobal'][no]['E']
        N = transfL2G['dictPtsGlobal'][no]['N']
        fichier.write('{:5s} {:12.3f} {:12.3f} {:12.3f} {:12.3f}\n'.format(no,y,x,E,N))

    fichier.close()

def transfGlobal2Local(helm,dictPtsGlobal):
    """ transformation coord Global => Local

    Parameters
    ----------
        'helm' : dict
            dictionnaire des resultats de la fonction calculParamTransfHelmert(...)
        dictPtsGlobal : dict
            dictionnaire des points dans le systeme global

    Returns
    -------
        resultats : dict
        
            'helm' : dict
                dictionnaire des resultats de la fonction calculParamTransfHelmert(...)
            'dictPtsLocal' : dict
                dictionnaire des points dans le systeme local
            'dictPtsGlobal' : dict
                dictionnaire des points dans le systeme global
                

    """         
    
    resultats = {}

    EG = helm['EG']
    NG = helm['NG']
    yG = helm['yG']
    xG = helm['xG']
    lamda_moyen = helm['lamda_moyen']
    alpha_moyen = helm['alpha_moyen']
    
    #Calcul des points dans le systeme global
    dictPtsLocal = {}
    
    for no in dictPtsGlobal.keys():
        
        E = dictPtsGlobal[no]['E']
        N = dictPtsGlobal[no]['N']
    
        vec_X = np.array([[E],
                          [N]])
        
        vec_XG = np.array([[EG],
                           [NG]])
            
        vec_xG = np.array([[yG],
                           [xG]])
            
        alpha = alpha_moyen*np.pi/200.0
        mat_R =  np.array([[ np.cos(alpha) , np.sin(alpha) ],
                           [-np.sin(alpha) , np.cos(alpha) ]])
        
        vec_x = vec_xG + 1/lamda_moyen*mat_R.T@(vec_X-vec_XG)
        
        pt = {no:{'E':vec_x[0,0],'N':vec_x[1,0]}}
        dictPtsLocal.update(pt)    
    
    
    resultats.update({'helm':helm})
    resultats.update({'dictPtsGlobal':dictPtsGlobal})
    resultats.update({'dictPtsLocal':dictPtsLocal})     
    
    return resultats

def printTransfGlobal2Local(path,transfG2L):
    """ ecriture des resultats de la fonction transfLocal2Global(...)

    Parameters
    ----------
        path : str
            fichier des resultats            
        helm : dict
            dictionnaire des resultats de la fonction transfLocal2Global(...)
    
    Returns
    -------
        rien
                
    """ 
    
    if transfG2L == {}:
        return
    
    fichier = open(path,'a', encoding='utf-8') 

    
    fichier.write('\n\n=====================================================\n')
    fichier.write('TRANSFORMATION DE SIMILITUDE GLOBAL => LOCAL\n')
    fichier.write('=====================================================\n\n')

    fichier.write('FORMULES DE LA TRANSFORMATION\n')
    fichier.write('--------------------------------\n\n')

    fichier.write('y = yG + 1/lambda*[ cos(alpha)*(E-EG) - sin(alpha)*(N-NG) ]\n')
    fichier.write('x = xG + 1/lambda*[ sin(alpha)*(E-EG) + cos(alpha)*(N-NG) ]\n\n')
    
    fichier.write('PARAMETRES DE LA TRANSFORMATION\n')
    fichier.write('----------------------------------\n\n')
    
    fichier.write('{:<6s} : {:12.3f} [m]\n'.format('EG',transfG2L['helm']['EG']))
    fichier.write('{:<6s} : {:12.3f} [m]\n'.format('NG',transfG2L['helm']['NG']))
    fichier.write('{:<6s} : {:12.3f} [m]\n'.format('yG',transfG2L['helm']['yG']))
    fichier.write('{:<6s} : {:12.3f} [m]\n\n'.format('xG',transfG2L['helm']['xG']))
    fichier.write('{:<6s} : {:12.4f} [gon]\n'.format('alpha',transfG2L['helm']['alpha_moyen']))
    fichier.write('{:<6s} : {:12.6f} [-]\n'.format('lambda',transfG2L['helm']['lamda_moyen']))
    
    fichier.write('\nPOINTS TRANSFORMES\n')
    fichier.write('-----------------------------------------\n\n')
    
    fichier.write('{:5s} {:>12s} {:>12s} {:>12s} {:>12s}\n'.format('NO','E ','N ','y ','x '))
    fichier.write('{:5s} {:>12s} {:>12s} {:>12s} {:>12s}\n\n'.format('','[m]','[m]','[m]','[m]'))
    
    for no in transfG2L['dictPtsGlobal'].keys():
        y = transfG2L['dictPtsLocal'][no]['E']
        x = transfG2L['dictPtsLocal'][no]['N']
        E = transfG2L['dictPtsGlobal'][no]['E']
        N = transfG2L['dictPtsGlobal'][no]['N']
        print('{:5s} {:12.3f} {:12.3f} {:12.3f} {:12.3f}\n'.format(no,E,N,y,x))

    fichier.close()
    
    

def denivelleeTrigo(dHzReelle_AB_m,zen_AB_gon,I_m,S_m,k=0.13,R_Terre_m=6380000.0):
    """ denivellee trigonometrique 

    Parameters
    ----------
        'dHzReelle_AB_m' : float
            distance horizontale reelle [m]
        'zen_AB_gon' : float
            angle zenithal [gon]
        'I_m' : float
            hauteur d'instrument [m]
        'S_m' : float
            hauteur de signal [m]
        'k' : float
            coefficient de réfraction [-]
        'R_Terre' : float
            rayon de la Terre [m]

    Returns
    -------
        resultats : dict
        
        'dHzReelle_AB_m' : float
            distance horizontale reelle [m]
        'zen_AB_gon' : float
            angle zenithal [gon]
        'I_m' : float
            hauteur d'instrument [m]
        'S_m' : float
            hauteur de signal [m]
        'k' : float
            coefficient de réfraction [-]
        'R_Terre' : float
            rayon de la Terre [m]
        'h_AB_m' : float
            denivelle nette [m]

    """         
    
    zAB = zen_AB_gon*math.pi/200.0
    E_m = dHzReelle_AB_m**2/(2*R_Terre_m)
    R_m = k*dHzReelle_AB_m**2/(2*R_Terre_m)
    h_AB_m = dHzReelle_AB_m*1.0/math.tan(zAB) + E_m - R_m + I_m - S_m
    
    resultats = {}
    resultats.update({'dHzReelle_AB_m':dHzReelle_AB_m})
    resultats.update({'zen_AB_gon':zen_AB_gon})
    resultats.update({'I_m':I_m})
    resultats.update({'S_m':S_m})
    resultats.update({'E_m':E_m})
    resultats.update({'R_m':R_m})
    resultats.update({'R_Terre_m':R_Terre_m})
    resultats.update({'k':k})
    resultats.update({'h_AB_m':h_AB_m})
    return resultats

    
def importTopologiePolygonale(fichier):

    resultats = {}
    
    topologie = []
    
    fichier = open(fichier,'r')
    line = fichier.readline().strip()
    while line:
        data = line.split('\t')
        no = data[0]

        if no == 'ORI_STA':
            topologie.append([no,float(data[1])])
        else:          
            topologie.append([no])
        
        line = fichier.readline().strip()
    
    fichier.close()

    resultats.update({'topologie':topologie})    
    
    return resultats


def polygonale(dictPts,dictObs,resTopologie,N0_m,N_ref_m,H_ref_m):
    
    dictObs = copy.deepcopy(dictObs)
    
    #topologie de la polygonale
    topologie = resTopologie['topologie']

    #Calcul des angles aux sommets
    nbr_sommets = len(topologie)-2
    sommets = {}
    for i in range(0,nbr_sommets):
                
        no_sommet = topologie[i+1][0]
        no_visee_arriere = topologie[i][0]
        no_visee_avant = topologie[i+2][0]
        
        #si le sommet arriere (1er) est issu d une inconnue d orientation
        if no_visee_arriere == 'ORI_STA':
            dictObs.update({(no_sommet,no_visee_arriere):{'rhz':0.0,'I':np.nan,'S':np.nan,'zen':np.nan}})

        #si le sommet avant (dernier) est issu d une inconnue d orientation
        if no_visee_avant == 'ORI_STA':
            dictObs.update({(no_sommet,no_visee_avant):{'rhz':0.0,'I':np.nan,'S':np.nan,'zen':np.nan}})
            
        obs_arriere = dictObs[(no_sommet,no_visee_arriere)]
        obs_avant = dictObs[(no_sommet,no_visee_avant)]
        ri_arriere = obs_arriere['rhz']
        ri_avant = obs_avant['rhz']
        
        #calcul de l'angle au sommet
        alpha_i_prime = np.mod(ri_avant-ri_arriere,400)
    
        #update le dict des sommets avec le sommet courant
        sommets.update({no_sommet:{'alpha_prime':alpha_i_prime}})        

    #Calcul des gisements de départ et d'arrivee
    noM = topologie[0][0]
    noA = topologie[1][0]
    noB = topologie[-2][0]
    noN = topologie[-1][0]
    
    if topologie[0][0] == 'ORI_STA':
        phi_MA = topologie[0][1]+200.0
    else:
        phi_MA = gisement(dictPts,noM,noA)

    if topologie[-1][0] == 'ORI_STA':
        phi_BN = topologie[-1][1]
    else:
        phi_BN = gisement(dictPts,noB,noN)
    
    #Calcul des gisements des côtés
    cotes = {}
    
    #premier cote
    cotes.update({(noM,noA):{'phi_prime':phi_MA}})

    #cotes de la polygonale
    for i in range(0,nbr_sommets):
        no_sommet = topologie[i+1][0]
        no_visee_arriere = topologie[i][0]
        no_visee_avant = topologie[i+2][0]
        phi = np.mod(cotes[(no_visee_arriere,no_sommet)]['phi_prime'] + 200.0 + sommets[no_sommet]['alpha_prime'],400.0)
        cotes.update({(no_sommet,no_visee_avant):{'phi_prime':phi}})
            
    #Calcul du f_alpha
    f_alpha = phi_BN - cotes[(noB,noN)]['phi_prime']

    #Calcul des angles compensés
    for i in range(0,nbr_sommets):
        no_sommet = topologie[i+1][0]
        alpha_i = sommets[no_sommet]['alpha_prime'] + f_alpha/len(sommets)
        sommets[no_sommet].update({'alpha':alpha_i})

    #Calcul des gisements compensés   

    #premier cote
    cotes[(noM,noA)].update({'phi':phi_MA})     

    #cotes de la polygonale
    for i in range(0,nbr_sommets):
        no_sommet = topologie[i+1][0]
        no_visee_arriere = topologie[i][0]
        no_visee_avant = topologie[i+2][0]
        phi = np.mod(cotes[(no_visee_arriere,no_sommet)]['phi'] + 200.0 + sommets[no_sommet]['alpha'],400.0)
        cotes[(no_sommet,no_visee_avant)].update({'phi':phi})
        
    #Calcul des coordonnées
    for i in range(0,nbr_sommets-1):
        no_sommet = topologie[i+1][0]
        no_visee_avant = topologie[i+2][0]

        #Réduction des distances
        dHzReelle1_m = dInclReelle2dHzReelle(dictObs[(no_sommet,no_visee_avant)]['dincl'],dictObs[(no_sommet,no_visee_avant)]['zen'])
        res_dHzReelle2dPlanProj = dHzReelle2dPlanProj(dHzReelle1_m,N_ref_m,N0_m,H_ref_m)
        d_proj1 = res_dHzReelle2dPlanProj['dPlanProj_m']

        dHzReelle2_m = dInclReelle2dHzReelle(dictObs[(no_visee_avant,no_sommet)]['dincl'],dictObs[(no_visee_avant,no_sommet)]['zen'])
        res_dHzReelle2dPlanProj = dHzReelle2dPlanProj(dHzReelle2_m,N_ref_m,N0_m,H_ref_m)
        d_proj2 = res_dHzReelle2dPlanProj['dPlanProj_m']

        #Dénivelées
        I_m = dictObs[(no_sommet,no_visee_avant)]['I']
        S_m = dictObs[(no_sommet,no_visee_avant)]['S']
        dincl1 = dictObs[(no_sommet,no_visee_avant)]['dincl']
        zen1 =   dictObs[(no_sommet,no_visee_avant)]['zen']
        deniv1 = denivelleeTrigo(dHzReelle1_m,zen1,I_m,S_m,k=0.13,R_Terre_m=6380000.0)        
        DH1 = deniv1['h_AB_m']

        I_m = dictObs[(no_visee_avant,no_sommet)]['I']
        S_m = dictObs[(no_visee_avant,no_sommet)]['S']
        dincl2 = dictObs[(no_visee_avant,no_sommet)]['dincl']
        zen2 =   dictObs[(no_visee_avant,no_sommet)]['zen']
        deniv2 = denivelleeTrigo(dHzReelle2_m,zen2,I_m,S_m,k=0.13,R_Terre_m=6380000.0)        
        DH2 = deniv2['h_AB_m']
        
        DH = (DH1-DH2)/2

        d_proj = (d_proj1+d_proj2)/2        

        phi = cotes[(no_sommet,no_visee_avant)]['phi']
        
        DE = d_proj*np.sin(phi*np.pi/200.0)
        DN = d_proj*np.cos(phi*np.pi/200.0)
        
        cotes[(no_sommet,no_visee_avant)].update({'d_proj1':d_proj1})
        cotes[(no_sommet,no_visee_avant)].update({'d_proj2':d_proj2})
        cotes[(no_sommet,no_visee_avant)].update({'d_proj':d_proj})
        cotes[(no_sommet,no_visee_avant)].update({'DE_prime':DE})
        cotes[(no_sommet,no_visee_avant)].update({'DN_prime':DN})    
        cotes[(no_sommet,no_visee_avant)].update({'DH1_prime':DH1})    
        cotes[(no_sommet,no_visee_avant)].update({'DH2_prime':DH2})    
        cotes[(no_sommet,no_visee_avant)].update({'DH_prime':DH})
    
    #Calcul des écarts en coordonnées
    DE_AB = 0.0
    DN_AB = 0.0
    DH_AB = 0.0
    d_tot = 0.0
    d2_tot = 0.0

    for i in range(0,nbr_sommets-1):
        no_sommet = topologie[i+1][0]
        no_visee_avant = topologie[i+2][0]
        DE = cotes[(no_sommet,no_visee_avant)]['DE_prime']
        DN = cotes[(no_sommet,no_visee_avant)]['DN_prime']
        DH = cotes[(no_sommet,no_visee_avant)]['DH_prime']
        DE_AB += DE
        DN_AB += DN
        DH_AB += DH
        d_tot += cotes[(no_sommet,no_visee_avant)]['d_proj']
        d2_tot += cotes[(no_sommet,no_visee_avant)]['d_proj']**2
        
    DE_AB_doit = dictPts[noB]['E']-dictPts[noA]['E']
    DN_AB_doit = dictPts[noB]['N']-dictPts[noA]['N']
    fE = DE_AB_doit-DE_AB
    fN = DN_AB_doit-DN_AB
    fS = np.sqrt(fE**2+fN**2)

    DH_AB_doit = dictPts[noB]['H']-dictPts[noA]['H']
    fH = DH_AB_doit-DH_AB

    resultats = {}    
    resultats.update({'points':{}})

    #Calcul des différences et coordonnées compensées
    somme_DE = 0.0
    somme_DN = 0.0
    somme_DH = 0.0
    for i in range(0,nbr_sommets-1):
        no_sommet = topologie[i+1][0]
        no_visee_avant = topologie[i+2][0]
        d = cotes[(no_sommet,no_visee_avant)]['d_proj']
        DE = cotes[(no_sommet,no_visee_avant)]['DE_prime'] + fE*d/d_tot
        DN = cotes[(no_sommet,no_visee_avant)]['DN_prime'] + fN*d/d_tot
        DH = cotes[(no_sommet,no_visee_avant)]['DH_prime'] + fH*d**2/d2_tot
        cotes[(no_sommet,no_visee_avant)].update({'DE':DE})
        cotes[(no_sommet,no_visee_avant)].update({'DN':DN})
        cotes[(no_sommet,no_visee_avant)].update({'DH':DH})

        somme_DE += DE
        somme_DN += DN
        somme_DH += DH
        
        E_visee_avant = dictPts[noA]['E'] + somme_DE
        N_visee_avant = dictPts[noA]['N'] + somme_DN
        H_visee_avant = dictPts[noA]['H'] + somme_DH
        
        pt = {no_visee_avant:{'E':E_visee_avant,
                              'N':N_visee_avant,
                              'H':H_visee_avant}}
        resultats['points'].update(pt)
    
    resultats.update({'dictObs':dictObs})
    resultats.update({'dictPts':dictPts})
    resultats.update({'topologie':topologie})
    resultats.update({'cotes':cotes})
    resultats.update({'sommets':sommets})
    resultats.update({'falpha':f_alpha})
    resultats.update({'fE':fE})
    resultats.update({'fN':fN})
    resultats.update({'fS':fS})
    resultats.update({'fH':fH})
        
    return resultats
 
    

def printPolygonale(path,polygo):
    """ ecriture des resultats de la fonction polygonale(...)

    Parameters
    ----------
        path : str
            fichier des resultats            
        helm : dict
            dictionnaire des resultats de la fonction polygonale(...)
    
    Returns
    -------
        rien
                
    """         

    if polygo == {}:
        return
    
    fichier = open(path,'a', encoding='utf-8') 


    fichier.write('\n\n=====================================================\n')
    fichier.write('POLYGONALE RATACHEE\n')
    fichier.write('=====================================================\n\n')
    
    
    fichier.write('\nRESULTATS\n')
    fichier.write('=========\n\n')
    fichier.write('f alpha = {:+8.4f} [gon]\n'.format(polygo['falpha']))
    fichier.write('f E     = {:+8.4f} [m]\n'.format(polygo['fE']))
    fichier.write('f N     = {:+8.4f} [m]\n'.format(polygo['fN']))
    fichier.write('f S     = {:+8.4f} [m]\n'.format(polygo['fS']))
    fichier.write('f H     = {:+8.4f} [m]\n'.format(polygo['fH']))
    
    fichier.write('\nOBSERVATIONS\n')
    fichier.write('============\n\n')
    fichier.write('{:8s} {:8s} {:>7s} {:>7s} {:>10s} {:>10s} {:>10s}\n'.format('STATION','VISE','I','S','RI','ZEN','DI'))
    fichier.write('{:8s} {:8s} {:>7s} {:>7s} {:>10s} {:>10s} {:>10s}\n\n'.format('','','[m]','[m]','[gon]','[gon]','[m]'))

    topologie = polygo['topologie']
    nbr_sommets = len(topologie)-2
    for i in range(0,nbr_sommets):
        no_sta = topologie[i+1][0]
        no_arriere = topologie[i][0]        
        no_avant = topologie[i+2][0]
        
        obs = polygo['dictObs'][(no_sta,no_arriere)]
        if 'dincl' in obs:
            dincl = obs['dincl']
        else:
            dincl = np.nan
            
        fichier.write('{:8s} {:8s} {:7.4f} {:7.4f} {:10.4f} {:10.4f} {:10.4f}\n'.format(no_sta,no_arriere,obs['I'],obs['S'],obs['rhz'],obs['zen'],dincl))

        obs = polygo['dictObs'][(no_sta,no_avant)]        
        if 'dincl' in obs:
            dincl = obs['dincl']
        else:
            dincl = np.nan

        fichier.write('{:8s} {:8s} {:7.4f} {:7.4f} {:10.4f} {:10.4f} {:10.4f}\n\n'.format(no_sta,no_avant,obs['I'],obs['S'],obs['rhz'],obs['zen'],dincl))
    
    fichier.write('\nSOMMETS\n')
    fichier.write('========\n\n')
    fichier.write('{:8s} {:>10s} {:>10s}\n'.format('SOMMET','alpha\'','alpha'))
    fichier.write('{:8s} {:>10s} {:>10s}\n\n'.format('','[gon]','[gon]'))
    
    for i in range(0,nbr_sommets):
        no_sta = topologie[i+1][0]
        no_arriere = topologie[i][0]        
        no_avant = topologie[i+2][0]
        
        sommet = polygo['sommets'][no_sta]        
        fichier.write('{:8s} {:10.4f} {:10.4f}\n'.format(no_sta,sommet['alpha_prime'],sommet['alpha']))


    fichier.write('\nCOTES\n')
    fichier.write('=======\n\n')
    fichier.write('{:8s} {:8s} {:>10s} {:>10s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s}\n'.format('PT 1','PT 2','Phi\'','Phi','DP 1-2','DP 2-1','DP moyen','DE\'','DN\'','DE','DN','DH1\'','DH2\'','DH\'','DH','DH1+2'))
    fichier.write('{:8s} {:8s} {:>10s} {:>10s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s}\n\n'.format('','','[gon]','[gon]','[m]','[m]','[m]','[m]','[m]','[m]','[m]','[m]','[m]','[m]','[m]','[m]'))
    
    for i in range(0,nbr_sommets+1):
        pt1 = topologie[i][0]
        pt2 = topologie[i+1][0]
        
        cote = polygo['cotes'][(pt1,pt2)]        
        if len(cote)<3:
            fichier.write('{:8s} {:8s} {:10.4f} {:10.4f}\n'.format(pt1,pt2,cote['phi_prime'],cote['phi']))
        else:
            fichier.write('{:8s} {:8s} {:10.4f} {:10.4f} {:9.4f} {:9.4f} {:9.4f} {:9.4f} {:9.4f} {:9.4f} {:9.4f} {:9.4f} {:9.4f} {:9.4f} {:9.4f} {:+9.4f}\n'.format(pt1,pt2,cote['phi_prime'],
                          cote['phi'],cote['d_proj1'],cote['d_proj2'],cote['d_proj'],cote['DE_prime'],cote['DN_prime'],cote['DE'],cote['DN'],cote['DH1_prime'],cote['DH2_prime'],cote['DH_prime'],cote['DH'],cote['DH1_prime']+cote['DH2_prime']))

    fichier.write('\nNOUVEAUX POINTS\n')
    fichier.write('===============\n\n')
    fichier.write('{:8s} {:>12s} {:>12s} {:>12s}\n'.format('NO','E','N','H'))
    fichier.write('{:8s} {:>12s} {:>12s} {:>12s}\n\n'.format('','[m]','[m]','[m]'))
    
    for i in range(1,nbr_sommets-1):
        no_sta = topologie[i+1][0]
        pt = polygo['points'][no_sta]
        fichier.write('{:8s} {:12.4f} {:12.4f} {:12.4f}\n'.format(no_sta,pt['E'],pt['N'],pt['H']))
    


#=============================================================
#Fonctions pour enseignement    
#=============================================================

 
def creerPointsBruites(dictPts,sigma_E_m,sigma_N_m,sigma_H_m):
    
    dictPtsBruites = copy.deepcopy(dictPts)
    for key,data in dictPtsBruites.items():
        
        data['E'] += np.random.normal()*sigma_E_m
        data['N'] += np.random.normal()*sigma_N_m
        
        if 'H' in data.keys():
            data['H'] += np.random.normal()*sigma_H_m
        
    
    return dictPtsBruites
    
    
    
def simulationMesures(dictPts,dictObs,
                      wSta_gon,N0_m,k,
                      sigma_rhz_cc,sigma_zen_cc,sigma_d_mm,sigma_d_ppm,sigma_cent_mm):
            
    dictObsSimul = copy.deepcopy(dictObs)
    
    for key,data in dictObsSimul.items():
        
        noSta = key[0]
        noVise = key[1]
        I = data['I']
        S = data['S']
        
        if noSta in wSta_gon.keys():           
            wSta = wSta_gon[noSta]
        else:
            wSta = 0.0
            print('l inconnue d orientation de la station : {:s} n est pas definie => w_{:s}=0.0000 [gon]!'.format(noSta,noSta))
        
        #elements d implantation 2D
        elem = elementsImplantation(dictPts, noSta, wSta, noVise, N0_m)
        rhz = elem['elemImpl']['rhzAP_gon']
        dhz = elem['elemImpl']['dHzAPReelle_m']

        if 'H' in dictPts[noSta] and 'H' in dictPts[noVise]:
            DH = dictPts[noVise]['H'] - dictPts[noSta]['H']
        else:
            DH = 0.0
            print('Les altitudes des pts : {:s} et {:s} pas definie => DH=0.000 [m]!'.format(noSta,noVise))
            
        #angle zenithal
        R = 6380000.0
        E = dhz**2/(2*R)
        R = k*dhz**2/(2*R)
        I += np.random.normal(0.0,sigma_cent_mm*1e-3)
        
        arg = ( DH - ( E - R + I - S ) ) / dhz
        zen = 100.0 - math.atan( arg )*200.0/math.pi
        
        #distance incline
        dincl = dHzReelle2dInclReelle(dhz, zen)
        
        #bruit de mesure
        # dincl += np.random.normal(0.0,sigma_d_mm*1e-3) + np.random.normal(0.0,sigma_cent_mm*1e-3/dhz*200.0/math.pi)
        dincl += np.random.normal(0.0,sigma_d_mm*1e-3) + np.random.normal(0.0,sigma_d_ppm*1e-6*dincl) + np.random.normal(0.0,sigma_cent_mm*1e-3/dhz*200.0/math.pi)
        rhz += np.random.normal(0.0,sigma_rhz_cc*1e-4) + np.random.normal(0.0,sigma_cent_mm*1e-3/dhz*200.0/math.pi)
        zen += np.random.normal(0.0,sigma_zen_cc*1e-4)
        
        data.update({'rhz':rhz})
        data.update({'zen':zen})
        data.update({'dincl':dincl})
    
    return dictObsSimul    
    
def exportObservations(path,dictObs):
    
    fichier = open(path,'w')
    for key,data in dictObs.items():
        noSta = key[0]
        noVise = key[1]
        I = data['I']
        S = data['S']
        rhz = data['rhz']
        zen = data['zen']
        dincl = data['dincl']
        fichier.write('{:s}\t{:s}\t{:0.3f}\t{:0.3f}\t{:8.4f}\t{:8.4f}\t{:8.3f}\n'.format(noSta,noVise,I,S,rhz,zen,dincl))
        
    fichier.close()
        
        
    
    
    
    
    
    
    
    
    
    
    