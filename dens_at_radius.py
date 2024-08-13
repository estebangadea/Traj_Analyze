import sys, os
import numpy as np
from math import sqrt
import math
import matplotlib.pyplot as plt

TRAJPATH = os.path.abspath(sys.argv[1])
TRAJNAME = TRAJPATH.split('/')[-1].split('.')[0]

filein=open(TRAJPATH, "r")
lines=filein.readlines()
filein.close()

timesteps=[]
Coords=[]
delta = 1
swtch = 0
box = [0]*3
atom_type = 1
altura = 12
radio = float(sys.argv[2])
particles =0
steps = 0

##Lee la trayectoria y organiza la informacion en una liste de 3 dimensiones 

for i in range(len(lines)):
	if "TIMESTEP" in lines[i]:
		swtch=1
		steps+=1
	elif "ITEM: NUMBER OF ATOMS" in lines[i]:
		swtch =2
	elif "ITEM: BOX" in lines[i]:
		swtch =3
		if particles==0:
			box[0] = float(lines[i+1].split()[1])
			box[1] = float(lines[i+2].split()[1])
			box[2] = float(lines[i+3].split()[1])
	elif "ITEM: ATOM" in lines[i]:
		swtch = 4 
	elif swtch == 4:
		itype = int(lines[i].split()[1])
		iz = float(lines[i].split()[4])
		if itype == atom_type and iz<16:
			ix = float(lines[i].split()[2])-box[0]/2
			iy = float(lines[i].split()[3])-box[1]/2
			ir = sqrt(ix*ix+iy*iy)
			if ir<(radio+delta) and ir>(radio-delta):
				particles += 1
				
volumen = 6 * math.pi * ((radio+delta)**2-(radio-delta)**2)

print(particles/(volumen*steps))
