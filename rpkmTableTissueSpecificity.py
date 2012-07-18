import getopt,sys

opts, args = getopt.getopt(sys.argv[1:],'')
ifile = args[0]

lines = open(ifile).readlines()
header = lines[0].split("\t")

print lines[0]

for line in lines[1:]:
	pieces = line.strip().split("\t")
	s = 0.0
	m = 0.0
	for i in pieces[2:-2]:
		f = float(i)
		s += f
		if f > m:
			m = f
	if s == 0:
		print line.strip() + "\t" + str(0.0)
	else:
		print line.strip() + "\t" + str(m/s)
