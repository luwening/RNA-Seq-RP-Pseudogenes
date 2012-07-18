#!/usr/local/bin/python
#for a bam/sam (assumed bam) file output a bam/sam (assumed sam) file viewing only regions with pseudogenes

import sys, subprocess
from getopt import getopt
from fileconversion import efficientFileRead
from bash import runCommand
from samtools import samtoolsViewRegions
from pseudogenes import load_all

if __name__ == "__main__":
	
	inSam = False
	outSam = False
	opts,args = getopt(sys.argv[1:],'sS')
	if len(args) < 2:
		print "usage: samtoolsViewPseudogenes.py infile outfile"
		sys.exit()
		
	filename = args[0]
	outfile = args[1]
	for opt,val in opts:
		if opt == "-s":
			inSam = True
		elif opt == "-S":
			outSam = True
	
	pseudogenes = load_all()
	
	viewString = ""
	for pseudogene in pseudogenes:
		viewString += pseudogene.chrom+":"+str(pseudogene.start)+"-"+str(pseudogene.end)+" "
	viewString = viewString[:-1]
	
	samtoolsViewRegions(filename,outfile,viewString)
