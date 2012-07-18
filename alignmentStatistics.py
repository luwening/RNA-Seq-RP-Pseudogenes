from bash import runCommand

alignLoc = "/zhang/ptonner/ribo_proteins/"

tissues = ["adipose","adrenal","brain","breast","colon","heart","kidney","liver","lung","lymph","muscle","ovary","prostate","testes","thyroid","whiteBloodCells"]

outTable = []

def getTotalAlignments(f):
	runCommand("samtools idxstats " + f,open("temp","w"))
	total = 0
	for line in open("temp").readlines():
		total+=int(line.split()[2])
	runCommand("rm temp")
	return total

for tissue in tissues:
	
	one = getTotalAlignments(alignLoc+tissue+"/"+tissue+".sorted.bam")
	two = getTotalAlignments(alignLoc+tissue+"/"+tissue+".unique.sorted.bam")
	three = getTotalAlignments(alignLoc+tissue+".hg18/"+tissue+".hg18.unique.sorted.bam")
	
	outTable.append((tissue,one,two,three))

print "Tissue\tTotal Alignments (composite)\tTotal Unique Alignments (composite)\tTotal Unique Alignments (hg18)"
for tissue,one,two,three in outTable:
	print tissue+"\t"+str(one)+"\t"+str(two)+"\t"+str(three)
