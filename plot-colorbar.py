import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.interpolate import spline
import matplotlib.cm as cm


TRAJPATH = os.path.abspath(sys.argv[1])
TRAJNAME = TRAJPATH.split('/')[-1].split('.')[0]
LEVEL = float(sys.argv[2])
filein=open(TRAJPATH, "r")
lines=filein.readlines()
filein.close()

Xm=float(lines[0].split(" ")[0])
Ym=float(lines[0].split(" ")[1])
#print Xm, Ym
M = (len(lines)-1)
N =len(lines[1].split())
X, Y = np.mgrid[0:Xm:complex(0, M), 0:Ym:complex(0, N)]

dat=[]


for i in lines[1:]:
	a=[]
	for j in range(len(lines[1].split())):
		a.append(float(i.split()[j]))
	dat.append(a)


dat2 = []
for i in range(len(dat)):
	a=[]
	for j in range(len(dat[i])):
		k=len(dat[i])-j-1
		a.append(dat[i][k])
	for j in range(len(dat[i])):
		a.append(dat[i][j])
	dat2.append(a)



Z=np.array(dat)

#print Z.shape, len(lines[1:])

fig, ax = plt.subplots(2, 1)
ax[0].set_title('Implementacion 1 a 250mV')
pcm = ax[0].pcolor(X, Y, Z, cmap='BuPu')
CS = ax[0].contour(X, Y, Z, levels=[LEVEL])
level0 = CS.levels[0]
c0 = CS.collections[0]
paths = c0.get_paths()
path0 = paths[0]
xy = path0.vertices

with open(os.path.abspath(os.getcwd())+"/"+TRAJNAME+"_isodens.dat", "w") as out:
    for i in range(len(xy)):
        out.write(("%f\t%f \n")%(xy[i][0], xy[i][1]))

out.close()


fig.colorbar(pcm, ax=ax[0], extend='max')

C=[0]*len(dat)
Sum=0
Num=1
for j in range(len(dat)):
	if Z[0, j]>0.005 and Z[0, j]<0.015:
		Sum=Sum+Z[0,j]
		Num+=1
Cut=Sum/(Num*2)
for i in range(len(dat)):
	for j in range(len(dat)):
		if (Z[i,(j-1)]>Cut and Z[i,j]<Cut):
			C[i]=(j)*Ym/len(dat[1])
#print C
#print Cut
###################################
tr = np.arange(0.0, Xm, Xm/len(dat))
tz = np.arange(0.0, Ym, Ym/len(dat[0]))
s = np.array(C)
r = Z[0,:]

ax[0].set_xlim([0,Xm])
ax[0].set_ylim([0,Ym])

#tnew = np.linspace(tr.min(),tr.max(),300) #300 represents number of points to make between T.min and T.max

#power_smooth = spline(tr,s,tnew)

#ax[0].plot(tnew,power_smooth)
ax[0].plot(tr, s)

ax[1].plot(tz, r)	
####################################

#pcm = ax[1].pcolor(X, Y, Z, cmap='PuBu_r')
#fig.colorbar(pcm, ax=ax[1], extend='max')

plt.show()

