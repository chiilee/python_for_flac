# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:18:22 2020

@author: chiilee
"""
import sys
sys.path.append("/home/chiilee/git-flac/flac/util")
sys.path.append("/home/chiilee/code")
sys.path.append("/home/chiilee/code/git-code")
import os
import numpy as np
import function_DataProcess as cd
import function_DataInOut as ip
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#----------------------------
#          SETTING
#----------------------------
inputpath='/home/chiilee/data/feb2020=/stand/'
outputpath='/home/chiilee/Pic/feb_stand/'
foldername='s0.5-'
arcf=0.15
vts=600

axis_tick=1
legend=1
folderplot=1
#--------------------------------------------------------------------------------#
path = inputpath+foldername
os.chdir(path)
results_dir = os.path.abspath(outputpath+foldername)
if not os.path.isdir(results_dir):
       os.makedirs(results_dir)
import flac
fl=flac.Flac()

vts_numbers=vts-1

def read_area(xmesh,zmesh,x_index,z_index):
# get the total area of element(x,z) 

#    1(i,j) --------------- 2(i+1,j)
#           |             |
#           |    area     |
#           |             |
#  4(i,j+1) --------------- 3(i+1,j+1)   
#
    x1 = xmesh[x_index,z_index]
    y1 = zmesh[x_index,z_index]
    x2 = xmesh[x_index,z_index+1]
    y2 = zmesh[x_index,z_index+1]
    x3 = xmesh[x_index+1,z_index+1]
    y3 = zmesh[x_index+1,z_index+1]
    x4 = xmesh[x_index+1,z_index]
    y4 = zmesh[x_index+1,z_index]
    area1 = ((x1-x2)*(y3-y2))-((x3-x2)*(y1-y2))
    area2 = ((x1-x4)*(y3-y4))-((x3-x4)*(y1-y4))    
    area = (abs(area1)+abs(area2))*0.5           

    return area

def magma_prodction():
    mt=ip.read_data('D_melt',path,4)
    mi_index=ip.read_data('D_melt',path,5)
    mj_index=ip.read_data('D_melt',path,6)

    magmaP=[]
    Time=[]
    column=1
    for frame in range(1,vts):
        magmastep=0
        time=fl.time[frame]
        countmarker=fl.read_countmarker(frame)
        x,z=fl.read_mesh(frame)
        for column_now in range(column,len(mt)):
            if mt[column_now]<=time:
            #=======every melted markers=====================
            
                area=read_area(x,z,mi_index[column_now],mj_index[column_now])
                magma=area*0.25/countmarker[mi_index[column_now],mj_index[column_now]]
                ##print(column_now,time,mt[column_now])
                ##print(area,magma)
                magmastep=magmastep+magma
            
            #=========================================
            else:
                column=column_now
                #print('break')
                break
        magmaP.append(magmastep)
        Time.append(time)
    return magmaP, Time

def crust_production():
    print("crust production")
    arc=[]
    for frame in range(1,vts):
        arc_area=0
        phase=fl.read_phase(frame)
        print(fl.time[frame])
        x,z=fl.read_mesh(frame)
        for kki in range(fl.nx-1):
            for kkj in range(fl.nz-1):
                if phase[kki,kkj]==14:
                    arc_area=arc_area+read_area(x,z,kki,kkj)
        arc.append(arc_area)
    return arc
    
def get_arcT():
        
    arc_phase=[14]
    
    arcmaxT=[]
    arcmeanT=[]
    for frame in range(1,vts):
        arcthickness=[0]
        if frame != 1:
            phase=fl.read_phase(frame)          
            x,z=fl.read_mesh(frame)
            #zz=z[:,0]
            #imax = zz.argmax() #the highest point = arc peak
            
            for kk1 in range(0,fl.nx-1):
                if phase[kk1,0] in arc_phase:
                    for kk2 in range(fl.nz):
                        if phase[kk1,kk2] not in arc_phase:
                            break
                    arcthickness.append(z[kk1,0]-z[kk1,kk2])
                    
            print 
            arcmaxT.append(round(max(arcthickness),2))
            arcmeanT.append(round(np.mean(arcthickness),2))
        else:
            arcmaxT.append(0.0)
            arcmeanT.append(0.0)
    return arcmaxT, arcmeanT
    
#get data
magmaP, Time = magma_prodction()
##smooth
magmaP=cd.moving_window_smooth(magmaP,10)
magmaP=cd.moving_window_smooth(magmaP,5)
magmaP=cd.rate_calculating(magmaP,Time)  #km3 km-1 Myr-1

arcP=[i*arcf for i in magmaP] #from markers
#arcP2=crust_production()      #from elements area
#arcP2=cd.rate_calculating2(arcP2,Time)
#arcP2=cd.moving_window_smooth(arcP2,10)
#arcP2=cd.moving_window_smooth(arcP2,5)

arcmaxT,arcmeanT=get_arcT()

#aa=[i*0.05 for i in arcP]
#aa2=[i*0.05 for i in arcP2]

#print(np.sum(aa),np.sum(aa2))
#print(np.sum(aa2)*0.14)

fig1_1=plt.figure(figsize=(10,5))

ax = fig1_1.add_subplot(111)
plt.grid()
ax2 = ax.twinx()

line1 = ax.plot(Time, magmaP,  '-g', label = 'magma P',  lw=2)
line2 = ax.plot(Time, arcP, '-r', label = 'arc P',  lw=2)
#line3 = ax.plot(Time, arcP2, '--r', label = 'trench retreat rate',  lw=2)
line4 = ax2.plot(Time, arcmaxT, ':b', label = 'max thickness' ,lw=4)
line5 = ax2.plot(Time, arcmeanT, '-b', label = 'mean thickness', lw=2)


ax.set_xlim(0,30)
ax.set_ylim(0,125)
ax2.set_ylim(0,25)


if (axis_tick<1):
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)   
else:
    ax.set_xlabel("time(Myr)")
    ax.set_ylabel("magma production(km$^2$)")
if (legend >= 1): 
    lines = line1+line2+line4+line5
    labs = [l.get_label() for l in lines]
    ax.legend(lines, labs, loc=2)   
if (folderplot >=1):
    plt.text(1,16,foldername)
    
plt.savefig(results_dir+'/arctest'+'.png')
    
fig1_2=plt.figure(figsize=(6,3))
ax = fig1_2.add_subplot(111)

line1 = ax.plot(Time, magmaP,  '-g', label = 'magma P',  lw=2)
line2 = ax.plot(Time, arcP, '-r', label = 'arc P',  lw=2)
plt.grid()
#line3 = ax.plot(Time, arcP2, '--r', label = 'trench retreat rate',  lw=2)

