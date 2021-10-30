#!/usr/bin/env python3
"""
@author Corentin GOETGHEBEUR (SNS 2023)
Ce programme permet de créer un fichier mémoire pour le simulateur contenant une matrice NxN de valeurs aléatoires.
"""

from python_files.Data import Storage
import numpy as np

if __name__ == '__main__':
    mem = Storage()

    n = 3
    mat = np.random.randint(0, 10, (n, n))
    print(mat)

    # écriture du fichier de départ
    mem.write(0, n)
    for i in range(n):
        for j in range(1, n+1):
            address = n * i + j
            mem.write(address, mat[i, j-1])
    mem.writeMem("data.hex")

    mat2 = np.dot(mat, mat)
    print(mat2)

    for i in range(n):
        for j in range(1, n+1):
            address = n * i + j + n**2 +3
            mem.write(address, mat2[i, j-1])
    mem.writeMem("data_final.hex")