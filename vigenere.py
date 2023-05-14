#############################################################################################################
# Team: 7
# Member Names: Majd Tahat, Christina Simino, Jaden Box, Robert Emory, Jeremy Fountain, Anousith Keomaly, Ty Pederson.
# Date: 22 Mar 2023
# Description: Vigenere encoder and decoder
# How to run:
#            Run using Linux terminal. Make sure you are using python 3.10 or higher or else the code won't work.
#            To encode, the keyword is -e and decode it is -d. Only use one or the other. Code will produce nothing if any other argument is given.
#            First type "python3 vigenere.py <-e/-d> <your key>" and then enter. You may need to wrap your key with quotations if there are spaces. 
#            Then type "<plaintext/ciphertext>" once finished press enter and then ctrl + d. 
#
# Additional Notes:
#            Key only takes alphabetical characters (a-z and A-Z) or spaces. Numbers or symbols will break the code.
#            However, the input (plaintext/ciphertext) can take characters, spaces, numbers, and symbols.
#            The encoding/decoding process will only apply to characters meaning anything else is retained in the ouput.
#############################################################################################################

# Modules
import sys

# Function(s)
def create_list(x,y):               # for this implementation it maps the order of the alphabet according to an index
    ret_list = []                   # and returns the list
    for i in range(x,y):
        ret_list.append(chr(i))
    return ret_list

# Main Code
mode = sys.argv[1]  
key = sys.argv[2]
text = sys.stdin.read()

key_copy = key.replace(" ", "")     # removes any space within the key and stores as a copy since we will reuse the key variable later
key_copy_length = len(key_copy) 
index = 0
key = ""

for i in text:                      # here we make the key length the same length as our plaintext/ciphertext so that way we can properly encode/decode
    if i.isalpha():                 
        key += key_copy[index % key_copy_length]    
        index += 1
    else:
        key += " "                  # this way anytime the plaintext/ciphertext has a non alphebtical character it is skipped as the key tries to match its length
                                    # ex. output with key as the key:     plaintext: hello world
                                    #                                     key:       keyke ykeyk
new_text = ""

upper = create_list(65,91)          # contains A-Z
lower = create_list(97,123)         # contains a-z

for i in range(len(text)):
    # if the plaintext/cipher text contains symbols, numbers, or spaces its retained during the encode/decode process
    if not text[i].isalpha():
        new_text += text[i]
    else:
        # changes which list we are using depending if the text is uppercase and makes sure the key's character is capitalized if text is capitalized  
        if text[i].isupper():
            letter_mode = upper
            key_char = key[i].upper()
        else:
            letter_mode = lower
            key_char = key[i].lower()

        # this keyword functions like switch case from java
        match mode:
            
            case '-e':
                new_text += letter_mode[(letter_mode.index(text[i]) + letter_mode.index(key_char)) %26]
                
            case '-d':
                new_text += letter_mode[(26 + letter_mode.index(text[i]) - letter_mode.index(key_char)) %26]

sys.stdout.write(new_text)


            
        
    
    
