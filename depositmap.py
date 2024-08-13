#################################################
# Generador de mapa x,y de los sitios de reaccion
#################################################

import sys, getopt
import os
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from matplotlib import cm

def Deposit_map(OUTNAME, length, tstep, sampletime):
	PATH = os.getcwd()
	OUTPATH = PATH + "/" +OUTNAME
	NAME = OUTNAME.split(".")[0]
	filein=open(OUTPATH, "r")
	lines=filein.readlines()
	filein.close()
	R=[0]*length
	swtch = 0
	data = np.zeros((length,length))
	#if sampletime!="all":
		#start=float(sampletime.split("-")[0])
		#end=float(sampletime.split("-")[1])
	
	if sampletime=="all":
		for i in lines:
			if "Step Temp TotEng Atoms 2[10] 2[11] 2[12] 2[13]" in i:
				swtch=1
			elif "Loop time" in i:
				swtch=0
			elif swtch==1:
				if "freaction" in i:
					j = int(round(float(i.split()[1][2:])))
					k = int(round(float(i.split()[2][2:])))
					data[j,k]+=1
					r = int(round(sqrt(((float(i.split()[1][2:])-45)**2)+(float(i.split()[2][2:])-45)**2)))
					R[r]+=1
	else:
		sample=False
		for i in lines:
			if "Step Temp TotEng Atoms 2[10] 2[11] 2[12] 2[13]" in i:
				swtch=1
			elif "Loop time" in i:
				swtch=0
			elif swtch==1:
				if "freaction" in i:
					if sample:
						j = int(round(float(i.split()[1][2:])))
						k = int(round(float(i.split()[2][2:])))
						data[j,k]+=1
						r = int(round(sqrt((float(i.split()[1][2:])-45)*(float(i.split()[2][2:])-45))))
						R[r]+=1
				else:
					time=float(i.split()[0])*tstep/1e6
					if time>=start:
						sample=True
					elif time>=end:
						sample=False
	for i in range(len(R)):
		print(i,  R[i])
	# Make plot with vertical (default) colorbar
	fig, ax = plt.subplots()
	plt.rc('text', usetex=True)
	plt.rc('font', family='serif')
	
	cax = ax.imshow(data, interpolation='nearest', cmap=cm.coolwarm)
	plt.title(r'Mapa de sitios de reacci\'on', fontsize=22)
	plt.xlabel(r'\AA', fontsize=20)
	ax.tick_params(axis='both', labelsize=18)
	
	# Add colorbar, make sure to specify tick locations to match desired ticklabels
	cbar = fig.colorbar(cax)
	cbar.ax.tick_params(labelsize=10)
	
	
	# Make plot with horizontal colorbar
	
	plt.savefig("depositmap.png")
	plt.show()
	
