
pseudogeneDataFile = "/home/ptonner/genes/rp-genes-pseudo-genes_hg18.fa"
annotationDownloadLink = "http://tables.pseudogene.org/"

class Pseudogene():
	
	def __init__(self,ensid,psgid,gene,chrom,start,end,seq="",strand="+"):
		self.parentEnsmblID = ensid
		self.pseudogeneID = psgid
		self.gene = gene
		self.chrom = chrom
		self.start = int(start)
		self.end = int(end)
		self.seq = seq
		self.strand = strand
		
	def length(self):
		return end - start
	
	def sequence(self):
		return self.seq
		
	def annotationURL(self):
		return annotationDownloadLink+self.pseudogeneID
		

def createPseudogene(string):
	ensid,psgid,gene,chrom,start,end,s = string.split("_")
	return Pseudogene(ensid,psgid,gene,chrom,start,end,strand=s)

def load_all():

	genes = []
	
	for line in open(pseudogeneDataFile).readlines():
	
		if not line[0] == ">":
			if len(genes) > 0:
				genes[-1].seq = line.strip()
			continue
			
		genes.append(createPseudogene(line.strip("\n>")))

	return genes
	
def mappingFile():
	
	for gene in load_all():
		print gene.pseudogeneID + "\t" + gene.gene +"_"+gene.chrom+"_"+str(gene.start)+"_"+str(gene.end)
		
def getID(gene,chrom,start,end):
	
	for g in load_all():
		if g.gene == gene and g.chrom == chrom and g.start == int(start) and g.end == int(end):
			return g.pseudogeneID
	return None
