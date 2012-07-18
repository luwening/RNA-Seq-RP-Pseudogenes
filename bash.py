import subprocess
import os


def runCommand(command,out=None,err=None):

	p = subprocess.Popen(command,stdout=out,stderr=err,shell=True)
	p.wait()
	
def changeDir(d):
	os.chdir(d)
