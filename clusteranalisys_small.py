import sys, getopt
import os
from collections import Counter
import numpy as np
import math

def Cluster_Analisys(TRAJNAME, atom_type, cutoff, timestep):

	PATH = os.getcwd()
	TRAJPATH = PATH + "/" +TRAJNAME
	NAME = TRAJNAME.split(".")[0]
	filein=open(TRAJPATH, "r")
	lines=filein.readlines()
	filein.close()
	
	coords = []
	maxclus=[]
	ids = []
	clusterids = []
	box = [0, 0, 0]
	swtch = 0
	cutoffsqd = cutoff*cutoff
	atomsincluster=[]
	atomsincluster_old=[]
	I_d=0
	AD=0
	
	for i in range(len(lines)):
		if "TIMESTEP" in lines[i]:
			currentstep=int(lines[i+1])
			if swtch == 4:
				particles = len(coords)
				npcoords = np.array(coords)
				cluscounter=0
				
				conv=1
				#
				#Clusterize particles with d<cutoff
				#
				while conv!=0:
					conv=0
					
					for k in range(particles):
						for j in range(k, particles):
							dx=npcoords[j,0]-npcoords[k,0]
							dx=dx-box[0]*round(dx/box[0])
							dy=npcoords[j,1]-npcoords[k,1]
							dy=dy-box[1]*round(dy/box[1])
							dz=npcoords[j,2]-npcoords[k,2]
							#dz=dz-box[2]*round(dz/box[2])
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
				#Find the biggest cluster
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
				#max_id = clusterfound[max_reducedid]
				#for k in range(particles):
				#	if clusterids[k]==max_id:
				#		atomsincluster.append(ids[k])
				#for k in range(len(atomsincluster)):
				#	if atomsincluster[k] not in atomsincluster_old:
				#		I_d+=1
				#for k in range(len(atomsincluster_old)):
				#	if atomsincluster_old[k] not in atomsincluster:
				#		AD+=1
				#print(I_d, AD)
				#atomsincluster_old=atomsincluster
				#atomsincluster=[]
				#I_d=0
				#AD=0
						
				maxclus.append([currentstep*timestep/1e6, max(clustersize)])				
			swtch =1
			clusterids=[]
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
			#Extracts atom data
			#
			if itype == atom_type or itype == 4:
				iid = int(lines[i].split()[0])
				ix = float(lines[i].split()[2])#*box[0]
				iy = float(lines[i].split()[3])#*box[1]
				iz = float(lines[i].split()[4])#*box[2]
				if (iz*2<box[2] and iz+ix+iy>0) and ix > 30:
					coords.append([ix, iy, iz])
					ids.append(iid)
					clusterids.append(0)
							
	with open(os.path.abspath(os.getcwd())+"/"+NAME+"_maxcluster.dat", "w") as out:
		for i in maxclus:
			out.write(("%f\t%i\n")%(i[0],i[1]))
	out.close
	print(50*"-"+'\nThe file "'+NAME+'_maxcluster.dat" has been created\n'+50*"-")
