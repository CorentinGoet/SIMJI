#!/usr/bin/env python3
"""
Programme de vérification de résultat de la suite de Syracuse.
"""

n = 0   # durée de vol
u = 15  # point de départ

while u != 1:
    if u % 2 == 0:
        u /= 2
    else:
        u = 3 * u + 1

    n += 1

print("Durée de vol: {}".format(n))

