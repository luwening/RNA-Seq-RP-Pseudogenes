#!/usr/local/bin/python
#from a bed alignment file and uniquely mappable locations bed file, compute the rpkm for pseudogene locations

import sys
from getopt import getopt
from bedtools import findBedAlignmentsByName
from rpkm import rpkm

if __name__ == "__main__":
	
	opts,args = getopt(sys.argv[1:],'')
	
	if len(args) < 3:
		print "Usage: pseudogeneRPKM.py alignment.bed uniqueLocations.bed totalAlignments"
		sys.exit()
	
	alignmentFile = args[0]
	uniqueFile = args[1]
	total = int(args[2])
	
	alignments = findBedAlignmentsByName(alignmentFile)
	pseudogenes = findBedAlignmentsByName(uniqueFile)
	
	for gene in alignments.keys():
			
		alignLine = alignments[gene][0]
		chrom = alignLine.chrom
		start = alignLine.start
		end = alignLine.end
		count = sum([line.thickStart for line in alignments[gene]])#alignments[gene][0].thickStart
		r = 0.0
		
		if gene in pseudogenes:
			#mappableLocations = sum([line.length() for line in pseudogenes[gene]])
			mappableLocations = sum([line.thickStart for line in pseudogenes[gene]])
			r = rpkm(count,mappableLocations,total)
		else:
			print gene
			
		print chrom + "\t" + str(start) + "\t" + str(end) + "\t" + gene + "\t" + str(count) + "\t" + str(mappableLocations) + "\t" + str(r)
