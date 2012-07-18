#!/usr/local/bin/python
#take an input BED and extend each region by a specified length

import sys, getopt
import bedtools
from fileconversion import efficientFileRead

if __name__ == "__main__":
	
	opts, args = getopt.getopt(sys.argv[1:],"")
	if len(args) < 2:
		print "expandBed.py filename length"
		sys.exit()
	
	filename = args[0]
	try:
		length = int(args[1])
	except ValueError:
		print "expandBed.py filename length"
		print "expecting int value for length"
		sys.exit()
	
	def lineParse(line):
		split = line.split("\t")
		sc = 1
		try:
			int(split[3])
			sc = split[3]
			line = bedtools.BEDLine(split[0],split[1],split[2],score = sc)
		except:
			sc = split[4]
			line = bedtools.BEDLine(split[0],split[1],split[2],split[3],score = sc)
		
		print line.chrom + "\t" + str(line.start) + "\t" + str(line.end+length) + "\t" + line.name + "\t" + str(line.score) + "\t" + line.strand
	
	efficientFileRead(filename,lineParse)
	
	#lines = bedtools.BEDFile(filename).lines
	
	#for line in lines:
	#	for i in range(line.start,line.end+1):
	#		print line.chrom + "\t" + str(i) + "\t" + str(i+length) + "\t" + line.name + "\t" + line.score + "\t" + line.strand
