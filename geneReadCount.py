import subprocess

class Command:

	def __init__(self,command,index):
		self.command = command
		self.index = index
		self.pipe = None
		self.options = {}
		self.hasArg = {}
		self.args = []
		self.stdout = None
		self.stderr = None
		
	def __str__(self):
		return self.generateCommand()
		
	def addOption(self,option,hasArg = False):
		self.options[option] = None
		self.hasArg[option] = hasArg
		
	def addArg(self):
		self.args.append(None)
		
	def setOptionArg(self,option,arg):
		self.options[option]=arg
		
	def setArg(self,index,arg):
		if index >= len(self.args):
			raise "Error: arg index out of bounds!"
		self.args[index] = arg
		
	def generateCommand(self):
		ret = self.command
		for option in self.options.keys():
			ret += " " + option
			if self.hasArg[option] and not self.options[option] == None:
				ret += " " + self.options[option]
		for arg in self.args:
			if not arg == None:
				ret += " " + arg
		return ret
		
	def ready(self):
		for option in self.options.keys():
			if self.hasArg[option] and self.options[option] == None:
				return False
		for arg in self.args:
			if arg == None:
				return False
		return True
		
	def setPipe(self,command):
		self.pipe = command
		
	def setStdout(self,stdout):
		self.stdout = stdout
		
	def setStderr(self,stderr):
		self.stderr = sterr
		
	def execute(self):
		command = self.generateCommand()
		if not self.pipe == None:
			if not self.pipe.ready():
				raise "Error: command " + str(self.pipe) + " not ready!"
			command += " | " + self.pipe.generateCommand()
		print command
		stdout = None
		if not self.stdout == None:
			stdout = open(self.stdout,"w")
		stderr = None
		if not self.stderr == None:
			stderr = open(self.stderr,"w")
		p = subprocess.Popen(command,stdout=stdout,stderr=stderr,shell=True)
		p.wait()
	

class Pipeline:

	def __init__(self, name=""):
		self.name = name
		self.commands = []
		self.steps = []
		
	def __str__(self):
		outs = self.name
		ind = 1
		for command in self.commands:
			outs+="\t"+str(command.index)+str(command)
			ind += 1
		return outs
		
	def addCommand(self,command,addToSteps=True):
		
		ind = -1
		
		if addToSteps:
			ind = len(self.commands)
		c = Command(command,ind)
		
		self.commands.append(c)
		if addToSteps:
			self.steps.append(c)		
		return c
			
	def execute(self):
		for c in self.commands:
			if not c.ready():
				raise "Error: command " + str(c) + " not ready!"
		for c in self.steps:
			c.execute()


if __name__ == "__main__":
	
	pipeline = Pipeline("Gene Read Count Pipeline")
	
	intersect = pipeline.addCommand("intersectBed")
	intersect.addOption("-abam",True)
	intersect.addOption("-b",True)
	#intersect.setOptionArg("-abam","alignments/adrenal/adrenal.unique.sorted.bam")
	#intersect.setOptionArg("-b","genes/pseudogenes.bed")
	#intersect.setStdout("results/07.17.2012/adrenal.unique.sorted.bam")
	#print intersect #1) intersectBed -abam <option1> -b <option2>
	
	index = pipeline.addCommand("samtools index")
	index.addArg()
	#index.setArg(0,"results/07.17.2012/adrenal.unique.sorted.bam")
	#print index #2) samtools sort <arg1>
	
	stats = pipeline.addCommand("samtools idxstats")
	stats.addArg()
	countReads = pipeline.addCommand("awk '{SUM+=$3}END{print SUM}'", False) #False: not added to steps
	stats.setPipe(countReads)	
	#stats.setArg(0,"results/07.17.2012/adrenal.unique.sorted.bam")
	#print stats #3) samtools idxstats <arg1> | awk '{SUM+=$3}END{print SUM}'
	
	import os
	from config import tissues,project_root
	
	os.chdir(project_root)
	
	for tissue in range(len(tissues)-1):
		tissues.append(tissues[tissue+1]+".hg18")
	
	for tissue in tissues[1:]:
		# Composite Pseudogenes
		intersect.setOptionArg("-abam","alignments/%s/%s.unique.sorted.bam" % (tissue,tissue))
		intersect.setOptionArg("-b","genes/pseudogenes.bed")
		intersect.setStdout("results/07.18.2012/%s.unique.sorted.pseudo.bam"%tissue)
		
		index.setArg(0,"results/07.18.2012/%s.unique.sorted.pseudo.bam"%tissue)
		
		stats.setArg(0,"results/07.18.2012/%s.unique.sorted.pseudo.bam"%tissue)
		stats.setStdout("results/07.18.2012/%s.pseudo.txt"%tissue)
	
		pipeline.execute()
		
		# Composite Refseq
		intersect.setOptionArg("-abam","alignments/%s/%s.unique.sorted.bam" % (tissue,tissue))
		intersect.setOptionArg("-b","genes/refseq.bed")
		intersect.setStdout("results/07.18.2012/%s.unique.sorted.refseq.bam"%tissue)
		
		index.setArg(0,"results/07.18.2012/%s.unique.sorted.refseq.bam"%tissue)
		
		stats.setArg(0,"results/07.18.2012/%s.unique.sorted.refseq.bam"%tissue)
		stats.setStdout("results/07.18.2012/%s.refseq.txt"%tissue)
	
		pipeline.execute()
