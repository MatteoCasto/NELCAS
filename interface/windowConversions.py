
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem, QStandardItemModel
import json
import xmltodict
from PyQt5 import uic
import libUtils.processUtils as processUtils
import libUtils.conversionUtils as conversionUtils
import os



class UI_ongletConversions(QtWidgets.QMainWindow):
    
    def __init__(self):
        
        super(UI_ongletConversions, self).__init__()
        # Charger le ui
        uic.loadUi(os.getcwd()+"\\interface\\OngletConversions.ui", self)
        
        
        # Connection des boutons
        # tab LTOP
        self.browseMesLTOP.clicked.connect(self.browseMesLTOPClicked)
        self.browseObsXml.clicked.connect(self.browseObsXmlClicked)
        self.runConversionLTOP2xml.clicked.connect(self.runConversionsMes2XmlClicked)
        
        self.browseKooLTOP.clicked.connect(self.browseKooLTOPClicked)
        self.browsePtsXML.clicked.connect(self.browsePtsXmlClicked)
        self.runConversionLTOP2xml_2.clicked.connect(self.runConversionsKoo2XmlClicked)
        
        # tab Homère
        self.browseConversionHomere.clicked.connect(self.browseConversionHomereClicked)
        self.browseHomToXmlPoints.clicked.connect(self.browseHomToXmlPointsClicked)
        self.browseHomToXmlObs.clicked.connect(self.browseHomToXmlObsClicked)
        self.runConversionHom2Xml.clicked.connect(self.runConversionsHom2XmlClicked)
        
        # tab XML vers CSV
        self.browsePtsXML_3.clicked.connect(self.browsePtsXML_3_clicked)
        self.browsePtsCSV.clicked.connect(self.browsePtsCSV_clicked)
        self.runConversionPtsXMLtoCSV.clicked.connect(self.runConversionPtsXMLtoCSV_clicked)
        
        
        # Afficher la fenêtre
        self.show()
        
    
    """
    ENSEMBLE DE FONCTION PERMETTANT DE SAISIR DES EMPLACEMENTS DES FICHIERS SUR LES QLineEdit.
    """     
    def browseMesLTOPClicked(self):
        try:
            file = QtWidgets.QFileDialog().getOpenFileName(None,"Sélection du fichier MESURES de LTOP", None, "*.mes; *.MES; *.me; *.ME")[0]
            self.inputMesLTOP.setText(file)
        except:
            return None
        
    def browseObsXmlClicked(self):
        try:
            file = QtWidgets.QFileDialog().getSaveFileName(None,'Fichier XML des observations après conversion', None, '*.xml')[0]
            self.outputObsXml.setText(file)
        except:
            return None
        
        
        
        
    def browseKooLTOPClicked(self):
        try:
            file = QtWidgets.QFileDialog().getOpenFileName(None,"Sélection du fichier COORDONNEES de LTOP", None, "*.coo; *.COO; *.koo; *.KOO; *.RES; *.res")[0]
            self.inputKooLTOP.setText(file)
        except:
            return None
    
    def browsePtsXmlClicked(self):
        try:
            file = QtWidgets.QFileDialog().getSaveFileName(None,'Fichier XML des points après conversion', None, '*.xml')[0]
            self.outputPtsXml.setText(file)
        except:
            return None
        
    def browseConversionHomereClicked(self):
        try:
            file = QtWidgets.QFileDialog().getOpenFileName(None,'Sélection du fichier résultats de Homère', None, '*.ll1')[0]
            self.inputResHomere.setText(file)
        except:
            return None
        
    def browseHomToXmlPointsClicked(self):
        try:
            file = QtWidgets.QFileDialog().getSaveFileName(None,'Fichier XML des points après conversion', None, '*.xml')[0]
            self.outputHomereToXmlPoints.setText(file)
        except:
            return None
        
    def browseHomToXmlObsClicked(self):
        try:
            file = QtWidgets.QFileDialog().getSaveFileName(None,'Fichier XML des points après conversion', None, '*.xml')[0]
            self.outputHomereToXmlObs.setText(file)
        except:
            return None
        
        
        
        
        
        
    def browsePtsXML_3_clicked(self):
        try:
            file = QtWidgets.QFileDialog().getOpenFileName(None,'Fichier XML des points en entrée', None, '*.xml')[0]
            self.inputXMLpts.setText(file)
        except:
            return None
        
    def browsePtsCSV_clicked(self):
        try:
            file = QtWidgets.QFileDialog().getSaveFileName(None,'Fichier CSV des points en sortie', None, '*.csv')[0]
            self.ouputPtsCSV.setText(file)
        except:
            return None
        
    
        
        
        
        
    
        

    def runConversionsMes2XmlClicked(self):
        """
        Fonction qui lance la conversion des mesures LTOP vers XML.
        """
        conversionUtils.LTOPMES2xml(self.inputMesLTOP.text(), self.outputObsXml.text())
        
    def runConversionsKoo2XmlClicked(self):
        """
        Fonction qui lance la conversion des points LTOP vers XML.
        """
        conversionUtils.LTOPKOO2xml(self.inputKooLTOP.text(), self.outputPtsXml.text())
        
    
    def runConversionsHom2XmlClicked(self):
        """
        Fonction qui lance la conversion des résultats Homère vers XML.
        """
        conversionUtils.points2xml(self.inputResHomere.text(), self.outputHomereToXmlPoints.text())
        dictPoints = conversionUtils.xml2dictionnaire(self.outputHomereToXmlPoints.text())# A besoin du dictpoints (nature et thème)
        conversionUtils.canevas2xml(self.inputResHomere.text(), self.outputHomereToXmlObs.text(), dictPoints)


    def runConversionPtsXMLtoCSV_clicked(self):
        """
        Fonction qui lance la conversion des points XML vers CSV
        """
        conversionUtils.pointsXMLtoCSV(self.inputXMLpts.text(), self.ouputPtsCSV.text())

            
            
        
        

        
    

        
        