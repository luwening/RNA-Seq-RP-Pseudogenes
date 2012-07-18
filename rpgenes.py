
rpgeneDataFile = "/zhang/ptonner/genes/real.names"

class RPgene():
	
	def __init__(self,gene,chrom,start,end,seq=""):
		self.gene = gene
		self.chrom = chrom
		self.start = int(start)
		self.end = int(end)
		self.seq = seq
		
	def length(self):
		return end - start
	
	def sequence(self):
		return self.seq
		
def loadRawStrings():
	pseudogeneStrings = []
	ifile = open(rpgeneDataFile)
	for line in ifile.readlines():
		pseudogeneStrings.append(line.strip("\n"))
	return pseudogeneStrings

def createRPgene(string):
	gene,chrom,start,end = string.split("_")
	return RPgene(gene,chrom,start,end)

def load_all():
	return [createRPgene(s) for s in loadRawStrings()]
