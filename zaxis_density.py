import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
#from scipy.interpolate import splrep
import matplotlib.cm as cm

def Zaxis_Dens(GRIDNAME):
	
	PATH = os.getcwd()
	GRIDPATH = PATH + "/" +GRIDNAME
	NAME = GRIDNAME.split(".")[0]
	filein=open(GRIDPATH, "r")
	lines=filein.readlines()
	filein.close()
	
	Xm=float(lines[0].split(" ")[0])
	Ym=float(lines[0].split(" ")[1])
	#print Xm, Ym
	M = (len(lines)-1)
	N =len(lines[1].split())
	X, Y = np.mgrid[0:Xm:complex(0, M), 0:Ym:complex(0, N)]
	
	dat=[]
	
	
	for i in lines[1:]:
		a=[]
		for j in range(len(lines[1].split())):
			a.append(float(i.split()[j]))
		dat.append(a)
		
	Z=np.array(dat)
	
	fig, ax =plt.subplots()
	tz = np.arange(0.0, Ym, Ym/len(dat[0]))
	r = Z[0,:]
	
	with open(os.path.abspath(os.getcwd())+"/"+NAME+"_zdens.dat", "w") as out:
		for i in range(len(tz)):
			out.write(("%f %f\n")%(tz[i], r[i]))
		
	ax.plot(tz, r)
	ax.set_xlabel('Z')
	ax.set_ylabel("Density")
	
	plt.show()
	
