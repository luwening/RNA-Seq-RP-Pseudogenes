import bash

def bamToBedGraph(align,chroms,out):
	bash.runCommand("genomeCoverageBed -bg -ibam "+align+" -g "+chroms,open(out,"w"))
	
def sortBedGraph(align,out):
	bash.runCommand("sort -k1,1 -k2,2n "+align,open(out,"w"))
	
def bedGraphToBigWig(align,chroms,out):
	bash.runCommand("bedGraphToBigWig "+align+" "+chroms+" "+out)

if __name__=="__main__":
	
	import sys, getopt
	
	opts,args = getopt.getopt(sys.argv[1:],"")
	
	align = args[0]
	chroms = args[1]
	out = args[2]
	
	bamToBedGraph(align,chroms,"temp")
	sortBedGraph("temp","temp.sorted")
	bedGraphToBigWig("temp.sorted",chroms,out)
	
	bash.runCommand("rm temp temp.sorted")
	
