### Script para obtener la MSD de una particula en una trayectoria de Lammps ###
###USO: python pathto/MAD.py <*.lammpstrj> <timestep>


import sys, os
import numpy as np
from math import sqrt
import math
import matplotlib.pyplot as plt

TRAJPATH = os.path.abspath(sys.argv[1])
TRAJNAME = TRAJPATH.split('/')[-1].split('.')[0]
timestep = int(sys.argv[2])

filein=open(TRAJPATH, "r")
lines=filein.readlines()
filein.close()

timesteps=[]
Coords=[]
MSD = []
swtch = 0
box = [0]*3
atom_type = 2
altura = 12
radio = 10
Ngrid = np.zeros((altura, radio))
VZgrid = np.zeros((altura, radio))
VRgrid = np.zeros((altura, radio))

##Lee la trayectoria y organiza la informacion en una liste de 3 dimensiones 

for i in range(len(lines)):
	if "TIMESTEP" in lines[i]:
		time=float(lines[i+1])*timestep/1e6
		timesteps.append(time)
		swtch=1
	elif "ITEM: NUMBER OF ATOMS" in lines[i]:
		swtch =2
	elif "ITEM: BOX" in lines[i]:
		swtch =3
		if len(MSD)==1:
			box[0] = float(lines[i+1].split()[1])
			box[1] = float(lines[i+2].split()[1])
			box[2] = float(lines[i+3].split()[1])
	elif "ITEM: ATOM" in lines[i]:
		swtch = 4 
	elif swtch == 4:
		itype = int(lines[i].split()[1])
		if itype == atom_type:
			ix = float(lines[i].split()[2])-box[0]/2
			iy = float(lines[i].split()[3])-box[1]/2
			iz = float(lines[i].split()[4])
			ir = sqrt(ix*ix+iy*iy)
			vx = float(lines[i].split()[5])
			vy = float(lines[i].split()[6])
			vz = float(lines[i].split()[7])
			vr = (vx*ix+vy*iy)/ir
			if iz<altura*4 and ir<radio*4:
				r=int(iz/4)
				s=int(ir/4)
				Ngrid[r,s]+=1
				VZgrid[r,s]+=vz
				VRgrid[r,s]+=vr
				
			
X = np.arange(0, radio*4, 4)
Y = np.arange(0, altura*4, 4)

filein=[]

for r in range(altura):
	for s in range(radio):
		VZgrid[r,s]=VZgrid[r,s]/(math.pi*16*((s+1)*(s+1)-s*s)*4)
		VRgrid[r,s]=VRgrid[r,s]/(math.pi*16*((s+1)*(s+1)-s*s)*4)

print(VRgrid)
print(VZgrid)

fig, ax = plt.subplots()
ax.streamplot(X, Y, VRgrid, VZgrid, density=[0.5, 1])

plt.show()

