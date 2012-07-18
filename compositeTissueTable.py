#!/usr/local/bin/python

import sys, getopt, subprocess
import ostools
from fileconversion import efficientFileRead

opts,args = getopt.getopt(sys.argv[1:],'rht:')
#tissues = ['adipose','adipose.hg18','adrenal','brain','breast','colon','heart','kidney','liver','lung','lymph','muscle','ovary','prostate','testes','thyroid','whiteBloodCells']
tissues = ['adipose','adrenal','brain','breast','colon','heart','kidney','liver','lung','lymph','muscle','ovary','prostate','testes','thyroid','whiteBloodCells']

tissueLocation = args[0]
RPKM = False
HTML = False
Limit = 0
for opt,val in opts:
	if opt=="-r":
		RPKM = True
	elif opt=="-h":
		HTML = True
	elif opt=="-t":
		Limit=int(val)
		
def readMappability(fname):
	ifile = open(fname)
	mapp = dict()
	for line in ifile.readlines():
	
		line = line[:-1]
		pieces = line.split()
		piece = pieces[0].split("_")
		gene = piece[0]
		chrom = piece[1]
		start = piece[2]
		end = piece[3]
		mapp[(gene,chrom,start,end)] = int(pieces[1])
		
	ifile.close()
	return mapp
	
mapp2 = readMappability(tissueLocation + "/mappability/" + "mappability.2mis")

genef = open("/nas/ptonner/genes/pseudo.names")
genes = []
for gene in genef.readlines():
	piece = gene.split()[0].split("_")
	gene = piece[2]
	chrom = piece[3]
	start = piece[4]
	end = piece[5]
	genes.append((gene,chrom,start,end))

table = dict()
for tissue in tissues:
	readsInDataSet = None
	if RPKM:
		#collect alignment information
		alignmentInfo = open(tissueLocation + tissue + "/" + tissue+".out")
		readsInDataSet = int(alignmentInfo.readline().split(":")[1])
		readsAligned = int(alignmentInfo.readline().split(":")[1].split("(")[0])
		alignmentInfo.close()
		
	for line in open(tissueLocation + tissue + "/" + tissue + ".mappability").readlines():
		line = line[:-1]
		tag = line.split()[0]
		count = int(line.split()[1])
		piece = tag.split("_")
		gene = piece[0]
		chrom = piece[1]
		start = piece[2]
		end = piece[3]
		if not (gene,chrom,start,end) in table: 
			table[(gene,chrom,start,end)] = dict()
		if RPKM:
			if mapp2[(gene,chrom,start,end)] > 0:
				rpkm = float(count*1000*1000000)/mapp2[(gene,chrom,start,end)]/readsAligned
				table[(gene,chrom,start,end)][tissue] = rpkm
			else:
				table[(gene,chrom,start,end)][tissue] = -1
		else:
			table[(gene,chrom,start,end)][tissue] = count

total = dict()
for gene,tissueCount in table.iteritems():
	for tissue,count in tissueCount.iteritems():
		if gene in total:
			total[gene] += count
		else:
			total[gene] = count
table['total'] = total

sortedValues = [(count,gene) for gene,count in total.iteritems()]
sortedValues.sort()
sortedValues.reverse()

if Limit > 0:
	sortedValues = sortedValues[:Limit+1]

if not HTML:
	headerLine = "Gene name\tGenome location\t"
	for tissue in tissues:
		headerLine += tissue + "\t"
	headerLine += "total\taverage"
	print headerLine

	for count,gene in sortedValues:
		line = gene[0]+"\t"+gene[1]+":"+gene[2]+"-"+gene[3]+"\t"
		for tissue in tissues:
			if tissue in tissueCount:
					line += str(table[gene][tissue])+"\t"
			else:
				line += "*\t"
		if gene in total:
				line += str(total[gene])+"\t"
				line += str(float(total[gene])/len(tissues))
		else:
			line += "*\t*"
		print line
else:
	
	#html row generators
	def rowData(data,cls,di,tag):
		return "<"+tag+" id=\""+di+"\" class=\""+cls+"\" >" + str(data) + "</"+tag+">"
	
	def headerRowData(data,cls="",di=""):
		return rowData(data,cls,di,"th")
	
	def regRowData(data,cls="",di=""):
		return rowData(data,cls,di,"td")

	#header
	print "<html>\n<head>\n<style type=\"text/css\">\n"
	#basic table format
	print "#table\
		{\
		font-size:11;\
		font-family:\"Trebuchet MS\", Arial, Helvetica, sans-serif;\
		width:100%;\
		border-collapse:collapse;\
		}"
	print "#table td, #table th \
		{\
		border:1px solid #98bf21;\
		}"
	#header format
	print "#table th \
		{\
		text-align:left;\
		background-color:#A7C942;\
		color:#ffffff;\
		}"
	#alternating row colors
	print "#table tr.alt td \
		{\
		color:#000000;\
		background-color:#80F2D1;\
		}"
	#above ten coloring (g10)
	print "#table tr td.g10 , #table tr.alt td.g10\
		{\
		color:#000000;\
		background-color:#FF0000;\
		}"
	#above three coloring (g3)
	print "#table tr td.g3 , #table tr.alt td.g3\
		{\
		color:#000000;\
		background-color:#FFFF33;\
		}"
	#above one coloring (g1)
	print "#table tr td.g1 , #table tr.alt td.g1\
		{\
		color:#000000;\
		background-color:#00CC00;\
		}"
	#end header, start body and table
	print "</style>\
		</head>\
		<body>\
		<table id=\"table\">"
	#table header
	print "<tr id=\"header\">"
	print headerRowData("Gene name")
	print headerRowData("Genome location")
	for tissue in tissues:
		print headerRowData(tissue)
	print headerRowData("total")
	print headerRowData("average")
	print "</tr>"
	#pseudogene data
	for count,gene in sortedValues:
		print "<tr>"
		print regRowData(gene[0])
		print regRowData(gene[1]+":"+gene[2]+"-"+gene[3])
		for tissue in tissues:
			if tissue in tissueCount:
				data = table[gene][tissue]
				if data > 10:
					print regRowData(table[gene][tissue],"g10")
				elif data > 3:
					print regRowData(table[gene][tissue],"g3")
				elif data > 1:
					print regRowData(table[gene][tissue],"g1")
				else:
					print regRowData(table[gene][tissue])
			else:
				print regRowData("*")
		if gene in total:
			print regRowData(total[gene])
			print regRowData(float(total[gene])/len(tissues))
		else:
			print regRowData("*")
			print regRowData("*")
		print "</tr>"
	print "</table>\
		</body>\
		</html>"
		
		
