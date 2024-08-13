### Script para obtener contar particulas con una conidicon ###
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

cutoff=5
atom_type=2
solv_atomtype = 1
coords = []
maxclus = []
ids = []
clusterids = []
reactives=[]
follow=[]
box = [0, 0, 0]
swtch = 0
cutoffsqd = cutoff*cutoff
atomsincluster = []
atomsincluster_old = []
I_d = 0
AD = 0
isin = []
isout = []
sample = 0
populations=[0]*6

##Lee la trayectoria y organiza la informacion en una liste de 3 dimensiones 

for i in range(len(lines)):
	if "TIMESTEP" in lines[i]:
		for parti in range(len(isin)):
			if isin[parti]+isout[parti] == 51:
				#print(("in:%i\tout:%i")%(isin[parti],isout[parti]))
				if isin[parti]==0:
					populations[0]+=1
				elif isin[parti]<10:
					populations[1]+=1
				elif isin[parti]<20:
					populations[2]+=1
				elif isin[parti]<30:
					populations[3]+=1
				elif isin[parti]<40:
					populations[4]+=1
				elif isin[parti]<51:
					populations[5]+=1
		
		currentstep=int(lines[i+1])
		if swtch == 4:
			particles = len(coords)
			npcoords = np.array(coords)
			cluscounter=0
			
			conv=1
			#
			##Clusterize particles with d<cutoff
			#
			while conv!=0:
				conv=0
				
				for k in range(particles):
					for j in range(k, particles):
						dx=npcoords[j,0]-npcoords[k,0]
						dy=npcoords[j,1]-npcoords[k,1]
						dz=npcoords[j,2]-npcoords[k,2]
						if dx*dx+dy*dy+dz*dz < cutoffsqd:
							if (clusterids[k]==0 and
							clusterids[j]==0):
								#print("NewCluster")
								cluscounter+=1
								clusterids[k]=cluscounter
								clusterids[j]=cluscounter
								conv+=1
							elif clusterids[k]==0:
								#print("AddUp")
								clusterids[k]=clusterids[j]
								conv+=1
							elif clusterids[j]==0:
								#print("AddUp")
								clusterids[j]=clusterids[k]
								conv+=1
							elif clusterids[k]!=clusterids[j]:
								#print("Merge")
								for l in range(particles):
									if clusterids[l]==clusterids[j]:
										clusterids[l]=clusterids[k]
								conv+=1
			#
			##Find the biggest cluster
			#
			clusterfound=[0]
			for k in range(particles):
				if clusterids[k] not in clusterfound:
					clusterfound.append(clusterids[k])
			clustersize=[0]*len(clusterfound)
			#print(clusterfound)
			for j in range(len(clusterfound)):
				for k in clusterids:
					if k==clusterfound[j] and k!=0:
						clustersize[j]+=1
			#print(clustersize)
			max_reducedid = clustersize.index(max(clustersize))
			max_id = clusterfound[max_reducedid]
			for k in range(particles):
				if clusterids[k]==max_id:
					atomsincluster.append(ids[k])
			for k in range(len(follow)):
				if follow[k] not in atomsincluster:
					#print(str(follow[k])+" out")
					isout[k]+=1
				else:
					#print(str(follow[k])+" in")
					isin[k]+=1
			#for k in range(len(atomsincluster_old)):
			#	if atomsincluster_old[k] not in atomsincluster:
			#		AD+=1
			#print(I_d, AD)
			#atomsincluster_old=atomsincluster
			atomsincluster=[]
			I_d=0
			AD=0
					
			maxclus.append([currentstep*timestep/1e6, max(clustersize)])
		swtch =1
		clusterids=[]
		reactives_old=reactives
		reactives=[]
		coords=[]
		ids=[]
	elif "ITEM: NUMBER OF ATOMS" in lines[i]:
		swtch =2
	elif "ITEM: BOX" in lines[i]:
		swtch =3
		box[0] = float(lines[i+1].split()[1])
		box[1] = float(lines[i+2].split()[1])
		box[2] = float(lines[i+3].split()[1])
	elif "ITEM: ATOM" in lines[i]:
		swtch = 4 
	elif swtch == 4:
		itype = int(lines[i].split()[1])
		#
		##Extracts atom data
		#
		if itype == atom_type:
			iid = int(lines[i].split()[0])
			ix = float(lines[i].split()[2])#*box[0]
			iy = float(lines[i].split()[3])#*box[1]
			iz = float(lines[i].split()[4])#*box[2]
			if iid in reactives_old:
				follow.append(iid)
				#print("follow")
				isin.append(0)
				isout.append(0)
			if (iz*2<box[2] and iz+ix+iy>0):
				coords.append([ix, iy, iz])
				ids.append(iid)
				clusterids.append(0)
				
		####FIND SOLVENT IN REACTIVE ZONE####
		elif itype == solv_atomtype:
			iz = float(lines[i].split()[4])
			if iz<35:
				ix = float(lines[i].split()[2])-box[0]/2
				iy = float(lines[i].split()[3])-box[1]/2
				ir = ix*ix+iy*iy
				if ir<2500:
					iid = int(lines[i].split()[0])
					reactives.append(iid)
#print(isin)
#print(isout)
print(populations)


