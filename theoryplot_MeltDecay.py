# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 16:31:54 2019

@author: chiilee
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

ratio=[]

ratiolog=[]

weaken_launch=0.00
weaken_saturated=1330 
ratio_max=20
ratio_min=0.05   
    
meltvol = np.arange(0,1500,1)
for kk in range(0,len(meltvol)):
           vis_down1 = (math.log(ratio_min)-math.log(ratio_max))*(meltvol[kk]-weaken_launch)/(weaken_saturated-weaken_launch)+math.log(ratio_max)
           vis_down2 = math.exp(vis_down1)
           ratiolog.append(vis_down1)
           #ratio.append(vis_down2)
           ratio.append(1)

           
    
fig=plt.figure(figsize=(6,4))
ax = fig.add_subplot(111)
#line = ax.plot(meltvol, ratio, '-', color='red', lw=3, label='decay rate ratio') 
line = ax.plot(meltvol, ratio, '-', color='black', lw=3, label='Orgi.') 
line = ax.plot(meltvol, r1, '-', color='red', lw=2, label='10-0.1') 
line = ax.plot(meltvol, r2, '-', color='green', lw=2, label='5-0.2') 
line = ax.plot(meltvol, r3, '-', color='blue', lw=2, label='20-0.05') 




plt.grid()
plt.xlim(0,1500)
plt.ylim(0,10)
plt.xlabel('Temperature',fontsize=12, color='black')
plt.ylabel('Decay rate ratio',fontsize=12, color='black')

plt.legend(loc='upper right')
plt.savefig('/home/chiilee/Pic/theory/'+'/pic_MeltDecay'+'.png') 