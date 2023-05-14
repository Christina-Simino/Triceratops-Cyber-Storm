######################################################################################################################
# Team: 7
# Member Names: Majd Tahat, Christina Simino, Jaden Box, Robert Emory, Jeremy Fountain, Anousith Keomaly, Ty Pederson.
# Date: 05 May 2023
# Description: Encodes and decodes files using steganography
#              When entering wrapper file and hidden file, be sure to enclose the argument in "".
#              Otherwise, it will separate the filename and extension at the period.
#              The - arguments are:
#               -s or -r    for storage or retrieval method
#               -b or -B    for bit mode or byte mode
#               -o          to specify an offset.  Default is 0.
#               -i          to specifiy an interval.  Default is 1.
#               -w          to specify wrapper file.  Enclose filename in ""
#               -h          to specify hidden file.  Not required for retrieval method.  Enclose filename in ""
######################################################################################################################
import sys
import os.path

# set default values
offset = 0
interval = 1
mode = "empty"
method = "empty"

FILE_PATH="empty"
HIDDEN_PATH="empty"
SENTINEL=bytearray(b'\x00\xff\x00\x00\xff\x00')

# get the command line arguments and classify them
args = []
for i in range(1,len(sys.argv)):
    args.append(sys.argv[i])

for arg in args:
    operator = arg[0:2]
    match operator:
        
        case '-s':
            if (method == "retrieve"):
                sys.stderr.write("use -s or -r, but not both please")
                exit()
            method = "store"
        case '-r':
            if (method == "store"):
                sys.stderr.write("use -s or -r, but not both please")
                exit()
            method = "retrieve"
        case '-b':
            if (mode == "byte"):
                sys.stderr.write("use -b or -B, but not both please")
                exit()
            mode = "bit"
        case '-B':
            if (mode == "bit"):
                sys.stderr.write("use -b or -B, but not both please")
                exit()
            mode = "byte"
        case '-o':
            offset = int(arg[2:])
        case '-i':
            interval = int(arg[2:])
        case '-w':
            if (os.path.exists(arg[2:])):
                FILE_PATH = arg[2:]
            else:
                sys.stderr.write("Invalid wrapper file!")
                exit()
        case '-h':
            if (os.path.exists(arg[2:])):
                HIDDEN_PATH = arg[2:]
            else:
                sys.stderr.write("Invalid hidden file!")
                exit()

if (method == "empty" or mode == "empty" or FILE_PATH == "empty" or (method == "store" and HIDDEN_PATH == "empty")):
    sys.stderr.write("Invalid usage.  Please follow: python Steg.py -(sr) -(bB) -o<val> [-i<val>] -w<val> [-h<val>]")
    exit()

# get the bytes from each file as a list
with open(FILE_PATH, "rb") as file:
    w = bytearray(file.read())

if (HIDDEN_PATH != "empty"):
    with open(HIDDEN_PATH, "rb") as file:
        h = bytearray(file.read())

# BYTE STORAGE
# THIS WORKS
def byteS(wrapper, hidden, offset, interval):
    i = 0
    while i < len(hidden):
        wrapper[offset] = hidden[i]
        offset += interval
        i += 1

    i = 0
    while i < len(SENTINEL):
        wrapper[offset] = SENTINEL[i]
        offset += interval
        i += 1
    return wrapper


# BYTE EXTRACTION
# THIS WORKS
def byteE(wrapper, offset, interval):

    hidden = bytearray()

    counter = 0
    while offset < len(wrapper):
        byte = wrapper[offset]

        # check if byte matches a sentinel byte
        if (byte == SENTINEL[counter]):
            counter += 1
        else:
            counter = 0
        if (counter >= len(SENTINEL)):
            return hidden[:-5]

        byte = byte.to_bytes(1, 'big')
        hidden += byte
        offset += interval

# BIT STORAGE
# THIS WORKS
def bitS(wrapper, hidden, offset, interval):

    # storing hidden file's bits
    i = 0
    while i < len(hidden):
        for j in range(8):
            wrapper[offset] &= 0b11111110
            wrapper[offset] |= ((hidden[i] & 0b10000000) >> 7)
            
            hidden[i] = (hidden[i] << 1) & (2 ** 8 - 1) # see pdf note on shifting
            offset += interval

        i += 1

    # storing the SENTINEL bits
    i = 0
    while i < len(SENTINEL):

        for j in range(8):
            wrapper[offset] &= 0b11111110
            wrapper[offset] |= ((SENTINEL[i] & 0b10000000) >> 7)
            SENTINEL[i] = (SENTINEL[i] << 1) & (2 ** 8 - 1) # see pdf note
            offset += interval
        i += 1

    return wrapper

# BIT EXTRACTION
# THIS WORKS
def bitE(wrapper, offset, interval):

    hidden = bytearray()

    counter = 0
    while offset < len(wrapper):
        byte = 0
        
        for j in range(8):
            byte |= (w[offset] & 0b00000001)
            if j < 7:
                byte = (byte << 1 % 8) & (2 ** 8 - 1) # see pdf note on shifting
                offset += interval


        byte=byte.to_bytes(1, 'big')

        # check if byte matches a sentinel byte
        if (byte == SENTINEL[counter].to_bytes(1, 'big')):
            counter += 1
        else:
            counter = 0
        if (counter >= len(SENTINEL)):
            return hidden[:-5]
            
        hidden += byte
        offset += interval


if (method == "store"):
    if (mode == "bit"):
        output = bitS(w, h, offset, interval)
    elif (mode == "byte"):
        output = byteS(w, h, offset, interval)
    else:
        sys.stderr.write("How did I get here?")
        exit()

else:
    if (mode == "bit"):
        output = bitE(w, offset, interval)
    elif (mode == "byte"):
        output = byteE(w, offset, interval)
    else:
        sys.stderr.write("How did I get here?")
        exit()

sys.stdout.buffer.write(output)
