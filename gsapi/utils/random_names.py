'''
Created on: 2011-06-13
Last update: nil
Kulverstukas
http://9v.lt/projects/python/RandomName/GeneratedNames.py
'''

import sys
import os
import string
import random

#==============================
def GetFromArg(What, FromWhere):
    for GotArg in FromWhere:
        if string.find(GotArg, What) != -1:
            GotArg = string.replace(GotArg, What, '')
            break
    return GotArg 
#==============================
print
print 'Random name generator - takes a list, randomly picks out 2 words and puts them together to make a full name'
print 'Command line arguments:  --list=NAME -- file with names'
print '                         --number=X -- number of names to generate'
print 'This script automagicaly writes everything to a file where the script was ran'
#==============================
arguments = sys.argv[1:]
if len(arguments) < 2:
    print 'Not enough arguments, nigger!'
    exit()
#==============================
list = GetFromArg('--list=',arguments)
number = GetFromArg('--number=',arguments)
number = int(number)
#==============================
if os.path.isdir(list) == True:
    print 'File does not exist!'
    exit()
try:     
    ListOfNames = [] # initiate the array
    FileWithNames = file(list,'r') # assign the file
    for Temp in FileWithNames: # read whole file into an array
        ListOfNames.append(string.strip(Temp))
    FileWithNames.close()    
except:
    print 'Something went wrong :( exiting...'
    exit()    
#==============================
TempInt = 0
GeneratedNameArray = []  # initiate another array
GeneratedName = '' 
while TempInt != number:
    RandNumb1 = random.randint(1,len(ListOfNames)-1)
    RandNumb2 = random.randint(1,len(ListOfNames)-1)
    GeneratedNameArray.append(ListOfNames[RandNumb1]+' '+ListOfNames[RandNumb2])
    TempInt = TempInt + 1    
#==============================
FileWithNames = file('Generated_names','w')
for Temp in GeneratedNameArray: FileWithNames.write(Temp+'\r\n')
FileWithNames.close()
print
print 'Successfully generated '+str(number)+' names!'
#==============================
