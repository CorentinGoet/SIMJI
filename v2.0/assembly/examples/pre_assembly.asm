# this code was written by Corentin Goetghebeur
add r0,3,r1; this stores 3 in the first register
add r0,6,r2
add r0,2,r3

sub r1,r2,r4
mul r3,r4,r1
scall 1 #this line prints r1 in the standard output


stop