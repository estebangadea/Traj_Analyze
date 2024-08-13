#################################################
# Generador de mapa x,y de los sitios de reaccion
#################################################

import sys, getopt
import os
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, floor
from matplotlib import cm

OUTNAME = sys.argv[1]
PATH = os.getcwd()
OUTPATH = PATH + "/" +OUTNAME
NAME = OUTNAME.split(".")[0]
filein=open(OUTPATH, "r")
lines=filein.readlines()
filein.close()
swtch = 0
R = []
RR = [0]*31
tot = 0

for i in lines:
	if "Step Temp TotEng Atoms 2[10] 2[11] 2[12] 2[13]" in i:
		swtch=1
	elif "Loop time" in i:
		swtch=0
	elif swtch==1:
		if "freaction" in i:
			r = sqrt(((float(i.split()[1][2:])-30)**2)+(float(i.split()[2][2:])-30)**2)
			u=floor(r)
			R.append(r)
			RR[u]+=1

npR=np.array(R)

for i in RR:
	print(i)


print(np.mean(npR), np.std(npR))

