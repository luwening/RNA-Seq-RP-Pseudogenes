#!/usr/local/bin/python
#collect RPKM values across the supplied tissues and store in a table

import rpgenes
import sys,getopt

root = "/zhang/ptonner/"
tissueLocation = root + "ribo_proteins/"

def countReadsAligned(fname):
	count = 0
	for line in open(fname).readlines():
		if line[0:3] == "chr":
			count += int(line.split("\t")[2])
	return count

opts,args = getopt.getopt(sys.argv[1:],'')

tissue = args[0]

genes = rpgenes.load_all()

geneDict = {}
table = {}
for g in genes:
	geneDict[g.gene] = g
	
ifile = open(tissueLocation+tissue+"/"+tissue+".rpgenes.rpkm.txt")
for line in ifile.readlines():
	split = line.split()
	ident = split[0]
	alignments = split[4]
	length = split[5]
	rpkm = float(split[6])
	table[ident] = {}
	table[ident]["alignments"] = alignments
	table[ident]["length"] = length
	table[ident]["rpkm"] = rpkm

ifile.close()
ifile = open(tissueLocation+tissue+"/"+tissue+".rpgenes.uniquePositions.txt")
for line in ifile.readlines():
	split = line.split()
	ident = split[3]
	unique = split[4]
	table[ident]["unique"] = unique
		
totals = [(table[ident]["rpkm"],ident) for ident in geneDict.keys()]
totals.sort()
totals.reverse()

totalAlignments = countReadsAligned(tissueLocation+tissue+"/"+tissue+".unique.idxstats.txt")
header = tissue + ": " + str(totalAlignments) + " alignments in uniqueome 4 regions\n\
Gene\tPosition\tUnique Alignments\tUnique Positions\tGene Length\tUniqueome 4 Length\tRPKM"
print header
for val,ident in totals:
	
	outs = ""
	gene = geneDict[ident]
	
	outs += ident + "\t"
	outs += gene.chrom+":"+str(gene.start)+"-"+str(gene.end)+"\t"
	outs += table[ident]["alignments"] + "\t"
	outs += table[ident]["unique"] + "\t"
	outs += str(gene.end-gene.start) +"\t"
	outs += table[ident]["length"] + "\t"
	outs += str(table[ident]["rpkm"])
	
	print outs
		
