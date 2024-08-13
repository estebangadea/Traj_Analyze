###Script para completar el numero de atomos en la trayectoria de lammps###

import sys, getopt
import os
from collections import Counter

def Dump_Fix(TRAJNAME):

	PATH = os.getcwd()
	TRAJPATH = PATH + "/" +TRAJNAME
	NAME = TRAJNAME.split(".")[0]
	filein=open(TRAJPATH, "r")
	lines=filein.readlines()
	filein.close()


	Nat=0 #collects the max N of atoms
	TypeMax=[0, 0, 0, 0, 0, 0] #Collects the max N of each type
	Frames=[] #Frame collector
	IDmax=[] #Frame collector for each type
	nFrames=lines.count("ITEM: TIMESTEP")


	for i in range(len(lines)):
		if "TIMESTEP" in lines[i]:
			k=i
			k+=3
			if int(lines[k])>Nat:
				Nat=int(lines[k])
			k+=6
			TypeParc=[0, 0, 0, 0, 0, 0]
			ID=0
			while "TIMESTEP" not in lines[k]:
				split=lines[k].split()
	#			print split
				TypeParc[int(split[1])]+=1
				if int(split[0])>ID:
					ID=int(split[0])

				for j in range(6):
					if TypeParc[j]>TypeMax[j]:
						TypeMax[j]=TypeParc[j]
				#print TypeParc
				if k<(len(lines)-1):
					k+=1
				else:
					break
			IDmax.append(ID)
			#print sum(TypeParc)
			Frames.append(TypeParc)

	with open(os.path.abspath(os.getcwd())+"/"+NAME+"_fix.lammpstrj", "w") as out:
		curframe=0
		for i in range(len(lines)):
			if "TIMESTEP" in lines[i]:
				IDs=[0, 0, TypeMax[1], TypeMax[1]+TypeMax[2], TypeMax[1]+TypeMax[2]+TypeMax[3],
				TypeMax[1]+TypeMax[2]+TypeMax[3]+TypeMax[4]]
				out.write(lines[i]+lines[i+1]+lines[i+2])
				out.write(("%i\n")%(sum(TypeMax)))
				out.write(''.join(map(str,lines[i+4:i+9])))
				for j in range(sum(Frames[curframe])):
					splits=lines[i+9+j].split()
					if splits[1]=="1":
						out.write(("%i 1 %f %f %f\n")%(IDs[1], float(splits[2]), float(splits[3]), float(splits[4])))
						IDs[1]+=1
					if splits[1]=="2":
						out.write(("%i 2 %f %f %f\n")%(IDs[2], float(splits[2]), float(splits[3]), float(splits[4])))
						IDs[2]+=1
					if splits[1]=="3":
						out.write(("%i 3 %f %f %f\n")%(IDs[3], float(splits[2]), float(splits[3]), float(splits[4])))
						IDs[3]+=1
					if splits[1]=="4":
						out.write(("%i 4 %f %f %f\n")%(IDs[4], float(splits[2]), float(splits[3]), float(splits[4])))
						IDs[4]+=1
					if splits[1]=="5":
						out.write(("%i 5 %f %f %f\n")%(IDs[5], float(splits[2]), float(splits[3]), float(splits[4])))
						IDs[5]+=1

				for j in range(len(TypeMax)):
					if Frames[curframe][j]<TypeMax[j]:
						for l in range(TypeMax[j]-Frames[curframe][j]):
							out.write(("%i %i 0.00000 0.00000 0.00000\n")%(IDs[j], j))
							IDs[j]+=1
				curframe+=1

	out.close()
	print(50*"-"+'\nThe file "'+NAME+'_fix.lammpstrj" has been created\n'+50*"-")
#print Frames[curframe-1], TypeMax
