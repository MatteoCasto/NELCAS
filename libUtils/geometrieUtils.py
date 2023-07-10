# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 10:59:16 2022

@author: matteo.casto
"""

import numpy as np
import math
from skspatial.objects import Line, Point
from skspatial.plotting import plot_2d


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


def chOrtho2systemeLocal(chOrtho):
    
    """
    Fonction permettant de générer un système local yx à partir d'un cheminement orthogonal avec cotes signées successives

    Parameters
    ----------
    chOrtho : liste
        Liste de cotes successives de la forme [cote1, cote2, ...]

    Returns
    -------
    systemeLocal : numpy array
        Matrice de type np.array([[y,x],[y,x],...]) 

    """
    
    # Initialisation
    systemeLocal = np.zeros(shape=(len(chOrtho),2))
    gisements = np.zeros(shape=(len(chOrtho),1))
    gisPrec = 0.0
    
    # Parcourir les cotes successives signées et générer un système local yx
    for i in range(0,len(chOrtho)):  
        
        cote = chOrtho[i]
        
        if i == 1:
            systemeLocal[i] = np.array([0,cote])
            
        if i != 0 and i != 1:
            
            yPrec = systemeLocal[i-1,0]
            xPrec = systemeLocal[i-1,1]
            gisPrec = gisements[i-1,0]
            if cote < 0: 
                gisNouv = gisPrec - 100.0
                yNouv = np.sin(gisNouv*np.pi/200.0)*abs(cote) + yPrec
                xNouv = np.cos(gisNouv*np.pi/200.0)*abs(cote) + xPrec
                systemeLocal[i,0] = yNouv
                systemeLocal[i,1] = xNouv
                gisements[i,0] = gisNouv
                
            if cote > 0:
                gisNouv = gisPrec + 100.0
                yNouv = np.sin(gisNouv*np.pi/200.0)*abs(cote) + yPrec
                xNouv = np.cos(gisNouv*np.pi/200.0)*abs(cote) + xPrec
                systemeLocal[i,0] = yNouv
                systemeLocal[i,1] = xNouv
                gisements[i,0] = gisNouv
            
    return systemeLocal     




def nivellementTrigoDH(ZD,DS,k,R, I, S) : 

    """
    Calcul une dénivelée DH avec ZD et DS (niv. trigo.) en tenant compte de la sphéricité de la terre et du coefficient de réfraction k.
    
    Parameters
    ----------
    ZD : float
        angle zénithal [g]
        
    DS : float
        distance inclinée brute [m]
    
    k : float
        coefficient de réfraction [-]
        
    R : float
        rayon terrestre apprpoximé [m]
        
    Returns
    -------
    DH : float
        Dénivelée [m]
    
    """
    
    DH = np.cos(ZD*np.pi/200.0)*DS + ((1-k)*DS**2)/(2*R)*np.sin(ZD*np.pi/200.0)**2  +   I - S
    
    return DH





def incOriFromCoord(Esta ,Nsta, Ep, Np, RI):
    
    """
    Simple fonction pour calculer une inconnue d'orientation à partir d'une visée avec coordonnées connues.
    Utilisée dans le contrôle de cohérence géométrique sur les directions RI
    
    Parameters
    ----------
    Esta,Nsta,Ep,Np,RI : float
        Elements de calcul.
    
    Returns
    -------
    incOri : float
        Iconnue d'orientation pour UNE seule visée.
    """
    
    return np.mod( np.arctan2(Ep-Esta,Np-Nsta)*200.0/np.pi - RI, 400) 



def gisement(Ea,Na,Eb,Nb):
    
    """
    Simple fonction pour calculer un gisement entre 2 points.
    
    Parameters
    ----------
    Ea,Na,Ep,Np : float
        Elements de calcul.
    
    Returns
    -------
    gisement : float
        En [g].
    """

    dE = Eb - Ea
    dN = Nb - Na
    gisement = math.atan2(dE,dN)*200/math.pi
    if gisement < 0.0:
        gisement += 400.0
        
    return gisement




def pointAligne(inconnues):
    
    """
    Fonction permettant de calculer une contrainte (c(x)=0) de pointz aligné avec la possibilité d'inclure un
    déplacement dm1 (> 0 pour droite de AB, < 0 pour gauche de AB).
    
    Parameters
    ----------
    inconnues : dictionnaire
        Dictionnaire contenant tous les paramètres nécéssaires au calcul de la contrainte
    
    Returns
    -------
    c(x) : float
        Se rapproche de 0.
    """
    
    Ea,Na = inconnues['Ea'], inconnues['Na']
    Eb,Nb = inconnues['Eb'], inconnues['Nb']
    Ep,Np = inconnues['Ep'], inconnues['Np']
    dm1 = inconnues['dm1']
    
    # Calcul des points' projetés sur la parrallèle (même gisement AA2 = BB2)
    gisAB = gisement(Ea, Na, Eb, Nb)
    if dm1 < 0.0:
        gisAA2 = np.mod(gisAB - 100.0, 400.0)
    elif dm1 >= 0.0:
        gisAA2 = np.mod(gisAB + 100.0, 400.0)
    
    # Méthode des points lancés
    Ea2, Na2  = np.sin(gisAA2*np.pi/200.0)*abs(dm1) + Ea, np.cos(gisAA2*np.pi/200.0)*abs(dm1) + Na
    Eb2, Nb2  = np.sin(gisAA2*np.pi/200.0)*abs(dm1) + Eb, np.cos(gisAA2*np.pi/200.0)*abs(dm1) + Nb
    
    # Vecteurs
    AP = [ Ep-Ea2,Np-Na2 ]
    AB = [ Eb2-Ea2,Nb2-Na2 ]
    
    # Contrainte pour theta = 0.0g ou -200.0g
    fractSup = np.dot(AB, AP)
    fractInf = np.linalg.norm(AB) * np.linalg.norm(AP)
    
    if fractInf == 0.0 :
        return 0
    
    pScalaire = abs(fractSup/fractInf) # la valeur abs. doit être égale à 0 (-1, si vect. opposés)

    return  pScalaire - 1   # c(x) = 0 
    
    





def droitePerpendiculaire(inconnues):
    
    """
    Fonction permettant de calculer une contrainte (c(x)=0) de perpendicularité.
    
    Parameters
    ----------
    inconnues : dictionnaire
        Dictionnaire contenant tous les paramètres nécéssaires au calcul de la contrainte.
    
    Returns
    -------
    c(x) : float
        Se rapproche de 0.
    """
    
    Ea,Na = inconnues['Ea'], inconnues['Na']
    Eb,Nb = inconnues['Eb'], inconnues['Nb']
    Ep,Np = inconnues['Ep'], inconnues['Np']
    
    PA = [ Ea-Ep,Na-Np ]
    PB = [ Eb-Ep,Nb-Np ]
    
    pScalaire =  PA[0]*PB[0] + PA[1]*PB[1]

    return  pScalaire    # c(x) = 0 (produit scal. = 0)





def line(p1, p2):
    """
    Simple fonction used to structure a line with 2 points.
    Next, this output is used with lineIntersection as an input.
    """
    
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def lineIntersection(L1, L2):
    """
    Fucntion that is used in the approximate coordinates algorithm for contraints.

    Parameters
    ----------
    line1 : np.array
        Arrays that contains data defining a line.
    line2 : np.array
        Arrays that contains data defining a line.

    Returns
    -------
    x,y : float
        coordinates of the intersection.

    """
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False
        print('Intersection not found')
        
        
def projectPointOnLine(pointA, pointB, pointC):
    """
    Function that process a projection of a point on a line.

    Parameters
    ----------
    pointA : list
        First point of the line. [Ei,Ni]
    pointB : list
        Second point of the line. [Ei,Ni]
    pointC : list
        Point to project -> P. [Ei,Ni]

    Returns
    -------
    point_projected : list
        Coordinates of the point P. [Ei,Ni]

    """
    
    line = Line.from_points(point_a=pointA, point_b=pointB)
    point = Point(pointC)
  
    return line.project_point(point) 
    










