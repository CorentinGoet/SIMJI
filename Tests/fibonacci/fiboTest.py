"""
Programme de vérification du résultat de l'exécution de la suite de fibonacci
"""

n = 15
r1 = 0
r2 = 1

for i in range(n):
    r1, r2 = r2, r1 + r2
print(r1)