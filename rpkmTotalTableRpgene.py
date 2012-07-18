#!/usr/local/bin/python
#collect RPKM values across the supplied tissues and store in a table

import rpgenes
import sys,getopt

root = "/zhang/ptonner/"
tissueLocation = root + "ribo_proteins/"

opts,args = getopt.getopt(sys.argv[1:],'')

tissues = args[0].split(",")

genes = rpgenes.load_all()

geneDict = {}
table = {}
for gene in genes:
	geneDict[gene.gene] = gene
	table[gene.gene] = {}
	
for tissue in tissues:
	ifile = open(tissueLocation+tissue+"/"+tissue+".rpgenes.rpkm.txt")
	for line in ifile.readlines():
		split = line.split()
		ident = split[0]
		rpkm = split[6]
		table[ident][tissue] = float(rpkm)
		
totals = [(sum(table[ident].values()),ident) for ident in geneDict.keys()]
totals.sort()
totals.reverse()

header = "Gene\tLocation\t"
for tissue in tissues:
	header+=tissue+"\t"
header+="average\ttotal"
print header
for val,ident in totals:
	
	outs = ""
	gene = geneDict[ident]
	outs += gene.gene+"\t"
	outs += gene.chrom+"_"+str(gene.start)+"_"+str(gene.end)+"\t"
	for tissue in tissues:
		outs+=str(table[ident][tissue])+"\t"
	outs+=str(val/len(tissues))+"\t"+str(val)
	print outs
		
