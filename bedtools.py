class BEDLine:
	
	def __init__(self,chrom,start,end,name="",score=0,strand="+",thickStart=0):
		self.chrom = chrom.strip()
		self.start = int(start)
		self.end = int(end)
		self.name = name.strip()
		self.score = int(score)
		self.strand = strand.strip()
		self.thickStart = int(thickStart)
	
	def getLine(self):
		return self.chrom + "\t" + str(self.start) + "\t" + str(self.end) + "\t" + self.name + "\t" + str(self.score) + "\t" + self.strand
		
	def length(self):
		return self.end - self.start - 1

class BEDFile:
	
	def __init__(self,filename):
		self.filename = filename
		self.lines = []
		self.load()
		
	def load(self):
		for line in open(self.filename).readlines():
			split = line.split("\t")
			if len(split) > 6:
				self.lines.append(BEDLine(split[0],split[1],split[2],split[3],split[4],split[5],split[6]))
			elif len(split) > 5:
				self.lines.append(BEDLine(split[0],split[1],split[2],split[3],split[4]))
			else:
				self.lines.append(BEDLine(split[0],split[1],split[2]))
		
#simple case, need to expand	
def createBedLine(s):
	
	split = s.split("\t")
	return BEDLine(split[0],split[1],split[2])
		
def findBedAlignmentsByName(filename):
	
	lines = BEDFile(filename).lines
	ret = {}
	for line in lines:
		if line.name in ret:
			#sys.stderr.write("Error " + line.name + " duplicated!\n")
			ret[line.name].append(line)
		else:
			ret[line.name] = [line]
			
	return ret
	
def fastaTagToBedLine(line,chrom=3,start=4,end=5,tag=2,strand=6,delim="_"):
	if not line[0]==">":
		return None
	split = line.split(delim)
	
	ch = split[chrom]
	s = split[start]
	e = split[end]
	st = split[strand]
	t = split[tag]
	
	try:
		return BEDLine(ch,s,e,t,strand=st)
	except Exception:
		return None

def fastaTagsToBedLines(fastaFile,chrom=3,start=4,end=5,tag=2,strand=6,delim="_"):
	
	lines = []
	
	for line in open(fastaFile).readlines():
		if not line[0]==">":
			continue
		split = line.split(delim)
		
		ch = split[chrom]
		s = split[start]
		e = split[end]
		st = split[strand]
		t = split[tag]
		
		try:
			lines.append(BEDLine(ch,s,e,t,strand=st))
		except Exception:
			continue
	return lines
