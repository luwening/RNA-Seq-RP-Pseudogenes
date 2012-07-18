#!/usr/local/bin/python

genomeLocation = "/zhang/ptonner/hg18/"
chromosomes = ["chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22","chr23","chrX","chrY","chrM"]

genome = dict()
visited = []

def readChrom(chrom):
	if chrom in visited:
		return
	for line in open(genomeLocation+chrom+".fa").readlines():
		if line[0]==">":
			target = line.strip(">\n").lower()
		else:
			if target in genome:
				genome[target].append(line.strip())
			else:
				genome[target]=[line.strip()]
	visited.append(chrom)

def search(chrom,start,end):
	readChrom(chrom)
	if chrom in genome and len(genome[chrom]) * len(genome[chrom][0]) > end+1:
		seqLen = len(genome[chrom][0])
		seqs = start/seqLen+1
		seqStart = start%seqLen
		seqe = end/seqLen+1
		seqEnd = end%seqLen
		out = ""
		if seqs == seqe:
			out+=genome[chrom.lower()][seqs][seqStart:seqEnd+1]+"\n"
		else:
			out+=genome[chrom.lower()][seqs][seqStart:]+"\n"
			while seqs < seqe - 1 :
				out+=genome[chrom.lower()][seqs]+"\n"
				seqs+=1
			
			out+=genome[chrom.lower()][seqs][:seqEnd]+"\n"
		
		return out
	return "FAIL"

if __name__=="__main__":
	
	import sys,getopt
	import re
	
	opts,args = getopt.getopt(sys.argv[1:],'')
	inputFile = args[0]	
	
	for line in open(inputFile).readlines():
		line = line.strip()
		m = re.search("(chr[0-9]*):([0-9]*)-([0-9]*)",line)
		if m == None:
			continue
		chrom = m.group(1)
		start = int(m.group(2))
		end = int(m.group(3))
		print ">"+line
		print search(chrom,start,end)
		
