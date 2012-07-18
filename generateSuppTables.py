
import getopt,sys
import web.html

opts,args = getopt.getopt(sys.argv[1:],'')

outLoc = args[0]

tableLocation = "/zhang/ptonner/pseudo_rp/tables/rpkm/"
alignLocation = "/var/www/html/ptonner/alignments/"
uniqueLocation = "/var/www/
tissues = ['adipose','adrenal','brain','breast','colon','heart','kidney','liver','lung','lymph','muscle','ovary','prostate','testes','thyroid','whiteBloodCells']

table = {}

for tissue in tissues:
	
	ifile = open(tableLocation+tissue+".rpkm.txt")
	
	#initialize table with header row
	elems = [["RP Pseudogene","Reads Aligned","Gene Length","RPKM"]]
	
	#parse all lines to add to the table
	for line in ifile.readlines():
		split = line.split()
		elems.append(split[3:])
		
	ofile = open(outLoc+tissue+".html","w")
	
	outLines.append(alignmentLoadString(tissue,alignLocation+tissue+".unique.sorted.bam"))
	outLines.append(readCoverageLoadString(tissue))
	outLines.append(bigBedLoadString("Uniqueome",uniqLocation))
	outLines.append(bedLoadString("Pseudogenes","genome.ucf.edu/pseudo_rp/genes/pseudogenes.bed"))
	
	ofile.write(web.html.makeTable(elems))
	ofile.close()
