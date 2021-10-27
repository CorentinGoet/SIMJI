# Corentin GOETGHEBEUR (SNS 2023)
# Ce programme calcule la durée de vol de la suite de Syracuse
#en partant du nombre stockée à l'adresse 0.

# Initialisation
    add r0,0,r1 ;r1 correspond à la durée de vol
    load r0,0,r2 ;r2 correspond à la valeur de la suite

Label_start:
    seq r2,1,r3
    branz r3,Label_end ; si r2 = 0, alors stop
    add r1,1,r1 ; On incrémente r1

    div r2,2,r4
    sub r2,r4,r4 ; r4 recoit r2 % 2
    braz r4,Label_pair

    # si r2 est impair
    mult r2,3,r2
    add r2,1,r2 ; r2 recoit 3*r2 + 1
    jmp Label_start,r5

Label_pair: ; si r2 est pair
    div r2,2,r2 ; r2 recoit r2 / 2
    jmp Label_start,r5

Label_end:
    store r0,1,r1 ; On stocke le résultat à l'adresse 1
    scall 1 ; On affiche le résultat
    stop


