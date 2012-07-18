#!/usr/local/bin/python

import sys,getopt

opt,args = getopt.getopt(sys.argv[1:],'')

lines = open(args[0]).readlines()

total = 0
for line in lines:
	split = line.split("\t")
	total+=int(split[2])
print total
