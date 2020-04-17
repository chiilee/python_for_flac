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

weaken_launch=0.24
weaken_saturated=0.60 
weaken_max=100   
    
meltvol = np.arange(0,0.80,0.001)
for kk in range(0,len(meltvol)):
       if (meltvol[kk] > weaken_launch):
           if (weaken_saturated > meltvol[kk]):
                vis_down =1+(weaken_max-1)*(meltvol[kk]-weaken_launch)/(weaken_saturated-weaken_launch)
           else:
                vis_down =weaken_max
           vis.append(1./vis_down)
       else:
           vis.append(1)
           
ys=[]
ys_threshold=0.24
ys_weakratio=0.1

for kk in range(0,len(meltvol)):
    if (meltvol[kk] > 0.001):
         if (meltvol[kk] < ys_threshold):
             ys_down=1.
         else:
             ys_down=ys_weakratio
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
plt.xlim(0,0.70)
plt.ylim(0,1.1)
plt.xlabel('Melt vol.',fontsize=12, color='black')
plt.ylabel('weak ratio',fontsize=12, color='black')
ax.spines['right'].set_visible(False) 
ax.spines['top'].set_visible(False) 

plt.legend(loc='upper right')
plt.savefig('/home/chiilee/Pic/theory/'+'/pic_WeakRatio_old'+'.png')     


