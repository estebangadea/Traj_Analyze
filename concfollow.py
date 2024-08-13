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

solvtype = 1
reacttype = 2

timesteps=[]
Conc1 = []
Conc2 = []
nsolv1 = 1.0
nsolv2 = 1.0
nreact1 = 0.0
nreact2 = 0.0
rbox = 18.0

##Lee la trayectoria y organiza la informacion en una liste de 3 dimensiones 

for i in range(len(lines)):
	if "TIMESTEP" in lines[i]:
		time=float(lines[i+1])*timestep/1e6
		timesteps.append(time)
		Conc1.append(nreact1)
		#Conc2.append(nreact2/nsolv2)
		nreact1=0.0
		nreact2=0.0
		nsolv1=0.0
		nsolv2=0.0
		swtch=1
	elif "ITEM: NUMBER OF ATOMS" in lines[i]:
		swtch =2
	elif "ITEM: BOX" in lines[i]:
		swtch =3
	elif "ITEM: ATOM" in lines[i]:
		swtch = 4 
	elif swtch == 4:
		itype = int(lines[i].split()[1])
		if itype == solvtype:
			ix = float(lines[i].split()[2])
			iy = float(lines[i].split()[3])
			ir = sqrt((ix-30)*(ix-30)+(iy-30)*(iy-30))
			iz = float(lines[i].split()[4])
			if iz < 30 and ir<11:
				nsolv1+=1
			#elif iz > 60:
			#	nsolv2+=1
		elif itype == reacttype:
			ix = float(lines[i].split()[2])
			iy = float(lines[i].split()[3])
			#ir = sqrt((ix-30)*(ix-30)+(iy-30)*(iy-30))
			iz = float(lines[i].split()[4])
			ir = sqrt((ix-30)*(ix-30)+(iy-30)*(iy-30)+(iz-14)*(iz-14))
			if iz>75:
				nreact1+=1
			#elif iz > 60:
			#	nreact2+=1
			
for i in range(len(Conc1)):
	print(timesteps[i], Conc1[i])

