import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
#from scipy.interpolate import spline
import matplotlib.cm as cm

def Dens_Level(GRIDNAME, LEVEL=0.01):
	
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
	pcm = ax.pcolor(X, Y, Z, cmap='BuPu')
	fig.colorbar(pcm)
	
	CS = ax.contour(X, Y, Z, levels=[LEVEL])
	level0 = CS.levels[0]
	c0 = CS.collections[0]
	paths = c0.get_paths()
	path0 = paths[0]
	xy = path0.vertices
	
	with open(os.path.abspath(os.getcwd())+"/"+NAME+"_isodens.dat", "w") as out:
		for i in range(len(xy)):
			out.write(("%f\t%f \n")%(xy[i][0], xy[i][1]))
	
	out.close()

	ax.set_xlabel('R')
	ax.set_ylabel("Z")
	
	plt.show()
	
