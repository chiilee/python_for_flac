# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 11:37:24 2019

@author: chiilee
"""

import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import sys
sys.path.append("/home/chiilee/code/git-code")
sys.path.append("/home/chiilee/git-flac/flac/util")
import matplotlib.pyplot as plt
import function_GroupXY as gxy
import function_DataInOut as ip


figfolder='AFc'
figname='xy_arcT'

gxy.inputpath='/home/chiilee/data/dec2019/AFc/'
#gxy.foldername=['AFc1-','AFc1-0.5']#,'AFc1-0.1','AFc1-0.01','AFc1-0.001']

gxy.foldername=['AFc1-','AFc1-0.5','AFc1-0.1','AFc1-0.01','AFc1-0.001',
               'AFc0.5-1','AFc0.5-','AFc0.5-0.1re','AFc0.5-0.01','AFc0.5-0.001',
               'AFc0.1-1','AFc0.1-0.5','AFc0.1-','AFc0.1-0.01re','AFc0.1-0.001re',
               'AFc0.01-1','AFc0.01-0.5','AFc0.01-0.1','AFc0.01-','AFc0.01-0.001',
               'AFc0.001-1','AFc0.001-0.5','AFc0.001-0.1','AFc0.001-0.01','AFc0.001-']

grouptype=[1, 1, 1, 2, 2,
               1, 1, 1, 2, 2,
               1, 1, 1, 2, 2,
               3, 1, 2, 2, 2,
               3, 1, 2, 2, 2]
groupcolor=['black','red','green','blue']

'''
fa.inputpath='/home/chiilee/data/dec2019/AFcD/'
fa.foldername=['AFcD1-','AFcD1-0.5','AFcD1-0.1','AFcD1-0.01',
               'AFcD0.5-1','AFcD0.5-','AFcD0.5-0.1','AFcD0.5-0.01',
               'AFcD0.1-1','AFcD0.1-0.5','AFcD0.1-','AFcD0.1-0.01',
               'AFcD0.01-1','AFcD0.01-0.5','AFcD0.01-0.1','AFcD0.01-']
fa.arraysize=(4,4)
'''

fig=plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)


for folderk in range(len(gxy.foldername)):
    gxy.path = gxy.inputpath+gxy.foldername[folderk]
    os.chdir(gxy.path)
    
    #time=ip.read_data1('D_time',gxy.path)
    #all_magmaP=ip.read_data('D_melt_count',gxy.path,1)
    #all_magmaP=all_magmaP*0.25
    all_magmaP, time = gxy.all_magmaP(min(401,gxy.getfinalvts(gxy.path)))
    line = ax.plot(time, all_magmaP, '-', color=groupcolor[grouptype[folderk]], lw=1.5)

ax.grid()
ax.set_xlim(0,20)
ax.set_ylim(0,40)
ax.set_xlabel("Time (Myrs)")
ax.set_ylabel("production rate (km$^{2}$/ Myr)")


'''
 if (axis_tick<1):
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    plt.setp(ax2.get_yticklabels(), visible=False)
    plt.setp(ax3.get_xticklabels(), visible=False)   
 else:
    
 if (legend >= 1): 
    lines = line1+line2+line3
    labs = [l.get_label() for l in lines]
    ax.legend(lines, labs, loc=4)   
 if (folderplot >=1):
    plt.text(20,-4,foldername[folderk])  
 
 plt.savefig(results_dir+'/Lpic1-'+'.png')
'''  