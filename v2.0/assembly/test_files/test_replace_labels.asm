add r0,1,r2
add r0,3,r3
add r0,0,r1

L1: braz r1,L_end
mul r2,r3,r4
jump L1,r1

branz r1,L_end

L_end:
stop