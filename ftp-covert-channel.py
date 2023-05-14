#############################################################################################################
# Team: 7
# Member Names: Majd Tahat, Christina Simino, Jaden Box, Robert Emory, Jeremy Fountain, Anousith Keomaly, Ty Pederson.
# Date: 31 Mar 2023
# Description: FTP (storage) Covert Channel.  Runs without any command-line arguments.
#			   The folder and method are changed by altering the corresponding variables.
#############################################################################################################



from ftplib import FTP

# FTP server details
IP = "138.47.99.64"				#"localhost" for self
PORT = 21
USER = "anonymous"
PASSWORD = ""
FOLDER = "/7"		# "/" for root, "/7" for testing 7 bit, "/10" for testing 10 bit
USE_PASSIVE = True # set to False if the connection times out

# Decoding method:	7 or 10
METHOD = "7"

# connect and login to the FTP server
ftp = FTP()
ftp.connect(IP, PORT)
ftp.login(USER, PASSWORD)
ftp.set_pasv(USE_PASSIVE)

# navigate to the specified directory and list files
ftp.cwd(FOLDER)
files = []
ftp.dir(files.append)

# exit the FTP server
ftp.quit()

# the folder contents
file_listing = ""
for f in files:
    file_listing += (f + " ")

###### Converting the Permissions To Binary ######

permissions = file_listing.split()

# binary will contain an element for the permissions of each file, converted to binary
binary = []

counter = 0
for item in permissions:
	# grab just the permissions elements
	if (counter%9 == 0):
		bits = ""

		# checking each individual character to convert to proper bit
		for x in range(0, len(item)):
			if (item[x] == '-'):
				bits += "0"
			elif ((item[x] == 'r') or (item[x] == 'w') or (item[x] == 'x') or (item[x] == 'd')):
				bits += "1"

		binary.append(bits)
	counter += 1


###### Preparing message for decoding based on method ######

m = ""

if (METHOD == "10"):
	for code in binary:
		m += code

if (METHOD == "7"):
	for code in binary:
		# filter out files that have noise in the first 3 bits
		if ((code[0] == '0') and (code[1] == '0') and (code[2] == '0')):
			string = code[3:]
			m += string

###### Decoding Message ######
# this is borrowed from the binary decoder program

lenm = len(m)
if(lenm % 7 == 0):
    c = 7
    for i in range(int(lenm / c)):
        print(chr(int(m[i*c:i*c + c],2)), end='')
    print("")
