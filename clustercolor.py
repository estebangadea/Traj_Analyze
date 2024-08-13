#levanta la salida del clustering junto al .lammptrj para modificarlo y poder ver los clusters en VMD

############################################
# Uso: python clustercolor.py <clustering.dat> <*_fix.lammptrj>
# Devuelve la trayectoria con vx=1 para los miembros del cluster
# Genera un archivo con el tamano del cluster en funcion del frame
############################################

import sys, getopt
import os
from collections import Counter

####################################################
# Lee el archivo.dat generado con el clustering
# Genera las listas necesarias para modificar la trj
####################################################


CLUSPATH = os.path.abspath(sys.argv[1])
CLUSNAME = CLUSPATH.split('/')[-1].split('.')[0]
clusin=open(CLUSPATH, "r")
clines=clusin.readlines()
clusin.close()

FRAMES=[]
F=[] #Contiene los IDs (impares) y los clusterID (pares) para cada frame
ID=[]
C=[]
ClusterID=[] 
ClusterSize=[] 

for line in clines:
	if "FRAME:" in line:
		ID=[]
		C=[]
	elif "ENDFRAME" in line:
		F.append(ID)
		ClusterID=[]
		ClusterSize=[]
		A=1
		for i in range(len(C)):
			n=0
			for j in range(len(C)):
				if C[j]==C[i]:
					n+=1
			
			if C[i] not in ClusterID:
				ClusterSize.append(n)
				ClusterID.append(C[i])
		for i in range(len(ClusterSize)):
			if ClusterSize[i]>10 and ClusterID[i]!=0: #ClusterID=0 se reserva para las particulas que no formaron ningun cluster
				for j in range(len(ID)):
					if C[j]==ClusterID[i]:
						C[j]="M"

		F.append(C)
	
	else:
		ID.append(int(line.split(" ")[0]))
		C.append(int(line.split(" ")[1]))
print(len(F))

##############################
#Lee y modifica la trayectoria
##############################

TRAJPATH = os.path.abspath(sys.argv[2])
TRAJNAME = TRAJPATH.split('/')[-1].split('.')[0]
filein=open(TRAJPATH, "r")
tlines=filein.readlines()
filein.close()
with open(os.path.abspath(os.getcwd())+"/"+TRAJNAME+"_clus.lammpstrj", "w") as out:
	fram=0
	swtch=0
	j=0
	for line in tlines:
		if "TIMESTEP" in line:
			fram+=1
			swtch=1
			j=0
			out.write(line)
		elif "ITEM: NUMBER" in line:
			swtch=2
			out.write(line)
		elif "ITEM: BOX" in line:
			swtch=3
			out.write(line)
		elif "ITEM: ATOM" in line:
			swtch=4
			out.write(line[0:-1]+" vx\n")
		if swtch==1 and "ITEM" not in line:
			out.write(line)
			FRAMES.append(line.split(" ")[0])
		elif swtch==2 and "ITEM" not in line:
			out.write(line)
		elif swtch==3 and "ITEM" not in line:
			out.write(line)
		elif swtch==4 and "ITEM" not in line:
			if line.split(" ")[1]=="2":
				if F[2*fram-1][j]=="M":
				
					out.write(line.split(" ")[0])
					out.write(" "+line.split(" ")[1])
					out.write(" "+line.split(" ")[2])
					out.write(" "+line.split(" ")[3])
					out.write(" "+line.split(" ")[4][0:-1])
					out.write(" 1\n")
				else:
					out.write(line)
				j+=1
			else:
				out.write(line)

out.close()

print(F[1].count("M"))

###################################################
#Exporta el tamano del cluster en funcion del frame
###################################################

with open(os.path.abspath(os.getcwd())+"/"+TRAJNAME+"_maxcluster.dat", "w") as out:
	for i in range(int(len(F)/2)):
		out.write(("%f\t%i\n")%(float(FRAMES[i])*10/1000000,F[i*2+1].count("M")))
out.close()

