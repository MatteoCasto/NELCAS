import numpy as np


def importMesuresPolaires(nom_fichier):
    dict_mesures = {}
    
    fichier = open(nom_fichier,'r')
    line = fichier.readline().strip()
    while line:
        if line[0] != "#" :
            data = line.split('\t')
            sta = data[0]
            vis = data[1]
            angle_horiz = float(data[4])
            dist_plat = float(data[6])
            angle_vert = float(data[5])
            i = float(data[2])
            s = float(data[3])
            dict_mesures.update({(sta,vis):[angle_horiz,dist_plat,angle_vert,i,s]})
        line = fichier.readline().strip()
    
    return(dict_mesures)

def importMesuresGNSS(nom_fichier):
    dict_mesures = {}
    
    fichier = open(nom_fichier,'r')
    line = fichier.readline().strip()
    while line:
        if line[0] != "#" :
            data = line.split('\t')
            No = data[0]
            E = float(data[1])
            N = float(data[2])
            H = float(data[3])
            dict_mesures.update({No:[E,N,H]})
        line = fichier.readline().strip()
    
    return(dict_mesures)

dict_mesures_polaires = importMesuresPolaires('Mesures_generees_alea.txt')
# dict_mesures_GNSS_1 = importMesuresGNSS('Session_1.txt')
# dict_mesures_GNSS_2 = importMesuresGNSS('Session_2.txt')
# dict_mesures_GNSS_3 = importMesuresGNSS('Session_3.txt')

def exportMesPolaires(dict_mesures, nom_fichier):
    
    r = open(nom_fichier, "w")
    r.write('$$ME Mesures fictives\n')
    
    for key,data in dict_mesures.items():
        sta = key[0]
        vis = key[1]
        angle_horiz = data[0]
        dist_plat = data[1]
        angle_v = data[2]
        i = data[3]
        s = data[4]
        
        r.write("ST{:<16}{:>33.3f}\n".format(sta,i))
        r.write("RI{:<16}{:>18.4f}{:>21.3f}\n".format(vis,angle_horiz,s))
        # if s > 0:
        r.write("DS{:<16}{:>18.4f}{:>21.3f}\n".format(vis,dist_plat,s))
        r.write("ZD{:<16}{:>18.4f}{:>21.3f}\n".format(vis,angle_v,s))
    
    r.close()
    return()

def exportMesGNSS(dict_mesures, nom_fichier, no_session):
    
    r = open(nom_fichier, "w")
    r.write('SLSession {}                               RIEN\n'.format(no_session))
    
    for key,data in dict_mesures.items():
        no = key
        E = data[0]
        N= data[1]
        H= data[2]
        
        r.write("LY{:<4}{:>30.4f}\n".format(no,E))
        r.write("LX{:<4}{:>30.4f}\n".format(no,N))
        r.write("LH{:<4}{:>30.4f}\n".format(no,H))
    
    r.close()
    return()

exportMesPolaires(dict_mesures_polaires, 'mes_polaires.MES')
# exportMesGNSS(dict_mesures_GNSS_1, 'mes_GNSS_1.MES', 1)
# exportMesGNSS(dict_mesures_GNSS_2, 'mes_GNSS_2.MES', 2)
# exportMesGNSS(dict_mesures_GNSS_3, 'mes_GNSS_3.MES', 3)
















