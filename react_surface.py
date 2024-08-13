import sys, getopt
import os
import numpy as np
import math
import matplotlib.pyplot as plt
from math import sqrt, exp, floor
from matplotlib import cm

def Grid_Plot(TRAJNAME, atom_type, M, tstep):

	PATH = os.getcwd()
	TRAJPATH = PATH + "/" +TRAJNAME
	NAME = TRAJNAME.split(".")[0]
	filein=open(TRAJPATH, "r")
	lines=filein.readlines()
	filein.close()
	
	densgrid = np.zeros((M,M))
	coords = []
	box = [0, 0, 0]
	swtch = 0
	step = 0
	R=[0]*31
	

	
	
	for i in range(len(lines)):
		if "TIMESTEP" in lines[i]:
			time=float(lines[i+1])*tstep/1e6
			step+=1
			swtch=1
		elif "ITEM: NUMBER OF ATOMS" in lines[i]:
			swtch =2
		elif "ITEM: BOX" in lines[i]:
			swtch =3
			if step==1:
				box[0] = float(lines[i+1].split()[1])
				box[1] = float(lines[i+2].split()[1])
				box[2] = float(lines[i+3].split()[1])
		elif "ITEM: ATOM" in lines[i]:
			swtch = 4 
		elif swtch == 4:
			itype = int(lines[i].split()[1])
			#
			#Extracts atom data
			#
			if itype == atom_type:
				ix = float(lines[i].split()[2])-box[0]/2
				iy = float(lines[i].split()[3])-box[1]/2
				iz = float(lines[i].split()[4])
				ir = math.sqrt(ix*ix+iy*iy)
				if iz<16 and ir<31:
					r=floor((ix+box[0]/2))
					s=floor((iy+box[1]/2))
					u=floor(ir)
					if ir<25:
						kvel=6e-7*exp(19.470675*0.25)*exp(-iz+10)
						densgrid[r,s]+=1-exp(-kvel*10)
						R[u]+=1-exp(-kvel*10)
					else:
						kvel=6e-7*exp(19.470675*0.25)*exp(-sqrt((iz-10)**2+(ir-25)**2))
						densgrid[r,s]+=1-exp(-kvel*10)
						R[u]+=1-exp(-kvel*10)
	
	for i in range(M):
		for j in range(M):
			densgrid[i,j]=densgrid[i,j]*2000
	
	for i in R:
		print(i*2000)
							
	with open(os.path.abspath(os.getcwd())+"/"+NAME+"_grid.dat", "w") as out:
		out.write(("%i %i\n")%(M, M))
		for i in range(M):
				for j in range(M):
					out.write(("%f ")%(densgrid[i,j]))
				out.write("\n")
	out.close
	print(50*"-"+'\nThe file "'+NAME+'_grid.dat" has been created\n'+50*"-")
	# Make plot with vertical (default) colorbar
	fig, ax = plt.subplots()
	
	cax = ax.imshow(densgrid, interpolation='nearest', cmap=cm.coolwarm)
	ax.set_title('Reacctive population')
	
	# Add colorbar, make sure to specify tick locations to match desired ticklabels
	cbar = fig.colorbar(cax)
	
	
	# Make plot with horizontal colorbar
	
	plt.savefig("reactivepop.png")
	 #plt.show()
	
	
TRAJPATH = os.path.abspath(sys.argv[1])
TRAJNAME = TRAJPATH.split('/')[-1]
timestep = int(sys.argv[2])
atomtype = int(sys.argv[3])
length = int(sys.argv[4])

Grid_Plot(TRAJNAME, atomtype, length, timestep)


