from bash import runCommand
from fileconversion import efficientFileRead

def samtoolsViewRegion(bamfile,chrom,start,end,outfile):
	
	command = "samtools view " + bamfile + " " + chrom + ":" + str(start) + "-" + str(end)
	outf = open(outfile,"w")
	runCommand(command,outf,None)
	outf.close()
	
def samtoolsViewRegions(bamfile,outfile,regions):
	
	command = "samtools view -h " + bamfile + " " + regions
	outf = open(outfile,"w")
	runCommand(command,outf,None)
	outf.close()

def findBamAlignments(bamfile,chrom,start,end):
	
	samtoolsViewRegion(bamfile,chrom,start,end,"temp")
	alignRange = [start,end]
	def rangeCheck(line):
		if line[0] == "@":
				return #header line
		pieces = line.split()
		seqname = pieces[0]
		ch = pieces[2]
		pos = int(pieces[3])
		testnumber = int(pieces[1])

		if testnumber&0x4 == 0x4:
			pass
		else:
			if pos < alignRange[0]:
				alignRange[0] = pos
			if pos > alignRange[1]:
				alignRange[1] = pos
	efficientFileRead("temp",rangeCheck)
	
	def lineCheck(line):
		if line[0] == "@":
			return #header line
		pieces = line.split()
		seqname = pieces[0]
		ch = pieces[2]
		pos = int(pieces[3])
		testnumber = int(pieces[1])

		if testnumber&0x4 == 0x4:
			pass
		elif ch == chrom:
			ret[pos-start]+=1

	ret = [0 for x in range(alignRange[1]-alignRange[0]+1)]
	efficientFileRead("temp",lineCheck)
	runCommand("rm temp")	
	return ret

def findSamAlignments(samfile,start,end):
	ret = [0 for x in range(end-start+1)]
	
	def lineCheck(line):
			if line[0] == "@":
				return #header line
			pieces = line.split()
			seqname = pieces[0]
			pos = int(pieces[3])
			testnumber = int(pieces[1])
	
			if testnumber&0x4 == 0x4:
				pass
			else:
				ret[pos-start]+=1
				
	efficientFileRead(samfile,lineCheck)
	return ret
