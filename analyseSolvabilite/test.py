# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 18:04:18 2023

@author: matteo.casto

"""

import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth



#                     #inc. ori       #inc. ori           # E3           # N3              # E4           # N4
# # A = np.array(   [[ 34383.23111345,     0.        ,-17672.08116041,     0.        , -17224.53192517, 12918.39894387],   
# #                  [     0.        , 34383.23111345,-17224.53192517,-12918.39894387,-17672.08116041 ,     0.         ],  # 
# #                  [-17672.08116041,-17224.53192517, 58379.66228006,  2139.28884853,-4444.44444444  ,     0.         ],
# #                  [     0.        ,-12918.39894387,  2139.28884853, 47518.14980314,      0.        ,     0.         ],
# #                  [-17224.53192517,-17672.08116041, -4444.44444444,     0.        ,58379.66228006  , -2139.28884853 ],
# #                  [ 12918.39894387,     0.        ,     0.        ,     0.        ,-2139.28884853  , 47518.14980314 ]])


#                     #inc. ori  1     #inc. ori 2        # E3           # N3              # E4           # N4
# A = np.array(   [[ 34383.23111345,     0.        ,-17672.08116041,     0.        , -17224.53192517, 12918.39894387],   
#                  [     0.        , 34383.23111345,-17224.53192517,-12918.39894387,-17672.08116041 ,     0.         ],  # 
#                  [-17672.08116041,-17224.53192517, 58379.66228006,  2139.28884853,-4444.44444444  ,     0.         ],
#                  [     0.        ,-12918.39894387,  2139.28884853, 47518.14980314,      0.        ,     0.         ],
#                  [-17224.53192517,-17672.08116041, -4444.44444444,     0.        ,58379.66228006  , -2139.28884853 ],
#                  [ 12918.39894387,     0.        ,     0.        ,     0.        ,-2139.28884853  , 47518.14980314 ]])


def find_empty_columns(matrix):
    """
    Function that analyses if there is any columns of the matrix 
    that contains only 0s. 

    Parameters
    ----------
    matrix : np.array 
        Input cofactor matrix that bind observations, constraints and unknowns.

    Returns
    -------
    list(empty_columns) : list
        List that contains all index of columns that contains only 0s.

    """
    empty_columns = np.where(~matrix.any(axis=0))[0]
    return list(empty_columns)

def binary_matrix(matrice):
    matrice_transformee = np.where(matrice != 0, 1, 0)
    return matrice_transformee

def indices_colonnes_non_resolues(A):
    Q, R = np.linalg.qr(A)
    indices_non_resolus = np.where(np.abs(np.diag(R)) < 1e-8)[0]
    return indices_non_resolus, Q,R

# def indices_colonnes_non_resolues(A):
#     _, singular_values, _ = np.linalg.svd(A)
#     indices_non_resolus = np.where(np.abs(singular_values) < 1e-8)[0]
#     return indices_non_resolus


# def indices_colonnes_non_resolues(A):
#     _, singular_values, _ = np.linalg.svd(A)
#     indices_non_resolus = np.where(np.abs(singular_values) < 1e-8)[0].tolist()
#     return indices_non_resolus


# ## ORIGINALE (A issue des fichiers)
                
A = np.array(
 # ori st 1    # ori st 2    # E2         # N2        # E3        # N3
[[-1.        , 0.        ,-0.04453211,-2.1176922 , 0.        , 0.        ], # 1->2 RI
 [ 0.        , 0.        , 0.999779  ,-0.02102396, 0.        , 0.        ], # 1->2 DP
 [-1.        , 0.        , 0.        , 0.        , 1.5891929 ,-0.03327429], # 1->3 RI
 [ 0.        , 0.        , 0.        , 0.        , 0.02093327, 0.9997809 ], # 1->3 DP
 [-1.        , 0.        , 0.        , 0.        , 0.        , 0.        ], # 1->4 RI
 [ 0.        , 0.        , 0.        , 0.        , 0.        , 0.        ], # 1->4 DP
 [ 0.        ,-1.        ,-1.0326124 ,-0.7415835 , 1.0326124 , 0.7415835 ], # 2->3 RI
 [ 0.        , 0.        , 0.58332133,-0.8122415 ,-0.58332133, 0.8122415 ], # 2->3 DP
 [ 0.        ,-1.        ,-0.04453211,-2.1176922 , 0.        , 0.        ], # 2->1 RI
 [ 0.        , 0.        , 0.999779  ,-0.02102396, 0.        , 0.        ], # 2->1 DP
 [ 0.        ,-1.        ,-1.5542898 , 0.03992161, 0.        , 0.        ]] # 2->4 RI 

 )

# ## MODIFIEE : solution infinie (pt 2 déterm. par une distance uniquement)
# A = np.array(
#  # ori st 1    # ori st 2    # E2         # N2        # E3        # N3
# [[-1.        , 0.        , 0.        , 0.        , 0.        , 0.        ], # 1->2 RI
#  [ 0.        , 0.        , 0.        , 0.        , 0.        , 0.        ], # 1->2 DP
#  [-1.        , 0.        , 0.        , 0.        , 1.5891929 ,-0.03327429], # 1->3 RI
#  [ 0.        , 0.        , 0.        , 0.        , 0.02093327, 0.9997809 ], # 1->3 DP
#  [-1.        , 0.        , 0.        , 0.        , 0.        , 0.        ], # 1->4 RI
#  [ 0.        , 0.        , 0.        , 0.        , 0.        , 0.        ], # 1->4 DP
#  [ 0.        ,-1.        , 0.        , 0.        , 1.0326124 , 0.7415835 ], # 2->3 RI
#  [ 0.        , 0.        , 0.        , 0.        ,-0.58332133, 0.8122415 ], # 2->3 DP
#  [ 0.        ,-1.        , 0.        , 0.        , 0.        , 0.        ], # 2->1 RI
#  [ 0.        , 0.        , 0.022     ,-0.02102396, 0.        , 0.        ], # 2->1 DP
#  [ 0.        ,-1.        , 0.        , 0.        , 0.        , 0.        ]] # 2->4 RI 
#  )


# ## MODIFIEE : solution infinie (pt 2 ET pt 3 déterm. par une distance uniquement)
# A = np.array(
#  # ori st 1    # ori st 2    # E2         # N2        # E3        # N3
# [[ -1.       , 0.        , 0.        , 0.        , 0.        , 0.        ], # 1->2 RI
#  [ 0.        , 0.        , 0.        , 0.        , 0.        , 0.        ], # 1->2 DP
#  [ 0.        , 0.        , 0.        , 0.        , 0.        , 0.        ], # 1->3 RI
#  [ 0.        , 0.        , 0.        , 0.        , 0.        , 0.        ], # 1->3 DP
#  [ 0.        , 0.        , 0.        , 0.        , 0.        , 0.        ], # 1->4 RI
#  [ 0.        , 0.        , 0.        , 0.        , 0.        , 0.        ], # 1->4 DP
#  [ 0.        , 0.        , 0.        , 0.        , 0.        , 0.        ], # 2->3 RI
#  [ 0.        , 0.        , 0.        , 0.        ,-0.58332133, 0.8122415 ], # 2->3 DP
#  [ 0.        , 0.        , 0.        , 0.        , 0.        , 0.        ], # 2->1 RI
#  [ 0.        , 0.        , 0.022     ,-0.02102396, 0.        , 0.        ], # 2->1 DP
#  [ 0.        , 0.        ,-1.5542898 , 0.03992161, 0.        , 0.        ]] # 2->4 RI 
#  )



# Data Girard non-nettoyé - matrice singulière
A = np.load('A.npy')


binary_matrix = binary_matrix(A)

indices_non_resolus, Q, R = indices_colonnes_non_resolues(A)



# emptyCols = find_empty_columns(A)
ATA = A.T@A

invATA = np.linalg.inv(ATA)




print(np.array2string(binary_matrix))



# def dfs(i, j, visited, island):
#     if i < 0 or i >= binary_matrix.shape[0] or j < 0 or j >= binary_matrix.shape[1]:
#         return
#     if binary_matrix[i][j] == 0 or visited[i][j]:
#         return
#     visited[i][j] = True
#     island.append((i, j))
#     dfs(i - 1, j, visited, island)  # Voisin du haut
#     dfs(i + 1, j, visited, island)  # Voisin du bas
#     dfs(i, j - 1, visited, island)  # Voisin de gauche
#     dfs(i, j + 1, visited, island)  # Voisin de droite

# # Parcourir la matrice et trouver les îlots
# visited = np.zeros_like(binary_matrix, dtype=bool)
# islands = []
# for i in range(binary_matrix.shape[0]):
#     for j in range(binary_matrix.shape[1]):
#         if binary_matrix[i][j] == 1 and not visited[i][j]:
#             island = []
#             dfs(i, j, visited, island)
#             islands.append(island)

# # Nombre total d'îlots indépendants
# num_islands = len(islands)

# # Indices des éléments dans chaque îlot
# for i, island in enumerate(islands):
#     print(f"Ilot {i+1}:")
#     for index in island:
#         print(f"Element à l'indice {index}")
        
        
        
        



















