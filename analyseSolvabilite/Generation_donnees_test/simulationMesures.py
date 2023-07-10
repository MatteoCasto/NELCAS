import sys
import os

# sys.path.append('C:\\HEIG-VD\\TB\\02_dev\\01_import\\reseauFictif\\')
import libTopo as topo

currentDir = os.getcwd()
print(currentDir)


dictPts = topo.importPoints(currentDir+"\\intentionCoo.txt")
dictObs = topo.importObservations(currentDir+"\\intentionMesuresPolaires.txt")

wSta_gon = {'11':20.0,
            '14':40.0,
            '19':60.0,
            '21':80.0}

N0_m = 1200000 # Centre de la projection Suisse
k = 0.13
sigma_rhz_cc = 20.0
sigma_zen_cc = 20.0
sigma_d_mm = 5.0
sigma_d_ppm = 5.0
sigma_cent_mm = 5.0

dictObsSimul = topo.simulationMesures(dictPts,dictObs,wSta_gon,N0_m,k,
                                      sigma_rhz_cc,sigma_zen_cc,sigma_d_mm,sigma_d_ppm,sigma_cent_mm)

topo.exportObservations("Mesures_generees_alea.txt", dictObsSimul)

# topo.plotPoints(dictPts)
# topo.plotObservations(dictPts, dictObsSimul)



'''
# Conversion des pts au format XML
export = {'points':{'point':[]}}
for key,data in dictPts.items():
    sousDict = {'pointName':key,
                'E':data['E'],
                'N':data['N'],
                'H':data['H']}
    export['points']['point'].append(sousDict)
conversionUtils.dictionnaire2xml(export, currentDir+"points_standardised.xml")
'''