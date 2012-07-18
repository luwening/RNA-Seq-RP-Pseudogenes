#!/usr/local/bin/python
#analyze a supplied tissue

from bash import runCommand,changeDir
import sys,getopt

#setup filesystem constants
root = "/zhang/ptonner/pseudo_rp/"
tissueLocation = root + "redo/"
uniqueomeLocation = root+ "uniqueome/"
uniqueomeBed = uniqueomeLocation + "hg18_uniqueome.unique_starts.base-space.75.4.positive.extend75.bed"
genesLocation = root + "genes/"
pseudogeneBed = genesLocation + "pseudogenes.bed"
scriptsLocation = "/home/ptonner/projects/pseudo_rp/"

def countReadsAligned(fname):
	count = 0
	for line in open(fname).readlines():
		if line[0:3] == "chr":
			count += int(line.split("\t")[2])
	return count



opts,args = getopt.getopt(sys.argv[1:],'')

tissue = args[0]

changeDir(tissueLocation+tissue+"/")
errfile = open(tissue+".rpkmPipeline.err","a")
totalAlignments = 1

commands1 = [
#Intersect tissue with uniqueome
("intersectBed -abam " + tissue+".sorted.bam -b " + uniqueomeBed + " -f 1.0", tissue+".unique.bam"),
#Sort and Index Bam file
("samtools sort " + tissue+".unique.bam " + tissue + ".unique.sorted",None),
("samtools index " + tissue + ".unique.sorted.bam",None),
("samtools idxstats " + tissue + ".unique.sorted.bam",tissue+".unique.idxstats.txt")
]
for command,outfile in commands1:
	errfile.write("\n\nRUNNING: " + command + "\n")
	if outfile == None:
		runCommand(command,None,errfile)
	else:
		runCommand(command,open(outfile,"w"),errfile)
	#runCommand(command,open(outfile,"w"),errfile)
	#print command + " > " + str(outfile)
#Count total number of mapped reads

totalAlignments = countReadsAligned(tissue+".unique.idxstats.txt")


commands2 = [
#Collect reads in pseudogene locations
("intersectBed -abam " + tissue + ".unique.bam -b " + pseudogeneBed,tissue+".unique.pseudo.bam"),
("bamToBed -i " + tissue+".unique.pseudo.bam", tissue+".unique.pseudo.bed"),
#Count unique regions
("intersectBed -c -a " + pseudogeneBed + " -b " + tissue+".unique.pseudo.bed",tissue+".pseudo.align.bed"),
#Calculate RPKM
(scriptsLocation+"pseudogeneBedRPKM.py " + tissue+".pseudo.align.bed " + uniqueomeLocation + "hg18_uniqueome.pseudo.align.bed " + str(totalAlignments),tissue+".rpkm.txt"),
#Count unique positions of alignment
(scriptsLocation+"countUniquePositions.py " + tissue+".unique.sorted.bam", tissue+".pseudo.uniquePositions.txt")
]
for command,outfile in commands2:
	errfile.write("\n\nRUNNING: " + command + "\n")
	if outfile == None:
		runCommand(command,None,errfile)
	else:
		runCommand(command,open(outfile,"w"),errfile)
	#print command + " > " + str(outfile)
