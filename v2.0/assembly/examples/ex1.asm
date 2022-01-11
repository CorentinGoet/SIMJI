# This is the first example of the package assembly it computes the sum of r1 and r2 and displays the result

; first, lets initiate the values
add r0,2,r1
add r0,3,r2

add r1,r2,r1 #Now we add and store in r1

scall 0
stop