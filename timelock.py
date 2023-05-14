######################################################################################################################
# Team: 7
# Member Names: Majd Tahat, Christina Simino, Jaden Box, Robert Emory, Jeremy Fountain, Anousith Keomaly, Ty Pederson.
# Date: 04 May 2023
# Description: Finds the difference in seconds from epoch and current time, double hashes it with md_5 and then
#              outputs a string containing the first two letters from left to right and last two numbers from
#              right to left. Make sure to install pytz module.
######################################################################################################################

import sys
import sys
import hashlib
import datetime
import pytz

DEBUG = False

# Takes the command line arguments gets rid of trailing 0s, converts to int, then puts it in a list
args = []
for line in sys.argv[1:]:
    # I didn't know this was a problem until the challenge
    if line == "00":
        line = "0"
    else:
        line = line.lstrip('0')
    args.append(int(line))

# sets the local timezone to CST
user_timezone = pytz.timezone("America/Chicago")

# when not debugging uses command line argument but if debugging uses hard coded values
if not DEBUG:
    epoch_time = datetime.datetime(args[0], args[1], args[2], args[3], args[4], 0, 0)
    current_time = datetime.datetime.now()
else:
    epoch_time = datetime.datetime(2023, 1, 1, 0, 0, 0)
    current_time = datetime.datetime(2017, 4, 21, 18, 2, 30)

# localizes the epoch time and then converts to utc
epoch_time = user_timezone.localize(epoch_time, is_dst = None)
epoch_time = epoch_time.astimezone(pytz.utc)

# localizes the current time and then converts to utc 
current_time = user_timezone.localize(current_time, is_dst = None)
current_time_copy = current_time
current_time = current_time.astimezone(pytz.utc)
current_time = current_time.replace(second=0, microsecond=0)

if DEBUG:
    epoch_time = epoch_time.replace(second=0, microsecond=0)
    print(epoch_time)
    print(current_time)

# calculates change in time and converts to seconds
delta_time = int((current_time - epoch_time).total_seconds())

# double hashing with md5
md5_hash = hashlib.md5(str(delta_time).encode()).hexdigest()
md5_hash = hashlib.md5(md5_hash.encode()).hexdigest()

# debugging to see the total hash
if DEBUG:
    print(md5_hash)

# variables/flags we wil be using to navigate around the md5_hash string
i = 0
letters = ""
nums = ""
len_md5_hash = len(md5_hash) - 1
len_letter = 0
len_num = 0
# process for getting the final output (getting first two letters and last two numbers)
while (i < len_md5_hash):
    if (len_letter == 2 and len_num == 2):
        break
    else:
        # gets first two letters 
        if (len_letter < 2 and md5_hash[i].isalpha()):
            letters += md5_hash[i]
            len_letter += 1
        # gets last two numbers
        if (len_num < 2 and not md5_hash[len_md5_hash - i].isalpha()):
            nums += md5_hash[len_md5_hash - i]
            len_num += 1
    i += 1
    
# putting the two together
code = letters + nums

# command line outputs
sys.stdout.write(code)
sys.stdout.write("\n________________________________________________________________\n")

# formats the string to include leading 0s if need be
strf_current_time = "{} {} {} {} {} {}".format(str(current_time_copy.year), str(current_time_copy.month).zfill(2), str(current_time_copy.day).zfill(2),
                                       str(current_time_copy.hour).zfill(2), str(current_time_copy.minute).zfill(2), str(current_time_copy.second).zfill(2))

sys.stdout.write("current system time: " + strf_current_time)




