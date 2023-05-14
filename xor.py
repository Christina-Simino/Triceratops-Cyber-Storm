######################################################################################################################
# Team: Triceratops
# Member Names: Majd Tahat, Christina Simino, Jaden Box, Robert Emory, Jeremy Fountain, Anousith Keomaly, Ty Pederson.
# Date: 1 May 2023
# Description: XOR cryptographic program. Intake a key and encode plaintext or decode a given ciphertext.
######################################################################################################################
# imports
import sys

# get ciphertext from stdin
user_in = sys.stdin.buffer.read()

# get key
f = open('key2', 'rb')
key = f.read()
f.close()

# xor byte conversion
conversion = bytes([_a ^ _b for _a, _b in zip(user_in, key)])

# output conversion to user
sys.stdout.buffer.write(conversion)