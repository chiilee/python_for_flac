# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 14:36:34 2019

@author: chiilee

Histogram of the Melt vol.(M) in the model for each time
Melt Vol.的值在百分比上的變化，
用來討論侷限Melt Vol.的範圍時應該有的平移量或壓縮量

"""
import sys
sys.path.append("/home/chiilee/git-flac/flac/util")
sys.path.append("/home/chiilee/code")
sys.path.append("/home/chiilee/code/git-code")
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import function_DataProcess as cd


#----------------------------
#          SETTING
#----------------------------
#inputpath='/home/chiilee/data/apr2019/0422-arc/'
#outputpath='/home/chiilee/Pic/0422/'
#foldername='af100_0.01'
inputpath='/home/chiilee/data/dec2019/AFc/'
outputpath='/home/chiilee/Pic/AFc/'
foldername='AFc0.001-'

Nvts=502
fys=0.001
BAS1=11.7
BAS2=21.0

modelsize=2750*800
x_max=0.25
y_max=0.01

path = inputpath+foldername
os.chdir(path)
results_dir = os.path.abspath(outputpath+foldername)
if not os.path.isdir(results_dir):
       os.makedirs(results_dir)
       
import flac
fl=flac. Flac()

def to_percent(y, position):
    return str(100 * y) + '%'

def weakF(fys):
    if fys ==1:
        weak_label05=0.16
        weak_label01=0.225
    elif fys ==0.5:
        weak_label05=0.07
        weak_label01=0.214
    elif fys ==0.1:
        weak_label05=0.038
        weak_label01=0.07
    elif fys==0.01 or fys==0.001:
        weak_label05=0.035
        weak_label01=0.063
    return weak_label05,weak_label01
    
def make_color(vts_numbers,BAS1,BAS2):
    #color=['#FF0000','#ffa500','#008800','#00FFFF','#0066FF','#9400D3','#808080','#696969','#000000']
    color1=['#FF0000','#ff6347','#ff8c00','#f0e68c','#deb887','#cd853f','#a0522d']
    color2=['#006400','#228b22','#00ff7f','#adff2f','#32cd32','#9acd32','#6b8e23']
    color3=['#0000cd','#0000ff','#00bfff','#00ffff','#40e0d0','#20b2aa']#'#191970',
    color=[]
    kk1=0
    kk2=0
    kk3=0
    for kk in range(len(vts_numbers)):
        vts = vts_numbers[kk]    
        time=fl.time[vts]
        if time < BAS1:
            color.append(color1[kk1])
            kk1=kk1+1
        elif time < BAS2:
            color.append(color2[kk2])
            kk2=kk2+1
        else:
            color.append(color3[kk3])
            kk3=kk3+1          
    return color   

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
#---------------------------------------------------
#           >>>>> read data & Plot <<<<<
#---------------------------------------------------

vts_numbers=[50,100,150,200,250,300,400,500,599]
vts_number=[]
for kk in range(len(vts_numbers)):
    if vts_numbers[kk]< Nvts:
        vts_number.append(vts_numbers[kk])

fig=plt.figure(figsize=(6,4))

kk=0
color=make_color(vts_number,BAS1,BAS2)
weak_label05,weak_label01 = weakF(fys)

for kk in range(len(vts_number)):
    vts = vts_number[kk]    
    
    time=fl.time[vts]
    C=[0]
    W=[0]
    newC=[]
    chamber=fl.read_chamber(vts)
    xmesh,zmesh=fl.read_mesh(vts)
    nx=len(chamber)
    nz=len(chamber[1,:])
    for kki in range(1,nx):
        for kkj in range(1,nz):
            if chamber[kki,kkj]>0.001:
                C.append(chamber[kki,kkj])
                W.append(read_area(xmesh,zmesh,kki,kkj)/modelsize)
                
    C = cd.moving_window_smooth(C,15)

    kwargs = dict(weights= W,lw=1.75, histtype='step', alpha=1, bins=1000, color=color[kk],label=str(round(time,1)),cumulative=-1)
    plt.hist(C, **kwargs)    
    formatter = FuncFormatter(to_percent)
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.gca().yaxis.set_major_formatter(formatter)

    kk=kk+1

line_x1=[weak_label05,weak_label05]
line_x2=[weak_label01,weak_label01]
line_x3=[0.25,0.25]
line_y=[0,1]
plt.plot(line_x1, line_y, ':',color='black',lw=3)    
plt.plot(line_x2, line_y, ':',color='black',lw=3)   
plt.plot(line_x3, line_y, ':',color='black',lw=3)   
plt.text(weak_label05+0.002,y_max*0.85,'0.5')
plt.text(weak_label01+0.002,y_max*0.85,'0.1')
#plt.text(weak_label00+0.002,y_max*0.85,'0')
    
plt.grid()
plt.xlim(0,x_max)
plt.ylim(0,y_max)
plt.xlabel('Melt Vol.', fontsize=12, color='black')
plt.ylabel('probability density', fontsize=12, color='black')
plt.text(0.005,y_max*0.93,foldername)

plt.legend(loc='upper right')
plt.savefig(results_dir+'/pic_MeltvolHistogram'+'.png')
