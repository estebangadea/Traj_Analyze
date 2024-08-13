###Script para calcular la corriente a lo largo de la trayectoria de lammps###

import sys, getopt
import os
from collections import Counter

OUTPATH = os.path.abspath(sys.argv[1])
OUTNAME = OUTPATH.split('/')[-1].split('.')[0]
filein=open(OUTPATH, "r")
lines=filein.readlines()
filein.close()

swtch=0
current=0

frames=[]
currents=[]

for i in lines:
    if "f_2[2]" in i:
        swtch=1
        print("IN")
    elif "Loop time" in i:
        swtch=0
    else:
        if swtch==1:
            if "freaction" in i:
                current += 1
                #print fcurrent
            elif "breaction" in i:
                current -= 1
            elif "t1=" not in i:
                frames.append(float(i.split()[0]))
                currents.append(current)
                #fcurrent=0
                #bcurrent=0
print(current)
with open(os.path.abspath(os.getcwd())+"/"+OUTNAME+"_current.dat", "w") as out:
    for i in range(len(currents)):
        out.write(("%f\t%i \n")%(frames[i]*10/1000000, currents[i]))

out.close()
