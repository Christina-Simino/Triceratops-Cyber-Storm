#############################################################################################################
# Team: 7
# Member Names: Majd Tahat, Christina Simino, Jaden Box, Robert Emory, Jeremy Fountain, Anousith Keomaly, Ty Pederson.
# Date: 19 April 2023
# Description: Covert Chat Program.  Runs without any command-line arguments.
#			   Takes the timing between bits to find a covert message.
#############################################################################################################


# use Python 3
import socket
from sys import stdout
from time import time

# enables debugging output
DEBUG = False

# set the server's IP address and port
ip = "138.47.99.64"
port = 31337

# create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
s.connect((ip, port))
stdout.write("[connect to the chat server]\n...\n")
bit_message = ""
covert_message = "   "

# receive data until EOF
data = s.recv(4096).decode()
while (data.rstrip("\n") != "EOF" and covert_message[-3:] != "EOF"):
    # output the data
    stdout.write(data)
    stdout.flush()
    # start the "timer", get more data, and end the "timer"
    t0 = time()
    data = s.recv(4096).decode()
    t1 = time()
    # calculate the time delta (and output if debugging)
    delta = round(t1 - t0, 3)
    if (DEBUG):
        stdout.write(" {}\n".format(delta))
        stdout.flush()
    if (delta < 0.06):
        bit_message += "0"
    else:
        bit_message += "1"
    if len(bit_message) == 8:
        covert_message += chr(int(bit_message,2))
        bit_message = ""
            
# close the connection to the server
s.close()
stdout.write("...\n[disconnect from the chat server]\n...\n")

stdout.write("{}\n".format(covert_message[3:]))

