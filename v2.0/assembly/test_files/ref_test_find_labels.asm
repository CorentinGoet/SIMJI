0 add r0,1,r2
1 add r0,3,r3
2 add r0,0,r1
4 braz r1,L_end
5 mul r2,r3,r4
6 jump L1,r1
8 branz r1,L_end
11 stop
