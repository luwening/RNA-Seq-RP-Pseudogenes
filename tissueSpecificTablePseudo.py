#!/usr/local/bin/python
#collect RPKM values across the supplied tissues and store in a table

import pseudogenes
import sys,getopt

root = "/zhang/ptonner/pseudo_rp/"
tissueLocation = root + "redo/"

def countReadsAligned(fname):
	count = 0
	for line in open(fname).readlines():
		if line[0:3] == "chr":
			count += int(line.split("\t")[2])
	return count

opts,args = getopt.getopt(sys.argv[1:],'')

tissue = args[0]

genes = pseudogenes.load_all()

geneDict = {}
table = {}
for gene in genes:
	geneDict[gene.pseudogeneID] = gene
	
ifile = open(tissueLocation+tissue+"/"+tissue+".rpkm.txt")
for line in ifile.readlines():
	split = line.split()
	ident = split[3]
	alignments = split[4]
	length = split[5]
	rpkm = float(split[6])
	table[ident] = {}
	table[ident]["alignments"] = alignments
	table[ident]["length"] = length
	table[ident]["rpkm"] = rpkm
	
ifile.close()
ifile = open(tissueLocation+tissue+"/"+tissue+".pseudo.uniquePositions.txt")

for line in ifile.readlines():
	split = line.split()
	ident = split[3]
	unique = split[4]
	table[ident]["unique"] = unique
	
ifile = open(root+"genes/geneIdentities.txt")

for line in ifile.readlines()[1:]:
	split = line.split()
	ident = split[0]
	parent = split[1]
	pos = split[2]
	val = split[3]
	if ident in table:
		table[ident]["identity"] = val
	else:
		pass#print "Missing:",ident
		
totals = [(table[ident]["rpkm"],ident) for ident in table.keys()]
totals.sort()
totals.reverse()

totalAlignments = countReadsAligned(tissueLocation+tissue+"/"+tissue+".unique.idxstats.txt")
header = tissue + ": " + str(totalAlignments) + " alignments in uniqueome 4 regions\n\
Pseudogene\tPosition\tUnique Alignments\tUnique Positions\tGene Length\tUniqueome 4 Length\tSequence Identity\tStrand\tRPKM"
print header
for val,ident in totals:
	
	outs = ""
	gene = geneDict[ident]
	
	outs += gene.gene+"_"+gene.chrom+"_"+str(gene.start)+"_"+str(gene.end)+"\t"+gene.chrom+":"+str(gene.start)+"-"+str(gene.end)+"\t"
	outs += table[ident]["alignments"] + "\t"
	outs += table[ident]["unique"] + "\t"
	outs += str(gene.end-gene.start) +"\t"
	outs += table[ident]["length"] + "\t"
	outs += table[ident]["identity"] + "\t"
	outs += gene.strand + "\t"
	outs += str(table[ident]["rpkm"])
	
	print outs
		
