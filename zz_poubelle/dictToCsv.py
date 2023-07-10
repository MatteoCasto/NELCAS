# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 16:48:31 2022

@author: matteo.casto
"""

import libUtils.conversionUtils as conversionUtils
import xmltodict
import os


dirPath = os.getcwd()

with open(dirPath+'\\01_input\\plan17\\points.xml') as f:
    dictPoints = xmltodict.parse(f.read())

csvText = ''

for point in dictPoints['points']['point']:
    H = point['H'] # Possible qu'il n'y ai pas d'alitude (=None)
    if point['H'] == None:
        H = ''
    csvText += '{:s};{:s};{:s};{:s}\n'.format(point['pointName'], point['E'], point['N'], H)
   
    
   
    

with open(dirPath+'\\points.csv', 'w') as f:
    f.write(csvText)
    
    



