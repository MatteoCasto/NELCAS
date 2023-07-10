
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem, QStandardItemModel
import json
import xmltodict
from PyQt5 import uic
import sys
import os
import time


class UI_ongletParam(QtWidgets.QMainWindow):
    
    def __init__(self):
        
        super(UI_ongletParam, self).__init__()
        # Charger le ui
        uic.loadUi(os.getcwd()+'\\interface\\OngletParametres.ui', self)

        
        # Désactiver le widget principal
        self.centralwidget.setEnabled(False)
        
        
        # connection bouton de la menu bar
        self.actionNouveau.triggered.connect(self.newFile)
        self.actionOuvrir.triggered.connect(self.openFile)
        self.actionEnregistrer.triggered.connect(self.saveFile)
        self.actionEnregistrer_sous.triggered.connect(self.saveAsFile)
        
    
        # connection bouton d'ajout des groupes
        self.addGroupeDistance.clicked.connect(self.appendGroupeDistance)
        self.addGroupeDirection.clicked.connect(self.appendGroupeDirection)
        self.addGroupeCentrage.clicked.connect(self.appendGroupeCentrage)
        self.addGroupeGNSS.clicked.connect(self.appendGroupeGnss)
        self.addGroupeSystemeLocal.clicked.connect(self.appendGroupeSystemeLocal)
        self.addGroupeCote.clicked.connect(self.appendGroupeCote)
        

        # connection des boutons de MAJ des sigma plani et alti
        self.adaptSigmaPlani.clicked.connect(self.MAJsigmaPlani)
        self.adaptSigmaAlti.clicked.connect(self.MAJsigmaAlti)


        # Resize largeur des colonnes
        header = self.tableWidgetGrDist.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetGrDir.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetGrCent.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetGrGnss.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetGrSysLoc.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetMesSimple.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetDatumPlani.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetDatumPlani.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        
        # Afficher la fenêtre
        self.show()
        
        # initialisation du dictParametres et des listes de groupes et points fixes
        self.listeGroupesDistance, self.listeGroupesDirection, self.listeGroupesCentrage = [], [], []
        self.listeGroupesGnss = []
        self.listeGroupesSystemeLocal = []
        self.listeGroupesCote = []
        self.listePFplani, self.listePFalti = [], []
        self.dictParam = {'parameters':{}}
        
        
        
    def newFile(self):
        """
        Génére un fichier de paramètres vide XML après avoir cliqué sur "nouveau".
        """
    
        # Générer le fichier vide avec la fonction d'export
        # Path d'export
        try:
            self.filePath = QtWidgets.QFileDialog().getSaveFileName(None,"Save", None, "*.xml")[0]
            self.exportParametres() # exporte un fichier vide
            
            # vider tous les QTable
            self.tableWidgetGrDist.setRowCount(0)
            self.tableWidgetGrDir.setRowCount(0)
            self.tableWidgetGrCent.setRowCount(0)
            self.tableWidgetGrGnss.setRowCount(0)
            self.tableWidgetGrSysLoc.setRowCount(0)
            self.tableWidgetMesSimple.setRowCount(0)
            self.tableWidgetDatumPlani.setRowCount(0)
            self.tableWidgetDatumAlti.setRowCount(0)
            self.nomReseau.setText('') # texte vide pour le nom du réseau
            
            # Activer le tabwidget
            self.centralwidget.setEnabled(True)
            # Activer les boutons save et save as
            self.actionEnregistrer.setEnabled(True)
            self.actionEnregistrer_sous.setEnabled(True)
            
            # Set le nom du fichier lu
            self.setWindowTitle('Paramètres  -  {:s}  -  enregistré'.format(self.filePath))
            time.sleep(0.5)
            self.setWindowTitle('Paramètres  -  {:s}'.format(self.filePath))
        except:
            return None
        
        
    def openFile(self):
        """
        Fonction d'import du fichier XML des paramètres après avoir cliqué sur "ourvrir".
        """
        # import du fichier texte XML
        try:
            self.filePath = QtWidgets.QFileDialog().getOpenFileName(None,"Open", None, "*.xml")[0]
            self.importParametres()
                
            # Set le nom du fichier lu
            self.setWindowTitle('Paramètres  -  {:s}'.format(self.filePath))
            
            # Activer les boutons save et save as
            self.actionEnregistrer.setEnabled(True)
            self.actionEnregistrer_sous.setEnabled(True)
            # Activer le tabwidget
            self.centralwidget.setEnabled(True)
        except:
            return None
        
        
        
    def saveFile(self):
        """
        Sauvegarde le fichier et remplace celui qui a été importé avec le même nom. S'active après avoir cliqué sur "Enregistrer".
        """
        try:
        # Remplace le fichier courant avec sa nouvelle version de lui-même.
            self.exportParametres()
            # Set le nom du fichier lu
            self.setWindowTitle('Paramètres  -  {:s}  -  enregistré'.format(self.filePath))
            time.sleep(0.5)
            self.setWindowTitle('Paramètres  -  {:s}'.format(self.filePath))
        except:
            return None
        
    
    def saveAsFile(self):
        """
        Sauvegarde le fichier sous un nouvel emplacement. S'active après avoir cliqué sur "Enregistrer sous".
        """
        
        # Path du nouveau fichier
        try:
            self.filePath = QtWidgets.QFileDialog().getSaveFileName(None,"Save as", None, "*.xml")[0]
            
            # Génère un nouveau fichier avec sa nouvelle version de lui-même.
            self.exportParametres()
            
            # Set le nom du fichier lu
            self.setWindowTitle('Paramètres  -  {:s}  -  enregistré'.format(self.filePath))
            time.sleep(0.5)
            self.setWindowTitle('Paramètres  -  {:s}'.format(self.filePath))
        except:
            return None
        
        
        
        
        
        
        
        
        
    def isCheckedString(self, checkbox):
        '''
        Simple fonction permettant de retourner un string 'true' ou 'false' avec t et f minuscule
        afin de respecter le type de donnée 'bool' des fichiers modèles XSD.
        
        Returns
        -------
            string : 'true' ou 'false'
        '''
        if checkbox.isChecked() == True:
            return 'true'
        else:
            return 'false'
        
        
            

    
    def updateDataParamCalcul(self):
        '''
        Fonction simple permettant de refresh un dictionnaire de paramètres selon les entrées utilisateurs.
        '''
        
        self.dictParam = {
          'parameters': {
            'networkName': self.nomReseau.text(),
            'computationOptions': {
              'networkType': str(self.typeCalcul.currentText()),
              'calculationDimension': str(self.dimensionCalcul.currentText()),
              'maxIterationNbr': str(round(self.nbIterationsMax.value(),4)),
              'interruptionCondition': str(self.critereIterruption.value()),
              'robust': self.isCheckedString(self.robuste),
              'robustLimit': str(self.cRobuste.value()),
              'refractionk': str(round(self.refractionk.value(),3)),
              'sigmaRefractionk': str(self.sigmarefraction.value())
            },
            'groups': {
              'distanceGroups': {
                'distanceGroup': self.listeGroupesDistance
              },
              'directionGroups': {
                'directionGroup': self.listeGroupesDirection
              },
              'centringGroups': {
                'centringGroup': self.listeGroupesCentrage
              },
              'gnssGroups': {
                'gnssGroup': self.listeGroupesGnss
              },
              'localSystemGroups': {
                'localSystemGroup': self.listeGroupesSystemeLocal
              },
              'simpleMeasureGroups': {
                'simpleMeasureGroup': self.listeGroupesCote
              }
            },
            'planimetricControlPoints': {
              'point': self.listePFplani
            },
            'altimetricControlPoints': {
              'point': self.listePFalti
            }
          }
        }
        

        # print(json.dumps(self.dictParam, indent=2))
        

        return None
    
    
    
    
    '''
    Ensemble de fonctions permettant de MAJ les QTable des groupes en fonction des ajouts et après import.
    '''
    
    
    def updateTableGroupeDistance(self):
        self.tableWidgetGrDist.setRowCount(len(self.listeGroupesDistance))
        for row, groupe in enumerate(self.listeGroupesDistance):
            # On set les item dans la Table
            self.tableWidgetGrDist.setItem(row, 0, QtWidgets.QTableWidgetItem(groupe['distanceGroupName']))
            self.tableWidgetGrDist.setItem(row, 1, QtWidgets.QTableWidgetItem(groupe['stdDev']['mm']))
            self.tableWidgetGrDist.setItem(row, 2, QtWidgets.QTableWidgetItem(groupe['stdDev']['ppm']))
            self.tableWidgetGrDist.setItem(row, 3, QtWidgets.QTableWidgetItem(groupe['additionalUnknowns']['scaleFactor']))
            self.tableWidgetGrDist.setItem(row, 4, QtWidgets.QTableWidgetItem(groupe['additionalUnknowns']['additionConstant']))
            
    def updateTableGroupeDirection(self):
        self.tableWidgetGrDir.setRowCount(len(self.listeGroupesDirection))
        for row, groupe in enumerate(self.listeGroupesDirection):
            # On set les item dans la Table
            self.tableWidgetGrDir.setItem(row, 0, QtWidgets.QTableWidgetItem(groupe['directionGroupName']))
            self.tableWidgetGrDir.setItem(row, 1, QtWidgets.QTableWidgetItem(groupe['horizStdDev']['cc']))
            self.tableWidgetGrDir.setItem(row, 2, QtWidgets.QTableWidgetItem(groupe['zenithStdDev']['cc']))
            
    def updateTableGroupeCentrage(self):
        self.tableWidgetGrCent.setRowCount(len(self.listeGroupesCentrage))
        for row, groupe in enumerate(self.listeGroupesCentrage):
            # On set les item dans la Table
            self.tableWidgetGrCent.setItem(row, 0, QtWidgets.QTableWidgetItem(groupe['centringGroupName']))
            self.tableWidgetGrCent.setItem(row, 1, QtWidgets.QTableWidgetItem(groupe['stationCentring']['planiStdDev']['mm']))
            self.tableWidgetGrCent.setItem(row, 2, QtWidgets.QTableWidgetItem(groupe['stationCentring']['altiStdDev']['mm']))
            self.tableWidgetGrCent.setItem(row, 3, QtWidgets.QTableWidgetItem(groupe['targetCentring']['planiStdDev']['mm']))
            self.tableWidgetGrCent.setItem(row, 4, QtWidgets.QTableWidgetItem(groupe['targetCentring']['altiStdDev']['mm']))
            
    def updateTableGroupeGnss(self):
        self.tableWidgetGrGnss.setRowCount(len(self.listeGroupesGnss))
        for row, groupe in enumerate(self.listeGroupesGnss):
            # On set les item dans la Table
            self.tableWidgetGrGnss.setItem(row, 0, QtWidgets.QTableWidgetItem(groupe['gnssGroupName']))
            self.tableWidgetGrGnss.setItem(row, 1, QtWidgets.QTableWidgetItem(groupe['planiStdDev']['mm']))
            self.tableWidgetGrGnss.setItem(row, 2, QtWidgets.QTableWidgetItem(groupe['altiStdDev']['mm']))
            self.tableWidgetGrGnss.setItem(row, 3, QtWidgets.QTableWidgetItem(groupe['unknownParameters']['Etranslation']))
            self.tableWidgetGrGnss.setItem(row, 4, QtWidgets.QTableWidgetItem(groupe['unknownParameters']['Ntranslation']))
            self.tableWidgetGrGnss.setItem(row, 5, QtWidgets.QTableWidgetItem(groupe['unknownParameters']['Htranslation']))
            self.tableWidgetGrGnss.setItem(row, 6, QtWidgets.QTableWidgetItem(groupe['unknownParameters']['horizRotation']))
            self.tableWidgetGrGnss.setItem(row, 7, QtWidgets.QTableWidgetItem(groupe['unknownParameters']['horizScaleFactor']))
    
    def updateTableGroupeSystemeLocal(self):
        self.tableWidgetGrSysLoc.setRowCount(len(self.listeGroupesSystemeLocal))
        for row, groupe in enumerate(self.listeGroupesSystemeLocal):
            # On set les item dans la Table
            self.tableWidgetGrSysLoc.setItem(row, 0, QtWidgets.QTableWidgetItem(groupe['localSystemGroupName']))
            self.tableWidgetGrSysLoc.setItem(row, 1, QtWidgets.QTableWidgetItem(groupe['planiStdDev']['mm']))
            self.tableWidgetGrSysLoc.setItem(row, 2, QtWidgets.QTableWidgetItem(groupe['altiStdDev']['mm']))
            self.tableWidgetGrSysLoc.setItem(row, 3, QtWidgets.QTableWidgetItem(groupe['unknownParameters']['Etranslation']))
            self.tableWidgetGrSysLoc.setItem(row, 4, QtWidgets.QTableWidgetItem(groupe['unknownParameters']['Ntranslation']))
            self.tableWidgetGrSysLoc.setItem(row, 5, QtWidgets.QTableWidgetItem(groupe['unknownParameters']['Htranslation']))
            self.tableWidgetGrSysLoc.setItem(row, 6, QtWidgets.QTableWidgetItem(groupe['unknownParameters']['horizRotation']))
            self.tableWidgetGrSysLoc.setItem(row, 7, QtWidgets.QTableWidgetItem(groupe['unknownParameters']['horizScaleFactor']))
                
    def updateTableGroupeMesureSimple(self):
        self.tableWidgetMesSimple.setRowCount(len(self.listeGroupesCote))
        for row, groupe in enumerate(self.listeGroupesCote):
            # On set les item dans la Table
            self.tableWidgetMesSimple.setItem(row, 0, QtWidgets.QTableWidgetItem(groupe['simpleMeasureGroupName']))
            self.tableWidgetMesSimple.setItem(row, 1, QtWidgets.QTableWidgetItem(groupe['planiStdDev']['mm']))
            self.tableWidgetMesSimple.setItem(row, 2, QtWidgets.QTableWidgetItem(groupe['altiStdDev']['mm']))
            
    def updateTablePFplani(self):
        self.tableWidgetDatumPlani.setRowCount(len(self.listePFplani))
        for row, point in enumerate(self.listePFplani):
            # On set les item dans la Table
            self.tableWidgetDatumPlani.setItem(row, 0, QtWidgets.QTableWidgetItem(point['pointName']))
            self.tableWidgetDatumPlani.setItem(row, 1, QtWidgets.QTableWidgetItem(point['planiStdDev']['mm']))
    
    def updateTablePFalti(self):
        self.tableWidgetDatumAlti.setRowCount(len(self.listePFalti))
        for row, point in enumerate(self.listePFalti):
            # On set les item dans la Table
            self.tableWidgetDatumAlti.setItem(row, 0, QtWidgets.QTableWidgetItem(point['pointName']))
            self.tableWidgetDatumAlti.setItem(row, 1, QtWidgets.QTableWidgetItem(point['altiStdDev']['mm']))


            
            
        

            

    

    '''
    Ensemble de fonctions d'ajout des groupes à leurs listes respectives.
    '''
    
    def appendGroupeDistance(self):
        
        self.dictGroupeToAdd = {
          'distanceGroupName': self.nomGroupeDistance.text(),
          'stdDev': {
            'mm': str(self.sigmaDSmm.value()),
            'ppm': str(self.sigmaDSppm.value())
          },
          'additionalUnknowns': {
            'scaleFactor': self.isCheckedString(self.facteurEchelle),
            'additionConstant': self.isCheckedString(self.constanteAddition)
          }
        }
        self.listeGroupesDistance.append(self.dictGroupeToAdd)
        self.updateTableGroupeDistance()
   
    
    def appendGroupeDirection(self):
        
        self.dictGroupeToAdd = {
          'directionGroupName': self.nomGroupeDirection.text(),
          'horizStdDev': {
            'cc': str(self.sigmaRI.value())
          },
          'zenithStdDev': {
            'cc': str(self.sigmaZD.value())
          }
        }
        self.listeGroupesDirection.append(self.dictGroupeToAdd)
        self.updateTableGroupeDirection()

    def appendGroupeCentrage(self):
        
        self.dictGroupeToAdd = {
          'centringGroupName': self.nomGroupeCentrage.text(),
          'stationCentring': {
            'planiStdDev': {
              'mm': str(self.sigmaCentStaPlani.value())
            },
            'altiStdDev': {
              'mm': str(self.sigmaCentStaAlti.value())
            }
          },
          'targetCentring': {
            'planiStdDev': {
              'mm': str(self.sigmaCentVisPlani.value())
            },
            'altiStdDev': {
              'mm': str(self.sigmaCentVisAlti.value())
            }
          }
        }
        self.listeGroupesCentrage.append(self.dictGroupeToAdd)
        self.updateTableGroupeCentrage()
        
    def appendGroupeGnss(self):
        
        self.dictGroupeToAdd = {
          'gnssGroupName': self.nomGroupeGNSS.text(),
          'planiStdDev': {
            'mm': str(self.GNSSsigmaLYLX.value())
          },
          'altiStdDev': {
            'mm': str(self.GNSSsigmaLH.value())
          },
          'unknownParameters': {
            'Etranslation': self.isCheckedString(self.GNSS_tE),
            'Ntranslation': self.isCheckedString(self.GNSS_tN),
            'Htranslation': self.isCheckedString(self.GNSS_tH),
            'horizRotation': self.isCheckedString(self.GNSS_rotHz),
            'horizScaleFactor': self.isCheckedString(self.GNSS_factEchHz)
          }
        }
        self.listeGroupesGnss.append(self.dictGroupeToAdd)
        self.updateTableGroupeGnss() 
    
    def appendGroupeSystemeLocal(self):
        
        self.dictGroupeToAdd = {
          'localSystemGroupName': self.nomGroupeSystemeLocal.text(),
          'planiStdDev': {
            'mm': str(self.systemeLocalSigmaLYLX.value())
          },
          'altiStdDev': {
            'mm': str(self.systemeLocalSigmaLH.value())
          },
          'unknownParameters': {
            'Etranslation': 'true',
            'Ntranslation': 'true',
            'Htranslation': 'false',
            'horizRotation': 'true',
            'horizScaleFactor': self.isCheckedString(self.systemeLocal_factEchHz)
          }
        }
        self.listeGroupesSystemeLocal.append(self.dictGroupeToAdd)
        self.updateTableGroupeSystemeLocal()
        
    def appendGroupeCote(self):
        
        self.dictGroupeToAdd = {
            'simpleMeasureGroupName': self.nomGroupeCote.text(),
            'planiStdDev': {
              'mm': str(self.coteSigmaDP.value())
            },
            'altiStdDev': {
              'mm': str(self.coteSigmaDH.value())
            }
          }
        self.listeGroupesCote.append(self.dictGroupeToAdd)
        self.updateTableGroupeMesureSimple()
        
    
            
    def MAJsigmaPlani(self):
        '''
        Fonction permettant de MAJ tous les sigma plani (colonne de droite).
        '''
        nRows = self.tableWidgetDatumPlani.rowCount()
        for row in range(0,nRows):
            
            # Changer chaque valeurs par l'input planiEcartTypePoint
            val = str(self.planiEcartTypePoint.value())
            self.tableWidgetDatumPlani.setItem(row, 1, QtWidgets.QTableWidgetItem(val))
            
        
        
    def MAJsigmaAlti(self):
        '''
        Fonction permettant de MAJ tous les sigma alti (colonne de droite).
        '''
        nRows = self.tableWidgetDatumAlti.rowCount()
        for row in range(0,nRows):
            
            # Changer chaque valeurs par l'input altiEcartTypePoint
            val = str(self.altiEcartTypePoint.value())
            self.tableWidgetDatumAlti.setItem(row, 1, QtWidgets.QTableWidgetItem(val))
        
        
        
        
        
        
        

        
        
    
            
            
            
    def exportParametres(self):
        '''
        Fonction générale d'export des paramètres, groupes et PF saisis, au format XML. (avec les valeurs des QTable)
        '''
        
        #### GROUPES DISTANCE
        
        nRows = self.tableWidgetGrDist.rowCount()
        self.listeGroupesDistance = [] # Vider les data pour les remplacement par les valeurs de la QTable
        for row in range(0,nRows):
            
            # Attribution (avec condition si vide == '')
            distanceGroupName = self.tableWidgetGrDist.item(row, 0).text() if self.tableWidgetGrDist.item(row,0) is not None else ''
            stdDevMM = self.tableWidgetGrDist.item(row, 1).text() if self.tableWidgetGrDist.item(row,1) is not None else ''
            stdDevPPM = self.tableWidgetGrDist.item(row, 2).text() if self.tableWidgetGrDist.item(row, 2) is not None else ''
            scaleFactor = self.tableWidgetGrDist.item(row, 3).text() if self.tableWidgetGrDist.item(row, 3) is not None else ''
            additionConstant = self.tableWidgetGrDist.item(row, 4).text() if self.tableWidgetGrDist.item(row, 4) is not None else ''
            
            # Sous dictionnairte par mesure
            sousDict = {
              'distanceGroupName': distanceGroupName,
              'stdDev': {
                'mm': stdDevMM,
                'ppm': stdDevPPM
              },
              'additionalUnknowns': {
                'scaleFactor': scaleFactor,
                'additionConstant': additionConstant 
                }
              }                       
            self.listeGroupesDistance.append(sousDict)
            
        # Ajout au dict final pour export
        if len(self.listeGroupesDistance) > 0: # Il y'a au moins un élément dans la liste
            self.dictParam['parameters'].update({'groups':{
                                                'distanceGroups':self.listeGroupesDistance}}) 
            
            
            
        #### GROUPES DIRECTION
        
        nRows = self.tableWidgetGrDir.rowCount()
        self.listeGroupesDirection = [] # Vider les data pour les remplacement par les valeurs de la QTable
        for row in range(0,nRows):
            
            # Attribution (avec condition si vide == '')
            directionGroupName = self.tableWidgetGrDir.item(row, 0).text() if self.tableWidgetGrDir.item(row,0) is not None else ''
            stdDevHz = self.tableWidgetGrDir.item(row, 1).text() if self.tableWidgetGrDir.item(row,1) is not None else ''
            stdDevZd = self.tableWidgetGrDir.item(row, 2).text() if self.tableWidgetGrDir.item(row,2) is not None else ''
            
            # Sous dictionnairte par mesure
            sousDict = {
              'directionGroupName': directionGroupName,
              'horizStdDev': {
                'cc': stdDevHz
              },
              'zenithStdDev': {
                'cc': stdDevZd
              }
            }                      
            self.listeGroupesDirection.append(sousDict)
            
        # Ajout au dict final pour export
        if len(self.listeGroupesDirection) > 0: # Il y'a au moins un élément dans la liste
            self.dictParam['parameters'].update({'groups':{
                                                'directionGroups':self.listeGroupesDirection}}) 
        
        
        #### GROUPES CENTRAGE
        
        nRows = self.tableWidgetGrCent.rowCount()
        self.listeGroupesCentrage = [] # Vider les data pour les remplacement par les valeurs de la QTable
        for row in range(0,nRows):
            
            # Attribution (avec condition si vide == '')
            centringGroupName = self.tableWidgetGrCent.item(row, 0).text() if self.tableWidgetGrCent.item(row,0) is not None else ''
            STplaniStdDev = self.tableWidgetGrCent.item(row, 1).text() if self.tableWidgetGrCent.item(row,1) is not None else ''
            STaltiStdDev = self.tableWidgetGrCent.item(row, 2).text() if self.tableWidgetGrCent.item(row,2) is not None else ''
            VISplaniStdDev = self.tableWidgetGrCent.item(row, 3).text() if self.tableWidgetGrCent.item(row,3) is not None else ''
            VISaltiStdDev = self.tableWidgetGrCent.item(row, 4).text() if self.tableWidgetGrCent.item(row,4) is not None else ''
            
            # Sous dictionnairte par mesure
            sousDict = {
              'centringGroupName': centringGroupName,
              'stationCentring': {
                'planiStdDev': {
                  'mm': STplaniStdDev
                },
                'altiStdDev': {
                  'mm': STaltiStdDev
                }
              },
              'targetCentring': {
                'planiStdDev': {
                  'mm': VISplaniStdDev
                },
                'altiStdDev': {
                  'mm': VISaltiStdDev
                }
              }
            }                     
            self.listeGroupesCentrage.append(sousDict)
            
        # Ajout au dict final pour export
        if len(self.listeGroupesCentrage) > 0: # Il y'a au moins un élément dans la liste
            self.dictParam['parameters'].update({'groups':{
                                                 'centringGroups':self.listeGroupesCentrage}}) 
            
            
        #### GROUPES GNSS
        
        nRows = self.tableWidgetGrGnss.rowCount()
        self.listeGroupesGnss = [] # Vider les data pour les remplacement par les valeurs de la QTable
        for row in range(0,nRows):
            
            # Attribution (avec condition si vide == '')
            gnssGroupName = self.tableWidgetGrGnss.item(row, 0).text() if self.tableWidgetGrGnss.item(row,0) is not None else ''
            planiStdDev = self.tableWidgetGrGnss.item(row, 1).text() if self.tableWidgetGrGnss.item(row,1) is not None else ''
            altiStdDev = self.tableWidgetGrGnss.item(row, 2).text() if self.tableWidgetGrGnss.item(row,2) is not None else ''
            Etranslation = self.tableWidgetGrGnss.item(row, 3).text() if self.tableWidgetGrGnss.item(row,3) is not None else ''
            Ntranslation = self.tableWidgetGrGnss.item(row, 4).text() if self.tableWidgetGrGnss.item(row,4) is not None else ''
            Htranslation = self.tableWidgetGrGnss.item(row, 5).text() if self.tableWidgetGrGnss.item(row,5) is not None else ''
            horizRotation = self.tableWidgetGrGnss.item(row, 6).text() if self.tableWidgetGrGnss.item(row,6) is not None else ''
            horizScaleFactor = self.tableWidgetGrGnss.item(row, 7).text() if self.tableWidgetGrGnss.item(row,7) is not None else ''
            
            # Sous dictionnairte par mesure
            sousDict = {
              'gnssGroupName': gnssGroupName,
              'planiStdDev': {
                'mm': planiStdDev
              },
              'altiStdDev': {
                'mm': altiStdDev
              },
              'unknownParameters': {
                'Etranslation': Etranslation,
                'Ntranslation': Ntranslation,
                'Htranslation': Htranslation,
                'horizRotation': horizRotation,
                'horizScaleFactor': horizScaleFactor
              }
            }                    
            self.listeGroupesGnss.append(sousDict)
            
        # Ajout au dict final pour export
        if len(self.listeGroupesGnss) > 0: # Il y'a au moins un élément dans la liste
            self.dictParam['parameters'].update({'groups':{
                                                 'gnssGroups':self.listeGroupesGnss}}) 
            
        
        #### GROUPES SYSTEME LOCAL
        
        nRows = self.tableWidgetGrSysLoc.rowCount()
        self.listeGroupesSystemeLocal = [] # Vider les data pour les remplacement par les valeurs de la QTable
        for row in range(0,nRows):
            
            # Attribution (avec condition si vide == '')
            sysLocGroupName = self.tableWidgetGrSysLoc.item(row, 0).text() if self.tableWidgetGrSysLoc.item(row,0) is not None else ''
            planiStdDev = self.tableWidgetGrSysLoc.item(row, 1).text() if self.tableWidgetGrSysLoc.item(row,1) is not None else ''
            altiStdDev = self.tableWidgetGrSysLoc.item(row, 2).text() if self.tableWidgetGrSysLoc.item(row,2) is not None else ''
            Etranslation = self.tableWidgetGrSysLoc.item(row, 3).text() if self.tableWidgetGrSysLoc.item(row,3) is not None else ''
            Ntranslation = self.tableWidgetGrSysLoc.item(row, 4).text() if self.tableWidgetGrSysLoc.item(row,4) is not None else ''
            Htranslation = self.tableWidgetGrSysLoc.item(row, 5).text() if self.tableWidgetGrSysLoc.item(row,5) is not None else ''
            horizRotation = self.tableWidgetGrSysLoc.item(row, 6).text() if self.tableWidgetGrSysLoc.item(row,6) is not None else ''
            horizScaleFactor = self.tableWidgetGrSysLoc.item(row, 7).text() if self.tableWidgetGrSysLoc.item(row,7) is not None else ''
            
            # Sous dictionnairte par mesure
            sousDict = {
              'localSystemGroupName': sysLocGroupName,
              'planiStdDev': {
                'mm': planiStdDev
              },
              'altiStdDev': {
                'mm': altiStdDev
              },
              'unknownParameters': {
                'Etranslation': Etranslation,
                'Ntranslation': Ntranslation,
                'Htranslation': Htranslation,
                'horizRotation': horizRotation,
                'horizScaleFactor': horizScaleFactor
              }
            }                    
            self.listeGroupesSystemeLocal.append(sousDict)
            
        # Ajout au dict final pour export
        if len(self.listeGroupesSystemeLocal) > 0: # Il y'a au moins un élément dans la liste
            self.dictParam['parameters'].update({'groups':{
                                                 'localSystemGroups':self.listeGroupesSystemeLocal}}) 
            
            
        #### GROUPES MESURE SIMPLE
        
        nRows = self.tableWidgetMesSimple.rowCount()
        self.listeGroupesCote = [] # Vider les data pour les remplacement par les valeurs de la QTable
        for row in range(0,nRows):
            
            # Attribution (avec condition si vide == '')
            mesGroupName = self.tableWidgetMesSimple.item(row, 0).text() if self.tableWidgetMesSimple.item(row,0) is not None else ''
            planiStdDev = self.tableWidgetMesSimple.item(row, 1).text() if self.tableWidgetMesSimple.item(row,1) is not None else ''
            altiStdDev = self.tableWidgetMesSimple.item(row, 2).text() if self.tableWidgetMesSimple.item(row,2) is not None else ''

            # Sous dictionnairte par mesure
            sousDict = {
              'simpleMeasureGroupName': mesGroupName,
              'planiStdDev': {
                'mm': planiStdDev
              },
              'altiStdDev': {
                'mm': altiStdDev
              }
            }                    
            self.listeGroupesCote.append(sousDict)
            
        # Ajout au dict final pour export
        if len(self.listeGroupesCote) > 0: # Il y'a au moins un élément dans la liste
            self.dictParam['parameters'].update({'groups':{
                                                 'simpleMeasureGroups':self.listeGroupesCote}}) 
            
            
            
        
        #### PF PLANI
        
        nRows = self.tableWidgetDatumPlani.rowCount()
        self.listePFplani = [] # Vider les data pour les remplacement par les valeurs de la QTable
        for row in range(0,nRows):
            
            # Attribution (avec condition si vide == '')
            pointName = self.tableWidgetDatumPlani.item(row, 0).text() if self.tableWidgetDatumPlani.item(row,0) is not None else ''
            planiStdDev = self.tableWidgetDatumPlani.item(row, 1).text() if self.tableWidgetDatumPlani.item(row,1) is not None else ''

            # Sous dictionnairte par point
            sousDict = {'pointName': pointName,
                        'planiStdDev': {'mm': planiStdDev} }
                                          
            self.listePFplani.append(sousDict)
        # Ajout au dict final pour export
        if len(self.listePFplani) > 0: # Il y'a au moins un élément dans la liste
            self.dictParam['parameters'].update({'planimetricControlPoints':{'point':self.listePFplani}})
            
            
            
        #### PF ALTI
        
        nRows = self.tableWidgetDatumAlti.rowCount()
        self.listePFalti = [] # Vider les data pour les remplacement par les valeurs de la QTable
        for row in range(0,nRows):
            
            # Attribution (avec condition si vide == '')
            pointName = self.tableWidgetDatumAlti.item(row, 0).text() if self.tableWidgetDatumAlti.item(row,0) is not None else ''
            altiStdDev = self.tableWidgetDatumAlti.item(row, 1).text() if self.tableWidgetDatumAlti.item(row,1) is not None else ''

            # Sous dictionnairte par point
            sousDict = {'pointName': pointName,
                        'altiStdDev': {'mm': altiStdDev} }
                                          
            self.listePFalti.append(sousDict)
        # Ajout au dict final pour export
        if len(self.listePFalti) > 0: # Il y'a au moins un élément dans la liste
            self.dictParam['parameters'].update({'altimetricControlPoints':{'point':self.listePFalti}})
            
            
        
            
        
        
        
        
        
        #### EXPORT FILE
        self.updateDataParamCalcul()
        
        # si liste de groupe vide, enlever la balise du type de groupe
        if len(self.listeGroupesDistance) == 0:
            self.dictParam['parameters']['groups'].pop('distanceGroups')
        if len(self.listeGroupesDirection) == 0:
            self.dictParam['parameters']['groups'].pop('directionGroups')
        if len(self.listeGroupesCentrage) == 0:
            self.dictParam['parameters']['groups'].pop('centringGroups')
        if len(self.listeGroupesGnss) == 0:
            self.dictParam['parameters']['groups'].pop('gnssGroups')
        if len(self.listeGroupesSystemeLocal) == 0:
            self.dictParam['parameters']['groups'].pop('localSystemGroups')
        if len(self.listeGroupesCote) == 0:
            self.dictParam['parameters']['groups'].pop('simpleMeasureGroups')
     
        # si liste des PF vide, enlever la balise alti ou plani
        if len(self.listePFplani) == 0:
            self.dictParam['parameters'].pop('planimetricControlPoints')
        if len(self.listePFalti) == 0:
            self.dictParam['parameters'].pop('altimetricControlPoints')
        
        # Export du fichier texte XML
        # self.filePath = QtWidgets.QFileDialog().getSaveFileName(None,'Save', None, '*.xml')[0]
        self.dictParamString = xmltodict.unparse(self.dictParam, pretty=True)
        with open(self.filePath, 'w') as f:
            f.write(self.dictParamString)

        
        
        
        
        
    
        


    def importParametres(self):
        '''
        Fonction générale d'import des paramètres, groupes et PF saisis, à partir d'un format XML.
        '''
        
        # initialisation du dictParametres et des listes de groupes et points fixes
        self.listeGroupesDistance, self.listeGroupesDirection, self.listeGroupesCentrage = [], [], []
        self.listeGroupesGnss = []
        self.listeGroupesSystemeLocal = []
        self.listeGroupesCote = []
        self.listePFplani, self.listePFalti = [], []
        
        # initialisation des paramètres 
        self.updateDataParamCalcul()
        
        # improt du fichier texte XML
        # self.filePathImportParam = QtWidgets.QFileDialog().getOpenFileName(None,'Open', None, '*.xml')[0]
        with open(self.filePath) as f:
            self.dictParamImport = xmltodict.parse(f.read())

            
        # options générales
        self.nomReseau.setText(self.dictParamImport['parameters']['networkName']) 
        self.typeCalcul.setCurrentText(self.dictParamImport['parameters']['computationOptions']['networkType']) 
        self.dimensionCalcul.setCurrentText(self.dictParamImport['parameters']['computationOptions']['calculationDimension']) 
        self.nbIterationsMax.setValue(int(self.dictParamImport['parameters']['computationOptions']['maxIterationNbr']))
        self.critereIterruption.setValue(float(self.dictParamImport['parameters']['computationOptions']['interruptionCondition']))
        rob = True if self.dictParamImport['parameters']['computationOptions']['robust'] == 'true' else False
        self.robuste.setChecked(rob)
        self.cRobuste.setValue(float(self.dictParamImport['parameters']['computationOptions']['robustLimit']))
        self.refractionk.setValue(float(self.dictParamImport['parameters']['computationOptions']['refractionk']))
        self.sigmarefraction.setValue(float(self.dictParamImport['parameters']['computationOptions']['sigmaRefractionk']))
        
        # groupes (try dans le cas où il y a pas un type de groupe)
        try:
            if type(self.dictParamImport['parameters']['groups']['distanceGroups']['distanceGroup']) != list:
                self.listeGroupesDistance = [self.dictParamImport['parameters']['groups']['distanceGroups']['distanceGroup']]
            else: # déjà en liste
                self.listeGroupesDistance = self.dictParamImport['parameters']['groups']['distanceGroups']['distanceGroup']
        except:
            pass
        try:
            if type(self.dictParamImport['parameters']['groups']['directionGroups']['directionGroup']) != list:
                self.listeGroupesDirection = [self.dictParamImport['parameters']['groups']['directionGroups']['directionGroup']]
            else: # déjà en liste
                self.listeGroupesDirection = self.dictParamImport['parameters']['groups']['directionGroups']['directionGroup']
        except:
            pass
        try:
            if type(self.dictParamImport['parameters']['groups']['centringGroups']['centringGroup']) != list:
                self.listeGroupesCentrage = [self.dictParamImport['parameters']['groups']['centringGroups']['centringGroup']]
            else: # déjà en liste
                self.listeGroupesCentrage = self.dictParamImport['parameters']['groups']['centringGroups']['centringGroup']
        except:
            pass
        try:
            if type(self.dictParamImport['parameters']['groups']['gnssGroups']['gnssGroup']) != list:
                self.listeGroupesGnss= [self.dictParamImport['parameters']['groups']['gnssGroups']['gnssGroup']]
            else: # déjà en liste
                self.listeGroupesGnss = self.dictParamImport['parameters']['groups']['gnssGroups']['gnssGroup']
        except:
            pass
        try:
            if type(self.dictParamImport['parameters']['groups']['localSystemGroups']['localSystemGroup']) != list:
                self.listeGroupesSystemeLocal = [self.dictParamImport['parameters']['groups']['localSystemGroups']['localSystemGroup']]
            else: # déjà en liste
                self.listeGroupesSystemeLocal = self.dictParamImport['parameters']['groups']['localSystemGroups']['localSystemGroup']
        except:
            pass
        try:
            if type(self.dictParamImport['parameters']['groups']['simpleMeasureGroups']['simpleMeasureGroup']) != list:
                self.listeGroupesCote = [self.dictParamImport['parameters']['groups']['simpleMeasureGroups']['simpleMeasureGroup']]
            else: # déjà en liste
                self.listeGroupesCote = self.dictParamImport['parameters']['groups']['simpleMeasureGroups']['simpleMeasureGroup']
        except:
            pass


        # Liste des points fixes plani et alti
        try:
            if type(self.dictParamImport['parameters']['planimetricControlPoints']['point']) != list:
                self.listePFplani = [self.dictParamImport['parameters']['planimetricControlPoints']['point']]
            else: # déjà en liste
                self.listePFplani = self.dictParamImport['parameters']['planimetricControlPoints']['point']
        except:
            pass
        try:
            if type(self.dictParamImport['parameters']['altimetricControlPoints']['point']) != list:
                self.listePFalti= [self.dictParamImport['parameters']['altimetricControlPoints']['point']]
            else: # déjà en liste
                self.listePFalti = self.dictParamImport['parameters']['altimetricControlPoints']['point']
        except:
            pass



        
        # Refresh
        self.updateDataParamCalcul() # avec les données lues du fichier
        self.updateTableGroupeDistance()
        self.updateTableGroupeDirection()
        self.updateTableGroupeCentrage()
        self.updateTableGroupeGnss()
        self.updateTableGroupeSystemeLocal()
        self.updateTableGroupeMesureSimple()
        self.updateTablePFplani()
        self.updateTablePFalti()
        
        
        
        
        
    def addRow(self, tableWidget):
        '''
        Fonction permettant d'ajouter une ligne vide sous la ligne selectionnée.
        '''
        currentRow = tableWidget.currentRow()
        tableWidget.insertRow(currentRow+1)
        
        
    def removeRow(self, tableWidget):
        '''
        Fonction permettant de supprimer une ligne selectionée.
        '''
        currentRow = tableWidget.currentRow()
        if tableWidget.rowCount() > 0: # Uniquement si il y'a au moins une row 
            tableWidget.removeRow(currentRow)
            
            
    def contextMenuEvent(self, event):
        '''
        Redéfinition de la fonction pour le menu contextuel au clic droit sur une QTable.
        Ajouter ou supprimer une row.        
        '''
        # print('MOUSE GLOBAL:', self.centralwidget.mapToGlobal(event.pos()))
        clicGlobal = self.centralwidget.mapToGlobal(event.pos())
        
        #### GROUPES DISTANCE
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_2.mapToGlobal(self.tableWidgetGrDist.geometry().topLeft()) # -> QPoint
        topLeftLocal = self.tableWidgetGrDist.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetGrDir.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 1 and self.toolBox.currentIndex()==0:
            
            for i in self.tableWidgetGrDist.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction('Supprimer la ligne selectionnée')
            addRowAction = menu.addAction('Ajouter une ligne en dessous')
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetGrDist) 
                
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetGrDist)    
        
        
        #### GROUPES DIRECTION
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_3.mapToGlobal(self.tableWidgetGrDir.geometry().topLeft()) # -> QPoint
        topLeftLocal = self.tableWidgetGrDir.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetGrDir.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 1 and self.toolBox.currentIndex()==0:

            for i in self.tableWidgetGrDir.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction('Supprimer la ligne selectionnée')
            addRowAction = menu.addAction('Ajouter une ligne en dessous')
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetGrDir) 
                
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetGrDir)  
                
        
        #### GROUPES CENTRAGE
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_4.mapToGlobal(self.tableWidgetGrCent.geometry().topLeft()) # -> QPoint
        topLeftLocal = self.tableWidgetGrCent.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetGrCent.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 1 and self.toolBox.currentIndex()==0:

            for i in self.tableWidgetGrCent.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction('Supprimer la ligne selectionnée')
            addRowAction = menu.addAction('Ajouter une ligne en dessous')
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetGrCent) 
                
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetGrCent)  
                
        
        #### GROUPES GNSS
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_5.mapToGlobal(self.tableWidgetGrGnss.geometry().topLeft()) # -> QPoint
        topLeftLocal = self.tableWidgetGrGnss.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetGrGnss.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 1 and self.toolBox.currentIndex()==1:

            for i in self.tableWidgetGrGnss.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction('Supprimer la ligne selectionnée')
            addRowAction = menu.addAction('Ajouter une ligne en dessous')
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetGrGnss) 
                
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetGrGnss) 
                
        
        #### GROUPES SYSTEME LOCAL
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_6.mapToGlobal(self.tableWidgetGrSysLoc.geometry().topLeft()) # -> QPoint
        topLeftLocal = self.tableWidgetGrSysLoc.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetGrSysLoc.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 1 and self.toolBox.currentIndex()==2:

            for i in self.tableWidgetGrSysLoc.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction('Supprimer la ligne selectionnée')
            addRowAction = menu.addAction('Ajouter une ligne en dessous')
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetGrSysLoc) 
                
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetGrSysLoc) 
                
        
        #### GROUPES MESURES SIMPLES
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_7.mapToGlobal(self.tableWidgetMesSimple.geometry().topLeft()) # -> QPoint
        topLeftLocal = self.tableWidgetMesSimple.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetMesSimple.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 1 and self.toolBox.currentIndex()==3:

            for i in self.tableWidgetMesSimple.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction('Supprimer la ligne selectionnée')
            addRowAction = menu.addAction('Ajouter une ligne en dessous')
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetMesSimple) 
                
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetMesSimple) 
                
                
                
        #### POINTS FIXES PLANI
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_8.mapToGlobal(self.tableWidgetDatumPlani.geometry().topLeft()) # -> QPoint
        topLeftLocal = self.tableWidgetDatumPlani.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetDatumPlani.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 2 :

            for i in self.tableWidgetDatumPlani.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction('Supprimer la ligne selectionnée')
            addRowAction = menu.addAction('Ajouter une ligne en dessous')
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetDatumPlani) 
                
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetDatumPlani) 
                
                
                
        #### POINTS FIXES ALTI
        # Si le curseur se trouve dans la bonne QTable concernée
        topLeftGlobal = self.groupBox_9.mapToGlobal(self.tableWidgetDatumAlti.geometry().topLeft()) # -> QPoint
        topLeftLocal = self.tableWidgetDatumAlti.geometry().topLeft() # QPoint
        trans = topLeftGlobal - topLeftLocal
        if self.tableWidgetDatumAlti.geometry().contains(clicGlobal-trans) and self.tabWidget.currentIndex() == 2 :

            for i in self.tableWidgetDatumAlti.selectionModel().selection().indexes():
                row, _ = i.row(), i.column()
            menu = QtWidgets.QMenu()
            deleteRowAction = menu.addAction('Supprimer la ligne selectionnée')
            addRowAction = menu.addAction('Ajouter une ligne en dessous')
            action = menu.exec_(QtGui.QCursor.pos())
            
            # AJOUT DE ROW
            if action == addRowAction:
                # Ajouter ligne création
                self.addRow(self.tableWidgetDatumAlti) 
                
            # SUPPRESSION DE ROW 
            if action == deleteRowAction:
                # Supprimer la ligne sélectionnée
                self.removeRow(self.tableWidgetDatumAlti) 
            
            

    
    

