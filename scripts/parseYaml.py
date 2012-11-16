import sys

fileStream = open(sys.argv[1], 'r')
fileLines = []
for line in fileStream:
    fileLines.append(line)
onlineParserUrl = fileLines[0]
docDescription = fileLines[1]
cleanedUpDescription = docDescription.replace("#","")
    
resultFile = sys.argv[1] + ".parsed"
f = open(resultFile,'w')
f.write(cleanedUpDescription.strip() + "\n")
for index in range(len(cleanedUpDescription)):
    f.write("#")
f.write("\n")
f.write(".. code-block:: python\n")
f.write("\n")

indent = 4
for lineIndex in range(2,len(fileLines)):
    text = fileLines[lineIndex]
    for i in range (0, indent):
        text = " " + text
    f.write(text)
