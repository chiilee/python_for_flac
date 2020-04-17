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
import function_DataProcess as cd
import function_DataInOut as ip
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#----------------------------
#          SETTING
#----------------------------
inputpath='/home/chiilee/data/feb2020/stand/'
outputpath='/home/chiilee/Pic/stand/'
foldername='s0.01-'
vts=600

axis_tick=1
legend=0
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

#get data
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
            magma=area*1/countmarker[mi_index[column_now],mj_index[column_now]]
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

#smooth
magmaP=cd.moving_window_smooth(magmaP,10)
magmaP=cd.moving_window_smooth(magmaP,5)
magmaP=cd.moving_window_smooth(magmaP,25)
magmaPP=cd.rate_calculating(magmaP,Time)  #km3 km-1 Myr-1

fig1_1=plt.figure(figsize=(6,3))
ax = fig1_1.add_subplot(111)

line1 = ax.plot(Time, magmaP,  '-g', label = 'trench retreat rate',  lw=2)
line2 = ax.plot(Time, magmaPP, '-r', label = 'trench retreat rate',  lw=2)

ax.set_xlim(0,30)
ax.set_ylim(0,300)

if (axis_tick<1):
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)   
else:
    ax.set_xlabel("time(Myr)")
    ax.set_ylabel("magma production(km$^2$)")
'''
if (legend >= 1): 
    lines = line1+line2+line3
    labs = [l.get_label() for l in lines]
    ax.legend(lines, labs, loc=4)   
if (folderplot >=1):
    plt.text(20,-4,foldername[folderk])
'''