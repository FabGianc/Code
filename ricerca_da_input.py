# lo script chiede all'utente di inserire il testo da cercare all'interno di un file

import os
import sys
import fileinput

print ("Text to search for:")
textToSearch = input( "> " )

print ("File to perform Search-Replace on: u_ex210831.log")
#fileToSearch  = input( "> " )
fileToSearch = 'C:\\Users\\u_ex210831.log'

tempFile = open( fileToSearch, 'r+' )
i = 0

for line in fileinput.input( fileToSearch ):
    if textToSearch in line :
        i= i+1
        print(i, " ", textToSearch, " --> ", line)

tempFile.close()

input( '\n\n Press Enter to exit...' )