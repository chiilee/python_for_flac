# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 11:34:46 2019

@author: chiilee
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import FuncFormatter

def to_percent(y, position):
    return str(100 * y) + '%'

vis=[]
vislog=[]

weaken_launch=0.001
weaken_saturated=0.20 
weak=0.1
    
meltvol = np.arange(0,0.35,0.001)
for kk in range(0,len(meltvol)):
       if (meltvol[kk] > weaken_launch):
           if (weaken_saturated > meltvol[kk]):
                vis_down1 = math.log(weak)*(meltvol[kk]-weaken_launch)/(weaken_saturated-weaken_launch)
                vis_down2 = math.exp(vis_down1)
           else:
                vis_down2 =math.log(weak)
                vis_down2 = weak
           vislog.append(vis_down1)
           vis.append(vis_down2)
       else:
           vislog.append(0)
           vis.append(1)
           
ys=[]
ys_threshold=0.07
ys_weakratio=0.3

for kk in range(0,len(meltvol)):
    if (meltvol[kk] > 0.001):
         if (meltvol[kk] < ys_threshold):
#             ys_down=1-meltvol[kk]            
             ys_down=(ys_weakratio-1)*(meltvol[kk]-0.001)/(ys_threshold-0.001)+1
         elif(meltvol[kk] < 0.25):
             ys_down=(0-ys_weakratio)*(meltvol[kk]-ys_threshold)/(0.25-ys_threshold)+ys_weakratio
         else:
             ys_down=0
         #else:
         #    ys_down=ys_weakratio         
    else:
         ys_down=1.
    ys.append(ys_down)
    
fig=plt.figure(figsize=(6,2.5))
ax = fig.add_subplot(111)
line1 = ax.plot(meltvol, ys, '-', color='green', lw=3, label='yield stress') 
line2 = ax.plot(meltvol, vis, '-', color='orange', lw=3, label='viscosity') 

formatter = FuncFormatter(to_percent)
plt.gca().xaxis.set_major_formatter(formatter)
plt.grid()
plt.xlim(0,0.25)
plt.ylim(0,1.1)
plt.xlabel('Melt vol.',fontsize=12, color='black')
plt.ylabel('weak ratio',fontsize=12, color='black')
ax.spines['right'].set_visible(False) 
ax.spines['top'].set_visible(False) 
#plt.yticks([], [])

plt.legend(loc='upper right')
plt.savefig('/home/chiilee/Pic/theory/'+'/pic_WeakRatio'+'.png')     


