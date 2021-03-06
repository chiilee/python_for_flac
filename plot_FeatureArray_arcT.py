# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 14:28:09 2019

@author: chiilee
"""
import numpy as np

print ('ploting')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import function_FeatureArray as fa


cmin=2.5
cmax=17.5
figfolder='AFc'
figname='max_arcT'

fa.inputpath='/home/chiilee/data/dec2019/AFc/'
fa.foldername=['AFc1-','AFc1-0.5','AFc1-0.1','AFc1-0.01','AFc1-0.001',
               'AFc0.5-1','AFc0.5-','AFc0.5-0.1re','AFc0.5-0.01','AFc0.5-0.001',
               'AFc0.1-1','AFc0.1-0.5','AFc0.1-','AFc0.1-0.01re','AFc0.1-0.001re',
               'AFc0.01-1','AFc0.01-0.5','AFc0.01-0.1','AFc0.01-','AFc0.01-0.001',
               'AFc0.001-1','AFc0.001-0.5','AFc0.001-0.1','AFc0.001-0.01','AFc0.001-']
fa.arraysize=(5,5)

'''
fa.inputpath='/home/chiilee/data/dec2019/AFcD/'
fa.foldername=['AFcD1-','AFcD1-0.5','AFcD1-0.1','AFcD1-0.01',
               'AFcD0.5-1','AFcD0.5-','AFcD0.5-0.1','AFcD0.5-0.01',
               'AFcD0.1-1','AFcD0.1-0.5','AFcD0.1-','AFcD0.1-0.01',
               'AFcD0.01-1','AFcD0.01-0.5','AFcD0.01-0.1','AFcD0.01-']
fa.arraysize=(4,4)
'''
#subtime=[5,7.5,10,12,13,14,15,17.5,20,21,22,23,24,25]
subtime=[24]

for timek in range(len(subtime)):
 arcT= fa.get_maxarcT([subtime[timek]]*len(fa.foldername))
 #BAST, BASL = fa.get_BASdata()
 #dip= fa.getdip(depth1,depth2,BAST)
 data=arcT

 #=====================================================
 fig, ax = plt.subplots(figsize=(8,6))

 heatmap = ax.pcolor(data, cmap=plt.cm.PiYG, vmin=cmin,vmax=cmax)                  
 ax.set_xticks(np.arange(data.shape[1])+0.5, minor=False)
 ax.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
 for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        ax.text(j+0.5, i+0.5, format(str(round(data[i,j],2))),fontsize=12,
               ha="center", va="center",
               color="white" if data[i,j] ==10  else "black")
  #900254  
 ax.invert_yaxis()
 ax.xaxis.tick_top()
 ax.set_xlabel("f$_{ys}$", fontsize=22)
 ax.set_ylabel("f$_{v}$", fontsize=22)
 ax.set_xticklabels(['1','0.5','0.1','0.01','0.001'],  fontsize=15,minor=False)
 ax.set_yticklabels(['1','0.5','0.1','0.01','0.001'], fontsize=15,minor=False)
 
 Ffigname = figname+'_Y'+str(subtime[timek])
 colobartext='Max( arc thickness) in '+str(subtime[timek])+' Myrs (km) '
 #Ffigname = figname+'_1stBAS'
 #colobartext='Max( arc thickness) in 1$^{st}$ BAS ($^{o}$)'

 cbar = plt.colorbar(heatmap) 
 cbar.set_label(colobartext, fontsize=20, color='black')
 plt.savefig('/home/chiilee/Pic/'+figfolder+'/'+Ffigname+'.png') 



