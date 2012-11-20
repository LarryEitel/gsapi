import csv

isoCountryNameCodes = [] #list of tuples (name, code)
utcOffsets = [] #list of tuples (zone, UTC offset without DST, UTC offset with DST)

with open('isoCountryNamesCodes.txt', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    line_no = 1
    for row in spamreader:
        test = (','.join(row))
        if line_no > 2: 
            #print ', '.join(row)
            isoCountryNameCodes.append(test)
        line_no = line_no + 1
        
with open('utcoffset.txt', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter = ';')
    line_no = 1
    for row in spamreader:
        if line_no > 3: 
            test = (','.join(row))
            utcOffsets.append(test)
        line_no = line_no + 1
        