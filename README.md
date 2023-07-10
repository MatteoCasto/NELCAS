# NELCAS version CPU
## Notes importantes
- Python 3.9 IMPORTANT (peut se faire en téléchargant la dernière version de Anaconda)
- Il faudra importer certains modules avec des "pip install", voir au moment de run le programme avec une installation basique de Anaconda (conseillé) :
    - conda install -c conda -forge cupy
    - pip install scikit-spatial
    - pip install pyqtgraph
    - pip install PyQt5
    - pip install xmltodict
    - pip install lxml
    - pip install scipy
- Une version compilée du programme en EXE est aussi disponible, on peut l'ouvrir sans installer Python, on clique simplement sur NELCAS.exe après avoir téléchargé le dossier NELCAS_vXXXX_EXE.zip sur le Cyberlearn de NELCAS
- Dès que des modifications ont été apportées à certains scripts (p.ex. estimationUtils), il est intéréssant de "commit" le nouveau fichier et ainsi avoir un versionnage de ce dernier
- Cette version "CPU" se run sur le processeur, pour la partie GPU, il faudra voir dans un second temps (j'ai le code à dispo, il n'est pas très différent mais quelques installations sont à faire). Toutefois, jusqu'à 10-15'000 observations il n'y quasi aucune différence entre CPU et GPU (exponentiel ensuite). 






