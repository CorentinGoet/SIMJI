# Corentin GOETGHEBEUR (SNS 2023)
# programme de calcule du N-eme terme de la suite de Fibonacci
# Le nombre N doit être stocké en mémoire à l'adresse 0

# initialisation
    add r0,0,r1;stockage du terme précédent
    add r0,1,r2;stockage du terme actuel
    load r0,0,r3;nombre cible
    add r0,0,r4; compteur de boucle

# Boucle
L1:
    slt r4,r3,r5
    braz r5,Label_end; si i>n, on stop
    add r1,r2,r6; r6 (tmp) recoit r1 + r2
    add r2,0,r1; r1 recoit r2
    add r6,0,r2; r2 recoit r6 (tmp)
    add r4,1,r4; i++
    jmp L1,r10

#fin
Label_end:
    scall 1
    store r0,1,r1; on stocke la valeur de r1 dans la case mémoire 1
    stop
