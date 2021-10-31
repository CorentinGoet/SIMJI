#!/usr/bin/env python3
"""
@author Corentin GOETGHEBEUR (SNS 2023)
Ce programme permet de créer un fichier mémoire pour le simulateur contenant une matrice NxN de valeurs aléatoires.
"""

from python_files.Data import Storage
import numpy as np
import os

if __name__ == '__main__':
    os.chdir("../matrix/")
    mem = Storage()

    n = 3
    #mat = np.random.randint(0, 10, (n, n))
    mat = np.array([[-1, 0, 0],
                    [0, -1, 0],
                    [0, 0, -1]])
    print(mat)

    # écriture du fichier de départ
    mem.write(0, n)
    for i in range(n):
        for j in range(n):
            address = n * i + j
            mem.write(address, mat[i, j])
    mem.writeMem("data.hex")

    mat2 = np.dot(mat,mat)
    for i in range(n):
        for j in range(1, n+1):
            address = n * i + j + n**2
            mem.write(address, int(mat2[i, j-1]))
    mem.writeMem("data_final.hex")