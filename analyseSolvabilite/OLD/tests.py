import numpy as np

# Matrice des coefficients du système (10 équations, 4 inconnues)
A = np.array([ [1, 1, 0, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 1, 1, 1]])


M = A.T@A
b = np.array([1, 2, 0, 4])



    
    
    



def testSolvabilite(M, b):
    
    x, residuals, rank, s = np.linalg.lstsq(M, b, rcond=None)
    
    if rank < M.shape[1]:
        print("Le système est surdéterminé mais non résolvable.")
        
        # Extraire les inconnues non résolues
        x_unsolved = np.array([np.nan] * M.shape[1])
        x_unsolved[rank:] = x[rank:]
        
        # Afficher les inconnues non résolues
        print("Inconnues non résolues:")
        print(x_unsolved)
    else:
        print("Le système est résolvable.")
        print("Inconnues résolues:")
        print(x)
    
    # retourne une listes des indices des 
    return x_unsolved


testSolvabilite(M, b)

