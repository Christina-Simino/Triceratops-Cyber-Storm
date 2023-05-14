#############################################################################################################
# Team: 7
# Member Names: Majd Tahat, Christina Simino, Jaden Box, Robert Emory, Jeremy Fountain, Anousith Keomaly, Ty Pederson.
# Date: 22 Mar 2023
# Description: Binary Decoder
#############################################################################################################

import sys
m = sys.stdin.read()
hasReturn = 0
if(m[-1] == '\r' or m[-1] == '\n'):
    hasReturn = 1
lenm = len(m) - hasReturn
if(lenm % 7 == 0):
    c = 7
    for i in range(int(lenm / c)):
        print(chr(int(m[i*c:i*c + c],2)), end='')
    print("")

if(lenm % 8 == 0):
    c = 8
    for i in range(int(lenm / c)):
        print(chr(int(m[i*c:i*c + c],2)), end='')
    print("")
