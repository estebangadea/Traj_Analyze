###Script para calcular la corriente a lo largo de la trayectoria de lammps###

import sys, getopt
import os
from collections import Counter

def Current(OUTNAME, timestep):
	PATH = os.getcwd()
	OUTPATH = PATH + "/" +OUTNAME
	NAME = OUTNAME.split(".")[0]
	filein=open(OUTPATH, "r")
	lines=filein.readlines()
	filein.close()

	swtch=0
	current=0
	tstep = int(timestep)
	frames=[]
	currents=[]

	for i in lines:
		if "Step          Temp          TotEng        Atoms       f_2[11]        f_3[11]" in i:
			swtch=1
		elif "Loop time" in i:
			swtch=0
		else:
			if swtch==1:
				if "freaction" in i:
					current += 1
					#print fcurrent
				elif "breaction" in i:
					current -= 1
				elif "t1=" not in i:
					frames.append(float(i.split()[0]))
					currents.append(current)
					#fcurrent=0
					#bcurrent=0
	with open(os.path.abspath(os.getcwd())+"/"+NAME+"_current.dat", "w") as out:
		for i in range(len(currents)):
			out.write(("%f\t%i \n")%(frames[i]*tstep/1000000, currents[i]))

	out.close()
	print(50*"-"+'\nThe file "'+NAME+'_current.dat" has been created\n'+50*"-")
