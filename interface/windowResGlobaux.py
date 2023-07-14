
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QVariant
import json
import xmltodict
from PyQt5 import uic
import libUtils.processUtils as processUtils
import os
import time
import json
import copy











class UI_ongletResGlobaux(QtWidgets.QMainWindow):
    
    def __init__(self):
        
        super(UI_ongletResGlobaux, self).__init__()
        
        # Charger le ui
        uic.loadUi(os.getcwd()+"\\interface\\OngletResGlobaux.ui", self)
        
        # connection bouton "ouvrir" de la menu bar
        self.actionOuvrir.triggered.connect(self.openFile)
        

        # Resize largeur des colonnes
        header = self.tableWidgetWiPlani.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetWiAlti.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetRattachPlani.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header = self.tableWidgetRattachAlti.horizontalHeader()   
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    


        # Init du filepath
        self.filePathImportResGlobaux = None
        
        # Afficher la fenêtre
        self.show()
        
    
    def parcourir_dictionnaire(self, dictionnaire):
        """
        Function qui s'appelle elle-même pour mettre sous forme de liste les éléments demandés
        dans TOUT le dictionnaire et ses enfants.

        Parameters
        ----------
        dictionnaire : dict
            Dictionnaires et sous-dictionnaires (enfants)

        Returns
        -------
        None.

        """
        
        for cle, valeur in dictionnaire.items():
            # Si la clé est dans la possiblité d'être SEULE ou MULTIPLE, la mettre en liste
            if cle in self.listeItemToPutInList:
                # mettre en liste le dict
                if not isinstance(valeur, list):
                    valeurNew = copy.deepcopy(valeur)
                    del dictionnaire[cle]
                    del valeur
                    dictionnaire.update({cle:[valeurNew]})
                for sousdict in dictionnaire[cle]:
                    self.parcourir_dictionnaire(sousdict)
            else:
                if isinstance(valeur, dict):
                    self.parcourir_dictionnaire(valeur)
                
    
    
        
        
        
        
        
        
        
        
    
    
    def setFloatInQTableWidget(self, QTableWidget, row, col, dataToAdd):
        """
        Fonction permettant d'ajouter un élément (float ou string) à une tableau pour permettre un tri selon son type.

        Parameters
        ----------
        QTableWidget : QTableWidget
            Tableau concerné.
        row : int
            No de ligne.
        col : int
            no de colonne.
        dataToAdd : Float ou String
            Donnée à ajouter au tableau.

        Returns
        -------
        None.

        """
        
        QTableWidget.setItem(row, col, QtWidgets.QTableWidgetItem())
        QTableWidget.item(row, col).setData(QtCore.Qt.DisplayRole, QtCore.QVariant(dataToAdd))

    



    def openFile(self, filePath=None):
        """
        Fonction qui lance l'explorateur de fichier à l'action triggered "ouvrir".
        Peut être activée si un calcul est réalisé -> filePath est celui saisie
        """
        
        if filePath: # Si la fenêtre s'ouvre après un calcul
            self.filePathImportResGlobaux = filePath
            try:
                self.importResultatsGlobaux()
            except:
                print('--- ERROR IMPORTING',self.filePathImportResGlobaux)
                return None # Ne rien importer
        else: # Ouvrerture d'un fichier en cliquant sur "ouvrir"
            self.filePathImportResGlobaux = QtWidgets.QFileDialog().getOpenFileName(None,"Open", None, "*.xml")[0]
            try:
                self.importResultatsGlobaux()
            except:
                print('--- ERROR IMPORTING',self.filePathImportResGlobaux)
                return None # Ne rien importer
    
    
    def importResultatsGlobaux(self):
        """
        Fonction d'import des résultats globaux qui s'active au clic du bouton prévu à cet effet.
        """
        
        # INIT LES ZONES DE TEXTES "GENERAL"
        self.RES_nomReseau.setText('xxx')
        self.RES_date.setText('xxx')
        self.RES_heure.setText('xxx')
        self.RES_typeReseau.setText('xxx')
        self.RES_dimension.setText('xxx')
        self.RES_robuste.setText('xxx')
        self.RES_limiteRobuste.setText('xxx')
        self.RES_refractionk.setText('xxx')
        self.RES_sigmak.setText('xxx')
        self.RES_ctrl_coh_geom.setText('xxx')
        
        # INIT LES ZONES DE TEXTE PLANI ET ALTI
        self.RES_PLANI_duree.setText('xxx')
        self.RES_PLANI_nb_iteration.setText('xxx')
        self.RES_PLANI_inc.setText('xxx')
        self.RES_PLANI_obs.setText('xxx')
        self.RES_PLANI_contr.setText('xxx')
        self.RES_PLANI_surabondance.setText('xxx')
        self.RES_ALTI_duree.setText('xxx')
        self.RES_ALTI_nb_iteration.setText('xxx')
        self.RES_ALTI_inc.setText('xxx')
        self.RES_ALTI_obs.setText('xxx')
        self.RES_ALTI_surabondance.setText('xxx')
        
        # INIT LES TABLEAUX
        self.RES_PLANI_treeViewQuotientsPlani.setModel(None)
        self.tableWidgetWiPlani.setRowCount(0)
        self.tableWidgetRattachPlani.setRowCount(0)
        self.RES_ALTI_treeViewQuotients.setModel(None)
        self.tableWidgetRattachAlti.setRowCount(0)
        self.tableWidgetWiAlti.setRowCount(0)
        
        
        # Initiliser une dict vide (sera ré-attribué)
        self.dictResGlobaux = []
        
        # import du fichier texte XML
        
        with open(self.filePathImportResGlobaux) as f:
            self.dictResGlobaux = xmltodict.parse(f.read())
        
            
        # Structure du dictionnaire (listes pour certains éléments)
        self.listeItemToPutInList = ['distanceGroup', 'directionGroup', 'centringGroup', 
                                     'gnssGroup', 'localSystemGroup', 'simpleMeasureGroup']
        try:
            self.parcourir_dictionnaire(self.dictResGlobaux)
        except:
            pass
        
        
        # Set le nom du fichier importé dans l'en-tête de la fenêtre
        self.setWindowTitle('Résultats  -  {:s}'.format(self.filePathImportResGlobaux))
        
        
        #### OPTIONS GENERALES
        self.RES_nomReseau.setText(self.dictResGlobaux['results']['parameters']['networkName'])
        self.RES_date.setText(self.dictResGlobaux['results']['globalResults']['date'])
        self.RES_heure.setText(self.dictResGlobaux['results']['globalResults']['time'])
        self.RES_typeReseau.setText(self.dictResGlobaux['results']['parameters']['computationOptions']['networkType'])
        self.RES_dimension.setText(self.dictResGlobaux['results']['parameters']['computationOptions']['calculationDimension'])
        self.RES_robuste.setText(self.dictResGlobaux['results']['parameters']['computationOptions']['robust'])
        self.RES_limiteRobuste.setText(self.dictResGlobaux['results']['parameters']['computationOptions']['robustLimit'])
        self.RES_refractionk.setText(self.dictResGlobaux['results']['parameters']['computationOptions']['refractionk'])
        self.RES_sigmak.setText(self.dictResGlobaux['results']['parameters']['computationOptions']['sigmaRefractionk'])
        self.RES_ctrl_coh_geom.setText(self.dictResGlobaux['results']['parameters']['computationOptions']['geometryPreChecks'])

        

        #### PLANIMETRIE
        if self.dictResGlobaux['results']['parameters']['computationOptions']['calculationDimension'] == "2D+1" or self.dictResGlobaux['results']['parameters']['computationOptions']['calculationDimension'] == "2D": 
            
            
            
            self.RES_PLANI_duree.setText(self.dictResGlobaux['results']['globalResults']['planimetry']['CalculationTime'])
            self.RES_PLANI_nb_iteration.setText(self.dictResGlobaux['results']['globalResults']['planimetry']['iterationsCount'])
            self.RES_PLANI_inc.setText(self.dictResGlobaux['results']['globalResults']['planimetry']['counting']['unknowns'])
            self.RES_PLANI_obs.setText(self.dictResGlobaux['results']['globalResults']['planimetry']['counting']['observations'])
            self.RES_PLANI_contr.setText(self.dictResGlobaux['results']['globalResults']['planimetry']['counting']['constraints'])
            self.RES_PLANI_surabondance.setText(self.dictResGlobaux['results']['globalResults']['planimetry']['counting']['overdetermination'])
            
            
            #### ^---- Quotients treeView
            # Génération du treeView
            self.RES_PLANI_treeViewQuotientsPlani.setHeaderHidden(True)
            self.treeModelQuotientsPlani = QStandardItemModel()
            self.treeModelQuotientsPlani.setColumnCount(2)
            self.rootNodeQuotientsPlani = self.treeModelQuotientsPlani.invisibleRootItem()
            
            # Quotient global en premier
            quotientGlobal = self.dictResGlobaux['results']['globalResults']['planimetry']['globalStdDevQuotient']
            self.rootNodeQuotientsPlani.appendRow([QStandardItem('GLOBAL'), QStandardItem(quotientGlobal)])

            # # get uniquement les noms de groupe et leurs quotient 2D
            try: 
                if 'distanceGroups' in self.dictResGlobaux['results']['parameters']['groups'].keys():
                    for group in self.dictResGlobaux['results']['parameters']['groups']['distanceGroups']['distanceGroup']:
                        self.rootNodeQuotientsPlani.appendRow([QStandardItem(group['distanceGroupName']), QStandardItem(group['stdDevQuotientFor2D'])])
            except:
                pass
            try: 
                if 'directionGroups' in self.dictResGlobaux['results']['parameters']['groups'].keys():
                    for group in self.dictResGlobaux['results']['parameters']['groups']['directionGroups']['directionGroup']:
                        self.rootNodeQuotientsPlani.appendRow([QStandardItem(group['directionGroupName']), QStandardItem(group['stdDevQuotientFor2D'])])  
            except:
                pass
            try:   
                if 'gnssGroups' in self.dictResGlobaux['results']['parameters']['groups'].keys():
                    for group in self.dictResGlobaux['results']['parameters']['groups']['gnssGroups']['gnssGroup']:
                        self.rootNodeQuotientsPlani.appendRow([QStandardItem(group['gnssGroupName']), QStandardItem(group['stdDevQuotientFor2D'])])  
            except:
                pass
            try: 
                if 'localSystemGroups' in self.dictResGlobaux['results']['parameters']['groups'].keys():
                    for group in self.dictResGlobaux['results']['parameters']['groups']['localSystemGroups']['localSystemGroup']:
                        self.rootNodeQuotientsPlani.appendRow([QStandardItem(group['localSystemGroupName']), QStandardItem(group['stdDevQuotientFor2D'])])  
            except:
                pass
            try: 
                if 'simpleMeasureGroups' in self.dictResGlobaux['results']['parameters']['groups'].keys():
                    for group in self.dictResGlobaux['results']['parameters']['groups']['simpleMeasureGroups']['simpleMeasureGroup']:
                        self.rootNodeQuotientsPlani.appendRow([QStandardItem(group['simpleMeasureGroupName']), QStandardItem(group['stdDevQuotientFor2D'])])  
            except:
                pass

            self.RES_PLANI_treeViewQuotientsPlani.setModel(self.treeModelQuotientsPlani)
            self.RES_PLANI_treeViewQuotientsPlani.expandAll()
            self.RES_PLANI_treeViewQuotientsPlani.resizeColumnToContents(0)
            self.RES_PLANI_treeViewQuotientsPlani.resizeColumnToContents(1)
            
            
            
                
            #### ^---- Wi QTableWidget PLANI
            
            # Set le nombre de wi sup à 3.5
            self.RES_PLANI_WiMax.setText(self.dictResGlobaux['results']['globalResults']['planimetry']['nbWiSup3.5'])
            self.listeWiMaxPlani = self.dictResGlobaux['results']['globalResults']['planimetry']['biggestWi']['wiMax']
            self.tableWidgetWiPlani.setRowCount(len(self.listeWiMaxPlani))
            for row, wiMax in enumerate(self.listeWiMaxPlani):
                # On set les item dans la Table
                self.setFloatInQTableWidget(self.tableWidgetWiPlani, row, 0, wiMax['parent'])
                self.setFloatInQTableWidget(self.tableWidgetWiPlani, row, 1, wiMax['pointName'])
                self.setFloatInQTableWidget(self.tableWidgetWiPlani, row, 2, wiMax['observation']['obsType'])
                if wiMax['observation']['obsType'] in  ['DP', 'LY', 'LX', 'EE', 'NN']:
                    factor = 1000 # pour mm
                if wiMax['observation']['obsType'] == 'RI':
                    factor = 10000 # pour cc
                     
                # Utilisation d'une petite fonction permettant que conserver le type float
                self.setFloatInQTableWidget(self.tableWidgetWiPlani, row, 3, float(wiMax['observation']['idObsPlani']))
                self.setFloatInQTableWidget(self.tableWidgetWiPlani, row, 4, float(wiMax['observation']['value']))
                self.setFloatInQTableWidget(self.tableWidgetWiPlani, row, 5, round(float(wiMax['observation']['stdDev'])*factor,1))
                self.setFloatInQTableWidget(self.tableWidgetWiPlani, row, 6, round(float(wiMax['observation']['vi'])*factor,1))
                self.setFloatInQTableWidget(self.tableWidgetWiPlani, row, 7, float(wiMax['observation']['wi']))
                self.setFloatInQTableWidget(self.tableWidgetWiPlani, row, 8, float(wiMax['observation']['zi']))
                self.setFloatInQTableWidget(self.tableWidgetWiPlani, row, 9, round(float(wiMax['observation']['nablaLi'])*factor,1))
                self.setFloatInQTableWidget(self.tableWidgetWiPlani, row, 10, round(float(wiMax['observation']['gi'])*factor,1))
                

                # mettre en évidence les wi > 3.5
                if abs(float(wiMax['observation']['wi'])) > 3.5:
                    font = QtGui.QFont()
                    font.setBold(True)
                    self.tableWidgetWiPlani.item(row, 7).setForeground(QtGui.QColor(255,0,0))
                    self.tableWidgetWiPlani.item(row, 7).setFont(font)
                    
                
                # Si RI, il y'a un écart latéral (angle * distance) et affichage dist.
                if wiMax['observation']['obsType'] == 'RI':
                    self.setFloatInQTableWidget(self.tableWidgetWiPlani, row, 11, round(float(wiMax['observation']['viLat'])*1000,1))
                    try: # si ancienne version de resultats, ne pas bloquer le programme si pas de dist
                        self.setFloatInQTableWidget(self.tableWidgetWiPlani, row, 12, round(float(wiMax['observation']['dist']),3))
                    except:
                        pass
                else: # Vide sinon
                    self.tableWidgetWiPlani.setItem(row, 11, QtWidgets.QTableWidgetItem('')) 
                    self.tableWidgetWiPlani.setItem(row, 12, QtWidgets.QTableWidgetItem('')) 
                    
            
            
            #### ^---- LIBRE AJUSTE RATTACHEMENT
            
            if self.dictResGlobaux['results']['parameters']['computationOptions']['networkType'] == 'stochastic':
                
                # liste des balises <points> des pts de rattachement
                self.listeRattachPlani = self.dictResGlobaux['results']['parameters']['planimetricControlPoints']['point']
                self.tableWidgetRattachPlani.setRowCount(len(self.listeRattachPlani))
                for row, point in enumerate(self.listeRattachPlani): 
                    # On set les item dans la Table
                    self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 0, point['pointName'])
                    try: # ne pas bloquer le programme si c'est une autre version des resultats sans FS
                        self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 1,  round(float(point['FS'])*1000,1))
                    except:
                        pass
                    self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 2,  float(point['EE']))
                    self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 3,  float(point['NN']))
                    self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 4,  round(float(point['planiStdDev'])*1000,1))
                    # Indicateurs EE
                    self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 5,  round(float(point['indicateursEE']['vi'])*1000,1))
                    self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 6,  float(point['indicateursEE']['wi']))
                    # mettre en évidence les wi > 3.5
                    if abs(float(point['indicateursEE']['wi'])) > 3.5:
                        font = QtGui.QFont()
                        font.setBold(True)
                        self.tableWidgetRattachPlani.item(row, 6).setForeground(QtGui.QColor(255,0,0))
                        self.tableWidgetRattachPlani.item(row, 6).setFont(font)
                    self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 7,  float(point['indicateursEE']['zi']))
                    self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 8,  round(float(point['indicateursEE']['nablaLi'])*1000,1))
                    self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 9,  round(float(point['indicateursEE']['gi'])*1000,1))
                    
                    # Indicateurs NN
                    self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 10,  round(float(point['indicateursNN']['vi'])*1000,1))
                    self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 11,  float(point['indicateursNN']['wi']))
                    # mettre en évidence les wi > 3.5
                    if abs(float(point['indicateursNN']['wi'])) > 3.5:
                        font = QtGui.QFont()
                        font.setBold(True)
                        self.tableWidgetRattachPlani.item(row, 11).setForeground(QtGui.QColor(255,0,0))
                        self.tableWidgetRattachPlani.item(row, 11).setFont(font)
                    self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 12,  float(point['indicateursNN']['zi']))
                    self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 13,  round(float(point['indicateursNN']['nablaLi'])*1000,1))
                    self.setFloatInQTableWidget(self.tableWidgetRattachPlani, row, 14,  round(float(point['indicateursNN']['gi'])*1000,1))
                    
                
                
                
                


            
        #### ALTIMETRIE
        

        
        if self.dictResGlobaux['results']['parameters']['computationOptions']['calculationDimension'] == "2D+1" or self.dictResGlobaux['results']['parameters']['computationOptions']['calculationDimension'] == "1D": 
            self.RES_ALTI_duree.setText(self.dictResGlobaux['results']['globalResults']['altimetry']['CalculationTime'])
            self.RES_ALTI_nb_iteration.setText(self.dictResGlobaux['results']['globalResults']['altimetry']['iterationsCount'])
            self.RES_ALTI_inc.setText(self.dictResGlobaux['results']['globalResults']['altimetry']['counting']['unknowns'])
            self.RES_ALTI_obs.setText(self.dictResGlobaux['results']['globalResults']['altimetry']['counting']['observations'])
            self.RES_ALTI_surabondance.setText(self.dictResGlobaux['results']['globalResults']['altimetry']['counting']['overdetermination'])
            
            #### ^---- Quotients treeView
            # Génération du treeView
            self.RES_ALTI_treeViewQuotients.setHeaderHidden(True)
            self.treeModelQuotients = QStandardItemModel()
            self.treeModelQuotients.setColumnCount(2)
            self.rootNodeQuotients = self.treeModelQuotients.invisibleRootItem()
            
            
            ##### CORRIGER ICI
            # Quotient global en premier
            quotientGlobal = self.dictResGlobaux['results']['globalResults']['altimetry']['globalStdDevQuotient']
            self.rootNodeQuotients.appendRow([QStandardItem('GLOBAL'), QStandardItem(quotientGlobal)])

            # # get uniquement les noms de groupe et leurs quotient 2D
            try: 
                if 'directionGroups' in self.dictResGlobaux['results']['parameters']['groups'].keys():
                    for group in self.dictResGlobaux['results']['parameters']['groups']['directionGroups']['directionGroup']:
                        self.rootNodeQuotients.appendRow([QStandardItem(group['directionGroupName']), QStandardItem(group['stdDevQuotientFor1D'])])  
            except:
                pass
            try: 
                if 'gnssGroups' in self.dictResGlobaux['results']['parameters']['groups'].keys():
                    for group in self.dictResGlobaux['results']['parameters']['groups']['gnssGroups']['gnssGroup']:
                        self.rootNodeQuotients.appendRow([QStandardItem(group['gnssGroupName']), QStandardItem(group['stdDevQuotientFor1D'])])  
            except:
                pass
            try: 
                if 'localSystemGroups' in self.dictResGlobaux['results']['parameters']['groups'].keys():
                    for group in self.dictResGlobaux['results']['parameters']['groups']['localSystemGroups']['localSystemGroup']:
                        self.rootNodeQuotients.appendRow([QStandardItem(group['localSystemGroupName']), QStandardItem(group['stdDevQuotientFor1D'])])  
            except:
                pass
            try: 
                if 'simpleMeasureGroups' in self.dictResGlobaux['results']['parameters']['groups'].keys():
                    for group in self.dictResGlobaux['results']['parameters']['groups']['simpleMeasureGroups']['simpleMeasureGroup']:
                        self.rootNodeQuotients.appendRow([QStandardItem(group['simpleMeasureGroupName']), QStandardItem(group['stdDevQuotientFor1D'])])  
            except:
                pass   

            self.RES_ALTI_treeViewQuotients.setModel(self.treeModelQuotients)
            self.RES_ALTI_treeViewQuotients.expandAll()
            self.RES_ALTI_treeViewQuotients.resizeColumnToContents(0)
            self.RES_ALTI_treeViewQuotients.resizeColumnToContents(1)
            
            
            
            #### ^---- Wi treeView ALTI
            
            
            # Set le nombre de wi sup à 3.5
            self.RES_ALTI_WiMax.setText(self.dictResGlobaux['results']['globalResults']['altimetry']['nbWiSup3.5'])
            self.listeWiMaxAlti = self.dictResGlobaux['results']['globalResults']['altimetry']['biggestWi']['wiMax']
            self.tableWidgetWiAlti.setRowCount(len(self.listeWiMaxAlti))
            for row, wiMax in enumerate(self.listeWiMaxAlti):
                # On set les item dans la Table
                self.setFloatInQTableWidget(self.tableWidgetWiAlti, row, 0, wiMax['parent'])
                self.setFloatInQTableWidget(self.tableWidgetWiAlti, row, 1, wiMax['pointName'])
                self.setFloatInQTableWidget(self.tableWidgetWiAlti, row, 2, wiMax['observation']['obsType'])
                self.setFloatInQTableWidget(self.tableWidgetWiAlti, row, 3, float(wiMax['observation']['idObsAlti']))
                self.setFloatInQTableWidget(self.tableWidgetWiAlti, row, 4, float(wiMax['observation']['value']))
                self.setFloatInQTableWidget(self.tableWidgetWiAlti, row, 5, round(float(wiMax['observation']['stdDev'])*1000,1))
                self.setFloatInQTableWidget(self.tableWidgetWiAlti, row, 6, round(float(wiMax['observation']['vi'])*1000,1))
                self.setFloatInQTableWidget(self.tableWidgetWiAlti, row, 7, float(wiMax['observation']['wi']))
                # mettre en évidence les wi > 3.5
                if abs(float(wiMax['observation']['wi'])) > 3.5:
                    font = QtGui.QFont()
                    font.setBold(True)
                    self.tableWidgetWiAlti.item(row, 7).setForeground(QtGui.QColor(255,0,0))
                    self.tableWidgetWiAlti.item(row, 7).setFont(font)
                    
                self.setFloatInQTableWidget(self.tableWidgetWiAlti, row, 8, float(wiMax['observation']['zi']))
                self.setFloatInQTableWidget(self.tableWidgetWiAlti, row, 9, round(float(wiMax['observation']['nablaLi'])*1000,1))
                self.setFloatInQTableWidget(self.tableWidgetWiAlti, row, 10,round(float(wiMax['observation']['gi'])*1000,1))
                
            
            
            #### ^---- LIBRE AJUSTE RATTACHEMENT
            
            if self.dictResGlobaux['results']['parameters']['computationOptions']['networkType'] == 'stochastic':
                
                # liste des balises <points> des pts de rattachement
                self.listeRattachAlti = self.dictResGlobaux['results']['parameters']['altimetricControlPoints']['point']
                self.tableWidgetRattachAlti.setRowCount(len(self.listeRattachAlti))
                for row, point in enumerate(self.listeRattachAlti): 
                    # On set les item dans la Table
                    self.setFloatInQTableWidget(self.tableWidgetRattachAlti, row, 0, point['pointName'])
                    self.setFloatInQTableWidget(self.tableWidgetRattachAlti, row, 1, float(point['HH']))
                    self.setFloatInQTableWidget(self.tableWidgetRattachAlti, row, 2, round(float(point['altiStdDev'])*1000,1))
                    # Indicateurs HH
                    self.setFloatInQTableWidget(self.tableWidgetRattachAlti, row, 3, round(float(point['indicateursHH']['vi'])*1000,1))
                    self.setFloatInQTableWidget(self.tableWidgetRattachAlti, row, 4, float(point['indicateursHH']['wi']))
                    # mettre en évidence les wi > 3.5
                    if abs(float(point['indicateursHH']['wi'])) > 3.5:
                        font = QtGui.QFont()
                        font.setBold(True)
                        self.tableWidgetRattachAlti.item(row, 4).setForeground(QtGui.QColor(255,0,0))
                        self.tableWidgetRattachAlti.item(row, 4).setFont(font)
                    self.setFloatInQTableWidget(self.tableWidgetRattachAlti, row, 5, float(point['indicateursHH']['zi']))
                    self.setFloatInQTableWidget(self.tableWidgetRattachAlti, row, 6, round(float(point['indicateursHH']['nablaLi'])*1000,1))
                    self.setFloatInQTableWidget(self.tableWidgetRattachAlti, row, 7, round(float(point['indicateursHH']['gi'])*1000,1))
                    
        
                
        # MESSAGE QUE LE FICHIER RES A ETE IMPORTE
        print('--- RESULTS FILE IMPORTED')
            
            
            
            
            
            
            
            
            
            
            
            
            # if self.dictResGlobaux['results']['parameters']['computationOptions']['networkType'] == 'stochastic':
                
            #     # liste des balises <points> des pts de rattachement
            #     self.listeRattachAlti = self.dictResGlobaux['results']['globalResults']['altimetry']['stochasticNetwork']['point']
            #     self.tableWidgetRattachAlti.setRowCount(len(self.listeRattachAlti))
            #     for row, point in enumerate(self.listeRattachAlti): 
            #         # On set les item dans la Table
            #         self.tableWidgetRattachAlti.setItem(row, 0, QtWidgets.QTableWidgetItem(point['pointName']))
            #         self.tableWidgetRattachAlti.setItem(row, 1, QtWidgets.QTableWidgetItem(point['HH']))
            #         self.tableWidgetRattachAlti.setItem(row, 2, QtWidgets.QTableWidgetItem(point['altiStdDev']))
            #         self.tableWidgetRattachAlti.setItem(row, 3, QtWidgets.QTableWidgetItem(point['indicateursHH']['vi']))
            #         self.tableWidgetRattachAlti.setItem(row, 4, QtWidgets.QTableWidgetItem(point['indicateursHH']['wi']))
            #         # mettre en évidence les wi > 3.5
            #         if abs(float(self.tableWidgetRattachAlti.item(row, 4).text())) > 3.5:
            #             font = QtGui.QFont()
            #             font.setBold(True)
            #             self.tableWidgetRattachAlti.item(row, 4).setForeground(QtGui.QColor(255,0,0))
            #             self.tableWidgetRattachAlti.item(row, 4).setFont(font)
            #         self.tableWidgetRattachAlti.setItem(row, 5, QtWidgets.QTableWidgetItem(point['indicateursHH']['zi']))
            #         self.tableWidgetRattachAlti.setItem(row, 6, QtWidgets.QTableWidgetItem(point['indicateursHH']['nablaLi']))
            #         self.tableWidgetRattachAlti.setItem(row, 7, QtWidgets.QTableWidgetItem(point['indicateursHH']['gi']))

            
            
        
        
        
        
        
