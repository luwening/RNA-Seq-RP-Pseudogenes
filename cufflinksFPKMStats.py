import sys,getopt

def calc_stddev(vals):
	return pow(sum([pow(x - avg,2) for x in vals])/len(vals),.5)
	
def calc_greaterThan(vals,threshold):
	return 100*float(sum([1 for x in vals if x > threshold]))/len(vals)


opts,args = getopt.getopt(sys.argv[1:],'')

lines = open(args[0]).readlines()

header = lines[0].strip().split("\t")
tissues = header[1:]
genes = []

table = dict()

for tissue in tissues:
	table[tissue] = []

for line in lines[1:]:
	split = line.split("\t")	
	gene = split[0]
	genes.append(gene)
	fpkm = split[1:]
	
	if not gene in table:
		table[gene]=[]
	
	for i in range(len(tissues)):
		table[tissues[i]].append(float(fpkm[i]))
		table[gene].append(float(fpkm[i]))

tissueAvg = [0 for i in range(len(tissues))]
tissueStats = []
totalAvg = 0

runningTotal = 0.0
totalCount = 0
allVals = []
ind = 0
print "tissue\tavg\tmax\tmin\tstddev\t%>1\t%>2\t%>5\t%>10\t%>15"
for tissue in tissues:
	
	#find avg,min,max,stddev
	tissueFPKM = table[tissue]
	totalSum = sum(tissueFPKM)
	allVals.extend(tissueFPKM)
	avg = sum(tissueFPKM)/len(tissueFPKM)
	mx = max(tissueFPKM)
	mn = min(tissueFPKM)
	stddev = calc_stddev(tissueFPKM)
	greatOne = calc_greaterThan(tissueFPKM,1.0)
	greatTwo = calc_greaterThan(tissueFPKM,2.0)
	greatFive = calc_greaterThan(tissueFPKM,5.0)
	greatTen = calc_greaterThan(tissueFPKM,10.0)
	greatFifteen = calc_greaterThan(tissueFPKM,15.0)
	
	#print values
	outs = tissue
	outs += "\t%.2f" % avg
	outs += "\t%.2f" % mx
	outs += "\t%.2f" % mn
	outs += "\t%.2f" % stddev
	outs += "\t%.2f" % greatOne
	outs += "\t%.2f" % greatTwo
	outs += "\t%.2f" % greatFive
	outs += "\t%.2f" % greatTen
	outs += "\t%.2f" % greatFifteen
	print outs
	
	#print tissue+"\t"+str(avg)+"\t"+str(mx)+"\t"+str(mn)+"\t"+str(stddev)+"\t"+str(greatOne)+"\t"+str(greatTwo)+"\t"+str(greatFive)+"\t"+str(greatTen)+"\t"+str(greatFifteen)
	
	runningTotal += totalSum
	totalCount += len(tissueFPKM)
	ind+=1
	
allAvg = runningTotal/totalCount
allstddev = calc_stddev(allVals)
allgreatOne = calc_greaterThan(allVals,1.0)
allgreatTwo = calc_greaterThan(allVals,2.0)
allgreatFive = calc_greaterThan(allVals,5.0)
allgreatTen = calc_greaterThan(allVals,10.0)
allgreatFifteen = calc_greaterThan(allVals,15.0)

outs = "AllTissues"
outs += "\t%.2f" % allAvg
outs += "\t%.2f" % max(allVals)
outs += "\t%.2f" % min(allVals)
outs += "\t%.2f" % allstddev
outs += "\t%.2f" % allgreatOne
outs += "\t%.2f" % allgreatTwo
outs += "\t%.2f" % allgreatFive
outs += "\t%.2f" % allgreatTen
outs += "\t%.2f" % allgreatFifteen
print outs
#print "AllTissues\t"+str(runningTotal/totalCount)+"\t"+str(max(allVals))+"\t"+str(min(allVals))+"\t"+str(allstddev)+"\t"+str(allgreatOne)+"\t"+str(allgreatTwo)+"\t"+str(allgreatFive)+"\t"+str(allgreatTen)+"\t"+str(allgreatFifteen)

print ""

tissueSpecificity = []
for gene in genes:
	vals = table[gene]
	mx = max(vals)
	tot = sum(vals)
	if tot > 0:
		tissueSpecificity.append(mx/tot)
		
print "Tissue Specificity"
print "max\tmin\tavg\tstddev"
print str(max(tissueSpecificity))+"\t"+str(min(tissueSpecificity))+"\t"+str(sum(tissueSpecificity)/len(tissueSpecificity))+"\t"+str(calc_stddev(tissueSpecificity))

