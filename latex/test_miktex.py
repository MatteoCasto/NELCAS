# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 13:19:43 2023

@author: matteo.casto
"""

from jinja2 import Template
import subprocess

# Chemin d'accès au compilateur LaTeX portable
latex_compiler = './miktex/bin/x64/miktex-pdflatex.exe'
# Modèle de base pour votre fichier LaTeX
latexTextContent = r"""


\documentclass[a4paper, 9pt]{report}
\usepackage[margin=2cm]{geometry} % Marges de 2 cm à gauche et à droite
\usepackage{graphicx} % Required for inserting images
\usepackage[table]{xcolor}
\usepackage{titlesec}
\usepackage{array}
\usepackage{tabularx}
\usepackage{pdflscape} % Package pour le format paysage
\usepackage{fancyhdr} % pour no de page en format paysage



\title{Rapport de calcul}
\author{NELCAS - logiciel d'estimation par moindres carrés}
\date{\today}






\begin{document}

\maketitle

\tableofcontents

\titleformat{\chapter}[hang]{\normalfont\huge\bfseries}{\thechapter}{1em}{}

\begin{landscape} % Début de l'environnement paysage

\chapter{Détails des points}

    \rowcolors{2}{}{lightgray!25} % Alternance automatique gris-blanc

    \begin{tabularx}{\linewidth}{*{17}{>{\centering\arraybackslash}X}}
        \rowcolor{white} Nom de pt & E & N & H & elem. plani & elem. alti & id inc. E & id inc. N & id inc. H & demi-grand axe a & demi-petit axe b & gis. a & NA & gis. NA & id obs. resp. NA & dE & dN \\
        \rowcolor{white}  - & [m] & [m] & [m] & - & - & - & - & - & [mm] & [mm] & [g] & [mm] & [g] & - & [mm] & [mm] \\
        \hline
        0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 \\
        0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 \\
        % Ajoutez d'autres lignes ici...
    \end{tabularx}

    
\end{landscape} % Fin de l'environnement paysage

\end{document}


"""



# Écrire le contenu dans un fichier .tex
with open('output.tex', 'w', encoding='utf-8') as file:
    file.write(latexTextContent)

# Appeler le compilateur LaTeX portable pour générer un fichier PDF
subprocess.call([latex_compiler, '--interaction=nonstopmode', 'output.tex'])






