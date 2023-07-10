# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 15:48:16 2022

@author: Matteo Casto, INSIT
"""


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem, QStandardItemModel
import json
import xmltodict
from PyQt5 import uic
import libUtils.processUtils as processUtils



class Ui_Prototype(object):
    def setupUi(self, Prototype):
        Prototype.setObjectName("Prototype")
        Prototype.resize(1222, 842)
        Prototype.setStyleSheet("font: 8pt \"MS Shell Dlg 2\";\n"
"")
        self.tabCoordApproch = QtWidgets.QTabWidget(Prototype)
        self.tabCoordApproch.setGeometry(QtCore.QRect(10, 10, 1171, 791))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tabCoordApproch.setFont(font)
        self.tabCoordApproch.setAutoFillBackground(True)
        self.tabCoordApproch.setObjectName("tabCoordApproch")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabCoordApproch.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabCoordApproch.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabCoordApproch.addTab(self.tab_3, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabCoordApproch.addTab(self.tab_5, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.label_127 = QtWidgets.QLabel(self.tab_4)
        self.label_127.setGeometry(QtCore.QRect(30, 80, 1061, 16))
        self.label_127.setObjectName("label_127")
        self.tabCoordApproch.addTab(self.tab_4, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.groupBox = QtWidgets.QGroupBox(self.tab_6)
        self.groupBox.setEnabled(True)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 261, 51))
        self.groupBox.setObjectName("groupBox")
        self.nomReseau = QtWidgets.QLineEdit(self.groupBox)
        self.nomReseau.setGeometry(QtCore.QRect(20, 20, 221, 20))
        self.nomReseau.setObjectName("nomReseau")
        self.importParam = QtWidgets.QPushButton(self.tab_6)
        self.importParam.setGeometry(QtCore.QRect(950, 10, 75, 23))
        self.importParam.setObjectName("importParam")
        self.exportParam = QtWidgets.QPushButton(self.tab_6)
        self.exportParam.setGeometry(QtCore.QRect(1040, 10, 75, 23))
        self.exportParam.setObjectName("exportParam")
        self.tabWidget = QtWidgets.QTabWidget(self.tab_6)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(10, 70, 1081, 671))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_9 = QtWidgets.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.label = QtWidgets.QLabel(self.tab_9)
        self.label.setGeometry(QtCore.QRect(30, 50, 91, 16))
        self.label.setObjectName("label")
        self.typeCalcul = QtWidgets.QComboBox(self.tab_9)
        self.typeCalcul.setGeometry(QtCore.QRect(200, 50, 91, 22))
        self.typeCalcul.setObjectName("typeCalcul")
        self.typeCalcul.addItem("")
        self.typeCalcul.addItem("")
        self.label_2 = QtWidgets.QLabel(self.tab_9)
        self.label_2.setGeometry(QtCore.QRect(30, 90, 91, 16))
        self.label_2.setObjectName("label_2")
        self.dimensionCalcul = QtWidgets.QComboBox(self.tab_9)
        self.dimensionCalcul.setGeometry(QtCore.QRect(200, 90, 91, 22))
        self.dimensionCalcul.setObjectName("dimensionCalcul")
        self.dimensionCalcul.addItem("")
        self.dimensionCalcul.addItem("")
        self.dimensionCalcul.addItem("")
        self.label_3 = QtWidgets.QLabel(self.tab_9)
        self.label_3.setGeometry(QtCore.QRect(30, 130, 141, 16))
        self.label_3.setObjectName("label_3")
        self.nbIterationsMax = QtWidgets.QSpinBox(self.tab_9)
        self.nbIterationsMax.setGeometry(QtCore.QRect(200, 130, 42, 22))
        self.nbIterationsMax.setProperty("value", 15)
        self.nbIterationsMax.setObjectName("nbIterationsMax")
        self.label_4 = QtWidgets.QLabel(self.tab_9)
        self.label_4.setGeometry(QtCore.QRect(30, 170, 171, 16))
        self.label_4.setObjectName("label_4")
        self.critereIterruption = QtWidgets.QDoubleSpinBox(self.tab_9)
        self.critereIterruption.setGeometry(QtCore.QRect(200, 170, 62, 22))
        self.critereIterruption.setDecimals(4)
        self.critereIterruption.setMaximum(100.0)
        self.critereIterruption.setSingleStep(0.001)
        self.critereIterruption.setProperty("value", 0.003)
        self.critereIterruption.setObjectName("critereIterruption")
        self.label_5 = QtWidgets.QLabel(self.tab_9)
        self.label_5.setGeometry(QtCore.QRect(30, 210, 171, 16))
        self.label_5.setObjectName("label_5")
        self.robuste = QtWidgets.QCheckBox(self.tab_9)
        self.robuste.setGeometry(QtCore.QRect(200, 210, 21, 17))
        self.robuste.setText("")
        self.robuste.setObjectName("robuste")
        self.label_6 = QtWidgets.QLabel(self.tab_9)
        self.label_6.setGeometry(QtCore.QRect(300, 210, 171, 16))
        self.label_6.setObjectName("label_6")
        self.cRobuste = QtWidgets.QDoubleSpinBox(self.tab_9)
        self.cRobuste.setGeometry(QtCore.QRect(400, 210, 62, 22))
        self.cRobuste.setDecimals(2)
        self.cRobuste.setMaximum(100.0)
        self.cRobuste.setSingleStep(0.1)
        self.cRobuste.setProperty("value", 3.5)
        self.cRobuste.setObjectName("cRobuste")
        self.label_7 = QtWidgets.QLabel(self.tab_9)
        self.label_7.setGeometry(QtCore.QRect(30, 250, 171, 16))
        self.label_7.setObjectName("label_7")
        self.refractionk = QtWidgets.QDoubleSpinBox(self.tab_9)
        self.refractionk.setGeometry(QtCore.QRect(200, 250, 62, 22))
        self.refractionk.setDecimals(3)
        self.refractionk.setMaximum(100.0)
        self.refractionk.setSingleStep(0.01)
        self.refractionk.setProperty("value", 0.13)
        self.refractionk.setObjectName("refractionk")
        self.label_8 = QtWidgets.QLabel(self.tab_9)
        self.label_8.setGeometry(QtCore.QRect(300, 250, 171, 16))
        self.label_8.setObjectName("label_8")
        self.sigmarefraction = QtWidgets.QDoubleSpinBox(self.tab_9)
        self.sigmarefraction.setGeometry(QtCore.QRect(400, 250, 62, 22))
        self.sigmarefraction.setDecimals(3)
        self.sigmarefraction.setMaximum(100.0)
        self.sigmarefraction.setSingleStep(0.005)
        self.sigmarefraction.setProperty("value", 0.02)
        self.sigmarefraction.setObjectName("sigmarefraction")
        self.tabWidget.addTab(self.tab_9, "")
        self.tab_10 = QtWidgets.QWidget()
        self.tab_10.setObjectName("tab_10")
        self.toolBox_2 = QtWidgets.QToolBox(self.tab_10)
        self.toolBox_2.setGeometry(QtCore.QRect(20, 20, 601, 581))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.toolBox_2.setFont(font)
        self.toolBox_2.setStyleSheet("")
        self.toolBox_2.setObjectName("toolBox_2")
        self.toolBox_2Page1 = QtWidgets.QWidget()
        self.toolBox_2Page1.setGeometry(QtCore.QRect(0, 0, 601, 473))
        self.toolBox_2Page1.setObjectName("toolBox_2Page1")
        self.groupBox_3 = QtWidgets.QGroupBox(self.toolBox_2Page1)
        self.groupBox_3.setGeometry(QtCore.QRect(21, 169, 549, 143))
        self.groupBox_3.setObjectName("groupBox_3")
        self.nomGroupeDirection = QtWidgets.QLineEdit(self.groupBox_3)
        self.nomGroupeDirection.setGeometry(QtCore.QRect(180, 30, 251, 20))
        self.nomGroupeDirection.setObjectName("nomGroupeDirection")
        self.label_14 = QtWidgets.QLabel(self.groupBox_3)
        self.label_14.setGeometry(QtCore.QRect(20, 30, 81, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.groupBox_3)
        self.label_15.setGeometry(QtCore.QRect(20, 60, 201, 16))
        self.label_15.setObjectName("label_15")
        self.sigmaRI = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        self.sigmaRI.setGeometry(QtCore.QRect(180, 60, 51, 22))
        self.sigmaRI.setDecimals(1)
        self.sigmaRI.setMaximum(100.0)
        self.sigmaRI.setSingleStep(1.0)
        self.sigmaRI.setProperty("value", 20.0)
        self.sigmaRI.setObjectName("sigmaRI")
        self.label_16 = QtWidgets.QLabel(self.groupBox_3)
        self.label_16.setGeometry(QtCore.QRect(240, 60, 31, 16))
        self.label_16.setObjectName("label_16")
        self.addGroupeDirection = QtWidgets.QPushButton(self.groupBox_3)
        self.addGroupeDirection.setGeometry(QtCore.QRect(460, 30, 75, 23))
        self.addGroupeDirection.setStyleSheet("font: 8pt \"MS Shell Dlg 2\";")
        self.addGroupeDirection.setObjectName("addGroupeDirection")
        self.label_17 = QtWidgets.QLabel(self.groupBox_3)
        self.label_17.setGeometry(QtCore.QRect(20, 90, 201, 16))
        self.label_17.setObjectName("label_17")
        self.sigmaZD = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        self.sigmaZD.setGeometry(QtCore.QRect(180, 90, 51, 22))
        self.sigmaZD.setDecimals(1)
        self.sigmaZD.setMaximum(100.0)
        self.sigmaZD.setSingleStep(1.0)
        self.sigmaZD.setProperty("value", 20.0)
        self.sigmaZD.setObjectName("sigmaZD")
        self.label_18 = QtWidgets.QLabel(self.groupBox_3)
        self.label_18.setGeometry(QtCore.QRect(240, 90, 31, 16))
        self.label_18.setObjectName("label_18")
        self.groupBox_4 = QtWidgets.QGroupBox(self.toolBox_2Page1)
        self.groupBox_4.setGeometry(QtCore.QRect(21, 318, 549, 142))
        self.groupBox_4.setObjectName("groupBox_4")
        self.nomGroupeCentrage = QtWidgets.QLineEdit(self.groupBox_4)
        self.nomGroupeCentrage.setGeometry(QtCore.QRect(180, 30, 251, 20))
        self.nomGroupeCentrage.setObjectName("nomGroupeCentrage")
        self.label_19 = QtWidgets.QLabel(self.groupBox_4)
        self.label_19.setGeometry(QtCore.QRect(20, 30, 81, 16))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.groupBox_4)
        self.label_20.setGeometry(QtCore.QRect(20, 80, 201, 16))
        self.label_20.setObjectName("label_20")
        self.sigmaCentStaPlani = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.sigmaCentStaPlani.setGeometry(QtCore.QRect(180, 80, 51, 22))
        self.sigmaCentStaPlani.setDecimals(1)
        self.sigmaCentStaPlani.setMaximum(100.0)
        self.sigmaCentStaPlani.setSingleStep(1.0)
        self.sigmaCentStaPlani.setProperty("value", 3.0)
        self.sigmaCentStaPlani.setObjectName("sigmaCentStaPlani")
        self.label_21 = QtWidgets.QLabel(self.groupBox_4)
        self.label_21.setGeometry(QtCore.QRect(240, 80, 31, 16))
        self.label_21.setObjectName("label_21")
        self.addGroupeCentrage = QtWidgets.QPushButton(self.groupBox_4)
        self.addGroupeCentrage.setGeometry(QtCore.QRect(460, 30, 75, 23))
        self.addGroupeCentrage.setStyleSheet("font: 8pt \"MS Shell Dlg 2\";")
        self.addGroupeCentrage.setObjectName("addGroupeCentrage")
        self.sigmaCentVisPlani = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.sigmaCentVisPlani.setGeometry(QtCore.QRect(180, 110, 51, 22))
        self.sigmaCentVisPlani.setDecimals(1)
        self.sigmaCentVisPlani.setMaximum(100.0)
        self.sigmaCentVisPlani.setSingleStep(1.0)
        self.sigmaCentVisPlani.setProperty("value", 5.0)
        self.sigmaCentVisPlani.setObjectName("sigmaCentVisPlani")
        self.label_23 = QtWidgets.QLabel(self.groupBox_4)
        self.label_23.setGeometry(QtCore.QRect(240, 110, 31, 16))
        self.label_23.setObjectName("label_23")
        self.label_22 = QtWidgets.QLabel(self.groupBox_4)
        self.label_22.setGeometry(QtCore.QRect(20, 110, 131, 16))
        self.label_22.setObjectName("label_22")
        self.label_51 = QtWidgets.QLabel(self.groupBox_4)
        self.label_51.setGeometry(QtCore.QRect(190, 60, 31, 16))
        self.label_51.setObjectName("label_51")
        self.label_52 = QtWidgets.QLabel(self.groupBox_4)
        self.label_52.setGeometry(QtCore.QRect(330, 60, 51, 20))
        self.label_52.setObjectName("label_52")
        self.sigmaCentStaAlti = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.sigmaCentStaAlti.setGeometry(QtCore.QRect(310, 80, 51, 22))
        self.sigmaCentStaAlti.setDecimals(1)
        self.sigmaCentStaAlti.setMaximum(100.0)
        self.sigmaCentStaAlti.setSingleStep(1.0)
        self.sigmaCentStaAlti.setProperty("value", 3.0)
        self.sigmaCentStaAlti.setObjectName("sigmaCentStaAlti")
        self.label_53 = QtWidgets.QLabel(self.groupBox_4)
        self.label_53.setGeometry(QtCore.QRect(370, 80, 31, 16))
        self.label_53.setObjectName("label_53")
        self.sigmaCentVisAlti = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.sigmaCentVisAlti.setGeometry(QtCore.QRect(310, 110, 51, 22))
        self.sigmaCentVisAlti.setDecimals(1)
        self.sigmaCentVisAlti.setMaximum(100.0)
        self.sigmaCentVisAlti.setSingleStep(1.0)
        self.sigmaCentVisAlti.setProperty("value", 5.0)
        self.sigmaCentVisAlti.setObjectName("sigmaCentVisAlti")
        self.label_54 = QtWidgets.QLabel(self.groupBox_4)
        self.label_54.setGeometry(QtCore.QRect(370, 110, 31, 16))
        self.label_54.setObjectName("label_54")
        self.groupBox_2 = QtWidgets.QGroupBox(self.toolBox_2Page1)
        self.groupBox_2.setGeometry(QtCore.QRect(21, 21, 549, 142))
        self.groupBox_2.setObjectName("groupBox_2")
        self.nomGroupeDistance = QtWidgets.QLineEdit(self.groupBox_2)
        self.nomGroupeDistance.setGeometry(QtCore.QRect(180, 30, 251, 20))
        self.nomGroupeDistance.setObjectName("nomGroupeDistance")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(20, 30, 81, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(20, 60, 201, 16))
        self.label_10.setObjectName("label_10")
        self.sigmaDSmm = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.sigmaDSmm.setGeometry(QtCore.QRect(180, 60, 51, 22))
        self.sigmaDSmm.setDecimals(1)
        self.sigmaDSmm.setMaximum(100.0)
        self.sigmaDSmm.setSingleStep(1.0)
        self.sigmaDSmm.setProperty("value", 3.0)
        self.sigmaDSmm.setObjectName("sigmaDSmm")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(240, 60, 31, 16))
        self.label_11.setObjectName("label_11")
        self.sigmaDSppm = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.sigmaDSppm.setGeometry(QtCore.QRect(310, 60, 51, 22))
        self.sigmaDSppm.setDecimals(1)
        self.sigmaDSppm.setMaximum(100.0)
        self.sigmaDSppm.setSingleStep(1.0)
        self.sigmaDSppm.setProperty("value", 2.0)
        self.sigmaDSppm.setObjectName("sigmaDSppm")
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(370, 60, 41, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.groupBox_2)
        self.label_13.setGeometry(QtCore.QRect(20, 90, 201, 16))
        self.label_13.setObjectName("label_13")
        self.addGroupeDistance = QtWidgets.QPushButton(self.groupBox_2)
        self.addGroupeDistance.setGeometry(QtCore.QRect(460, 30, 75, 23))
        self.addGroupeDistance.setStyleSheet("font: 8pt \"MS Shell Dlg 2\";")
        self.addGroupeDistance.setObjectName("addGroupeDistance")
        self.facteurEchelle = QtWidgets.QCheckBox(self.groupBox_2)
        self.facteurEchelle.setGeometry(QtCore.QRect(180, 90, 121, 17))
        self.facteurEchelle.setObjectName("facteurEchelle")
        self.constanteAddition = QtWidgets.QCheckBox(self.groupBox_2)
        self.constanteAddition.setGeometry(QtCore.QRect(310, 90, 141, 17))
        self.constanteAddition.setObjectName("constanteAddition")
        self.toolBox_2.addItem(self.toolBox_2Page1, "")
        self.toolBox_2Page2 = QtWidgets.QWidget()
        self.toolBox_2Page2.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.toolBox_2Page2.setObjectName("toolBox_2Page2")
        self.layoutWidget = QtWidgets.QWidget(self.toolBox_2Page2)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 561, 421))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_5 = QtWidgets.QGroupBox(self.layoutWidget)
        self.groupBox_5.setObjectName("groupBox_5")
        self.nomGroupeGNSS = QtWidgets.QLineEdit(self.groupBox_5)
        self.nomGroupeGNSS.setGeometry(QtCore.QRect(180, 30, 251, 20))
        self.nomGroupeGNSS.setObjectName("nomGroupeGNSS")
        self.label_24 = QtWidgets.QLabel(self.groupBox_5)
        self.label_24.setGeometry(QtCore.QRect(20, 30, 81, 16))
        self.label_24.setObjectName("label_24")
        self.label_25 = QtWidgets.QLabel(self.groupBox_5)
        self.label_25.setGeometry(QtCore.QRect(20, 60, 201, 16))
        self.label_25.setObjectName("label_25")
        self.GNSSsigmaLYLX = QtWidgets.QDoubleSpinBox(self.groupBox_5)
        self.GNSSsigmaLYLX.setGeometry(QtCore.QRect(180, 60, 51, 22))
        self.GNSSsigmaLYLX.setDecimals(1)
        self.GNSSsigmaLYLX.setMaximum(100.0)
        self.GNSSsigmaLYLX.setSingleStep(1.0)
        self.GNSSsigmaLYLX.setProperty("value", 15.0)
        self.GNSSsigmaLYLX.setObjectName("GNSSsigmaLYLX")
        self.label_26 = QtWidgets.QLabel(self.groupBox_5)
        self.label_26.setGeometry(QtCore.QRect(240, 60, 31, 16))
        self.label_26.setObjectName("label_26")
        self.label_28 = QtWidgets.QLabel(self.groupBox_5)
        self.label_28.setGeometry(QtCore.QRect(20, 130, 201, 16))
        self.label_28.setObjectName("label_28")
        self.addGroupeGNSS = QtWidgets.QPushButton(self.groupBox_5)
        self.addGroupeGNSS.setGeometry(QtCore.QRect(460, 30, 75, 23))
        self.addGroupeGNSS.setStyleSheet("font: 8pt \"MS Shell Dlg 2\";")
        self.addGroupeGNSS.setObjectName("addGroupeGNSS")
        self.GNSS_tE = QtWidgets.QCheckBox(self.groupBox_5)
        self.GNSS_tE.setGeometry(QtCore.QRect(180, 130, 131, 17))
        self.GNSS_tE.setObjectName("GNSS_tE")
        self.GNSS_tN = QtWidgets.QCheckBox(self.groupBox_5)
        self.GNSS_tN.setGeometry(QtCore.QRect(220, 130, 131, 17))
        self.GNSS_tN.setObjectName("GNSS_tN")
        self.label_29 = QtWidgets.QLabel(self.groupBox_5)
        self.label_29.setGeometry(QtCore.QRect(20, 90, 201, 16))
        self.label_29.setObjectName("label_29")
        self.GNSSsigmaLH = QtWidgets.QDoubleSpinBox(self.groupBox_5)
        self.GNSSsigmaLH.setGeometry(QtCore.QRect(180, 90, 51, 22))
        self.GNSSsigmaLH.setDecimals(1)
        self.GNSSsigmaLH.setMaximum(100.0)
        self.GNSSsigmaLH.setSingleStep(1.0)
        self.GNSSsigmaLH.setProperty("value", 30.0)
        self.GNSSsigmaLH.setObjectName("GNSSsigmaLH")
        self.label_27 = QtWidgets.QLabel(self.groupBox_5)
        self.label_27.setGeometry(QtCore.QRect(240, 90, 31, 16))
        self.label_27.setObjectName("label_27")
        self.GNSS_tH = QtWidgets.QCheckBox(self.groupBox_5)
        self.GNSS_tH.setGeometry(QtCore.QRect(260, 130, 131, 17))
        self.GNSS_tH.setObjectName("GNSS_tH")
        self.GNSS_rotHz = QtWidgets.QCheckBox(self.groupBox_5)
        self.GNSS_rotHz.setGeometry(QtCore.QRect(300, 130, 131, 17))
        self.GNSS_rotHz.setObjectName("GNSS_rotHz")
        self.GNSS_factEchHz = QtWidgets.QCheckBox(self.groupBox_5)
        self.GNSS_factEchHz.setGeometry(QtCore.QRect(360, 130, 131, 17))
        self.GNSS_factEchHz.setObjectName("GNSS_factEchHz")
        self.gridLayout_2.addWidget(self.groupBox_5, 0, 0, 1, 1)
        self.label_42 = QtWidgets.QLabel(self.layoutWidget)
        self.label_42.setObjectName("label_42")
        self.gridLayout_2.addWidget(self.label_42, 1, 0, 1, 1)
        self.toolBox_2.addItem(self.toolBox_2Page2, "")
        self.toolBox_2Page3 = QtWidgets.QWidget()
        self.toolBox_2Page3.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.toolBox_2Page3.setObjectName("toolBox_2Page3")
        self.layoutWidget1 = QtWidgets.QWidget(self.toolBox_2Page3)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 20, 561, 421))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_6 = QtWidgets.QGroupBox(self.layoutWidget1)
        self.groupBox_6.setObjectName("groupBox_6")
        self.nomGroupeSystemeLocal = QtWidgets.QLineEdit(self.groupBox_6)
        self.nomGroupeSystemeLocal.setGeometry(QtCore.QRect(180, 30, 251, 20))
        self.nomGroupeSystemeLocal.setObjectName("nomGroupeSystemeLocal")
        self.label_30 = QtWidgets.QLabel(self.groupBox_6)
        self.label_30.setGeometry(QtCore.QRect(20, 30, 81, 16))
        self.label_30.setObjectName("label_30")
        self.label_31 = QtWidgets.QLabel(self.groupBox_6)
        self.label_31.setGeometry(QtCore.QRect(20, 60, 201, 16))
        self.label_31.setObjectName("label_31")
        self.systemeLocalSigmaLYLX = QtWidgets.QDoubleSpinBox(self.groupBox_6)
        self.systemeLocalSigmaLYLX.setGeometry(QtCore.QRect(180, 60, 51, 22))
        self.systemeLocalSigmaLYLX.setDecimals(1)
        self.systemeLocalSigmaLYLX.setMaximum(100.0)
        self.systemeLocalSigmaLYLX.setSingleStep(1.0)
        self.systemeLocalSigmaLYLX.setProperty("value", 15.0)
        self.systemeLocalSigmaLYLX.setObjectName("systemeLocalSigmaLYLX")
        self.label_32 = QtWidgets.QLabel(self.groupBox_6)
        self.label_32.setGeometry(QtCore.QRect(240, 60, 31, 16))
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(self.groupBox_6)
        self.label_33.setGeometry(QtCore.QRect(20, 130, 201, 16))
        self.label_33.setObjectName("label_33")
        self.addGroupeSystemeLocal = QtWidgets.QPushButton(self.groupBox_6)
        self.addGroupeSystemeLocal.setGeometry(QtCore.QRect(460, 30, 75, 23))
        self.addGroupeSystemeLocal.setStyleSheet("font: 8pt \"MS Shell Dlg 2\";")
        self.addGroupeSystemeLocal.setObjectName("addGroupeSystemeLocal")
        self.systemeLocal_tE = QtWidgets.QCheckBox(self.groupBox_6)
        self.systemeLocal_tE.setEnabled(False)
        self.systemeLocal_tE.setGeometry(QtCore.QRect(180, 130, 131, 17))
        self.systemeLocal_tE.setChecked(True)
        self.systemeLocal_tE.setObjectName("systemeLocal_tE")
        self.systemeLocal_tN = QtWidgets.QCheckBox(self.groupBox_6)
        self.systemeLocal_tN.setEnabled(False)
        self.systemeLocal_tN.setGeometry(QtCore.QRect(220, 130, 131, 17))
        self.systemeLocal_tN.setChecked(True)
        self.systemeLocal_tN.setObjectName("systemeLocal_tN")
        self.label_34 = QtWidgets.QLabel(self.groupBox_6)
        self.label_34.setEnabled(False)
        self.label_34.setGeometry(QtCore.QRect(20, 90, 201, 16))
        self.label_34.setObjectName("label_34")
        self.systemeLocalSigmaLH = QtWidgets.QDoubleSpinBox(self.groupBox_6)
        self.systemeLocalSigmaLH.setEnabled(False)
        self.systemeLocalSigmaLH.setGeometry(QtCore.QRect(180, 90, 51, 22))
        self.systemeLocalSigmaLH.setDecimals(1)
        self.systemeLocalSigmaLH.setMaximum(100.0)
        self.systemeLocalSigmaLH.setSingleStep(1.0)
        self.systemeLocalSigmaLH.setProperty("value", 30.0)
        self.systemeLocalSigmaLH.setObjectName("systemeLocalSigmaLH")
        self.label_35 = QtWidgets.QLabel(self.groupBox_6)
        self.label_35.setEnabled(False)
        self.label_35.setGeometry(QtCore.QRect(240, 90, 31, 16))
        self.label_35.setObjectName("label_35")
        self.systemeLocal_tH = QtWidgets.QCheckBox(self.groupBox_6)
        self.systemeLocal_tH.setEnabled(False)
        self.systemeLocal_tH.setGeometry(QtCore.QRect(260, 130, 131, 17))
        self.systemeLocal_tH.setObjectName("systemeLocal_tH")
        self.systemeLocal_rotHz = QtWidgets.QCheckBox(self.groupBox_6)
        self.systemeLocal_rotHz.setEnabled(False)
        self.systemeLocal_rotHz.setGeometry(QtCore.QRect(300, 130, 131, 17))
        self.systemeLocal_rotHz.setTabletTracking(False)
        self.systemeLocal_rotHz.setChecked(True)
        self.systemeLocal_rotHz.setObjectName("systemeLocal_rotHz")
        self.systemeLocal_factEchHz = QtWidgets.QCheckBox(self.groupBox_6)
        self.systemeLocal_factEchHz.setEnabled(True)
        self.systemeLocal_factEchHz.setGeometry(QtCore.QRect(360, 130, 131, 17))
        self.systemeLocal_factEchHz.setObjectName("systemeLocal_factEchHz")
        self.gridLayout_3.addWidget(self.groupBox_6, 0, 0, 1, 1)
        self.label_43 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_43.setObjectName("label_43")
        self.gridLayout_3.addWidget(self.label_43, 1, 0, 1, 1)
        self.toolBox_2.addItem(self.toolBox_2Page3, "")
        self.toolBox_2Page4 = QtWidgets.QWidget()
        self.toolBox_2Page4.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.toolBox_2Page4.setObjectName("toolBox_2Page4")
        self.layoutWidget2 = QtWidgets.QWidget(self.toolBox_2Page4)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 20, 571, 441))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox_7 = QtWidgets.QGroupBox(self.layoutWidget2)
        self.groupBox_7.setObjectName("groupBox_7")
        self.nomGroupeCote = QtWidgets.QLineEdit(self.groupBox_7)
        self.nomGroupeCote.setGeometry(QtCore.QRect(180, 30, 251, 20))
        self.nomGroupeCote.setObjectName("nomGroupeCote")
        self.label_36 = QtWidgets.QLabel(self.groupBox_7)
        self.label_36.setGeometry(QtCore.QRect(20, 30, 81, 16))
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self.groupBox_7)
        self.label_37.setGeometry(QtCore.QRect(20, 60, 201, 16))
        self.label_37.setObjectName("label_37")
        self.coteSigmaDP = QtWidgets.QDoubleSpinBox(self.groupBox_7)
        self.coteSigmaDP.setGeometry(QtCore.QRect(180, 60, 51, 22))
        self.coteSigmaDP.setDecimals(1)
        self.coteSigmaDP.setMaximum(100.0)
        self.coteSigmaDP.setSingleStep(1.0)
        self.coteSigmaDP.setProperty("value", 15.0)
        self.coteSigmaDP.setObjectName("coteSigmaDP")
        self.label_38 = QtWidgets.QLabel(self.groupBox_7)
        self.label_38.setGeometry(QtCore.QRect(240, 60, 31, 16))
        self.label_38.setObjectName("label_38")
        self.addGroupeCote = QtWidgets.QPushButton(self.groupBox_7)
        self.addGroupeCote.setGeometry(QtCore.QRect(460, 32, 75, 21))
        self.addGroupeCote.setStyleSheet("font: 8pt \"MS Shell Dlg 2\";")
        self.addGroupeCote.setObjectName("addGroupeCote")
        self.label_39 = QtWidgets.QLabel(self.groupBox_7)
        self.label_39.setEnabled(False)
        self.label_39.setGeometry(QtCore.QRect(20, 90, 201, 16))
        self.label_39.setObjectName("label_39")
        self.coteSigmaDH = QtWidgets.QDoubleSpinBox(self.groupBox_7)
        self.coteSigmaDH.setEnabled(False)
        self.coteSigmaDH.setGeometry(QtCore.QRect(180, 90, 51, 22))
        self.coteSigmaDH.setDecimals(1)
        self.coteSigmaDH.setMaximum(100.0)
        self.coteSigmaDH.setSingleStep(1.0)
        self.coteSigmaDH.setProperty("value", 15.0)
        self.coteSigmaDH.setObjectName("coteSigmaDH")
        self.label_40 = QtWidgets.QLabel(self.groupBox_7)
        self.label_40.setEnabled(False)
        self.label_40.setGeometry(QtCore.QRect(240, 90, 31, 16))
        self.label_40.setObjectName("label_40")
        self.gridLayout_4.addWidget(self.groupBox_7, 0, 0, 1, 1)
        self.label_50 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_50.setObjectName("label_50")
        self.gridLayout_4.addWidget(self.label_50, 1, 0, 1, 1)
        self.toolBox_2.addItem(self.toolBox_2Page4, "")
        self.treeViewGroupes = QtWidgets.QTreeView(self.tab_10)
        self.treeViewGroupes.setGeometry(QtCore.QRect(640, 50, 411, 551))
        self.treeViewGroupes.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.treeViewGroupes.setObjectName("treeViewGroupes")
        self.suppGroupe = QtWidgets.QPushButton(self.tab_10)
        self.suppGroupe.setGeometry(QtCore.QRect(890, 22, 161, 21))
        self.suppGroupe.setStyleSheet("font: 8pt \"MS Shell Dlg 2\" ")
        self.suppGroupe.setObjectName("suppGroupe")
        self.tabWidget.addTab(self.tab_10, "")
        self.tab_11 = QtWidgets.QWidget()
        self.tab_11.setObjectName("tab_11")
        self.groupBox_8 = QtWidgets.QGroupBox(self.tab_11)
        self.groupBox_8.setGeometry(QtCore.QRect(20, 40, 701, 221))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.groupBox_8.setFont(font)
        self.groupBox_8.setObjectName("groupBox_8")
        self.label_46 = QtWidgets.QLabel(self.groupBox_8)
        self.label_46.setGeometry(QtCore.QRect(20, 60, 201, 16))
        self.label_46.setObjectName("label_46")
        self.planiNumeroPoint = QtWidgets.QLineEdit(self.groupBox_8)
        self.planiNumeroPoint.setGeometry(QtCore.QRect(110, 30, 161, 20))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.planiNumeroPoint.setFont(font)
        self.planiNumeroPoint.setObjectName("planiNumeroPoint")
        self.label_45 = QtWidgets.QLabel(self.groupBox_8)
        self.label_45.setGeometry(QtCore.QRect(230, 60, 31, 16))
        self.label_45.setObjectName("label_45")
        self.planiEcartTypePoint = QtWidgets.QDoubleSpinBox(self.groupBox_8)
        self.planiEcartTypePoint.setGeometry(QtCore.QRect(170, 60, 51, 22))
        self.planiEcartTypePoint.setDecimals(1)
        self.planiEcartTypePoint.setMaximum(100.0)
        self.planiEcartTypePoint.setSingleStep(1.0)
        self.planiEcartTypePoint.setProperty("value", 15.0)
        self.planiEcartTypePoint.setObjectName("planiEcartTypePoint")
        self.label_41 = QtWidgets.QLabel(self.groupBox_8)
        self.label_41.setGeometry(QtCore.QRect(20, 30, 81, 16))
        self.label_41.setObjectName("label_41")
        self.addPlaniPoint = QtWidgets.QPushButton(self.groupBox_8)
        self.addPlaniPoint.setGeometry(QtCore.QRect(290, 30, 75, 23))
        self.addPlaniPoint.setObjectName("addPlaniPoint")
        self.treeViewDatumPlani = QtWidgets.QTreeView(self.groupBox_8)
        self.treeViewDatumPlani.setGeometry(QtCore.QRect(390, 20, 291, 191))
        self.treeViewDatumPlani.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeViewDatumPlani.setObjectName("treeViewDatumPlani")
        self.suppPFplani = QtWidgets.QPushButton(self.groupBox_8)
        self.suppPFplani.setGeometry(QtCore.QRect(240, 190, 141, 21))
        self.suppPFplani.setStyleSheet("font: 8pt \"MS Shell Dlg 2\" ")
        self.suppPFplani.setObjectName("suppPFplani")
        self.groupBox_9 = QtWidgets.QGroupBox(self.tab_11)
        self.groupBox_9.setGeometry(QtCore.QRect(20, 280, 701, 221))
        self.groupBox_9.setObjectName("groupBox_9")
        self.label_47 = QtWidgets.QLabel(self.groupBox_9)
        self.label_47.setGeometry(QtCore.QRect(20, 60, 201, 16))
        self.label_47.setObjectName("label_47")
        self.altiNumeroPoint = QtWidgets.QLineEdit(self.groupBox_9)
        self.altiNumeroPoint.setGeometry(QtCore.QRect(110, 30, 161, 20))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.altiNumeroPoint.setFont(font)
        self.altiNumeroPoint.setObjectName("altiNumeroPoint")
        self.label_48 = QtWidgets.QLabel(self.groupBox_9)
        self.label_48.setGeometry(QtCore.QRect(230, 60, 31, 16))
        self.label_48.setObjectName("label_48")
        self.altiEcartTypePoint = QtWidgets.QDoubleSpinBox(self.groupBox_9)
        self.altiEcartTypePoint.setGeometry(QtCore.QRect(170, 60, 51, 22))
        self.altiEcartTypePoint.setDecimals(1)
        self.altiEcartTypePoint.setMaximum(100.0)
        self.altiEcartTypePoint.setSingleStep(1.0)
        self.altiEcartTypePoint.setProperty("value", 30.0)
        self.altiEcartTypePoint.setObjectName("altiEcartTypePoint")
        self.label_49 = QtWidgets.QLabel(self.groupBox_9)
        self.label_49.setGeometry(QtCore.QRect(20, 30, 81, 16))
        self.label_49.setObjectName("label_49")
        self.addAltiPoint = QtWidgets.QPushButton(self.groupBox_9)
        self.addAltiPoint.setGeometry(QtCore.QRect(290, 30, 75, 23))
        self.addAltiPoint.setObjectName("addAltiPoint")
        self.treeViewDatumAlti = QtWidgets.QTreeView(self.groupBox_9)
        self.treeViewDatumAlti.setGeometry(QtCore.QRect(390, 20, 291, 191))
        self.treeViewDatumAlti.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeViewDatumAlti.setObjectName("treeViewDatumAlti")
        self.suppPFalti = QtWidgets.QPushButton(self.groupBox_9)
        self.suppPFalti.setGeometry(QtCore.QRect(240, 190, 141, 21))
        self.suppPFalti.setStyleSheet("font: 8pt \"MS Shell Dlg 2\" ")
        self.suppPFalti.setObjectName("suppPFalti")
        self.tabWidget.addTab(self.tab_11, "")
        self.label_44 = QtWidgets.QLabel(self.tab_6)
        self.label_44.setGeometry(QtCore.QRect(450, 10, 321, 61))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_44.setFont(font)
        self.label_44.setObjectName("label_44")
        self.tabCoordApproch.addTab(self.tab_6, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.label_55 = QtWidgets.QLabel(self.tab_7)
        self.label_55.setGeometry(QtCore.QRect(450, 10, 151, 61))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_55.setFont(font)
        self.label_55.setObjectName("label_55")
        self.widget = QtWidgets.QWidget(self.tab_7)
        self.widget.setGeometry(QtCore.QRect(140, 93, 851, 191))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_66 = QtWidgets.QLabel(self.widget)
        self.label_66.setObjectName("label_66")
        self.gridLayout_5.addWidget(self.label_66, 0, 0, 1, 1)
        self.pathObs = QtWidgets.QLineEdit(self.widget)
        self.pathObs.setObjectName("pathObs")
        self.gridLayout_5.addWidget(self.pathObs, 0, 1, 1, 1)
        self.parcourirObs = QtWidgets.QPushButton(self.widget)
        self.parcourirObs.setObjectName("parcourirObs")
        self.gridLayout_5.addWidget(self.parcourirObs, 0, 2, 1, 1)
        self.label_67 = QtWidgets.QLabel(self.widget)
        self.label_67.setObjectName("label_67")
        self.gridLayout_5.addWidget(self.label_67, 1, 0, 1, 1)
        self.pathPoints = QtWidgets.QLineEdit(self.widget)
        self.pathPoints.setObjectName("pathPoints")
        self.gridLayout_5.addWidget(self.pathPoints, 1, 1, 1, 1)
        self.parcourirPoints = QtWidgets.QPushButton(self.widget)
        self.parcourirPoints.setObjectName("parcourirPoints")
        self.gridLayout_5.addWidget(self.parcourirPoints, 1, 2, 1, 1)
        self.label_68 = QtWidgets.QLabel(self.widget)
        self.label_68.setObjectName("label_68")
        self.gridLayout_5.addWidget(self.label_68, 2, 0, 1, 1)
        self.pathParam = QtWidgets.QLineEdit(self.widget)
        self.pathParam.setObjectName("pathParam")
        self.gridLayout_5.addWidget(self.pathParam, 2, 1, 1, 1)
        self.parcourirParam = QtWidgets.QPushButton(self.widget)
        self.parcourirParam.setObjectName("parcourirParam")
        self.gridLayout_5.addWidget(self.parcourirParam, 2, 2, 1, 1)
        self.label_69 = QtWidgets.QLabel(self.widget)
        self.label_69.setObjectName("label_69")
        self.gridLayout_5.addWidget(self.label_69, 3, 0, 1, 1)
        self.resDirPath = QtWidgets.QLineEdit(self.widget)
        self.resDirPath.setObjectName("resDirPath")
        self.gridLayout_5.addWidget(self.resDirPath, 3, 1, 1, 1)
        self.parcourirRes = QtWidgets.QPushButton(self.widget)
        self.parcourirRes.setObjectName("parcourirRes")
        self.gridLayout_5.addWidget(self.parcourirRes, 3, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_5)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        spacerItem = QtWidgets.QSpacerItem(78, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem, 1, 2, 2, 1)
        spacerItem1 = QtWidgets.QSpacerItem(78, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem1, 1, 0, 2, 1)
        self.runCalcul = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runCalcul.sizePolicy().hasHeightForWidth())
        self.runCalcul.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.runCalcul.setFont(font)
        self.runCalcul.setAutoFillBackground(False)
        self.runCalcul.setStyleSheet("background-color: rgb(0, 218, 160);\n"
"border-color: rgb(0, 0, 0);")
        self.runCalcul.setObjectName("runCalcul")
        self.gridLayout_6.addWidget(self.runCalcul, 2, 1, 1, 1)
        self.checkBoxCtrlCoh = QtWidgets.QCheckBox(self.widget)
        self.checkBoxCtrlCoh.setChecked(True)
        self.checkBoxCtrlCoh.setObjectName("checkBoxCtrlCoh")
        self.gridLayout_6.addWidget(self.checkBoxCtrlCoh, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem2, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_6)
        self.tabCoordApproch.addTab(self.tab_7, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab_8)
        self.tabWidget_2.setGeometry(QtCore.QRect(10, 30, 1101, 731))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_27 = QtWidgets.QWidget()
        self.tab_27.setObjectName("tab_27")
        self.widget1 = QtWidgets.QWidget(self.tab_27)
        self.widget1.setGeometry(QtCore.QRect(20, 20, 311, 321))
        self.widget1.setObjectName("widget1")
        self.gridLayout = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_57 = QtWidgets.QLabel(self.widget1)
        self.label_57.setObjectName("label_57")
        self.gridLayout.addWidget(self.label_57, 0, 0, 1, 1)
        self.RES_nomReseau = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.RES_nomReseau.setFont(font)
        self.RES_nomReseau.setObjectName("RES_nomReseau")
        self.gridLayout.addWidget(self.RES_nomReseau, 0, 1, 1, 1)
        self.label_56 = QtWidgets.QLabel(self.widget1)
        self.label_56.setObjectName("label_56")
        self.gridLayout.addWidget(self.label_56, 1, 0, 1, 1)
        self.RES_date = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.RES_date.setFont(font)
        self.RES_date.setObjectName("RES_date")
        self.gridLayout.addWidget(self.RES_date, 1, 1, 1, 1)
        self.label_58 = QtWidgets.QLabel(self.widget1)
        self.label_58.setObjectName("label_58")
        self.gridLayout.addWidget(self.label_58, 2, 0, 1, 1)
        self.RES_heure = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.RES_heure.setFont(font)
        self.RES_heure.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.RES_heure.setObjectName("RES_heure")
        self.gridLayout.addWidget(self.RES_heure, 2, 1, 1, 1)
        self.label_59 = QtWidgets.QLabel(self.widget1)
        self.label_59.setObjectName("label_59")
        self.gridLayout.addWidget(self.label_59, 3, 0, 1, 1)
        self.RES_typeReseau = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.RES_typeReseau.setFont(font)
        self.RES_typeReseau.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.RES_typeReseau.setObjectName("RES_typeReseau")
        self.gridLayout.addWidget(self.RES_typeReseau, 3, 1, 1, 1)
        self.label_60 = QtWidgets.QLabel(self.widget1)
        self.label_60.setObjectName("label_60")
        self.gridLayout.addWidget(self.label_60, 4, 0, 1, 1)
        self.RES_dimension = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.RES_dimension.setFont(font)
        self.RES_dimension.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.RES_dimension.setObjectName("RES_dimension")
        self.gridLayout.addWidget(self.RES_dimension, 4, 1, 1, 1)
        self.label_61 = QtWidgets.QLabel(self.widget1)
        self.label_61.setObjectName("label_61")
        self.gridLayout.addWidget(self.label_61, 5, 0, 1, 1)
        self.RES_robuste = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.RES_robuste.setFont(font)
        self.RES_robuste.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.RES_robuste.setObjectName("RES_robuste")
        self.gridLayout.addWidget(self.RES_robuste, 5, 1, 1, 1)
        self.label_62 = QtWidgets.QLabel(self.widget1)
        self.label_62.setObjectName("label_62")
        self.gridLayout.addWidget(self.label_62, 6, 0, 1, 1)
        self.RES_limiteRobuste = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.RES_limiteRobuste.setFont(font)
        self.RES_limiteRobuste.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.RES_limiteRobuste.setObjectName("RES_limiteRobuste")
        self.gridLayout.addWidget(self.RES_limiteRobuste, 6, 1, 1, 1)
        self.label_63 = QtWidgets.QLabel(self.widget1)
        self.label_63.setObjectName("label_63")
        self.gridLayout.addWidget(self.label_63, 7, 0, 1, 1)
        self.RES_refractionk = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.RES_refractionk.setFont(font)
        self.RES_refractionk.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.RES_refractionk.setObjectName("RES_refractionk")
        self.gridLayout.addWidget(self.RES_refractionk, 7, 1, 1, 1)
        self.label_64 = QtWidgets.QLabel(self.widget1)
        self.label_64.setObjectName("label_64")
        self.gridLayout.addWidget(self.label_64, 8, 0, 1, 1)
        self.RES_sigmak = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.RES_sigmak.setFont(font)
        self.RES_sigmak.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.RES_sigmak.setObjectName("RES_sigmak")
        self.gridLayout.addWidget(self.RES_sigmak, 8, 1, 1, 1)
        self.tabWidget_2.addTab(self.tab_27, "")
        self.tab_12 = QtWidgets.QWidget()
        self.tab_12.setObjectName("tab_12")
        self.groupBox_10 = QtWidgets.QGroupBox(self.tab_12)
        self.groupBox_10.setGeometry(QtCore.QRect(21, 31, 342, 101))
        self.groupBox_10.setObjectName("groupBox_10")
        self.widget2 = QtWidgets.QWidget(self.groupBox_10)
        self.widget2.setGeometry(QtCore.QRect(10, 20, 301, 61))
        self.widget2.setObjectName("widget2")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.widget2)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.RES_PLANI_nb_iteration = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.RES_PLANI_nb_iteration.setFont(font)
        self.RES_PLANI_nb_iteration.setObjectName("RES_PLANI_nb_iteration")
        self.gridLayout_8.addWidget(self.RES_PLANI_nb_iteration, 1, 1, 1, 1)
        self.label_130 = QtWidgets.QLabel(self.widget2)
        self.label_130.setObjectName("label_130")
        self.gridLayout_8.addWidget(self.label_130, 0, 0, 1, 1)
        self.RES_PLANI_duree = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.RES_PLANI_duree.setFont(font)
        self.RES_PLANI_duree.setObjectName("RES_PLANI_duree")
        self.gridLayout_8.addWidget(self.RES_PLANI_duree, 0, 1, 1, 1)
        self.label_131 = QtWidgets.QLabel(self.widget2)
        self.label_131.setObjectName("label_131")
        self.gridLayout_8.addWidget(self.label_131, 1, 0, 1, 1)
        self.groupBox_21 = QtWidgets.QGroupBox(self.tab_12)
        self.groupBox_21.setGeometry(QtCore.QRect(20, 290, 343, 181))
        self.groupBox_21.setObjectName("groupBox_21")
        self.RES_PLANI_treeViewQuotientsPlani = QtWidgets.QTreeView(self.groupBox_21)
        self.RES_PLANI_treeViewQuotientsPlani.setEnabled(True)
        self.RES_PLANI_treeViewQuotientsPlani.setGeometry(QtCore.QRect(10, 30, 321, 141))
        self.RES_PLANI_treeViewQuotientsPlani.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.RES_PLANI_treeViewQuotientsPlani.setIndentation(0)
        self.RES_PLANI_treeViewQuotientsPlani.setObjectName("RES_PLANI_treeViewQuotientsPlani")
        self.groupBox_23 = QtWidgets.QGroupBox(self.tab_12)
        self.groupBox_23.setGeometry(QtCore.QRect(20, 480, 342, 212))
        self.groupBox_23.setObjectName("groupBox_23")
        self.RES_PLANI_treeViewIncSupplDist = QtWidgets.QTreeView(self.groupBox_23)
        self.RES_PLANI_treeViewIncSupplDist.setGeometry(QtCore.QRect(10, 30, 321, 171))
        self.RES_PLANI_treeViewIncSupplDist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.RES_PLANI_treeViewIncSupplDist.setObjectName("RES_PLANI_treeViewIncSupplDist")
        self.groupBox_24 = QtWidgets.QGroupBox(self.tab_12)
        self.groupBox_24.setGeometry(QtCore.QRect(20, 140, 342, 141))
        self.groupBox_24.setObjectName("groupBox_24")
        self.widget_4 = QtWidgets.QWidget(self.groupBox_24)
        self.widget_4.setGeometry(QtCore.QRect(10, 20, 301, 111))
        self.widget_4.setObjectName("widget_4")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.widget_4)
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.RES_PLANI_obs = QtWidgets.QLabel(self.widget_4)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.RES_PLANI_obs.setFont(font)
        self.RES_PLANI_obs.setObjectName("RES_PLANI_obs")
        self.gridLayout_11.addWidget(self.RES_PLANI_obs, 1, 1, 1, 1)
        self.label_132 = QtWidgets.QLabel(self.widget_4)
        self.label_132.setObjectName("label_132")
        self.gridLayout_11.addWidget(self.label_132, 0, 0, 1, 1)
        self.RES_PLANI_inc = QtWidgets.QLabel(self.widget_4)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.RES_PLANI_inc.setFont(font)
        self.RES_PLANI_inc.setObjectName("RES_PLANI_inc")
        self.gridLayout_11.addWidget(self.RES_PLANI_inc, 0, 1, 1, 1)
        self.label_133 = QtWidgets.QLabel(self.widget_4)
        self.label_133.setObjectName("label_133")
        self.gridLayout_11.addWidget(self.label_133, 1, 0, 1, 1)
        self.label_134 = QtWidgets.QLabel(self.widget_4)
        self.label_134.setObjectName("label_134")
        self.gridLayout_11.addWidget(self.label_134, 2, 0, 1, 1)
        self.label_135 = QtWidgets.QLabel(self.widget_4)
        self.label_135.setObjectName("label_135")
        self.gridLayout_11.addWidget(self.label_135, 3, 0, 1, 1)
        self.RES_PLANI_contr = QtWidgets.QLabel(self.widget_4)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.RES_PLANI_contr.setFont(font)
        self.RES_PLANI_contr.setObjectName("RES_PLANI_contr")
        self.gridLayout_11.addWidget(self.RES_PLANI_contr, 2, 1, 1, 1)
        self.RES_PLANI_surabondance = QtWidgets.QLabel(self.widget_4)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.RES_PLANI_surabondance.setFont(font)
        self.RES_PLANI_surabondance.setObjectName("RES_PLANI_surabondance")
        self.gridLayout_11.addWidget(self.RES_PLANI_surabondance, 3, 1, 1, 1)
        self.groupBox_25 = QtWidgets.QGroupBox(self.tab_12)
        self.groupBox_25.setGeometry(QtCore.QRect(380, 30, 361, 661))
        self.groupBox_25.setObjectName("groupBox_25")
        self.layoutWidget3 = QtWidgets.QWidget(self.groupBox_25)
        self.layoutWidget3.setGeometry(QtCore.QRect(10, 30, 341, 621))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.layoutWidget3)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.RES_PLANI_WiMax = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.RES_PLANI_WiMax.setFont(font)
        self.RES_PLANI_WiMax.setObjectName("RES_PLANI_WiMax")
        self.gridLayout_9.addWidget(self.RES_PLANI_WiMax, 0, 1, 1, 1)
        self.label_136 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_136.setObjectName("label_136")
        self.gridLayout_9.addWidget(self.label_136, 0, 0, 1, 1)
        self.label_137 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_137.setObjectName("label_137")
        self.gridLayout_9.addWidget(self.label_137, 1, 0, 1, 2)
        self.RES_PLANI_treeView5wiMax = QtWidgets.QTreeView(self.layoutWidget3)
        self.RES_PLANI_treeView5wiMax.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.RES_PLANI_treeView5wiMax.setObjectName("RES_PLANI_treeView5wiMax")
        self.gridLayout_9.addWidget(self.RES_PLANI_treeView5wiMax, 2, 0, 1, 2)
        self.groupBox_26 = QtWidgets.QGroupBox(self.tab_12)
        self.groupBox_26.setGeometry(QtCore.QRect(760, 30, 321, 661))
        self.groupBox_26.setObjectName("groupBox_26")
        self.RES_PLANI_treeViewLA = QtWidgets.QTreeView(self.groupBox_26)
        self.RES_PLANI_treeViewLA.setGeometry(QtCore.QRect(10, 30, 301, 621))
        self.RES_PLANI_treeViewLA.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.RES_PLANI_treeViewLA.setObjectName("RES_PLANI_treeViewLA")
        self.label_65 = QtWidgets.QLabel(self.tab_12)
        self.label_65.setGeometry(QtCore.QRect(520, 0, 138, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_65.setFont(font)
        self.label_65.setObjectName("label_65")
        self.tabWidget_2.addTab(self.tab_12, "")
        self.tab_13 = QtWidgets.QWidget()
        self.tab_13.setObjectName("tab_13")
        self.tabWidget_2.addTab(self.tab_13, "")
        self.importResGlobaux = QtWidgets.QPushButton(self.tab_8)
        self.importResGlobaux.setGeometry(QtCore.QRect(1040, 10, 75, 23))
        self.importResGlobaux.setObjectName("importResGlobaux")
        self.tabCoordApproch.addTab(self.tab_8, "")

        self.retranslateUi(Prototype)
        self.tabCoordApproch.setCurrentIndex(6)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Prototype)

    def retranslateUi(self, Prototype):
        _translate = QtCore.QCoreApplication.translate
        Prototype.setWindowTitle(_translate("Prototype", "Dialog"))
        self.tabCoordApproch.setTabText(self.tabCoordApproch.indexOf(self.tab), _translate("Prototype", "Acceuil"))
        self.tabCoordApproch.setTabText(self.tabCoordApproch.indexOf(self.tab_2), _translate("Prototype", "Conversions"))
        self.tabCoordApproch.setTabText(self.tabCoordApproch.indexOf(self.tab_3), _translate("Prototype", "Coordonnées approchées"))
        self.tabCoordApproch.setTabText(self.tabCoordApproch.indexOf(self.tab_5), _translate("Prototype", "Points"))
        self.label_127.setText(_translate("Prototype", "nom point RI s RI ecarteRI DS sDS ecarteDS ZD sZD ecarteZD S[m] dm1[m] dm2[m] centrage[mm] "))
        self.tabCoordApproch.setTabText(self.tabCoordApproch.indexOf(self.tab_4), _translate("Prototype", "Canevas"))
        self.groupBox.setTitle(_translate("Prototype", "Nom du réseau"))
        self.importParam.setText(_translate("Prototype", "Import"))
        self.exportParam.setText(_translate("Prototype", "Export"))
        self.label.setText(_translate("Prototype", "Type de calcul"))
        self.typeCalcul.setItemText(0, _translate("Prototype", "constrained"))
        self.typeCalcul.setItemText(1, _translate("Prototype", "stochastic"))
        self.label_2.setText(_translate("Prototype", "Dimension"))
        self.dimensionCalcul.setItemText(0, _translate("Prototype", "2D"))
        self.dimensionCalcul.setItemText(1, _translate("Prototype", "1D"))
        self.dimensionCalcul.setItemText(2, _translate("Prototype", "2D+1"))
        self.label_3.setText(_translate("Prototype", "Nombre d\'itérations max."))
        self.label_4.setText(_translate("Prototype", "Critière d\'interruption dx [m]"))
        self.label_5.setText(_translate("Prototype", "Robuste"))
        self.label_6.setText(_translate("Prototype", "Limite c robuste"))
        self.label_7.setText(_translate("Prototype", "Coefficient de réfraction k"))
        self.label_8.setText(_translate("Prototype", "σ k"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_9), _translate("Prototype", "Options générales"))
        self.groupBox_3.setTitle(_translate("Prototype", "Directions"))
        self.nomGroupeDirection.setText(_translate("Prototype", "groupeDirectionParDefaut"))
        self.label_14.setText(_translate("Prototype", "Nom du groupe"))
        self.label_15.setText(_translate("Prototype", "σ RI"))
        self.label_16.setText(_translate("Prototype", "cc"))
        self.addGroupeDirection.setText(_translate("Prototype", "Ajouter"))
        self.label_17.setText(_translate("Prototype", "σ ZD"))
        self.label_18.setText(_translate("Prototype", "cc"))
        self.groupBox_4.setTitle(_translate("Prototype", "Centrage "))
        self.nomGroupeCentrage.setText(_translate("Prototype", "groupeCentrageParDefaut"))
        self.label_19.setText(_translate("Prototype", "Nom du groupe"))
        self.label_20.setText(_translate("Prototype", "σ centrage station"))
        self.label_21.setText(_translate("Prototype", "mm"))
        self.addGroupeCentrage.setText(_translate("Prototype", "Ajouter"))
        self.label_23.setText(_translate("Prototype", "mm"))
        self.label_22.setText(_translate("Prototype", "σ centrage point visé"))
        self.label_51.setText(_translate("Prototype", "plani."))
        self.label_52.setText(_translate("Prototype", "alti."))
        self.label_53.setText(_translate("Prototype", "mm"))
        self.label_54.setText(_translate("Prototype", "mm"))
        self.groupBox_2.setTitle(_translate("Prototype", "Distances"))
        self.nomGroupeDistance.setText(_translate("Prototype", "groupeDistanceParDefaut"))
        self.label_9.setText(_translate("Prototype", "Nom du groupe"))
        self.label_10.setText(_translate("Prototype", "σ DS"))
        self.label_11.setText(_translate("Prototype", "mm"))
        self.label_12.setText(_translate("Prototype", "ppm"))
        self.label_13.setText(_translate("Prototype", "Inconnues supplémentaires"))
        self.addGroupeDistance.setText(_translate("Prototype", "Ajouter"))
        self.facteurEchelle.setText(_translate("Prototype", "Facteur d\'échelle"))
        self.constanteAddition.setText(_translate("Prototype", "Constante d\'addition"))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.toolBox_2Page1), _translate("Prototype", "Levés polaires"))
        self.groupBox_5.setTitle(_translate("Prototype", "Sessions"))
        self.nomGroupeGNSS.setText(_translate("Prototype", "groupeGNSSParDefaut"))
        self.label_24.setText(_translate("Prototype", "Nom du groupe"))
        self.label_25.setText(_translate("Prototype", "σ LY et LX"))
        self.label_26.setText(_translate("Prototype", "mm"))
        self.label_28.setText(_translate("Prototype", "Inconnues (par session)"))
        self.addGroupeGNSS.setText(_translate("Prototype", "Ajouter"))
        self.GNSS_tE.setText(_translate("Prototype", "tE"))
        self.GNSS_tN.setText(_translate("Prototype", "tN"))
        self.label_29.setText(_translate("Prototype", "σ LH"))
        self.label_27.setText(_translate("Prototype", "mm"))
        self.GNSS_tH.setText(_translate("Prototype", "tH"))
        self.GNSS_rotHz.setText(_translate("Prototype", "rot.Hz"))
        self.GNSS_factEchHz.setText(_translate("Prototype", "fact. éch. Hz"))
        self.label_42.setText(_translate("Prototype", "Description et infos"))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.toolBox_2Page2), _translate("Prototype", "GNSS"))
        self.groupBox_6.setTitle(_translate("Prototype", "Systèmes locaux"))
        self.nomGroupeSystemeLocal.setText(_translate("Prototype", "groupeSystemeLocalParDefaut"))
        self.label_30.setText(_translate("Prototype", "Nom du groupe"))
        self.label_31.setText(_translate("Prototype", "σ LY et LX"))
        self.label_32.setText(_translate("Prototype", "mm"))
        self.label_33.setText(_translate("Prototype", "Inconnues (par session)"))
        self.addGroupeSystemeLocal.setText(_translate("Prototype", "Ajouter"))
        self.systemeLocal_tE.setText(_translate("Prototype", "tE"))
        self.systemeLocal_tN.setText(_translate("Prototype", "tN"))
        self.label_34.setText(_translate("Prototype", "σ LH"))
        self.label_35.setText(_translate("Prototype", "mm"))
        self.systemeLocal_tH.setText(_translate("Prototype", "tH"))
        self.systemeLocal_rotHz.setText(_translate("Prototype", "rot.Hz"))
        self.systemeLocal_factEchHz.setText(_translate("Prototype", "fact. éch. Hz"))
        self.label_43.setText(_translate("Prototype", "Description et infos"))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.toolBox_2Page3), _translate("Prototype", "Systèmes locaux"))
        self.groupBox_7.setTitle(_translate("Prototype", "Cotes"))
        self.nomGroupeCote.setText(_translate("Prototype", "groupeCoteParDefaut"))
        self.label_36.setText(_translate("Prototype", "Nom du groupe"))
        self.label_37.setText(_translate("Prototype", "σ DP"))
        self.label_38.setText(_translate("Prototype", "mm"))
        self.addGroupeCote.setText(_translate("Prototype", "Ajouter"))
        self.label_39.setText(_translate("Prototype", "σ DH"))
        self.label_40.setText(_translate("Prototype", "mm"))
        self.label_50.setText(_translate("Prototype", "Description et infos"))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.toolBox_2Page4), _translate("Prototype", "Cotes"))
        self.suppGroupe.setText(_translate("Prototype", "Supprimer groupe selectionné"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_10), _translate("Prototype", "Groupes"))
        self.groupBox_8.setTitle(_translate("Prototype", "Datum planimétrique"))
        self.label_46.setText(_translate("Prototype", "σ EE et NN (libre-ajusté)"))
        self.planiNumeroPoint.setText(_translate("Prototype", "4001203    2330"))
        self.label_45.setText(_translate("Prototype", "mm"))
        self.label_41.setText(_translate("Prototype", "No du point"))
        self.addPlaniPoint.setText(_translate("Prototype", "Ajouter"))
        self.suppPFplani.setText(_translate("Prototype", "Supprimer point selectionné"))
        self.groupBox_9.setTitle(_translate("Prototype", "Datum altimétrique"))
        self.label_47.setText(_translate("Prototype", "σ HH (libre-ajusté)"))
        self.altiNumeroPoint.setText(_translate("Prototype", "351   0     113"))
        self.label_48.setText(_translate("Prototype", "mm"))
        self.label_49.setText(_translate("Prototype", "No du point"))
        self.addAltiPoint.setText(_translate("Prototype", "Ajouter"))
        self.suppPFalti.setText(_translate("Prototype", "Supprimer point selectionné"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_11), _translate("Prototype", "Points Fixes"))
        self.label_44.setText(_translate("Prototype", "<html><head/><body><p><span style=\" font-size:18pt; text-decoration: underline; color:#ff0000;\">PROTOTYPE </span></p></body></html>"))
        self.tabCoordApproch.setTabText(self.tabCoordApproch.indexOf(self.tab_6), _translate("Prototype", "Paramètres"))
        self.label_55.setText(_translate("Prototype", "<html><head/><body><p><span style=\" font-size:18pt; text-decoration: underline; color:#ff0000;\">PROTOTYPE </span></p></body></html>"))
        self.label_66.setText(_translate("Prototype", "Observations"))
        self.parcourirObs.setText(_translate("Prototype", "Parcourir"))
        self.label_67.setText(_translate("Prototype", "Points"))
        self.parcourirPoints.setText(_translate("Prototype", "Parcourir"))
        self.label_68.setText(_translate("Prototype", "Paramètres"))
        self.parcourirParam.setText(_translate("Prototype", "Parcourir"))
        self.label_69.setText(_translate("Prototype", "Dossier des résultats"))
        self.parcourirRes.setText(_translate("Prototype", "Parcourir"))
        self.runCalcul.setText(_translate("Prototype", "Run"))
        self.checkBoxCtrlCoh.setText(_translate("Prototype", "Contrôles de cohérences"))
        self.tabCoordApproch.setTabText(self.tabCoordApproch.indexOf(self.tab_7), _translate("Prototype", "Calcul"))
        self.label_57.setText(_translate("Prototype", "Nom du réseau:"))
        self.RES_nomReseau.setText(_translate("Prototype", "xxx"))
        self.label_56.setText(_translate("Prototype", "Date:"))
        self.RES_date.setText(_translate("Prototype", "xxx"))
        self.label_58.setText(_translate("Prototype", "Heure:"))
        self.RES_heure.setText(_translate("Prototype", "xxx"))
        self.label_59.setText(_translate("Prototype", "Type de réseau:"))
        self.RES_typeReseau.setText(_translate("Prototype", "xxx"))
        self.label_60.setText(_translate("Prototype", "Dimension de calcul:"))
        self.RES_dimension.setText(_translate("Prototype", "xxx"))
        self.label_61.setText(_translate("Prototype", "Robuste:"))
        self.RES_robuste.setText(_translate("Prototype", "xxx"))
        self.label_62.setText(_translate("Prototype", "Limite robuste:"))
        self.RES_limiteRobuste.setText(_translate("Prototype", "xxx"))
        self.label_63.setText(_translate("Prototype", "Refraction k:"))
        self.RES_refractionk.setText(_translate("Prototype", "xxx"))
        self.label_64.setText(_translate("Prototype", "σ k:"))
        self.RES_sigmak.setText(_translate("Prototype", "xxx"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_27), _translate("Prototype", "Options générales"))
        self.groupBox_10.setTitle(_translate("Prototype", "Général"))
        self.RES_PLANI_nb_iteration.setText(_translate("Prototype", "xxx"))
        self.label_130.setText(_translate("Prototype", "Durée de calcul:"))
        self.RES_PLANI_duree.setText(_translate("Prototype", "xxx"))
        self.label_131.setText(_translate("Prototype", "nombre d\'itérations:"))
        self.groupBox_21.setTitle(_translate("Prototype", "Quotients par groupe"))
        self.groupBox_23.setTitle(_translate("Prototype", "Inconnues supplémentaires des groupes de distance"))
        self.groupBox_24.setTitle(_translate("Prototype", "Dénombrement"))
        self.RES_PLANI_obs.setText(_translate("Prototype", "xxx"))
        self.label_132.setText(_translate("Prototype", "Inconnues:"))
        self.RES_PLANI_inc.setText(_translate("Prototype", "xxx"))
        self.label_133.setText(_translate("Prototype", "Observations:"))
        self.label_134.setText(_translate("Prototype", "Contraintes:"))
        self.label_135.setText(_translate("Prototype", "Surabondance:"))
        self.RES_PLANI_contr.setText(_translate("Prototype", "xxx"))
        self.RES_PLANI_surabondance.setText(_translate("Prototype", "xxx"))
        self.groupBox_25.setTitle(_translate("Prototype", "Résidus normés"))
        self.RES_PLANI_WiMax.setText(_translate("Prototype", "XXX"))
        self.label_136.setText(_translate("Prototype", "Nombre w > 3.5:"))
        self.label_137.setText(_translate("Prototype", "5 wi les plus grands:"))
        self.groupBox_26.setTitle(_translate("Prototype", "Rattachement (si ajustement libre-ajusté)"))
        self.label_65.setText(_translate("Prototype", "<html><head/><body><p><span style=\" font-size:18pt; text-decoration: underline; color:#ff0000;\">PROTOTYPE </span></p></body></html>"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_12), _translate("Prototype", "Planimétrie"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_13), _translate("Prototype", "Altimétrie"))
        self.importResGlobaux.setText(_translate("Prototype", "Import"))
        self.tabCoordApproch.setTabText(self.tabCoordApproch.indexOf(self.tab_8), _translate("Prototype", "Résultats globaux"))


        

        #### INITIALISATIONS SUPPLEMENTAIRES
        
        # police en gras (avec setFont())
        self.bold = QtGui.QFont()
        self.bold.setBold(True)

        # initialisation du dictParametres et des listes de groupes et points fixes
        self.listeGroupesDistance, self.listeGroupesDirection, self.listeGroupesCentrage = [], [], []
        self.listeGroupesGnss = []
        self.listeGroupesSystemeLocal = []
        self.listeGroupesCote = []
        self.listePFplani, self.listePFalti = [], []
        
        # initialisation d'un dict des paramètres 
        self.updateParamCalcul()
        
        
        # connection bouton d'ajout des groupes
        self.addGroupeDistance.clicked.connect(self.appendGroupeDistance)
        self.addGroupeDirection.clicked.connect(self.appendGroupeDirection)
        self.addGroupeCentrage.clicked.connect(self.appendGroupeCentrage)
        self.addGroupeGNSS.clicked.connect(self.appendGroupeGnss)
        self.addGroupeSystemeLocal.clicked.connect(self.appendGroupeSystemeLocal)
        self.addGroupeCote.clicked.connect(self.appendGroupeCote)
        
        # # initialisation treeview des groupes
        self.updateGroupeTreeView()
        
        ### GET VALUE AVEC ROW ET PARENT INDEXES
        self.treeViewGroupes.doubleClicked.connect(self.modifTreeViewGroupes)
        # connection du bouton pour supprimer le groupe séléctionné
        self.suppGroupe.clicked.connect(self.deleteGroupe)
        
        
        
        # connection des boutons d'ajout des PF
        self.addPlaniPoint.clicked.connect(self.appendPointFixePlani)
        self.addAltiPoint.clicked.connect(self.appendPointFixeAlti)
        # connection des boutons de suppression des PF
        self.suppPFplani.clicked.connect(self.deletePFplani)
        self.suppPFalti.clicked.connect(self.deletePFalti)
        
        

        # connection du bouton d'export des paramètres
        self.exportParam.clicked.connect(self.exportParametres)
        # connection du bouton d'import des paramètres
        self.importParam.clicked.connect(self.importParametres)
        
        
        
        # connection du bouton d'import des résultats globaux
        self.importResGlobaux.clicked.connect(self.importResultatsGlobaux)
        

        # VOLET DE CALCUL - INIT
        self.parcourirObs.clicked.connect(self.browseObsClicked)
        self.parcourirPoints.clicked.connect(self.browsePtsClicked)
        self.parcourirParam.clicked.connect(self.browseParamClicked)
        self.parcourirRes.clicked.connect(self.browseResDirClicked)
        
        # conncetion du bouton de lancement de calcul
        self.runCalcul.clicked.connect(self.runClicked)
        
        

        


    def isCheckedString(self, checkbox):
        """
        Simple fonction permettant de retourner un string "true" ou "false" avec t et f minuscule
        afin de respecter le type de donnée "bool" des fichiers modèles XSD.
        
        Returns
        -------
            string : "true" ou "false"
        """
        if checkbox.isChecked() == True:
            return "true"
        else:
            return "false"
        
        
            
            
            
    
    def updateParamCalcul(self):
        """
        Fonction simple permettant de refresh un dictionnaire de paramètres selon les entrées utilisateurs.
        """
        
        self.dictParam = {
          "parameters": {
            "networkName": self.nomReseau.text(),
            "computationOptions": {
              "networkType": str(self.typeCalcul.currentText()),
              "calculationDimension": str(self.dimensionCalcul.currentText()),
              "maxIterationNbr": str(round(self.nbIterationsMax.value(),4)),
              "interruptionCondition": str(self.critereIterruption.value()),
              "robust": self.isCheckedString(self.robuste),
              "robustLimit": str(self.cRobuste.value()),
              "refractionk": str(round(self.refractionk.value(),3)),
              "sigmaRefractionk": str(self.sigmarefraction.value())
            },
            "groups": {
              "distanceGroups": {
                "distanceGroup": self.listeGroupesDistance
              },
              "directionGroups": {
                "directionGroup": self.listeGroupesDirection
              },
              "gnssGroups": {
                "gnssGroup": self.listeGroupesGnss
              },
              "centringGroups": {
                "centringGroup": self.listeGroupesCentrage
              },
              "localSystemGroups": {
                "localSystemGroup": self.listeGroupesSystemeLocal
              },
              "simpleMeasureGroups": {
                "simpleMeasureGroup": self.listeGroupesCote
              }
            },
            "planimetricControlPoints": {
              "point": self.listePFplani
            },
            "altimetricControlPoints": {
              "point": self.listePFalti
            }
          }
        }
        

        # print(json.dumps(self.dictParam, indent=2))
        

        return None
    
    
    
    

    """
    Fonctions d'ajout des groupes à leurs listes respectives.
    """
    
    def appendGroupeDistance(self):
        

        
        self.dictGroupeToAdd = {
          "distanceGroupName": self.nomGroupeDistance.text(),
          "stdDev": {
            "mm": str(self.sigmaDSmm.value()),
            "ppm": str(self.sigmaDSppm.value())
          },
          "additionalUnknowns": {
            "scaleFactor": self.isCheckedString(self.facteurEchelle),
            "additionConstant": self.isCheckedString(self.constanteAddition)
          }
        }
        self.listeGroupesDistance.append(self.dictGroupeToAdd)
        self.updateGroupeTreeView()
   
    def appendGroupeDirection(self):
        
        self.dictGroupeToAdd = {
          "directionGroupName": self.nomGroupeDirection.text(),
          "horizStdDev": {
            "cc": str(self.sigmaRI.value())
          },
          "zenithStdDev": {
            "cc": str(self.sigmaZD.value())
          }
        }
        self.listeGroupesDirection.append(self.dictGroupeToAdd)
        self.updateGroupeTreeView()

    def appendGroupeCentrage(self):
        
        self.dictGroupeToAdd = {
          "centringGroupName": self.nomGroupeCentrage.text(),
          "stationCentring": {
            "planiStdDev": {
              "mm": str(self.sigmaCentStaPlani.value())
            },
            "altiStdDev": {
              "mm": str(self.sigmaCentStaAlti.value())
            }
          },
          "targetCentring": {
            "planiStdDev": {
              "mm": str(self.sigmaCentVisPlani.value())
            },
            "altiStdDev": {
              "mm": str(self.sigmaCentVisAlti.value())
            }
          }
        }
        self.listeGroupesCentrage.append(self.dictGroupeToAdd)
        self.updateGroupeTreeView()
        
    def appendGroupeGnss(self):
        
        self.dictGroupeToAdd = {
          "gnssGroupName": self.nomGroupeGNSS.text(),
          "planiStdDev": {
            "mm": str(self.GNSSsigmaLYLX.value())
          },
          "altiStdDev": {
            "mm": str(self.GNSSsigmaLH.value())
          },
          "unknownParameters": {
            "Etranslation": self.isCheckedString(self.GNSS_tE),
            "Ntranslation": self.isCheckedString(self.GNSS_tN),
            "Htranslation": self.isCheckedString(self.GNSS_tH),
            "horizRotation": self.isCheckedString(self.GNSS_rotHz),
            "horizScaleFactor": self.isCheckedString(self.GNSS_factEchHz)
          }
        }
        self.listeGroupesGnss.append(self.dictGroupeToAdd)
        self.updateGroupeTreeView() 
    
    def appendGroupeSystemeLocal(self):
        
        self.dictGroupeToAdd = {
          "localSystemGroupName": self.nomGroupeSystemeLocal.text(),
          "planiStdDev": {
            "mm": str(self.systemeLocalSigmaLYLX.value())
          },
          "altiStdDev": {
            "mm": str(self.systemeLocalSigmaLH.value())
          },
          "unknownParameters": {
            "horizScaleFactor": self.isCheckedString(self.systemeLocal_factEchHz)
          }
        }
        self.listeGroupesSystemeLocal.append(self.dictGroupeToAdd)
        self.updateGroupeTreeView()
        
    def appendGroupeCote(self):
        
        self.dictGroupeToAdd = {
            "simpleMeasureGroupName": self.nomGroupeCote.text(),
            "planiStdDev": {
              "mm": str(self.coteSigmaDP.value())
            },
            "altiStdDev": {
              "mm": str(self.coteSigmaDH.value())
            }
          }
        self.listeGroupesCote.append(self.dictGroupeToAdd)
        self.updateGroupeTreeView()
        
        
    def updateGroupeTreeView(self):
        """
        Fonction permettant de "refresh" le treeview des groupes si ajout ou suppression de groupes.
        """
        
        # initialisation
        self.treeViewGroupes.setHeaderHidden(True)
        self.treeModelGroupes = QStandardItemModel()
        self.treeModelGroupes.setColumnCount(2)
        self.rootNodeGroupes = self.treeModelGroupes.invisibleRootItem()
        
        # groupes
        self.groupes = QStandardItem('Groupes')
        self.groupes.setFont(self.bold)
        self.groupes.setEditable(False)
        self.groupesDistance = QStandardItem('Distance')
        self.groupesDistance.setFont(self.bold)
        self.groupesDirection = QStandardItem('Direction')
        self.groupesDirection.setFont(self.bold)
        self.groupesCentrage = QStandardItem('Centrage')
        self.groupesCentrage.setFont(self.bold)
        self.groupesGnss = QStandardItem('GNSS')
        self.groupesGnss.setFont(self.bold)
        self.groupesSystemeLocal = QStandardItem('Système local')
        self.groupesSystemeLocal.setFont(self.bold)
        self.groupesCote = QStandardItem('Cote')
        self.groupesCote.setFont(self.bold)
        self.groupes.appendRow(self.groupesDistance)
        self.groupes.appendRow(self.groupesDirection)
        self.groupes.appendRow(self.groupesCentrage)
        self.groupes.appendRow(self.groupesGnss)
        self.groupes.appendRow(self.groupesSystemeLocal)
        self.groupes.appendRow(self.groupesCote)
        
        #### GROUPE DISTANCE
        for groupe in self.listeGroupesDistance:
            groupeDist = QStandardItem('Groupe distance')
            groupeDist.appendRow([QStandardItem('Nom'), QStandardItem(groupe['distanceGroupName'])])
            sigmaDS = QStandardItem('σ DS')
            sigmaDS.appendRow([QStandardItem('[mm]'), QStandardItem(groupe['stdDev']['mm'])])
            sigmaDS.appendRow([QStandardItem('[ppm]'), QStandardItem(groupe['stdDev']['ppm'])])
            groupeDist.appendRow(sigmaDS)
            IncSuppl = QStandardItem('Inc. suppl.')
            IncSuppl.appendRow([QStandardItem('Fact. éch.'), QStandardItem(groupe['additionalUnknowns']['scaleFactor'])])
            IncSuppl.appendRow([QStandardItem('Const. add.'), QStandardItem(groupe['additionalUnknowns']['additionConstant'])])
            groupeDist.appendRow(IncSuppl)
            
            # ajout au type de groupe distance
            self.groupesDistance.appendRow(groupeDist)
            
            
        #### GROUPE DIRECTION
        for groupe in self.listeGroupesDirection:
            groupeDir = QStandardItem('Groupe direction')
            groupeDir.appendRow([QStandardItem('Nom'), QStandardItem(groupe['directionGroupName'])])
            groupeDir.appendRow([QStandardItem('σ RI [cc]'), QStandardItem(groupe['horizStdDev']['cc'])])
            groupeDir.appendRow([QStandardItem('σ ZD [cc]'), QStandardItem(groupe['zenithStdDev']['cc'])])
            
            # ajout au type de groupe distance
            self.groupesDirection.appendRow(groupeDir)
        
        
        #### GROUPE CENTRAGE
        for groupe in self.listeGroupesCentrage:
            groupeCent = QStandardItem('Groupe centrage')
            groupeCent.appendRow([QStandardItem('Nom'), QStandardItem(groupe['centringGroupName'])])
            station = QStandardItem('Station')
            station.appendRow([QStandardItem('σ plani [mm]'), QStandardItem(groupe['stationCentring']['planiStdDev']['mm'])])
            station.appendRow([QStandardItem('σ alti [mm]'),  QStandardItem(groupe['stationCentring']['altiStdDev']['mm'])])
            groupeCent.appendRow(station)
            pointVis = QStandardItem('Point visé')
            pointVis.appendRow([QStandardItem('σ plani [mm]'), QStandardItem(groupe['targetCentring']['planiStdDev']['mm'])])
            pointVis.appendRow([QStandardItem('σ alti [mm]'),  QStandardItem(groupe['targetCentring']['altiStdDev']['mm'])])
            groupeCent.appendRow(pointVis)
            
            # ajout au type de groupe distance
            self.groupesCentrage.appendRow(groupeCent)
            
            
        #### GROUPE GNSS
        for groupe in self.listeGroupesGnss:
            groupeGnss = QStandardItem('Groupe GNSS')
            groupeGnss.appendRow([QStandardItem('Nom'), QStandardItem(groupe['gnssGroupName'])])
            groupeGnss.appendRow([QStandardItem('σ plani [mm]'), QStandardItem(groupe['planiStdDev']['mm'])])
            groupeGnss.appendRow([QStandardItem('σ alti [mm]'),  QStandardItem(groupe['altiStdDev']['mm'])])
            paramInc = QStandardItem('Paramètres inc.')
            paramInc.appendRow([QStandardItem('tE'), QStandardItem(groupe['unknownParameters']['Etranslation'])])
            paramInc.appendRow([QStandardItem('tN'), QStandardItem(groupe['unknownParameters']['Ntranslation'])])
            paramInc.appendRow([QStandardItem('tH'), QStandardItem(groupe['unknownParameters']['Htranslation'])])
            paramInc.appendRow([QStandardItem('rotHz'), QStandardItem(groupe['unknownParameters']['horizRotation'])])
            paramInc.appendRow([QStandardItem('factEchHz'), QStandardItem(groupe['unknownParameters']['horizScaleFactor'])])
            groupeGnss.appendRow(paramInc)
            
            # ajout au type de groupe distance
            self.groupesGnss.appendRow(groupeGnss)
            
        #### GROUPE SYSTEME LOCAL
        for groupe in self.listeGroupesSystemeLocal:
            groupeSystemeLocal = QStandardItem('Groupe système local')
            groupeSystemeLocal.appendRow([QStandardItem('Nom'), QStandardItem(groupe['localSystemGroupName'])])
            groupeSystemeLocal.appendRow([QStandardItem('σ plani [mm]'), QStandardItem(groupe['planiStdDev']['mm'])])
            groupeSystemeLocal.appendRow([QStandardItem('σ alti [mm]'),  QStandardItem(groupe['altiStdDev']['mm'])])
            paramInc = QStandardItem('Paramètres inc.')
            paramInc.appendRow([QStandardItem('tE'), QStandardItem('true')])
            paramInc.appendRow([QStandardItem('tN'), QStandardItem('true')])
            paramInc.appendRow([QStandardItem('tH'), QStandardItem('false')])
            paramInc.appendRow([QStandardItem('rotHz'),  QStandardItem('true')])
            paramInc.appendRow([QStandardItem('factEchHz'), QStandardItem(groupe['unknownParameters']['horizScaleFactor'])])
            groupeSystemeLocal.appendRow(paramInc)
           
            
            # ajout au type de groupe distance
            self.groupesSystemeLocal.appendRow(groupeSystemeLocal)
            
        #### GROUPE COTE
        for groupe in self.listeGroupesCote:
            groupeCote = QStandardItem('Groupe cote')
            groupeCote.appendRow([QStandardItem('Nom'), QStandardItem(groupe['simpleMeasureGroupName'])])
            groupeCote.appendRow([QStandardItem('σ DP [mm]'), QStandardItem(groupe['planiStdDev']['mm'])])
            groupeCote.appendRow([QStandardItem('σ DH [mm]'),  QStandardItem(groupe['altiStdDev']['mm'])])

            # ajout au type de groupe distance
            self.groupesCote.appendRow(groupeCote)
            
            
        self.rootNodeGroupes.appendRow(self.groupes)
        self.treeViewGroupes.setModel(self.treeModelGroupes)
        self.treeViewGroupes.expandAll()
        self.treeViewGroupes.setColumnWidth(0,200)

        
        
        
        
     
    def deleteGroupe(self):
        """
        Fonction permettant de supprimer un groupe.
        """
        
        try : # filtrage pour supprimer que les en-tête de groupe
        
            # récupération des éléments pour la suppression
            itemToRemove = self.treeViewGroupes.selectedIndexes()[0]
            typeToRemove = self.treeModelGroupes.itemFromIndex(itemToRemove).text()
            indexToRemove = itemToRemove.row()
        
            # suppression de la liste
            if typeToRemove == "Groupe distance" and len(self.listeGroupesDistance) > 0:
                del self.listeGroupesDistance[indexToRemove]
            if typeToRemove == "Groupe direction" and len(self.listeGroupesDirection) > 0:
                del self.listeGroupesDirection[indexToRemove]
            if typeToRemove == "Groupe centrage" and len(self.listeGroupesCentrage) > 0:
                del self.listeGroupesCentrage[indexToRemove]
            if typeToRemove == "Groupe GNSS" and len(self.listeGroupesGnss) > 0:
                del self.listeGroupesGnss[indexToRemove]
            if typeToRemove == "Groupe système local" and len(self.listeGroupesSystemeLocal) > 0:
                del self.listeGroupesSystemeLocal[indexToRemove]
            if typeToRemove == "Groupe cote" and len(self.listeGroupesCote) > 0:
                del self.listeGroupesCote[indexToRemove]
            
            # refresh du tree view des groupes
            self.updateGroupeTreeView()
            
        except :
            print('PLEASE SELECT A GROUP TO DELETE')
            
    
    def modifTreeViewGroupes(self, val):
        """
        Fonction permettant de mettre à jour le dictionnaire des groupes quand une modification est entrée (colonne de droite)
        """

        # Au clic sur une données de la colonne de droite 
        # Certains types ont une descendance de plus
        if val.parent().parent().child(0,0).data() == 'Nom':
            nomGroupe = val.row(), val.column(), 'nom du groupe :', val.parent().parent().child(0,1).data()
            
        # Autres types de groupes
        if val.parent().child(0,0).data() == 'Nom':
            nomGroupe = val.row(), val.column(), 'nom du groupe :', val.parent().child(0,1).data()
            
        
        # CONTINUER ICI
    
            
            
    def appendPointFixePlani(self):
        """
        Fonction permettant d'ajout un point fixe planimétrique à la liste.
        """
        
        self.dictGroupeToAdd = {
          "pointName": self.planiNumeroPoint.text(),
          "planiStdDev": {
            "mm": str(self.planiEcartTypePoint.value())
          }
        }
        self.listePFplani.append(self.dictGroupeToAdd)
        self.updatePFplaniTreeView()
        
        
    def appendPointFixeAlti(self):
        """
        Fonction permettant d'ajout un point fixe altimétrique à la liste.
        """
        
        self.dictGroupeToAdd = {
          "pointName": self.altiNumeroPoint.text(),
          "altiStdDev": {
            "mm": str(self.altiEcartTypePoint.value())
          }
        }
        self.listePFalti.append(self.dictGroupeToAdd)
        self.updatePFaltiTreeView()
        
        
        
    def updatePFplaniTreeView(self):
        """
        Fonction qui "refresh" du treeview des PF plani si suppression ou ajout d'un point.
        """
        
        # initialisation
        self.treeViewDatumPlani.setHeaderHidden(True)
        self.treeModelPFplani = QStandardItemModel()
        self.treeModelPFplani.setColumnCount(2)
        self.rootNodePFplani = self.treeModelPFplani.invisibleRootItem()
        
        # planimétrie
        self.PFplani = QStandardItem('Datum planimétrique')
        self.PFplani.setFont(self.bold)
        
        for point in self.listePFplani:
            
            PF = QStandardItem('Point fixe')
            PF.appendRow([QStandardItem('Nom'), QStandardItem(point['pointName'])])
            PF.appendRow([QStandardItem('σ EE [mm]'), QStandardItem(point['planiStdDev']['mm'])])
            self.PFplani.appendRow(PF)
            
        
        self.rootNodePFplani.appendRow(self.PFplani)
        self.treeViewDatumPlani.setModel(self.treeModelPFplani)
        self.treeViewDatumPlani.expandAll()
        self.treeViewDatumPlani.setColumnWidth(0,170)
        
        
        
    def updatePFaltiTreeView(self):
        """
        Fonction qui "refresh" du treeview des PF alti si suppression ou ajout d'un point.
        """
        
        # initialisation
        self.treeViewDatumAlti.setHeaderHidden(True)
        self.treeModelPFalti = QStandardItemModel()
        self.treeModelPFalti.setColumnCount(2)
        self.rootNodePFalti = self.treeModelPFalti.invisibleRootItem()
        
        # altimétrie
        self.PFalti = QStandardItem('Datum altimétrique')
        self.PFalti.setFont(self.bold)
        
        for point in self.listePFalti:
            
            PF = QStandardItem('Point fixe')
            PF.appendRow([QStandardItem('Nom'), QStandardItem(point['pointName'])])
            PF.appendRow([QStandardItem('σ EE [mm]'), QStandardItem(point['altiStdDev']['mm'])])
            self.PFalti.appendRow(PF)
            
        
        self.rootNodePFalti.appendRow(self.PFalti)
        self.treeViewDatumAlti.setModel(self.treeModelPFalti)
        self.treeViewDatumAlti.expandAll()
        self.treeViewDatumAlti.setColumnWidth(0,170)
        
        
        
        
    def deletePFplani(self):
        """
        Fonction permettant la suppression d'un point de la liste des PFplani
        """
        
        try : # filtrage pour supprimer que les en-tête des PF
        
            # récupération des éléments pour la suppression
            itemToRemove = self.treeViewDatumPlani.selectedIndexes()[0]
            indexToRemove = itemToRemove.row()
        
            # suppression de la liste
            del self.listePFplani[indexToRemove]
            
            # refresh du tree view des PF 
            self.updatePFplaniTreeView()
            
        except :
            print('PLEASE SELECT A POINT TO DELETE')
            
    
    def deletePFalti(self):
        """
        Fonction permettant la suppression d'un point de la liste des PFplani.
        """
        
        try : # filtrage pour supprimer que les en-tête des PF
        
            # récupération des éléments pour la suppression
            itemToRemove = self.treeViewDatumAlti.selectedIndexes()[0]
            indexToRemove = itemToRemove.row()
        
            # suppression de la liste
            del self.listePFalti[indexToRemove]
            
            # refresh du tree view des PF 
            self.updatePFaltiTreeView()
            
        except :
            print('PLEASE SELECT A POINT TO DELETE')
    
            
            
            
    def exportParametres(self):
        """
        Fonction générale d'export des paramètres, groupes et PF saisis, au format XML respectant le modèle XSD.
        """
        
        try:
            self.updateParamCalcul()
            
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
            self.filePathExportParam = QtWidgets.QFile().getSaveFileName(None,"Save", None, "*.xml")[0]
            self.dictParamString = xmltodict.unparse(self.dictParam, pretty=True)
            with open(self.filePathExportParam, 'w') as f:
                f.write(self.dictParamString)
                
        except:
            pass
        
        
        
        
        
    
        


    def importParametres(self):
        """
        Fonction générale d'import des paramètres, groupes et PF saisis, à partir d'un format XML 
        """
        
        # initialisation du dictParametres et des listes de groupes et points fixes
        self.listeGroupesDistance, self.listeGroupesDirection, self.listeGroupesCentrage = [], [], []
        self.listeGroupesGnss = []
        self.listeGroupesSystemeLocal = []
        self.listeGroupesCote = []
        self.listePFplani, self.listePFalti = [], []
        
        # initialisation d'un dict des paramètres 
        self.updateParamCalcul()
        
        # improt du fichier texte XML
        self.filePathImportParam = QtWidgets.QFileDialog().getOpenFileName(None,"Open", None, "*.xml")[0]
        with open(self.filePathImportParam) as f:
            self.dictParamImport = xmltodict.parse(f.read())
            
        # options générales
        self.nomReseau.setText(self.dictParamImport['parameters']['networkName']) 
        self.typeCalcul.setCurrentText(self.dictParamImport['parameters']['computationOptions']['networkType']) 
        self.dimensionCalcul.setCurrentText(self.dictParamImport['parameters']['computationOptions']['calculationDimension']) 
        self.nbIterationsMax.setValue(int(self.dictParamImport['parameters']['computationOptions']['maxIterationNbr']))
        self.critereIterruption.setValue(float(self.dictParamImport['parameters']['computationOptions']['interruptionCondition']))
        rob = True if self.dictParamImport['parameters']['computationOptions']['robust'] == "true" else False
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



        
        # Refresh les paramètres et les treeview
        self.updateGroupeTreeView()
        self.updatePFplaniTreeView()
        self.updatePFaltiTreeView()
        self.updateParamCalcul()

        

        
        
        
            
            
        
    def importResultatsGlobaux(self):
        """
        Fonction d'import des résultats globaux qui s'active au clic du bouton prévu à cet effet.
        """
        
        # import du fichier texte XML
        self.filePathImportResGlobaux = QtWidgets.QFileDialog().getOpenFileName(None,"Open", None, "*.xml")[0]
        with open(self.filePathImportResGlobaux) as f:
            self.dictResGlobaux = xmltodict.parse(f.read())
        self.RES_nomReseau.setText(self.dictResGlobaux['globalResults']['networkName'])
        
        # Inconnues supplémentaires en liste (si un seul groupe)
        if type(self.dictResGlobaux['globalResults']['planimetry']['distanceGroupsAdditionalUnknowns']) != list:
            self.listePFalti= [self.dictResGlobaux['globalResults']['planimetry']['distanceGroupsAdditionalUnknowns']]
        else: # déjà en liste
            self.listePFalti = self.dictResGlobaux['globalResults']['planimetry']['distanceGroupsAdditionalUnknowns']

        
        
        #### OPTIONS GENERALES
        self.RES_date.setText(self.dictResGlobaux['globalResults']['date'])
        self.RES_heure.setText(self.dictResGlobaux['globalResults']['heure'])
        self.RES_typeReseau.setText(self.dictResGlobaux['globalResults']['computationOptions']['networkType'])
        self.RES_dimension.setText(self.dictResGlobaux['globalResults']['computationOptions']['calculationDimension'])
        self.RES_robuste.setText(self.dictResGlobaux['globalResults']['computationOptions']['robust'])
        self.RES_limiteRobuste.setText(self.dictResGlobaux['globalResults']['computationOptions']['robustLimit'])
        self.RES_refractionk.setText(self.dictResGlobaux['globalResults']['computationOptions']['refractionk'])
        self.RES_sigmak.setText(self.dictResGlobaux['globalResults']['computationOptions']['sigmaRefractionk'])

        
        
        #### PLANIMETRIE
        if self.dictResGlobaux['globalResults']['computationOptions']['calculationDimension'] == "2D+1" or self.dictResGlobaux['globalResults']['computationOptions']['calculationDimension'] == "2D": 
            self.RES_PLANI_duree.setText(self.dictResGlobaux['globalResults']['planimetry']['CalculationTime'])
            self.RES_PLANI_nb_iteration.setText(self.dictResGlobaux['globalResults']['planimetry']['iterationsCount'])
            self.RES_PLANI_inc.setText(self.dictResGlobaux['globalResults']['planimetry']['counting']['unknowns'])
            self.RES_PLANI_obs.setText(self.dictResGlobaux['globalResults']['planimetry']['counting']['observations'])
            self.RES_PLANI_contr.setText(self.dictResGlobaux['globalResults']['planimetry']['counting']['constraints'])
            self.RES_PLANI_surabondance.setText(self.dictResGlobaux['globalResults']['planimetry']['counting']['overdetermination'])
            
            #### ^---- Quotients treeView
            # Génération du treeView
            self.RES_PLANI_treeViewQuotientsPlani.setHeaderHidden(True)
            self.treeModelQuotientsPlani = QStandardItemModel()
            self.treeModelQuotientsPlani.setColumnCount(2)
            self.rootNodeQuotientsPlani = self.treeModelQuotientsPlani.invisibleRootItem()

            for nom,value in self.dictResGlobaux['globalResults']['planimetry']['stdDevQuotients'].items():
                self.rootNodeQuotientsPlani.appendRow([QStandardItem(nom), QStandardItem(value['quotient'])])

            self.RES_PLANI_treeViewQuotientsPlani.setModel(self.treeModelQuotientsPlani)
            self.RES_PLANI_treeViewQuotientsPlani.expandAll()
            self.RES_PLANI_treeViewQuotientsPlani.setColumnWidth(0,200)
            
            
            
            #### ^---- Inc. supplémentaires distances treeView
            # Génération du treeView si au moins un groupe de dist. est concerné
            if self.dictResGlobaux['globalResults']['planimetry']['distanceGroupsAdditionalUnknowns'] != None: 
                
                self.RES_PLANI_treeViewIncSupplDist.setHeaderHidden(True)
                self.treeModelIncSupplDist = QStandardItemModel()
                self.treeModelIncSupplDist.setColumnCount(2)
                self.rootNodeIncSupplDist = self.treeModelIncSupplDist.invisibleRootItem()
                
                for nom,value in self.dictResGlobaux['globalResults']['planimetry']['distanceGroupsAdditionalUnknowns'].items():

                    groupe = QStandardItem(nom)
                    if 'scaleFactor' in value.keys():
                        facteurEchelle = QStandardItem("Facteur d'échelle")
                        valeur = (float(value['scaleFactor']['value'])-1)*1e6 # en ppm
                        ecType = float(value['scaleFactor']['stdDev'])*1e6 # en ppm
                        facteurEchelle.appendRow([QStandardItem('valeur [ppm]'), QStandardItem("{:0.1f}".format(valeur))])
                        facteurEchelle.appendRow([QStandardItem('σ [ppm]'), QStandardItem("{:0.1f}".format(ecType))])
                        groupe.appendRow(facteurEchelle)

                    if 'additionConstant' in value.keys():
                        constanteAddition = QStandardItem("Constante d'addition")
                        valeur = float(value['additionConstant']['value'])*1000 # en mm
                        ecType = float(value['additionConstant']['stdDev'])*1000 # en mm
                        constanteAddition.appendRow([QStandardItem('valeur [mm]'), QStandardItem("{:0.1f}".format(valeur))])
                        constanteAddition.appendRow([QStandardItem('σ [mm]'), QStandardItem("{:0.1f}".format(ecType))])
                        groupe.appendRow(constanteAddition)
                    
                    self.rootNodeIncSupplDist.appendRow(groupe)
                    
                self.RES_PLANI_treeViewIncSupplDist.setModel(self.treeModelIncSupplDist)
                self.RES_PLANI_treeViewIncSupplDist.expandAll()
                self.RES_PLANI_treeViewIncSupplDist.setColumnWidth(0,200)
                
                
                
            #### ^---- Wi treeView
            self.RES_PLANI_treeView5wiMax.setHeaderHidden(True)
            self.treeModelWi = QStandardItemModel()
            self.treeModelWi.setColumnCount(2)
            self.rootNodeWi = self.treeModelWi.invisibleRootItem()
            
    
    """
    ENSEMBLE DE FONCTION PERMETTANT DE SAISIR DES EMPLACEMENTS DES FICHIERS SUR LES QLineEditDU DU VOLET "CALCUL."
    """
            
    def browseObsClicked(self):
        file = QtWidgets.QFileDialog().getOpenFileName(None,"Sélection du fichier XML des observations", None, "*.xml")[0]
        self.pathObs.setText(file)
    def browsePtsClicked(self):
        file = QtWidgets.QFileDialog().getOpenFileName(None,"Sélection du fichier XML des points", None, "*.xml")[0]
        self.pathPoints.setText(file)
    def browseParamClicked(self):
        file = QtWidgets.QFileDialog().getOpenFileName(None,"Sélection du fichier XML des paramètres", None, "*.xml")[0]
        self.pathParam.setText(file)
    def browseResDirClicked(self):
        directory = QtWidgets.QFileDialog().getExistingDirectory(None,"Sélection du dossier des résultats")
        self.resDirPath.setText(directory)
        
    
    def runClicked(self):
        """
        FONCTION QUI LANCE L'AJUSTEMENT.
        """
        
        processCtrlCoh = self.checkBoxCtrlCoh.isChecked()
        nomsFichiers = {'fichierXMLCanevas':self.pathObs.text(), 
                        'fichierXMLPoints':self.pathPoints.text(), 
                        'fichierXMLParametres':self.pathParam.text(),
                        'fichierXSDCanevas':"C:\\01_ContraintesMsMo\\02_dev\\01_code\\modeleDonnees\\modeleCanevas.xsd", 
                        'fichierXSDPoints':"C:\\01_ContraintesMsMo\\02_dev\\01_code\\modeleDonnees\\modelePoints.xsd", 
                        'fichierXSDParametres':"C:\\01_ContraintesMsMo\\02_dev\\01_code\\modeleDonnees\\modeleParamCalcul.xsd",
                        'dossierResultats': self.resDirPath.text()}
        
        Process = processUtils.Process(nomsFichiers, processCtrlCoh)
        Process.run()
        
        
        
        
        

        
    
        
        
        
            
            
                
        
        
        
        
    
        

                  
                

        
        
        
        
        
        



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Prototype = QtWidgets.QDialog()
    ui = Ui_Prototype()
    ui.setupUi(Prototype)
    Prototype.show()
    sys.exit(app.exec_())

    
    
    
    



