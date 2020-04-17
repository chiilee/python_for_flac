# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 14:28:09 2019

@author: chiilee
"""
import numpy as np

print ('ploting')
import matplotlib
matplotlib.use('Agg')
import sys
sys.path.append("/home/chiilee/code/git-code")
import matplotlib.pyplot as plt
import function_FeatureArray as fa

'''
fa.inputpath='/home/chiilee/data/dec2019/AFc/'
fa.foldername=['AFc1-','AFc1-0.5','AFc1-0.1','AFc1-0.01','AFc1-0.001',
            'AFc0.5-1','AFc0.5-','AFc0.5-0.1re','AFc0.5-0.01re','AFc0.5-0.001',
            'AFc0.1-1','AFc0.1-0.5','AFc0.1-','AFc0.1-0.01re','AFc0.1-0.001re',
            'AFc0.01-1','AFc0.01-0.5','AFc0.01-0.1','AFc0.01-','AFc0.01-0.001',
            'AFc0.001-1','AFc0.001-0.5','AFc0.001-0.1','AFc0.001-0.01','AFc0.001-']
fa.arraysize=(5,5)

BAST = np.array([  1000,  1000,  1000,  20.5,  23.6,
                   1000,  1000,  1000,  23.8,  21.8,
                   1000,  1000,  1000,  22.8,  21.6,
                   1000,  1000,  24.5,  20.8,  21.0,
                   1000,  1000,  22.6,  21.5,  21.0])
'''
fa.inputpath='/home/chiilee/data/dec2019/AFcD/'
fa.foldername=['AFcD1-','AFcD1-0.5','AFcD1-0.1','AFcD1-0.01',
            'AFcD0.5-1','AFcD0.5-','AFcD0.5-0.1','AFcD0.5-0.01',
            'AFcD0.1-1','AFcD0.1-0.5','AFcD0.1-','AFcD0.1-0.01',
            'AFcD0.01-1','AFcD0.01-0.5','AFcD0.01-0.1','AFcD0.01-']
fa.arraysize=(4,4)

BAST = np.array([ 1000, 1000, 1000, 11.9,
                  1000, 1000, 1000, 12.8,
                  1000, 1000, 16.7, 11.7,
                  1000, 1000, 14.0, 12.8])


#BAST, BASL = function_BASTL.get_BASdata(inputpath,foldername,arraysize)     
BAST, BASL = fa.BAST2L(fa.foldername,BAST,fa.arraysize)


picnameT='pic_2BAStime'
picnameL='pic_2BASlen'
#=====================================================
fig, ax = plt.subplots(figsize=(8,6))

heatmap = ax.pcolor(BAST, cmap=plt.cm.gist_earth, vmin=12,vmax=17)                  
ax.set_xticks(np.arange(BAST.shape[1])+0.5, minor=False)
ax.set_yticks(np.arange(BAST.shape[0])+0.5, minor=False)
for i in range(BAST.shape[0]):
    for j in range(BAST.shape[1]):
        ax.text(j+0.5, i+0.5, format(str(BAST[i,j])),fontsize=12,
               ha="center", va="center",
               color="white" if BAST[i,j] >999  else "black")
               #
ax.invert_yaxis()
ax.xaxis.tick_top()
ax.set_xlabel("f$_{ys}$", fontsize=22)
ax.set_ylabel("f$_{v}$", fontsize=22)
ax.set_xticklabels(['1','0.5','0.1','0.01','0.001'],  fontsize=15,minor=False)
ax.set_yticklabels(['1','0.5','0.1','0.01','0.001'], fontsize=15,minor=False)

cbar = plt.colorbar(heatmap) 
cbar.set_label('Time of 2$^{nd}$ BAS (Myrs)', fontsize=20, color='black')
plt.savefig('/home/chiilee/Pic/AFcD/'+'/'+picnameT+'.png') 

#=====================================================
fig, ax = plt.subplots(figsize=(8,6))

print(BASL)
heatmap = ax.pcolor(BASL, cmap=plt.cm.gist_heat, vmin=800,vmax=1400)
ax.set_xticks(np.arange(BASL.shape[1])+0.5, minor=False)
ax.set_yticks(np.arange(BASL.shape[0])+0.5, minor=False)
for i in range(BAST.shape[0]):
    for j in range(BAST.shape[1]):
        ax.text(j+0.5, i+0.5, format(str(BASL[i,j])),fontsize=12,
               ha="center", va="center",
               color="black" if BASL[i,j] <1380 and BASL[i,j] >1000 or BASL[i,j]==0 else "white")

ax.invert_yaxis()
ax.xaxis.tick_top()
ax.set_xlabel("f$_{ys}$", fontsize=22)
ax.set_ylabel("f$_{v}$", fontsize=22)
ax.set_xticklabels(['1','0.5','0.1','0.01','0.001'], fontsize=15,minor=False)
ax.set_yticklabels(['1','0.5','0.1','0.01','0.001'], fontsize=15,minor=False)

cbar = plt.colorbar(heatmap) 
cbar.set_label('subducted length at 2$^{nd}$ BAS (km)', fontsize=15, color='black')
plt.savefig('/home/chiilee/Pic/AFcD/'+'/'+picnameL+'.png') 

