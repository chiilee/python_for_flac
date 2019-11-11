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


#----------------------------
#          SETTING
#----------------------------
inputpath='/home/chiilee/data/nov2019/1104/'
outputpath='/home/chiilee/Pic/1104/'
foldername='reT_62c6782_c3'

vts_numbers=600

path = inputpath+foldername
os.chdir(path)
results_dir = os.path.abspath(outputpath+foldername)
if not os.path.isdir(results_dir):
       os.makedirs(results_dir)
       
import flac
fl=flac. Flac()

def to_percent(y, position):
    return str(100 * y) + '%'
kk=0
color=['#FF0000','#FFFF00','#32CD32','#00FFFF','#0066FF','#9400D3']
#---------------------------------------------------
#           >>>>> read data & Plot <<<<<
#---------------------------------------------------
for vts in range(50,vts_numbers,100):
    
    time=fl.time[vts]
    C=[0]
    chamber=fl.read_chamber(vts)
    nx=len(chamber)
    nz=len(chamber[1,:])
    for kki in range(1,nx):
        for kkj in range(1,nz):
            if chamber[kki,kkj]>0.01:
                C.append(chamber[kki,kkj])
                

    kwargs = dict(weights= [1./len(C)] * len(C),lw=1.5, histtype='step', alpha=0.95, bins=30, color=color[kk],label=str(time))
    plt.hist(C, **kwargs)    
    formatter = FuncFormatter(to_percent)
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.gca().yaxis.set_major_formatter(formatter)

    kk=kk+1
    
plt.grid()
plt.xlim(0,0.35)
plt.ylim(0,0.07)
plt.xlabel('Melt Vol.', fontsize=12, color='black')
plt.ylabel('probability density', fontsize=12, color='black')

plt.legend(loc='upper right')
plt.savefig(results_dir+'/pic_MeltvolHistogram'+'.png')
