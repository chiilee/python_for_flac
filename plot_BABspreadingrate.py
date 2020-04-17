# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 10:15:47 2020

@author: chiilee
"""
import sys
sys.path.append("/home/chiilee/flac-git/flac/util")
sys.path.append("/home/chiilee/code/git-code")
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import function_DataInOut as ip
import function_DataProcess as cd

def time2frame(time,path):
    T=ip.read_data1('D_time',path)

    for kk in range(len(T)-1):
        if T[kk] < time and T[kk+1] >= time:
            break
    return kk 
    
def xloca2xindex(xloca,frame):
    x,z=fl.read_mesh(frame)
    xx=x[:,0]

    for kk in range(len(xx)-1):
        if xx[kk] < xloca and xx[kk+1] >= xloca:
            break
    return kk

#----------------------------
#          SETTING
#----------------------------
'''
inputpath='/home/chiilee/data/dec2020/AFc/'
outputpath='/home/chiilee/Pic/AFc/'
foldername=['AFc1-','AFc1-0.5','AFc1-0.1','AFc1-0.01','AFc1-0.001',
            'AFc0.5-1','AFc0.5-','AFc0.5-0.1re','AFc0.5-0.01','AFc0.5-0.001',
            'AFc0.1-1','AFc0.1-0.5','AFc0.1-','AFc0.1-0.01re','AFc0.1-0.001re',
            'AFc0.01-1','AFc0.01-0.5','AFc0.01-0.1','AFc0.01-','AFc0.01-0.001',
            'AFc0.001-1','AFc0.001-0.5','AFc0.001-0.1','AFc0.001-0.01','AFc0.001-']
'''
inputpath='/home/chiilee/data/feb2020/DG80/'
outputpath='/home/chiilee/Pic/DG80/'            
foldername=['DG80_0.5-','DG80_0.1-','DG80_0.01-','DG80_1-0.1']           
''''
inputpath='/home/chiilee/data/dec2019/AFc/'
outputpath='/home/chiilee/Pic/AFc/'       
foldername=['AFc0.01-']
'''
axis_tick=1
legend=1
folderplot=1



for folderk in range(len(foldername)):
 path = inputpath+foldername[folderk]
 sys.path.append("/home/chiilee/git-flac/flac/util")

 os.chdir(path)
 results_dir = os.path.abspath(outputpath+foldername[folderk])
 if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
 import flac
 #import flacmarker2vtk
 fl=flac. Flac()


 #-------------------------------------------
 print ('>>>>> read data in <<<<<')
 #-------------------------------------------
 
 meanMORloca=[] 
 MORtime=[] 
 MORl=[]
 
 if os.path.isfile(path+'/D_time.txt'):
   time=ip.read_data1('D_time',path)
   Ltime=ip.read_data1('D_Ltime',path)
   rx=ip.read_data('D_rifting',path,1)
   rz=ip.read_data('D_rifting',path,2)
   rt=ip.read_data('D_rifting',path,3)
             
   for kkt in range(len(time)-1):
       MORloca=[]
       for kkr in range(len(rt)):
           if time[kkt] < rt[kkr] and time[kkt+1] >= rt[kkr]:
               MORloca.append(rx[kkr])
       if len(MORloca) != 0:
           meanMORloca.append(sum(MORloca)/len(MORloca))
           MORtime.append(time[kkt])
           MORl.append(Ltime[kkt])

   MORrate=cd.rate_calculating(meanMORloca,MORtime)
   
   RightV=[]   
   LeftV=[]
   for kkMOR in range(len(meanMORloca)):
       MORframe=time2frame(MORtime[kkMOR],path)
       MORindex=xloca2xindex(meanMORloca[kkMOR],MORframe)

       vx,vz=fl.read_vel(MORframe)
       
       # right side
       rightV=0
       for kkx in range(MORindex+5,MORindex+15):
           for kkz in range(2,27):
               rightV=vx[kkx,kkz]+rightV
       rightV=rightV/(10*25)
       RightV.append(rightV)

       # left side
       leftV=0
       for kkx in range(MORindex-15,MORindex-5):
           for kkz in range(2,27):
               leftV=vx[kkx,kkz]+leftV
       leftV=leftV/(10*25) 
       LeftV.append(leftV)
       
 MORrate=cd.moving_window_smooth(MORrate,5)
 RightV=cd.moving_window_smooth(RightV,5)
 LeftV=cd.moving_window_smooth(LeftV,5)
 MORrate=cd.moving_window_smooth(MORrate,3)
 RightV=cd.moving_window_smooth(RightV,3)
 LeftV=cd.moving_window_smooth(LeftV,3)
       
 fig1=plt.figure(figsize=(12,6))
 ax = fig1.add_subplot(111)
 ax2 = ax.twinx()
 
 line1 = ax.plot(MORtime, MORrate, '-g', label = 'MOR rate',  lw=2)
 line2 = ax.plot(MORtime, RightV, '-',color='#FF3333', label = 'half-spreading rate(R)',  lw=2)
 line3 = ax.plot(MORtime, LeftV, '-',color='#0044bb', label = 'half-spreading rate(L)',  lw=2)
 line4 = ax2.plot(MORtime, meanMORloca, '--',color='black', label = 'MOR location',  lw=2)

 ax.grid()
 ax.set_xlim(5,30)
 ax.set_ylim(-5,10)
 ax2.set_ylim(800,1400)

 
 if (axis_tick<1):
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    plt.setp(ax2.get_yticklabels(), visible=False)  
 else:
    ax.set_xlabel("Time (Myr)")
    ax.set_ylabel(r"velcoity ($cm/yr$)")
    ax2.set_ylabel(r"location ($km$)")
 if (legend >= 1): 
    lines = line1+line2+line3+line4
    labs = [l.get_label() for l in lines]
    ax.legend(lines, labs, loc=4)   
 if (folderplot >=1):
    plt.text(5.3,1380,foldername[folderk])  
 
 plt.savefig(results_dir+'/spreading1-'+'.png')    
 
 reRightV= [RightV[i] - MORrate[i] for i in range(len(MORrate))]
 reLeftV= [LeftV[i] - MORrate[i] for i in range(len(MORrate))]
 
 fig2=plt.figure(figsize=(12,6))
 ax = fig2.add_subplot(111)
 ax2 = ax.twinx()
 
 #line1 = ax.plot(MORtime, MORrate, '-g', label = 'MOR rate',  lw=2)
 line2 = ax.plot(MORtime, reRightV, '-',color='#FF3333', label = 'half-spreading rate(R)',  lw=2)
 line3 = ax.plot(MORtime, reLeftV, '-',color='#0044bb', label = 'half-spreading rate(L)',  lw=2)
 line4 = ax2.plot(MORtime, meanMORloca, '--',color='black', label = 'MOR location',  lw=2)

 ax.grid()
 ax.set_xlim(5,30)
 ax.set_ylim(-6,6)
 ax2.set_ylim(800,1400)

 
 if (axis_tick<1):
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    plt.setp(ax2.get_yticklabels(), visible=False)  
 else:
    ax.set_xlabel("Time (Myr)")
    ax.set_ylabel(r"velcoity ($cm/yr$)")
    ax2.set_ylabel(r"location ($km$)")
 if (legend >= 1): 
    lines = line2+line3+line4
    labs = [l.get_label() for l in lines]
    ax.legend(lines, labs, loc=2)   
 if (folderplot >=1):
    plt.text(575,1380,foldername[folderk])  
    
 plt.savefig(results_dir+'/spreading2-'+'.png')  
 
 fig3=plt.figure(figsize=(12,6))
 ax = fig3.add_subplot(111)
 ax2 = ax.twinx()
 
 #line1 = ax.plot(MORtime, MORrate, '-g', label = 'MOR rate',  lw=2)
 line2 = ax.plot(MORl, reRightV, '-',color='#FF3333', label = 'half-spreading rate(R)',  lw=2)
 line3 = ax.plot(MORl, reLeftV, '-',color='#0044bb', label = 'half-spreading rate(L)',  lw=2)
 line4 = ax2.plot(MORl, meanMORloca, '--',color='black', label = 'MOR location',  lw=2)

 ax.grid()
 ax.set_xlim(5,2000)
 ax.set_ylim(-6,6)
 ax2.set_ylim(800,1400)

 
 if (axis_tick<1):
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    plt.setp(ax2.get_yticklabels(), visible=False)  
 else:
    ax.set_xlabel("Subducted slab (km)")
    ax.set_ylabel(r"velcoity ($cm/yr$)")
    ax2.set_ylabel(r"location ($km$)")
 if (legend >= 1): 
    lines = line2+line3+line4
    labs = [l.get_label() for l in lines]
    ax.legend(lines, labs, loc=2)   
 if (folderplot >=1):
    plt.text(575,1380,foldername[folderk])  
    
 plt.savefig(results_dir+'/spreading3-'+'.png')  
             