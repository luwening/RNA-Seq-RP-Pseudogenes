#!/usr/local/bin/python
#count the number of unique positions aligned to in each pseudogene region

import pseudogenes,rpgenes
import bedtools
import samtools
import sys,getopt

rpgenes = False

opts,args = getopt.getopt(sys.argv[1:],'')
for opt,arg in opts:
	if opt == "-r":
		rpgenes = True
geneFile = args[0]
alignmentFile = args[1]

genes = []
"""
if not rpgenes:
	genes = pseudogenes.load_all()
else:
	genes = rpgenes.load_all()
"""
genes = bedtools.findBedAlignmentsByName(geneFile)
	
for k in genes.keys():
	
	total = 0
	mn = 987654321
	mx = 0
	for gene in genes[k]:
		if gene.start < mn:
			mn = gene.start
		if gene.end > mx:
			mx = gene.end
		alignments = samtools.findBamAlignments(alignmentFile,gene.chrom,gene.start,gene.end)
		for alignment in alignments:
			if alignment > 0:
				total+=1
	
	print gene.chrom + "\t" + str(mn) + "\t" + str(mx) + "\t" + k + "\t" + str(total)

	

