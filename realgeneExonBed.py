

realgeneGtf = "/zhang/ptonner/genes/real.gtf"
realNames = "/zhang/ptonner/genes/real.names"

realgenes = [(x[0],x[1],x[2],x[3]) for x in [line.strip().split("_") for line in open(realNames).readlines()]]
genomeLocations = {}
for gene,chrom,start,end in realgenes:
	if not chrom in genomeLocations:
		genomeLocations[chrom] = ([],[],[])
	genomeLocations[chrom][0].append(int(start))
	genomeLocations[chrom][1].append(int(end))
	genomeLocations[chrom][2].append(gene)

outExons = []
for line in open(realgeneGtf).readlines():
	
	split = line.strip().split("\t")
	chrom = split[0]
	region = split[2]
	if not region == "exon":
		continue
	if not chrom in genomeLocations:
		continue
	start = int(split[3])
	end = int(split[4])
	for ind in range(len(genomeLocations[chrom][0])):
		if start > genomeLocations[chrom][0][ind] and start < genomeLocations[chrom][1][ind]:
			outExons.append((genomeLocations[chrom][2][ind],chrom,start,end))
			break
		elif end > genomeLocations[chrom][0][ind] and end < genomeLocations[chrom][1][ind]:
			outExons.append((genomeLocations[chrom][2][ind],chrom,start,end))
			break
			

geneCount = []
for gene,chrom,start,end in outExons:
	print chrom + "\t" + str(start) + "\t" + str(end) + "\t" + gene + "\t1\t+"
	if not gene in geneCount:
		geneCount.append(gene)
			
	
