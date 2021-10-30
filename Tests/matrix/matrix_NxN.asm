# Corentin GOETGHEBEUR (SNS 2023)
# Ce programme calcule le carré d'une matrice carrée de taille quelconque N.
# La taille de la matrice doit être stockée à l'adresse 0
# Le coefficient (i,j) de la matrice doit être stocké à l'adresse n*i + j
# Pour la matrice de sortie, le coefficient (i,j) sera stocké à l'adresse n*i+j + n²+3

# Initialisation
    load r0,0,r1; r1 recoit n
    mul r1,r1,r2
    add r2,3,r2; r2 recoit n²+3 (offset resultat)
    add r0,0,r3; i recoit 0

L_boucle_i:
    slt r3,r1,r5; si i > n, alors stop
    braz r5,L_end
    add r3,1,r3; i++
    add r0,0,r4; j = 0

L_boucle_j:
    slt r4,r1,r5
    braz r5,L_boucle_i
    add r4,1,r4; j++
    add r0,0,r6; a = 0
    add r0,0,r7; k = 0

L_boucle_k:
    slt r7,r1,r5
    braz r5,L_store
    add r7,1,r7; k++

    mul r1,r3,r10
    sub r10,r1,r10
    add r10,r7,r10; r10 recoit n*i+k
    load r10,0,r10; r10 recoit M[i,k]

    mul r1,r7,r11
    sub r11,r1,r11
    add r11,r4,r11; r11 recoit n*k + j
    load r11,0,r11; r11 recoit M[k,j]

    mul r10,r11,r12; r12 recoit M[i,k] * M[k,j]
    add r6,r12,r6; a += r12

    jmp L_boucle_k,r30

L_store:
    mul r1,r3,r12
    add r4,r12,r12; r12 recoit n*i+j
    add r12,r2,r12; r12 recoit r12 + offset
    store r12,0,r6; A[i,j] recoit a
    jmp L_boucle_j,r30

L_end:
    stop

