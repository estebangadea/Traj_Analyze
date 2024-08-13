import sys, getopt
import os
import numpy as np
import math

def Grid_Plot(TRAJNAME, atom_type, M, N, tstep, sampletime):

	PATH = os.getcwd()
	TRAJPATH = PATH + "/" +TRAJNAME
	NAME = TRAJNAME.split(".")[0]
	filein=open(TRAJPATH, "r")
	lines=filein.readlines()
	filein.close()
	
	densgrid = np.zeros((M,N))
	coords = []
	box = [0, 0, 0]
	swtch = 0
	step = 0
	if sampletime!="all":
		start=float(sampletime.split("-")[0])
		end=float(sampletime.split("-")[1])
	
	
	for i in range(len(lines)):
		if "TIMESTEP" in lines[i]:
			time=float(lines[i+1])*tstep/1e6
			if sampletime == "all":
				sample=True
				step+=1
			elif time>=start and time<=end:
				sample=True
				step+=1
			else:
				sample=False
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
			if sample:
				itype = int(lines[i].split()[1])
				#
				#Extracts atom data
				#
				if itype == atom_type:
					ix = float(lines[i].split()[2])*box[0]-box[0]/2
					iy = float(lines[i].split()[3])*box[1]-box[1]/2
					iz = float(lines[i].split()[4])*box[2]
					ir = math.sqrt(ix*ix+iy*iy)
					if iz<N*2 and ir<M*2:
						r=int(ir/2)
						s=int(iz/2)
						#print(r, s)
						densgrid[r,s]+=1
	#print(densgrid)
	
	for i in range(M):
		for j in range(N):
			densgrid[i,j]=densgrid[i,j]/(step*math.pi*4*((i+1)*(i+1)-i*i)*2)
							
	with open(os.path.abspath(os.getcwd())+"/"+NAME+"_grid.dat", "w") as out:
		out.write(("%i %i\n")%(M*2, N*2))
		for i in range(M):
				for j in range(N):
					out.write(("%f ")%(densgrid[i,j]))
				out.write("\n")
	out.close
	print(50*"-"+'\nThe file "'+NAME+'_grid.dat" has been created\n'+50*"-")
