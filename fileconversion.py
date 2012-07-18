#!/usr/local/bin/python
	

def efficientFileRead(fname, callback, bytesize=100000):
	
	ifile = open(fname)
	while True:
		lines = ifile.readlines(bytesize)
		if not lines:
			break
		for line in lines:
			line = line[:-1]
			callback(line)
		del lines
	ifile.close()

def Sam2Fasta(samfile,outfile,targets=None):

	ofile = open(outfile,"w")
	
	def checkSamLine(line):
		if line[0] == "@":
			return
		else:
			query = line.split()[0]
			subject = line.split()[2]
			pos = line.split()[3]
			seq = line.split()[9]
			
			if targets == None or subject in targets:
				ofile.write(">"+query+"|"+subject+"|"+pos+"\n")
				ofile.write(seq)
				
	efficientFileRead(samfile,checkSamLine)
	ofile.close()
	
def zipFasta(files,outfile):
	
	ofile = open(outfile,"w")
	
	def appendFile(line):
		
		temp = open(line)
		def copyLine(line):
			ofile.write(line)
			
		efficientFileRead(line,copyLine)
	
	efficientFileRead(files,appendFile)
	ofile.close()


if __name__ == "__main__":
	
	import sys,getopt
	
	opts,args = getopt.getopt(sys.argv[1:],'-z-s')
	
	for opt,val in opts:
		if opt == "-s":
			targets = args[2].split(",")
			Sam2Fasta(args[0],args[1],targets)
			break
		elif opt == "-z":
			zipFasta(args[0],args[1])
			break
