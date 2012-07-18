#!/usr/local/bin/python
#collect RPKM values across the supplied tissues and store in a table

import pseudogenes
import sys,getopt

root = "/zhang/ptonner/pseudo_rp/"
tissueLocation = root + "tables/rpkm/"


opts,args = getopt.getopt(sys.argv[1:],'')

tissues = args[0].split(",")

genes = pseudogenes.load_all()

geneDict = {}
table = {}
	
for tissue in tissues:
	ifile = open(tissueLocation+tissue+".rpkm.txt")
	for line in ifile.readlines():
		split = line.split()
		ident = split[3]
		rpkm = split[6]
		if ident not in table:
			table[ident] = dict()
		table[ident][tissue] = float(rpkm)

for gene in genes:
	geneDict[gene.pseudogeneID] = gene
	#table[gene.pseudogeneID] = {}
	if gene.pseudogeneID not in table:
		table[gene.pseudogeneID] = dict()
		for tissue in tissues:
			table[gene.pseudogeneID][tissue] = 0.0
	else:
		for tissue in tissues:
			if tissue not in table[gene.pseudogeneID]:
				table[gene.pseudogeneID][tissue] = 0.0

totals = []
#for ident in table.keys():
#	totals.append( ( max( table[ident].values() ), ident ) )

totals = [(max([val for val in table[ident].values()]),ident) for ident in table.keys()]
totals.sort()
totals.reverse()

header = "Parent Gene\tLocation\tPseudogene ID\tStrand\t"
for tissue in tissues:
	header+=tissue+"\t"
header+="max\ttotal"
print header
for val,ident in totals:
	
	outs = ""
	gene = geneDict[ident]
	outs += gene.gene+"\t"
	outs += gene.chrom+"_"+str(gene.start)+"_"+str(gene.end)+"\t"+gene.pseudogeneID+"\t"
	outs += gene.strand+"\t"
	for tissue in tissues:
		outs+=str(table[ident][tissue])+"\t"
	outs+=str(max([table[ident][tissue] for tissue in tissues]))+"\t"+str(sum([table[ident][tissue] for tissue in tissues]))
	print outs
		
