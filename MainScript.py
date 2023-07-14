# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:13:26 2022

@author: Matteo Casto, INSIT
"""

import libUtils.conversionUtils as conversionUtils
import libUtils.processUtils as processUtils
import libUtils.controlesCoherenceUtils as controlesCoherenceUtils
import os




# ---   Réprétoir de base où se trouve les fichiers inpput et output (facillite la lecture)
dirPath = os.getcwd()


# ---   FUSION DES STATIONS POLAIRES 
# conversionUtils.fusionFichiers('C:\\01_ContraintesMsMo\\02_dev\\01_code\\output\\allBelmont\\', 'C:\\01_ContraintesMsMo\\02_dev\\01_code\\output\\fusion\\fusionRes.xml')


# ---   CONVERSION POINTS
# conversionUtils.points2xml(dirPath+'\\01_input\\plan17\\C351P17.ll1', dirPath+'\\01_input\\plan17\\Points.xml')
# dictPoints = conversionUtils.xml2dictionnaire(dirPath+'\\01_input\\plan17\\Points.xml')


# ---   CONVERSION MESURES HOMERE
# conversionUtils.canevas2xml(dirPath+'\\01_input\\plan17\\C351P17.ll1', dirPath+'\\01_input\\plan17\\Observations.xml', dictPoints)
# dictCanevas = conversionUtils.xml2dictionnaire(dirPath+'\\01_input\\plan17\\Observations.xml')

# ---   CONVERSION MESURES LTOP
# debug = conversionUtils.LTOP2xml(dirPath+'\\01_input\\LTOP\\BELMONT\\351387R.MES', dirPath+'\\01_input\\LTOP\\BELMONT\\observationsFromLTOP.xml')
# debug = conversionUtils.LTOP2xml(dirPath+'\\01_input\\LTOP\\PAUDEX\\PAUDEX_C.mes', dirPath+'\\01_input\\LTOP\\PAUDEX\\observationsFromLTOP.xml')



# ---   INITIALISATION DU XML DES PARAMETRES
# paramCalculUtils.initialisationParamCalculXml(dirPath+'\\fichiersInput\\PLAN17\\ParametresCalcul.xml')
# dictParametres = controleCoherenceUtils.xml2dictionnaire(dirPath+'\\ParametresCalcul.xml')





if __name__ == "__main__":
    
    # # Ajout de 30cm d'erreur sur une zone des coordonnées approchées
    # dictPoints = conversionUtils.xml2dictionnaire(dirPath+'\\01_input\\plan17\\Points.xml')
    # for i, point in enumerate(dictPoints['points']['point']):
    #     if i < 500 and i > 700: # Une centain de point avec la même erreur (translation)
    #         point['E'], point['N'] = float(point['E']) + 0.50, float(point['N']) - 0.25
        
    # conversionUtils.dictionnaire2xml(dictPoints, dirPath+'\\01_input\\plan17\\testCoordApproch\\points_avec_translation_30cm.xml')
    
    
    
    
    # nomsFichiers = {'fichierXMLCanevas':dirPath+'\\01_input\\allBelmont\\Canevas.xml', 
    #                 'fichierXMLPoints':dirPath+'\\01_input\\allBelmont\\XXXXXXXXXXXX, 
    #                 'fichierXMLParametres':dirPath+'\\01_input\\allBelmont\\Parametres.xml',
    #                 'fichierXSDCanevas':dirPath+'\\modeleDonnees\\modeleCanevas.xsd', 
    #                 'fichierXSDPoints':dirPath+'\\modeleDonnees\\modelePoints.xsd', 
    #                 'fichierXSDParametres':dirPath+'\\modeleDonnees\\modeleParamCalcul.xsd',
    #                 'fichierLog': dirPath+'\\01_input\\allBelmont\\ctrlCoherence.log',
    #                 'dossierResultats': dirPath+'\\02_output\\allBelmont'}
    
    
    

    nomsFichiersGirard = {'fichierXMLCanevas':dirPath+'\\analyseSolvabilite\\Generation_donnees_test\\donnees_Girard_avec_problèmes\\Observations.xml', 
                            'fichierXMLPoints':dirPath+'\\analyseSolvabilite\\Generation_donnees_test\\donnees_Girard_avec_problèmes\\Points.xml', 
                            'fichierXMLParametres':dirPath+'\\analyseSolvabilite\\Generation_donnees_test\\donnees_Girard_avec_problèmes\\Parametres.xml',
                            'fichierXSDCanevas':dirPath+'\\modeleDonnees\\observationsModel.xsd', 
                            'fichierXSDPoints':dirPath+'\\modeleDonnees\\pointsModel.xsd', 
                            'fichierXSDParametres':dirPath+'\\modeleDonnees\\parametersModel.xsd',
                            'dossierResultats': dirPath+'\\analyseSolvabilite\\Generation_donnees_test\\donnees_Girard_avec_problèmes\\res\\'}
    
    
    
    nomsFichiersBelmont = {'fichierXMLCanevas':dirPath+'\\analyseSolvabilite\\Generation_donnees_test\\donnes_Belmont\\Observations.xml', 
                            'fichierXMLPoints':dirPath+'\\analyseSolvabilite\\Generation_donnees_test\\donnes_Belmont\\Points.xml', 
                            'fichierXMLParametres':dirPath+'\\analyseSolvabilite\\Generation_donnees_test\\donnes_Belmont\\Parametres.xml',
                            'fichierXSDCanevas':dirPath+'\\modeleDonnees\\observationsModel.xsd', 
                            'fichierXSDPoints':dirPath+'\\modeleDonnees\\pointsModel.xsd', 
                            'fichierXSDParametres':dirPath+'\\modeleDonnees\\parametersModel.xsd',
                            'dossierResultats': dirPath+'\\analyseSolvabilite\\Generation_donnees_test\\donnes_Belmont\\res\\'}
            


    Process = processUtils.Process(nomsFichiersBelmont)
    debug = Process.run()
    
    
    
    
            

            
        
            
        
         
        
        
        






















