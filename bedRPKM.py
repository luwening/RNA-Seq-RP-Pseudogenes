#!/usr/local/bin/python
#from a bed alignment file and uniquely mappable locations bed file, compute the rpkm gene locations

import sys
from getopt import getopt
from bedtools import findBedAlignmentsByName
from rpkm import rpkm

if __name__ == "__main__":
	
	opts,args = getopt(sys.argv[1:],'')
	
	if len(args) < 3:
		print "bedRPKM.py alignment.bed uniqueLocations.bed totalAlignments"
		sys.exit()
	
	alignmentFile = args[0]
	uniqueFile = args[1]
	total = int(args[2])
	
	alignments = findBedAlignmentsByName(alignmentFile)
	pseudogenes = findBedAlignmentsByName(uniqueFile)
	
	for gene in alignments.keys():
		if gene in alignments and gene in pseudogenes:

			alignLine = alignments[gene][0]
			#find the beginning and end of the gene
			minStart,maxEnd = 987654321,0
			for line in alignments[gene]:
				if line.start < minStart:
					minStart = line.start
				if line.end > maxEnd:
					maxEnd = line.end
			chrom = alignLine.chrom
			count = sum([line.thickStart for line in alignments[gene]])#alignments[gene][0].thickStart
			mappableLocations = sum([line.thickStart for line in pseudogenes[gene]])
			
			r = rpkm(count,mappableLocations,total)
			print gene + "\t" + chrom + "\t" + str(minStart) + "\t" + str(maxEnd) + "\t" + str(count) + "\t" + str(mappableLocations) + "\t" + str(r)
		else:
			print gene + "\t-"
