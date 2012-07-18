import sys,getopt,bash

opts,args = getopt.getopt(sys.argv[1:],'')

#read 500 MB at a time
readSize = 524288000

if len(args) < 2:
	print "Usage: hugeDiff.py file1 file2"

file1 = open(args[0])
file2 = open(args[1])

file1Buffer = file1.readlines(readSize)
file2Buffer = file2.readlines(readSize)
result = []

while len(file1Buffer) > 0 or len(file2Buffer) > 0:

	#write temporary files
	of1 = open("temp1.txt","w")
	of2 = open("temp2.txt","w")
	
	#write lines to temporary files
	ind = min(len(file1Buffer),len(file2Buffer))
	of1.writelines(file1Buffer[:ind])
	of2.writelines(file2Buffer[:ind])
	of1.close()
	of2.close()
	
	#erase used buffer lines
	if ind < len(file1Buffer):
		file1Buffer = file1Buffer[ind:]
	else:
		file1Buffer = []
	if ind < len(file2Buffer):
		file2Buffer = file2Buffer[ind:]	
	else:
		file2Buffer = []
	
	#run diff
	bash.runCommand("diff temp1.txt temp2.txt",open("diff.txt","w"),None)
	
	#read result
	result.extend(open("diff.txt").readlines())
	
	#refill buffers
	file1Buffer.extend(file1.readlines(readSize))
	file2Buffer.extend(file2.readlines(readSize))

bash.runCommand("rm temp1.txt")
bash.runCommand("rm temp2.txt")
bash.runCommand("rm diff.txt")

for line in result:
	print line.strip()
